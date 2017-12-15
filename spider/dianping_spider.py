# _*_ coding:utf-8 _*_
import sys
import time
import urllib
import urllib2
import requests
import numpy as np
from bs4 import BeautifulSoup
from openpyxl import Workbook

reload(sys)
sys.setdefaultencoding('utf8')
#some User Agents
hds = [{'User_Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'},{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}]

def bus_spider():
    print 'begin'
    page = 'p'
    page_num =1 
    try_time = 0
    while(1):
        url = 'http://www.dianping.com/search/category/1/50/p'+str(page_num)+'?aid=14894422%2C20816759%2C22799131%2C57870609%2C23558461%2C24712018'
        time.sleep(np.random.rand()*5)
        try:
            req = urllib2.Request(url, headers=hds[page_num%len(hds)])
            source_code = urllib2.urlopen(req).read()
            plain_text = str(source_code)

        except (urllib2.HTTPError, urllib2.URLError), e:
            print 's',e
            continue
        soup = BeautifulSoup(plain_text)
        list_soup = soup.find('div',{'id':'shop-all-list'})
        try_time += 1
        if list_soup == None and try_times <200:
            continue
        elif list_soup == None or len(list_soup)<=1:
            break
        li = list_soup.findAll('li')
        for bus in li:
            img_src = bus.find('img',attrs={'data-src':True}).attrs['data-src']
            tit = bus.find('a')
            url = tit.get('href')
            name = bus.find('h4').string.strip()
            print img_src, url, name
            get_bus_mes(url)

        page_num+=1

#获得地址电话等具体信息
def get_bus_mes(bus_url):
    try:
        #headers = {'Cookie':r'_lxsdk_cuid=1600ba03c44c8-092631b1ece31a-b373f68-144000-1600ba03c44c8; _lxsdk=1600ba03c44c8-092631b1ece31a-b373f68-144000-1600ba03c44c8; _hc.v=6caf536f-faf2-2f16-2fbf-f7250c5f4adb.1512023539; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; s_ViewType=10; _lxsdk_s=160254fb692-b8b-00c-0aa%7C%7C23; aburl=1; cy=1; cye=shanghai; _hc.s="\"6caf536f-faf2-2f16-2fbf-f7250c5f4adb.1512023539.1512454412.1512456929\""','User_Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36', 'Host':'hls.dianping.com', 'Referer':bus_url, 'Accept':'image/webp,image/*,*/*;q=0.8', 'Connection':'keep-alive', 'Accept-Encoding':'gzip, deflate, sdch', 'Cache-Control':'no-cache', 'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.6,en-US;q=0.4,en;q=0.2','Pragma':'no-cache'}
        headers = {'User_Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36','Host':'rt1.map.gtimg.com'}
        print bus_url
        time.sleep(np.random.rand()*5)

        #req = urllib2.Request(bus_url, headers=hds[np.random.randint(0, len(hds))])
        req = urllib2.Request(bus_url, headers=headers)
        source_code = urllib2.urlopen(req).read()
        plain_text = str(source_code)
    except (urllib2.HTTPError, urllib2.URLError),e:
        print e,'phone_error'
    print 'get_bus_mes'
    soup = BeautifulSoup(plain_text)
    print plain_text
    addr = soup.find('span',{'itemprop':'street-address'}).string.strip()
    phone = soup.find('span',{'itemprop':'tel'}).string.strip()

    jishi = soup.find('p',{'class':'recommend-name'})
    print jishi
    for a in jishi:
        name = jishi.find('a',{'class':'item'}).string.strip()
        print name

    



if __name__ == '__main__':
    #book_tag_lists = ['科普','经典','生活','心灵','文学']
    bus_spider()
        
