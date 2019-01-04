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
import csv
reload(sys)
sys.setdefaultencoding('utf8')
#some User Agents
header_url = 'http://sh.imeiyebang.com'
#每个nav的信息
#self.dict_mes = {'info':info,'cards':cards,'serviceProduct':serviceProduct,'product':product,'record':record,'balance':balance,'coupon':coupon,'nursing':nursing,'healthy':healthy}
#拉取详情信息
def detail_spider(nav_url):
    f = open('./html/urlmes.csv')
    reader  = csv.DictReader(f)
    change_header = 1
    for r in reader:
        #time.sleep(np.random.rand()*5)
        nav_url = r['url']
        file_r_name = r['file_path']
        tp = r['type']
        req_nav = urllib2.Request(nav_url, headers = hds[change_header%len(hds)])
        source_nav = urllib2.urlopen(req_nav).read()
        source_nav  = source_nav.decode('utf-8')
        #print str(source_nav)
        print nav_url, file_r_name
        f = open(file_r_name,'w')
        f.write(source_nav)
        f.close()









if __name__ == '__main__':
    #book_tag_lists = ['科普','经典','生活','心灵','文学']
    #book_tag_lists = ['摄影']
    #book_lists = do_spider(book_tag_lists)
    #print_book_lists_excel(book_lists, book_tag_lists)
    #meiye_spider()
    detail_spider(None)
        
