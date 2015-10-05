from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from crawl.items import LinksItem
from scrapy.http import Request
from scrapy import log
from scrapy.utils.project import get_project_settings

import common

class Haha365LinksSpider(BaseSpider):
    name = "haha365_links"
    allowed_domains = []
    start_urls = []
    settings = get_project_settings()
    cid = settings.get('CID')
    _com = None

    def __init__(self):
        self._com = common.Common()
        cinfo = self._com.get_cat_info(self.cid)
        if cinfo is False:
            return False
        self.allowed_domains.append(cinfo['host'])
        for i in range(1, cinfo['pcnt']+1):
            url = cinfo['url'] % i
            self.start_urls.append("http://%s/%s" % (cinfo['host'], url))
        print self.start_urls

    def parse(self, response):
    	sel = Selector(response)
        item = LinksItem()
        item['cid'] = self.cid
        item['url'] = sel.xpath("//ul[@class='text_doublelist1']/li/a[2]/@href").extract()
        item['pubtime'] = sel.xpath("//ul[@class='text_doublelist1']/li/span/text()").extract()
        print item
        return item 
