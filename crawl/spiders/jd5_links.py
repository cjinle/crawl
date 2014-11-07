from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from crawl.items import LinksItem
from scrapy import log


class Jd5LinksSpider(BaseSpider):
    name = "jd5_links"
    allowed_domains = ["jd5.com"]
    start_urls = []
    start_urls.append('http://www.jd5.com/meirong/skincare/')
    for i in range(2, 46):
        start_urls.append('http://www.jd5.com/meirong/skincare/index_%s.html' % i)
    # print start_urls

    def parse(self, response):
        sel = Selector(response)
        i = LinksItem()
        i['url'] = sel.xpath('//h4/a/@href').extract()
        print i['url']
        # i['url'] = sel.xpath("//div[@id='list']/ul/li/a/@href").extract()
        return i