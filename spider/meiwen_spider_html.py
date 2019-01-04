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
header_url = 'http://sh.imeiyebang.com'
#每个nav的信息
#self.dict_mes = {'info':info,'cards':cards,'serviceProduct':serviceProduct,'product':product,'record':record,'balance':balance,'coupon':coupon,'nursing':nursing,'healthy':healthy}
f_write = open('./html/urlmes.csv','w')
fieldnames = ['url','file_path','type']
write = csv.DictWriter(f_write, fieldnames = fieldnames)
def meiye_spider():
    try_times = 0
    change_header = 1
    #page = 1
    f = open('index','w')
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
    plain_text = None


    try:
        for page in xrange(1,7):
            params1['pageIndex'] = page
            #params = json.dumps(params1)
            params = urllib.urlencode(params1)
            req = urllib2.Request(url,data=params, headers = hds[change_header%len(hds)])

            #urllib.urlretrieve(url,'./html/index.txt',headers=hds[change_header%len(hds)])#保存在当前路径的htm2.txt中
            source_code = urllib2.urlopen(req).read()
            plain_text = str(source_code)
            print '----------new page--------'
            print plain_text
            source_code = source_code.decode('utf-8')
            index_path = './html/index/' +'page_' + str(page) + '.txt'
            f1 = open(index_path,'w')
            f1.write(source_code)
            soup = BeautifulSoup(plain_text)
            detail = soup.find('tbody')
            trs = detail.find_all('tr')
            for tr in trs:
                k = 0
                tds = tr.find_all('td')
                num,detail_request = None,None
                for index, td in enumerate(tds):
                    if index == 1:num=td.text
                    elif index == 8:
                        detail_request = td.find('a').get('href') 

                #num,detail_request = tds[1],tds[8]
                detail_name = 'detail_'+ str(page) +'_' + str(num)
                #detail_request = td.find('a').get('href')
                detail_url = header_url + detail_request
                #print td.find('a').href
                req_detail = urllib2.Request(detail_url, headers = hds[change_header%len(hds)])
                source_detail = urllib2.urlopen(req_detail).read()
                detail_text = str(source_detail)
                detail_spider(detail_text, detail_name)

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

#拉取详情信息
def detail_spider(detail_text,file_name):
    change_header = 1
    try:
        soup = BeautifulSoup(detail_text, features="html.parser")
        #print soup
        ul = soup.find('ul',{'class':'nav-tabs'})
        lis = ul.find_all('li')
        for li in lis:
            time.sleep(np.random.rand()*5)
            nav_request = li.find('a').get('href')
            nav_url = header_url + nav_request
            nav_type = nav_request.split('type=')[1]
            file_r_name = './html/' + file_name + '_'+nav_type + '.txt'
            write.writerow({'url':nav_url,'file_path':file_r_name,'type':nav_type})
            print nav_url+','+file_r_name +','+nav_type
            '''
            req_nav = urllib2.Request(nav_url, headers = hds[change_header%len(hds)])
            source_nav = urllib2.urlopen(req_nav).read()
            #nav_text = str(source_nav)
            source_nav = source_nav.decode('utf-8')
            nav_type = nav_request.split('type=')[1]
            print nav_type,nav_request
            file_r_name = './html/' + file_name + '_'+nav_type + '.txt'
            file_r_name = str(file_r_name)
            #urllib.urlretrieve(req_nav,file_r_name,headers=hds[change_header%len(hds)])#保存在当前路径的htm2.txt中
            f = open(file_r_name,'w')
            f.write(source_nav)
            f.close()
            '''
            change_header += 1
    except Exception,e:
        print e









if __name__ == '__main__':
    #book_tag_lists = ['科普','经典','生活','心灵','文学']
    #book_tag_lists = ['摄影']
    #book_lists = do_spider(book_tag_lists)
    #print_book_lists_excel(book_lists, book_tag_lists)
    meiye_spider()
        
