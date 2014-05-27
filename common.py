#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        sql = "select * from %s where status in (0, 1)" % tb
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

    def update_crawl_status(self, link_ids = [], site_id = 0):
        if not link_ids or not site_id:
            return False
        import time
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        link_ids = ',' . join([str(x) for x in link_ids])
        sql = "update crawl_links_%s set crawl_time='%s', status=1 where link_id in (%s) " % (site_id, now, link_ids)
        self._db.query(sql)
        self._db.commit()
        return True


