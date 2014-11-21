# Scrapy settings for crawl project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'crawl'

SPIDER_MODULES = ['crawl.spiders']
NEWSPIDER_MODULE = 'crawl.spiders'

ITEM_PIPELINES = {
                  'crawl.pipelines.CrawlPipeline' : 300,
                  'crawl.pipelines.Mp3Pipeline' : 300,
                  'scrapy.contrib.pipeline.images.ImagesPipeline' : 1,
                  }
IMAGES_STORE = 'download'

LOG_FILE = 'out.log'
LOG_LEVEL = 'INFO'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawl (+http://www.yourdomain.com)'

# custom settings
# only for jd5_links,jd5_contents spiders
SITEID = 6
SITEINFO = {
    2 : {
        'start_page' : 'http://www.jd5.com/meirong/skincare/',
        'max_page_num' : 46,
    },
    3 : {
        'start_page' : 'http://www.jd5.com/fushi/with/',
        'max_page_num' : 77,
    },
    4 : {
        'start_page' : 'http://www.jd5.com/fushi/single/',
        'max_page_num' : 29,
    },
    5 : {
        'start_page' : 'http://www.jd5.com/meirong/makeup/',
        'max_page_num' : 41,
    },
    6 : {
        'start_page' : 'http://www.jd5.com/meiti/fat/',
        'max_page_num' : 20,
    },
    7 : {
        'start_page' : 'http://www.jd5.com/meiti/loss/',
        'max_page_num' : 28,
    },
}
