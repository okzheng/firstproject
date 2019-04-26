# -*- coding:utf-8 -*-

import re

# 对于可能需要多次使用正则表达式的，为提高效率，可先编译该正则
def testone():
    re_compiled = re.compile(r'^(\d+?)([2-6]{2})-(\w+)')
    m = re_compiled.match('0212426-46czff')
    if m:
        s = m.groups()
        print(s)
    else:
        print("not match!")




testone()