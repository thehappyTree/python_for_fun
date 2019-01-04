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
import csv
reload(sys)
sys.setdefaultencoding('utf8')
#some User Agents
# 负债明细表
header_url = 'http://sh.imeiyebang.com'
#每个nav的信息
#self.dict_mes = {'info':info,'cards':cards,'serviceProduct':serviceProduct,'product':product,'record':record,'balance':balance,'coupon':coupon,'nursing':nursing,'healthy':healthy}
def account_detail():
    try_times = 0
    change_header = 1
    page = 1
    url = header_url + '/analyse/debt/detail.jhtml?type=courseCard'
    params1 = {"pageIndex":str(page),
            "pageSize": "20"
            }
    #params = urllib.urlencode(params1)
    #req = urllib2.Request(url,data=params, headers = hds[change_header%len(hds)])
    

    #url = 'https://www.douban.com/tag/'+urllib.quote(book_tag)+'?start='+str(page_num*20)+'&type=T'
    time.sleep(np.random.rand()*1)
    plain_text = None

    try:
        startIndex= 1
        endPage = 30
        endIndex = endPage + 1
        for page in xrange(startIndex, endIndex):
            params1['pageIndex'] = str(page)
            #params = json.dumps(params1)
            params = urllib.urlencode(params1)
            req = urllib2.Request(url,data=params, headers = hds[change_header%len(hds)])

            #urllib.urlretrieve(url,'./html/index.txt',headers=hds[change_header%len(hds)])#保存在当前路径的htm2.txt中
            source_code = urllib2.urlopen(req).read()
            plain_text = str(source_code)
            source_code = source_code.decode('utf-8')
            index_path = './html/account_detail/' +'account_detail_' + str(page) + '.txt'
            f1 = open(index_path,'w')
            f1.write(source_code)
            print index_path

    except (urllib2.HTTPError, urllib2.URLError), e:
        print e


    #list_soup = soup.find('div', {'class':'mod book-list'})
    #for d in detail:


    try_times += 1
    #if list_soup == None and try_times < 200:
    #    continue
    #elif list_soup == None or len(list_soup)<=1:
    #    break#200次请求后没有新的内容
    #    try_times=0#set 0 when got valid information
    change_header += 1






if __name__ == '__main__':
    #book_tag_lists = ['科普','经典','生活','心灵','文学']
    #book_tag_lists = ['摄影']
    #book_lists = do_spider(book_tag_lists)
    #print_book_lists_excel(book_lists, book_tag_lists)
    #meiye_spider()
    account_detail()
        
