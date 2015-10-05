from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from crawl.items import ContentItem
from scrapy.http import Request
from scrapy import log
from scrapy.utils.project import get_project_settings

import common


class Haha365Spider(BaseSpider):
    name = "haha365"
    allowed_domains = []
    start_urls = []
    settings = get_project_settings()
    cid = settings.get('CID')
    _urls = {}
    _com = None
    _cinfo = None

    def __init__(self):
        self._com = common.Common()
        self._cinfo = self._com.get_cat_info(self.cid)
        if self._cinfo is False:
            return False
        self.allowed_domains.append(self._cinfo['host'])
        for i in self._com.get_crawl_urls(self.cid):
            url = "http://%s/%s" % (self._cinfo['host'], i.get('url'))
            self.start_urls.append(url)
            self._urls[url] = i.get('pid')
        print self._urls

    def parse(self, response):
        sel = Selector(response)
        item = ContentItem()
        item['pid'] = self._urls.get(response.url)
        item['title'] = sel.xpath("//h1/text()").extract()[0].encode('utf-8').strip()
        item['keyword'] = ''
        item['desc'] = sel.xpath("//meta[@name='description']/@content").extract()[0].encode('utf-8').strip()
        item['content'] = '' . join(sel.xpath("//div[@class='nv_content']/*").extract()).encode('utf-8').strip()
        item['cid'] = self.cid
        pass 
