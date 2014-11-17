import time
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from crawl.items import ContentItem
from scrapy.http import Request
from scrapy import log
from scrapy.utils.project import get_project_settings

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.statscol import StatsCollector

import common

class Jd5ContentsSpider(BaseSpider):
    name = "jd5_contents"
    allowed_domains = ["jd5.com"]
    start_urls = []
    settings = get_project_settings()
    siteid = settings.get('SITEID')
    _urls = {}
    _com = None

    def __init__(self):
        self._com = common.Common()
        host = "http://www.jd5.com%s"
        for x in self._com.get_crawl_urls(self.siteid, True):
            if x.get('url', ''):
                self.start_urls.append(host % x.get('url', ''))
                self._urls[host % x.get('url', '')] = x.get('link_id', 0)
        print self._urls
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def first_page(self, item):
        print "first_page: %s, site_id: %s" % (int(item['link_id']), self.siteid)
        if not item['title'] or not item['content']:
            print "ERROR: (jd5:1) title or content null [link_id: %s, site_id: %s]" % (item['link_id'], self.siteid)
            log.msg("title: %s, link_id: %s, site_id: %s" % (item['title'], item['link_id'], self.siteid), level=log.ERROR)
            return False
        item['content'] = self._com.db_str(item['content'])
        item['title'] = self._com.db_str(item['title'])
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        sql = "insert into crawl_contents_%s (`link_id`, `site_id`, `add_time`, `title`, `keywords`, `desc`, `content`) values " \
              " ('%s', '%s', '%s', '%s', '%s', '%s', '%s') " % (self.siteid, item['link_id'], self.siteid, now, item['title'], item['keyword'], item['desc'], item['content'])
        self._com.query(sql)
        # update crawl time
        self._com.update_crawl_status([item['link_id']], self.siteid)
        return True

    def parse(self, response):
        sel = Selector(response)
        item = ContentItem()
        item['link_id'] = self._urls.get(response.url)
        # print "link_id: %s, url: %s" % (item['link_id'], response.url)
        item['title'] = sel.xpath("//h1/text()").extract()[0].encode('utf-8').strip()
        item['keyword'] = ''
        item['desc'] = sel.xpath("//meta[@name='description']/@content").extract()[0].encode('utf-8').strip()
        item['content'] = '' . join(sel.xpath("//div[@class='nv_content']/*").extract()).encode('utf-8').strip()
        item['siteid'] = self.siteid
        pages = sel.xpath("//div[@id='content_pages']/a/@href").extract()
        if len(pages):
            num = int(pages[-1].split('_')[-1].split('.')[0])
        else:
            num = 1
        
        if len(item['content']) and (num > 1):
            item['content'] += "\n<!--more-->\n" + "\n" . join(["<!--{%s}-->" % str(x) for x in range(2,num+1)])
        self.first_page(item)
        if num > 1:
            for i in range(2, num+1):
                url = response.url.replace('.html', '_%s.html' % i, -1)
                meta = {
                    'link_id': item['link_id'],
                    'page': i,
                    'num': num
                }
                yield Request(url, meta=meta, callback=self.parse_pages)

    def parse_pages(self, response):
        # http://www.icultivator.com/p/3166.html
        sel = Selector(response)
        item = ContentItem()
        item['link_id'] = response.meta['link_id']
        if response.meta['page'] == response.meta['num']:
            print "link_id:%s, site_id:%s done" % (item['link_id'], self.siteid)
        # print "link_id:%s, page:%s, num:%s, url:%s" % (item['link_id'], response.meta['page'], response.meta['num'], response.url)
        item['title'] = sel.xpath("//h1/text()").extract()[0].encode('utf-8').strip()
        item['keyword'] = ''
        item['desc'] = sel.xpath("//meta[@name='description']/@content").extract()[0].encode('utf-8').strip()
        item['content'] = '' . join(sel.xpath("//div[@class='nv_content']/*").extract()).encode('utf-8').strip()
        item['page'] = response.meta['page']
        item['siteid'] = self.siteid
        return item

    def spider_closed(self, spider):
        stats = self.crawler.stats.get_stats()
        stats['siteid'] = self.siteid
        import common
        com = common.Common()
        com.add_crawl_log(spider, self.siteid, stats)
