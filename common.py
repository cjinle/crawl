#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import mysqllib

class Common:
    """common class"""
    _db = None

    def __init__(self):
        self._db = mysqllib.MySQL()

    def get_crawl_urls(self, site_id = 0, update = False):
        if not site_id:
            return False
        tb = "crawl_links_%s" % site_id
        sql = "select * from %s where status in (0, 1) " % tb
        ret = self._db.get_all(sql)
        if update:
            link_ids = [ x.get('link_id', 0) for x in ret ]
            self.update_crawl_status(link_ids, site_id)
        return ret

    def query(self, sql):
        self._db.query(sql)
        self._db.commit()

    def db_str(self, s):
        return self._db.escape_string(s)

    def get_one(self, sql):
        return self._db.get_one(sql)

    def add_crawl_log(self, spider, site_id = 0, ext = None):
        if not spider:
            log.msg("add_crawl_log ERROR", level=log.ERROR)
            return False
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        import socket
        ext = self.db_str(ext.encode('utf-8').strip())
        sql = "insert into crawl_logs (site_id, spider, log_type, ip, add_time, ret, content) values " \
              " ('%s', '%s', '%s', '%s', '%s', '%s', '%s') " % (site_id, spider.name, 7, socket.gethostname(), now, 1, ext)
        self.query(sql)
        return True

    def update_crawl_status(self, link_ids = [], site_id = 0, status = 1):
        if not link_ids or not site_id:
            return False
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        link_ids = ',' . join([str(x) for x in link_ids])
        sql = "update crawl_links_%s set crawl_time='%s', status='%s' where link_id in (%s) " % \
              (site_id, now, status, link_ids)
        self.query(sql)
        return True


