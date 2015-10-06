#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import requests

import common


def post(data = {}):
	if not data or not api:
		return False
	param = {
		'title': data['title'],
		'body': data['content'],
		# 'picname': 'http://www.baidu.com/img/baidu_jgylogo3.gif',
		'username': 'admin',
		'password': 'admin',
		'typeid': data['rcid'],
		'channelid': 1,
		'autokey': 1,
		'ishtml': 1,
	}
	print param['title']
	r = requests.post(data['api'], data=param)
	return r.text




if __name__ == '__main__':
	print 'dedecms run ... '
	com = common.Common()
	rcinfo = com.get_rcat_info(12, 2)
	posts = com.get_sync_posts(rcinfo['cid'], 500)
	if not posts: sys.exit(1)
	api = "http://%s/dede/api.php" % rcinfo['host']
	pids = []
	for i in posts:
		i['api'] = api
		i['rcid'] = rcinfo['rcid']
		print post(i)
		pids.append(i['pid'])
	print pids
	com.update_crawl_status(pids, 2)
	print 'dedecms finish!'

