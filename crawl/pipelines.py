# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time
from scrapy import log

import common

class CrawlPipeline(object):
    _com = None
    _history = set()

    def __init__(self):
        self._com = common.Common()

    def process_item(self, item, spider):
        spider_name = spider.name
        print spider_name
        if spider_name in ['voa_links2','voa_links']:
            self.voa_links(item, spider)
        elif spider_name in ['voa_contents']:
            self.voa_contents(item, spider)
        elif spider_name in ['haha365_links']:
            self.haha365_links(item, spider)
        else:
            print spider.name
        return item

    def haha365_links(self, item, spider):
        values = ""
        cid = item['cid']
        print cid
        for (k, url) in enumerate(item['url']):
            pubtime = time.mktime(time.strptime("2015-%s" % item['pubtime'][k], "%Y-%m-%d"))
            if url not in self._history: values = "%s ('%s', '%s', '%s', '', '')," % (values, cid, url, pubtime)
            self._history.add(url)
        sql = "insert into cw_posts (cid, url, pubtime, content, ext) values %s" % values
        print sql
        self._com.query(sql.rstrip(','))
        return True


    def voa_links(self, item, spider):
        values = ""
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        for i in item['url']:
            if i not in self._history: values = "%s ('%s', '%s')," % (values, now, i)
            self._history.add(i)
        sql = "insert into crawl_links_1 (add_time, url) values %s" % values
        # print sql
        self._com.query(sql[:-1])
        return True

    def voa_contents(self, item, spider):
        if not item['title'] or not item['content']:
            print "ERROR: (voa) title or content null [link_id: %s]" % item['link_id']
            log.msg("title: %s, link_id: %s" % (item['title'], item['link_id']), level=log.ERROR)
            return False
        item['content'] = self._com.db_str(item['content'])
        item['title'] = self._com.db_str(item['title'])
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        sql = "insert into crawl_contents_1 (`link_id`, `site_id`, `add_time`, `title`, `keywords`, `desc`, `content`) values " \
              " ('%s', '%s', '%s', '%s', '%s', '%s', '%s') " % (item['link_id'], 1, now, item['title'], item['keyword'], item['desc'], item['content'])
        self._com.query(sql)
        # update crawl time
        self._com.update_crawl_status([item['link_id']], 1)
        return True

