from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from crawl.items import LinksItem
from scrapy import log

class VoaLinksSpider(CrawlSpider):
    name = 'voa_links'
    allowed_domains = ['51voa.com']
    start_urls = ['http://www.51voa.com/']
    # start_urls = this.urls()

    rules = (
        Rule(SgmlLinkExtractor(allow=r''), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        sel = Selector(response)
        # print sel
        i = LinksItem()
        i['url'] = sel.xpath('//a/@href').extract()
        log.msg("hello")
        i['base_url'] = 'http://www.51voa.com'
        #i['domain_id'] = sel.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = sel.xpath('//div[@id="name"]').extract()
        #i['description'] = sel.xpath('//div[@id="description"]').extract()
        return i

    def urls(self):
        return ['http://www.51voa.com/']
