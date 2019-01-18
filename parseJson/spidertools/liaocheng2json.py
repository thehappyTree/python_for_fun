# _*_ coding:utf-8 _*_
import sys
import time
import urllib
import urllib2
import requests
import numpy as np
from bs4 import BeautifulSoup
from openpyxl import Workbook
import json
import csv
import os
reload(sys)
sys.setdefaultencoding('utf8')
header_url = 'https://api-b.imeiyebang.com'
class LiaoCheng:
    def __init__(self,parent_path,liaochengReq):
        self.parent_path = parent_path
        self.liaochengReq= liaochengReq

    def action(self):
        try_times = 0
        change_header = 1
        rreq = open(self.parent_path+'/'+self.liaochengReq,'r')
        r_dict = eval(rreq.read())
        params1 = r_dict
        print params1
        url = header_url + '/card/objCourseCard/list'
        #url = 'https://www.douban.com/tag/'+urllib.quote(book_tag)+'?start='+str(page_num*20)+'&type=T'
        #time.sleep(np.random.rand()*5)
        #plain_text = None
        try:
            k=1
            for i in xrange(1,100):
                filePath = self.parent_path + '/memberpage/page_' + str(i)
                if not os.path.exists(filePath):
                    break
                with open(filePath,'r') as f:
                    member = json.load(f)
                    body = member['body']
                    member_list = body['list']
                    headers = {'Content-Type':'application/json','Host':'api-b.imeiyebang.com','appType':'IOS_B_PAD_STORE'}
                    liaochengFilePath = self.parent_path + '/liaocheng'
                    if not os.path.exists(liaochengFilePath):
                        os.makedirs(liaochengFilePath)

                    for m in member_list:
                        k += 1
                        print k,m['code']
                        params1['body']['belongToPartyCode'] = m['code']
                        textmod = json.dumps(params1)
                        time.sleep(np.random.rand())
                        print m['code']
                        req = urllib2.Request(url,data=textmod, headers = headers)
                        res = urllib2.urlopen(req)
                        res = res.read()
                        wFile = open(self.parent_path+'/liaocheng/'+m['code'],'w')
                        wFile.write(res)
                        wFile.close()


        except (urllib2.HTTPError, urllib2.URLError), e:
            print e
        try_times += 1
        change_header += 1


if __name__ == '__main__':
    #book_tag_lists = ['科普','经典','生活','心灵','文学']
    #book_tag_lists = ['摄影']
    #book_lists = do_spider(book_tag_lists)
    #print_book_lists_excel(book_lists, book_tag_lists)
    #meiye_spider()
    phone = '13675846617'
    #phone = '13915218983'
    ms = LiaoCheng(phone)
    ms.aciton()
