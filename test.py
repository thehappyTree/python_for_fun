# _*_ coding:utf-8 _*_
import sys
import time
import urllib
import urllib2
import requests
import numpy as np
from bs4 import BeautifulSoup
from openpyxl import Workbook
from headers import hds
import json
reload(sys)
sys.setdefaultencoding('utf8')
#some User Agents
header_url = 'http://sh.imeiyebang.com'
#每个nav的信息
#self.dict_mes = {'info':info,'cards':cards,'serviceProduct':serviceProduct,'product':product,'record':record,'balance':balance,'coupon':coupon,'nursing':nursing,'healthy':healthy}
def meiye_spider():
    try_times = 0
    change_header = 1
    page = 1
    params1 = {"shopCode":'' ,
            "customerTag": '',
            "startTime": '',
            "endTime": '',
            "customerName":'', 
            "mobile": '',
            "pageIndex": 0,
            "pageSize": 100}
    

    url = header_url + '/report/customer/list.jhtml'
    #url = 'https://www.douban.com/tag/'+urllib.quote(book_tag)+'?start='+str(page_num*20)+'&type=T'
    time.sleep(np.random.rand()*5)


    try:
        params1['pageIndex'] = 2
        params = json.dumps(params1)
        req = urllib2.Request(url,data=params, headers = hds[change_header%len(hds)])
        #urllib.urlretrieve(url,'./html/index.txt',headers=hds[change_header%len(hds)])#保存在当前路径的htm2.txt中
        source_code = urllib2.urlopen(req).read()
        plain_text = str(source_code)
        print plain_text

    except (urllib2.HTTPError, urllib2.URLError), e:
        print e

if __name__ == '__main__':
    #book_tag_lists = ['科普','经典','生活','心灵','文学']
    #book_tag_lists = ['摄影']
    #book_lists = do_spider(book_tag_lists)
    #print_book_lists_excel(book_lists, book_tag_lists)
    #meiye_spider()
    meiye_spider()
        
