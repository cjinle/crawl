#!/usr/bin/env python
# -*- coding=utf-8 -*-

import requests

url = 'http://data.zz.baidu.com/urls?site=www.pouman.com&token=GCQUnkSS450IClNv'
param = [
'http://www.pouman.com',
'http://www.pouman.com/a/youmoxiaohua/',
'http://www.pouman.com/a/youmoxiaohua/2015/1009/10637.html',
'http://www.pouman.com/a/duanzi/',
'http://www.pouman.com/a/duanzi/2015/1008/205.html',
]
print param
r = requests.post(url, data="\n".join(param))
print r.text
print r.json()
