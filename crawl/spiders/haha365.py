
import sys
reload(sys)
sys.setdefaultencoding("utf8")

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
        print response.url
        item['pid'] = self._urls.get(response.url)
        item['title'] = sel.xpath("//h1/text()").extract()[0]
        item['keywords'] = ''
        item['desc'] = ''
        # item['keywords'] = sel.xpath("//meta[@name='keywords']/@content").extract()[0]
        # item['desc'] = sel.xpath("//meta[@name='description']/@content").extract()[0]
        temp_content = sel.xpath("//div[@id='endtext']/*[1]/text()").extract()
        if not temp_content:
            temp_content = sel.xpath("//div[@id='endtext']/text()").extract()
        item['content'] = ('<br>'.join(temp_content).encode('utf-8')).strip()
        if not item['content']:
            item['content'] = sel.xpath("//div[@id='endtext']/*").extract()[0].encode('utf-8')
        item['cid'] = self.cid
        return item
