from scrapy.spider import BaseSpider


class Haha365Spider(BaseSpider):
    name = "haha365"
    allowed_domains = ["haha365.com"]
    start_urls = (
        'http://www.haha365.com/',
        )

    def parse(self, response):
        pass 
