#!/usr/local/bin/python2.7
# _*_ coding: utf-8 _*_
# file: getdata.py
# time: 2018/10/30 5:16 PM
# version: 1.0
# __author__: ChengChen
# contact: saicc4869@163.com
import cons
import urllib2
import re
import json
import time
import multiprocessing as mp


def getUserName():
    req = urllib2.Request('https://flightaware.com/ajax/ignoreuser/adsb/adsb_stats.rvt?table=sites&start=0&length=1000')
    req.add_header('user-agent', cons.headers())
    html = urllib2.urlopen(req).read()
    dict = json.loads(html)
    # print dict['data'][0]['user_username']
    names = list()
    for item in dict['data']:
        names.append(item['user_username'])
    return names


def getLocation(userName):
    req = urllib2.Request('https://flightaware.com/adsb/stats/user/'+userName)
    req.add_header('user-agent', cons.headers())
    html = urllib2.urlopen(req).read()
    loc = re.search(r'"latitude":(-?[0-9]*.[0-9]*),"longitude":(-?[0-9]*.[0-9]*),', html)
    location = (loc.group(1), loc.group(2))
    return location


# def thread_job(group, q):
#     for name in group:
#         if name is not None:
#             continue
#         # print name
#         global Max_Num
#         Max_Num = 5
#         for i in range(Max_Num):
#             try:
#                 locList.append(getLocation(name))
#                 break
#             except:
#                 if i < Max_Num:
#                     continue
#                 else:
#                     print 'URLError: <urlopen error [Errno 60] Operation timed out>'
#         # locList.append(getLocation(name))


if __name__ == '__main__':
    start = time.time()
    userList = getUserName()
    # pool = mp.Pool(4)
    # userList_jobs = [pool.apply_async()]
    # print userList
    locList = list()
    for name in userList:
        if name is None:
            continue
        print name
        global Max_Num
        Max_Num = 5
        for i in range(Max_Num):
            try:
                locList.append(getLocation(name))
                break
            except:
                if i < Max_Num:
                    continue
                else:
                    print 'URLError: <urlopen error [Errno 60] Operation timed out>'
    #     # locList.append(getLocation(name))
    # print locList
    end = time.time()
    print end - start
    with open('locaton.txt', 'w+') as f:
        for item in locList:
            f.write('('+item[0]+','+item[1]+')'+'\n')
