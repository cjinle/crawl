from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from crawl.items import ContentItem
from scrapy import log
import common

class VoaContentsSpider(BaseSpider):
    name = "voa_contents"
    allowed_domains = ["51voa.com"]
    start_urls = []
    _urls = {}

    def __init__(self):
        com = common.Common()
        str = "http://www.51voa.com%s"
        for x in com.get_crawl_urls(1, True):
            if x.get('url', ''):
                self.start_urls.append(str % x.get('url', ''))
                self._urls[str % x.get('url', '')] = x.get('link_id', 0)
        

    def parse(self, response):
        print response.url
        # print self._urls
        sel = Selector(response)
        i = ContentItem()
        # i['title'] = sel.xpath("//title/text()").extract()[0]
        i['link_id'] = self._urls.get(response.url)
        i['title'] = sel.xpath("//div[@id='title']/h1/text()").extract()[0].encode('utf-8').strip()
        i['keyword'] = sel.xpath("//meta[@name='keywords']/@content").extract()[0].encode('utf-8').strip()
        i['desc'] = sel.xpath("//meta[@name='keywords']/@content").extract()[0].encode('utf-8').strip()
        i['content'] = '' . join(sel.xpath("//div[@id='content']/*").extract()).encode('utf-8').strip()
        if not i['content']: 
            log.msg("id=content null [%s]" % i['link_id'], level=log.WARNING)
            i['content'] = '' . join(sel.xpath("//div[@class='articleBody']/*").extract()).encode('utf-8').strip()
        return i 
