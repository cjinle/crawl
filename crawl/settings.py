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
                  'scrapy.contrib.pipeline.images.ImagesPipeline' : 1,
                  }
IMAGES_STORE = 'download'

LOG_FILE = 'out.log'
LOG_LEVEL = 'INFO'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawl (+http://www.yourdomain.com)'

# custom settings
# only for haha365 spiders
# table cw_categories 
CID = 1