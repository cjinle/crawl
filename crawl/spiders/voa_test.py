import re
from scrapy import log
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from crawl.items import ContentItem

class VoaTestSpider(BaseSpider):
    name = "voa_test"
    allowed_domains = ["51voa.com"]
    start_urls = (
        'http://www.51voa.com/VOA_Standard_English/somalia-food-jun-56493.html',
        'http://www.51voa.com/VOA_Standard_English/obama-europe-visit-to-be-dominated-by-ukraine-56463.html',
        )

    def parse(self, response):
        sel = Selector(response)
        item = ContentItem()
        javascripts = sel.xpath("//script/text()").extract()
        image_urls = sel.xpath("//div[@id='content']//img/@src").extract()
        item['image_urls'] = [ 'http://www.51voa.com%s' % x for x in image_urls ]
        # item['image_urls'] = sel.xpath("//div[@id='content']//img/@src").extract()
        # print javascripts
        item['mp3'] = ''
        if type(javascripts) is list:
            for i in javascripts:
                m = re.match(r".*Player\(\"(.*)\"\);.*", i.strip())
                if m is not None:
                    try:
                        item['mp3'] = m.group(1)
                    except Exception as e:
                        print "Exception: %s" % e
        return item
