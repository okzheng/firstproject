# -*- coding:utf-8 -*-

from urllib import request
import re

def getwebpage(website):
    with request.urlopen(website) as f:
        data = f.read()
        print('Status:', f.status, f.reason)
        for k, v in f.getheaders():
            print('%s: %s' % (k, v))
        print('***************************')
        print('Data:', data.decode('utf-8'))


def website_check(website):
    compiled = re.compile(r'^https?://(\w+)\.(\w+)')
    s = compiled.match(website)
    if s:
        return website
    else:
        raise ValueError


getwebpage(website_check('http://www.baidu.com'))