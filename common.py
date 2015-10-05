#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import mysqllib

class Common:
    """common class"""
    _db = None

    def __init__(self):
        self._db = mysqllib.MySQL()

    def get_cat_info(self, cid = 0):
        if not cid:
            return False
        sql = "select c.*,s.host from cw_categories as c left join cw_sites as s on (c.sid=s.sid) " \
              " where c.cid='%s' " % cid
        return self._db.get_one(sql)

    def get_crawl_urls(self, cid = 0, status = 0):
        if not cid:
            return False
        sql = "select * from cw_posts where cid='%s' and status='%s' limit 2" % (cid, status)
        return self._db.get_all(sql)

    def query(self, sql):
        self._db.query(sql)
        self._db.commit()

    def db_str(self, s):
        return self._db.escape_string(s)

    def get_one(self, sql):
        return self._db.get_one(sql)

    def add_crawl_log(self, spider, site_id = 0, ext = {}):
        if not spider:
            log.msg("add_crawl_log ERROR", level=log.ERROR)
            return False
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        import socket
        subject = "crawl result [spider:%s] %s!" % (spider.name, socket.gethostname())
        ext = [ "%s: %s" % (str(k), str(v)) for k,v in ext.items() ]
        # self.send_mail('chenjinle@qq.com', subject, "\n".join(ext))
        # ext = self.db_str(ext.encode('utf-8').strip())
        ext = self.db_str("<br>".join(ext))
        sql = "insert into crawl_logs (site_id, spider, log_type, ip, add_time, ret, content) values " \
              " ('%s', '%s', '%s', '%s', '%s', '%s', '%s') " % (site_id, spider.name, 7, socket.gethostname(), now, 1, ext)
        self.query(sql)
        return True

    def send_mail(self, to, subject, content):
        import sys
        import ConfigParser
        import smtplib
        from email.mime.text import MIMEText
        from email.message import Message
        cfg = ConfigParser.ConfigParser()
        cfg.read('scrapy.cfg')
        config = cfg._sections['mail']
        try:
            smtp = smtplib.SMTP(local_hostname=config['host'])
            #smtp.set_debuglevel(1)
            smtp.connect(config['host'], config['port'])
            smtp.login(config['user'], config['passwd'])
            msg = MIMEText(content)
            msg['Subject'] = subject
            msg['From'] = config['user']
            msg['To'] = to
            smtp.sendmail(config['user'], to, msg.as_string())
        except Exception as e:
            print "Common.send_mail Exception: %s" % e
        return True


