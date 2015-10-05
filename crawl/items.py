# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class LinksItem(Item):
    url = Field()
    base_url = Field()
    siteid = Field()
    cid = Field()
    pubtime = Field()
    pass

class ContentItem(Item):
    title = Field()
    keyword = Field()
    desc = Field()
    url = Field()
    content = Field()
    pid = Field()
    cid = Field()
    pass