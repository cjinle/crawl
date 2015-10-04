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
        if spider_name in ['voa_links2','voa_links']:
            self.voa_links(item, spider)
        elif spider_name in ['voa_contents']:
            self.voa_contents(item, spider)
        elif spider_name in ['jd5_links']:
            self.jd5_links(item, spider)
        elif spider_name in ['jd5_contents']:
            self.jd5_contents(item, spider)
        else:
            print spider.name
        return item


    def jd5_links(self, item, spider):
        values = ""
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        for i in item['url']:
            if i not in self._history: values = "%s ('%s', '%s')," % (values, now, i)
            self._history.add(i)
        sql = "insert into crawl_links_%s (add_time, url) values %s" % (item['siteid'], values)
        self._com.query(sql[:-1])
        return True

    def jd5_contents(self, item, spider):
        if not item['title'] or not item['content']:
            print "ERROR: (jd5) title or content null [link_id: %s, site_id: %s]" % (item['link_id'], item['siteid'])
            log.msg("title: %s, link_id: %s" % (item['title'], item['link_id']), level=log.ERROR)
            return False
        item['content'] = self._com.db_str(item['content'])
        item['title'] = self._com.db_str(item['title'])
        sql = "select * from crawl_contents_%s where link_id='%s' limit 1" % (item['siteid'], item['link_id'])
        post = self._com.get_one(sql)
        if post:
            # content = post['content'].replace("<!--{2}-->", item['content'].encode('utf-8'))
            content = post['content'].encode('utf-8').replace("<!--{%s}-->" % item['page'], item['content'])
            sql = "update crawl_contents_%s set `content`='%s' where `link_id`='%s'" % (item['siteid'], content, item['link_id'])
            self._com.query(sql)
        else:
            log.msg("spider[%s] site_id[%s] link_id[%s] page[%s] source post not exist!" % (item['siteid'], spider.name, item['link_id'], item['page']), level=log.ERROR)
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


class Mp3Pipeline(object):
    def __init__(self):
        pass

    def open_spider(self, spider):
        log.msg("spider[%s] is open" % spider.name, level=log.INFO)

    def process_item(self, item, spider):
        # self.save_file(item['mp3'])
        return 

    def save_file(self, path):
        file_path = path
        url = 'http://slb.51voa.com' + path
        print url
        # import urllib
        # urllib.urlretrieve(url, 'download' + path)
        # also can use wget module wget.download(url)
        # urllib2.urlopen  or urllib.urlopen
        # urllib.get

    def close_spider(self, spider):
        log.msg("spider[%s] is closed" % spider.name, level=log.INFO)

