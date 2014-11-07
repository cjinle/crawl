from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from crawl.items import ContentItem
from scrapy import log
import common

class Jd5ContentsSpider(BaseSpider):
    name = "jd5_contents"
    allowed_domains = ["jd5.com"]
    start_urls = []
    _urls = {}

    def __init__(self):
        com = common.Common()
        str = "http://www.jd5.com%s"
        for x in com.get_crawl_urls(2, True):
            if x.get('url', ''):
                self.start_urls.append(str % x.get('url', ''))
                self._urls[str % x.get('url', '')] = x.get('link_id', 0)

    def parse(self, response):
        sel = Selector(response)
        i = ContentItem()
        # i['title'] = sel.xpath("//title/text()").extract()[0]
        i['link_id'] = self._urls.get(response.url)
        last_page = sel.xpath("//div[@id='content_pages']/a/@href").extract()[-1]
        num = int(last_page.split('_')[-1].split('.')[0])
        print num
        pass

    def parse_pages(self):
        # http://www.icultivator.com/p/3166.html
        pass
