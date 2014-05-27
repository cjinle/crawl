from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from crawl.items import LinksItem

class VoaLinks2Spider(BaseSpider):
    name = "voa_links2"
    allowed_domains = ["51voa.com"]
    start_urls = []

    def __init__(self):
        str = 'http://www.51voa.com/VOA_Standard_%s.html'
        self.start_urls = [ str % x for x in range(1, 70) ]

    def parse(self, response):
        sel = Selector(response)
        i = LinksItem()
        i['url'] = sel.xpath("//div[@id='list']/ul/li/a/@href").extract()
        return i
