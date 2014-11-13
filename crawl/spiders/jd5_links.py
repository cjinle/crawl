from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from crawl.items import LinksItem
from scrapy import log
from scrapy.utils.project import get_project_settings

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.statscol import StatsCollector


class Jd5LinksSpider(BaseSpider):
    name = "jd5_links"
    allowed_domains = ["jd5.com"]
    settings = get_project_settings()
    siteid = settings.get('SITEID')
    siteinfo = settings.get('SITEINFO')
    start_urls = []
    start_urls.append(siteinfo[siteid]['start_page'])
    for i in range(2, siteinfo[siteid]['max_page_num']+1):
        start_urls.append('%s/index_%s.html' % (siteinfo[siteid]['start_page'], i))

    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def parse(self, response):
        sel = Selector(response)
        i = LinksItem()
        i['url'] = sel.xpath('//h4/a/@href').extract()
        i['siteid'] = self.siteid
        print response.url
        # i['url'] = sel.xpath("//div[@id='list']/ul/li/a/@href").extract()
        return i

    def spider_closed(self, spider):
        stats = str(self.crawler.stats.get_stats())
        import common
        com = common.Common()
        com.add_crawl_log(spider, self.siteid, stats)
