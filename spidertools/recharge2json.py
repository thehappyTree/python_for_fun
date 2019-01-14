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
class Recharge:
    def __init__(self,parent_path,chargeReq):
        self.parent_path = parent_path
        self.chargeReq= chargeReq

    def action(self):
        try_times = 0
        change_header = 1
        rreq = open(self.parent_path+'/'+self.chargeReq,'r')
        r_dict = eval(rreq.read())
        params1 = r_dict
        url = header_url +'/card/objRecharge/list' 
        #url = 'https://www.douban.com/tag/'+urllib.quote(book_tag)+'?start='+str(page_num*20)+'&type=T'
        #time.sleep(np.random.rand()*5)
        #plain_text = None
        try:
            for i in xrange(1,100):
                filePath = self.parent_path + '/memberpage/page_' + str(i)
                if not os.path.exists(filePath):
                    break
                with open(filePath,'r') as f:
                    member = json.load(f)
                    body = member['body']
                    member_list = body['list']
                    headers = {'Content-Type':'application/json','Host':'api-b.imeiyebang.com'}
                    k=1
                    rechageFilePath = self.parent_path + '/recharg'
                    if not os.path.exists(rechageFilePath):
                        os.makedirs(rechageFilePath)

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
                        wFile = open(self.parent_path+'/recharg/'+m['code'],'w')
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
    #phone = '13675846617'
    phone = '13915218983'
    ms = Recharge(phone)
    ms.action()
        
