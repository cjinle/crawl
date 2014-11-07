# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class CrawlItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass


class LinksItem(Item):
    url = Field()
    base_url = Field()
    pass

class ContentItem(Item):
    title = Field()
    keyword = Field()
    desc = Field()
    url = Field()
    content = Field()
    link_id = Field()
    mp3 = Field()
    image_urls = Field()
    images = Field()
    page = Field()
    pass