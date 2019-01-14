# _*_ coding:utf-8 _*_
import sys
import time
import urllib
import urllib2
import requests
import numpy as np
import json
import math
import os
reload(sys)
sys.setdefaultencoding('utf8')
header_url = 'https://api-b.imeiyebang.com'
class ColMember:
    def __init__(self,parent_path,count,memberReq):
        self.parent_path = parent_path
        self.count = count
        self.memberReq= memberReq

    def action(self):
        try_times = 0
        change_header = 1
        f_page = open(self.parent_path + '/'+ self.memberReq)
        params1 = eval(f_page.read())
        url = header_url +'/clerk/customerProfile/listNew' 
        #url = 'https://www.douban.com/tag/'+urllib.quote(book_tag)+'?start='+str(page_num*20)+'&type=T'
        #time.sleep(np.random.rand()*5)
        #plain_text = None
        try:
            headers = {'Content-Type':'application/json','Host':'api-b.imeiyebang.com'}
            page = int(math.ceil(self.count/50.0))
            print page
            pageFilePath = self.parent_path+'/memberpage'
            if not os.path.exists(pageFilePath):
                os.makedirs(pageFilePath)
            for m in xrange(1,page+1):
                params1['body']['page'] = m
                textmod = json.dumps(params1)
                req = urllib2.Request(url,data=textmod, headers = headers)
                res = urllib2.urlopen(req)
                res = res.read()
                wFile = open(self.parent_path+'/memberpage/page_'+str(m),'w')
                print m
                wFile.write(res)
                wFile.close()
                time.sleep(np.random.rand())
                #break


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
    #phone = '13915218983'
    phone = '13675846617'
    count = 377

    ms = ColMember(phone,count )
    ms.action()
        
