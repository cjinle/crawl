from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from crawl.items import LinksItem
from scrapy import log

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.statscol import StatsCollector

class VoaLinksSpider(BaseSpider):
    name = "voa_links"
    allowed_domains = ["51voa.com"]
    start_urls = []

    def __init__(self):
        str = 'http://www.51voa.com/VOA_Standard_%s.html'
        self.start_urls = [ str % x for x in range(1, 70) ]
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def parse(self, response):
        sel = Selector(response)
        i = LinksItem()
        i['url'] = ''
        # i['url'] = sel.xpath("//div[@id='list']/ul/li/a/@href").extract()
        return i

    def spider_closed(self, spider):
        stats = str(self.crawler.stats.get_stats())
        # print spider.state.values()
        import common
        com = common.Common()
        com.add_crawl_log(spider, 1, stats)
        log.msg("spider closed", level=log.INFO)
        print "spider closed!"
