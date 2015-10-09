#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import argparse
import requests

import common


def post(data = {}):
	if not data:
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
	r = requests.post(data['api'], data=param)
	return r.json()




if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-r', type=int, help='remote category id')
	parser.add_argument('-s', type=int, help='site id')
	if len(sys.argv) < 2:
		parser.print_help()
		sys.exit(0)
	args = parser.parse_args()
	# print args
	rcid, sid = args.r, args.s
	if not rcid or not sid:
		print "[error] rcid or sid error!"
		sys.exit(2)
	com = common.Common()
	rcinfo = com.get_rcat_info(rcid, sid)
	if not rcinfo:
		print "[error] remote category info empty!"
		sys.exit(3)
	posts = com.get_sync_posts(rcinfo['cid'], 50)
	if not posts: 
		print "[error] posts empty!"
		sys.exit(1)
	api = "http://%s/dede/api.php" % rcinfo['host']
	pids = []
	for i in posts:
		i['api'] = api
		i['rcid'] = rcinfo['rcid']
		ret = post(i)
		print "[%s][%s] %s " % (ret['ret'], ret['msg'], i['title'])
		pids.append(i['pid'])
	# print pids
	com.update_crawl_status(pids, 2)
	print '[success] sync finish!'

