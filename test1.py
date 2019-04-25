# -*- coding:utf-8 -*-

import os
import re
import urllib
from datetime import datetime



def playfunc(func):
    def inner(school):
        if re.match(r'[A-Z]{1}[a-z]{1,11}[\s]?[a-zA-Z]{0,10}$', school):
            school = "Good " + school
        else:
            school = "low"
        func(school)
    return inner
# func1 = playfunc(func1)

@playfunc
def func1(school):
    print("The school is %s university!" % school)

if __name__ == "__main__":
    print os.name
    print os.environ
    print "i want to leave here right now"
    print("Process %s start ..." % os.getpid())
    now = datetime.now()
    da = datetime(2017,3,9,18,22)
    # da.fromtimestamp()
    # now.timestamp()
    print(type(now))
    s = r'ABE284-039 65a2'
    if re.match(r'[A-E]{3}[1-8]{3}-[0-9]{3}\s[2-6a-z]{4}',s):
        print("ok")
    else:
        print("failed")
    func1("Shanghai ")