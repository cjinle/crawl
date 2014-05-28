#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""mysql class"""

import ConfigParser
import MySQLdb
import MySQLdb.cursors

class MySQL:
    _con = None
    _cursor = None
    
    def __init__(self, **config):
        default_config = {
                          'host' : 'localhost',
                          'user' : 'root',
                          'passwd' : '',
                          'charset' : 'utf8',
                          'db' : 'test',
                          'cursorclass' : MySQLdb.cursors.DictCursor,
                          }
        if not config:
            cfg = ConfigParser.ConfigParser()
            cfg.read('scrapy.cfg')
            config = cfg._sections['db']
            config.pop('__name__')
        try:
            self._con = MySQLdb.connect(**dict(default_config, **config))
        except Exception as e:
            print "Exception: %s" % e
        self._cursor = self._con.cursor()
        
    def query(self, sql = None):
        if sql:
            try:
                self._cursor.execute(sql)
            except Exception as e:
                print "Exception: %s" % e
            
    def get_one(self, sql = None):
        ret = ()
        if sql:
            self.query(sql)
            ret = self._cursor.fetchone()
        return ret
        
    def get_row(self, sql = None):
        ret = ()
        if sql:
            self.query(sql)
            ret = self._cursor.fetchmany()[0]
        return ret
    
    def get_all(self, sql = None):
        ret = ()
        if sql:
            self.query(sql)
            ret = self._cursor.fetchall()
        return ret
    
    def commit(self):
        self._con.commit()

    def escape_string(self, s):
        return MySQLdb.escape_string(s)
    
    def __del__(self):
        self._con.close()