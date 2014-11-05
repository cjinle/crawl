from scrapy.spider import BaseSpider

class Jd5Spider(BaseSpider):
    name = "jd5"
    allowed_domains = ["www.jd5.com"]
    start_urls = (
        'http://www.www.jd5.com/',
        )

    def parse(self, response):
        pass 
