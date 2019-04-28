# -*- coding:utf-8 -*-


from urllib import request,parse
import re
import json


def getwebpage(website, **args):
    # req = request.Request(website)
    # req.add_header('key', args[0])
    # req.add_header('id', args[1])
    # newurl = website + "?" + strjoin(args)
    data = parse.urlencode(args)
    print(data)
    with request.urlopen(website + '?' + data) as f:
        data = f.read()
        print('Status:', f.status, f.reason)
        for k, v in f.getheaders():
            print('%s: %s' % (k, v))
        print('*****************************')
        raw_data = data.decode('utf-8')
        print('Data:', raw_data)
        print(json.dumps(raw_data,indent=2))


def website_check(website):
    compiled = re.compile(r'^https?://(\w+?)\.(\w+)')
    s = compiled.match(website)
    if s:
        return website
    else:
        raise ValueError

# replaced by parse.urlencode()
def strjoin(dic):
    s = ""
    for i in dic:
       s = s + i + '=' + dic[i] + '&'
    return s[0:-1]

if __name__ == '__main__':
    web = 'http://zuowen.api.juhe.cn/zuowen/typeList'
    getwebpage(website_check(web),key='db48e3dc51321fcb46d8b0d82dfb0bca',id='2')