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


#获得地址电话等具体信息
def get_bus_mes(bus_url=None):
    try:
        bus_url = 'http://www.dianping.com/shop/22799131'
        #headers = {'Cookie':r'pac_uid=0_62911f8c4a696; pgv_pvi=924917760; RK=ZDObGGEOmv; LW_sid=U1z5g1b1D3G2w2S244U969M677; LW_uid=W1d5j1f1W3C2b2O2b4a9A9d6d8; eas_sid=T1R5V1Y123P2b2s2L4i9g9w8o4; o_cookie=2409764492; mpuv=30b2efcb-5120-4fb9-b790-623df60344a3; pgv_pvid=9561182312; pgv_si=s5504714752; _qpsvr_localtk=0.07680523967353192; ptui_loginuin=18061625823; ptisp=ctc; ptcz=04a175e7a24629270e9857a3cfb6defbccf0e579b474f1571fe1108277772e33; uin=o2409764492; skey=@aJyRJ4yxl; pt2gguin=o2409764492','User_Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36', 'Host':'confinfo.map.qq.com', 'Referer':'http://www.dianping.com/search/category/1/50', 'Accept':'image/webp,image/*,*/*;q=0.8', 'Connection':'keep-alive', 'Accept-Encoding':'gzip, deflate, sdch', 'Cache-Control':'no-cache', 'Pragma':'no-cache'}
        headers = {'User_Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36','Host':'confinfo.map.qq.com','Referer':'http://www.dianping.com/search/category/1/50','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Cookie':'pac_uid=0_62911f8c4a696; pgv_pvi=924917760; RK=ZDObGGEOmv; LW_sid=U1z5g1b1D3G2w2S244U969M677; LW_uid=W1d5j1f1W3C2b2O2b4a9A9d6d8; eas_sid=T1R5V1Y123P2b2s2L4i9g9w8o4; o_cookie=2409764492; mpuv=30b2efcb-5120-4fb9-b790-623df60344a3; pgv_pvid=9561182312; pgv_si=s5504714752; _qpsvr_localtk=0.07680523967353192; ptui_loginuin=18061625823; ptisp=ctc; ptcz=04a175e7a24629270e9857a3cfb6defbccf0e579b474f1571fe1108277772e33; uin=o2409764492; skey=@aJyRJ4yxl; pt2gguin=o2409764492'}
        print bus_url
        time.sleep(np.random.rand()*5)

        #req = urllib2.Request(bus_url, headers=hds[np.random.randint(0, len(hds))])
        req = urllib2.Request(bus_url, headers=headers)
        source_code = urllib2.urlopen(req).read()
        plain_text = str(source_code)
        print plain_text
    except (urllib2.HTTPError, urllib2.URLError),e:
        print e,'phone_error'
    print 'get_bus_mes'
    soup = BeautifulSoup(plain_text)
    addr = soup.find('span',{'itemprop':'street-address'}).string.strip()
    phone = soup.find('span',{'itemprop':'tel'}).string.strip()

    jishi = soup.find('p',{'class':'recommend-name'})
    print jishi
    for a in jishi:
        name = jishi.find('a',{'class':'item'}).string.strip()
        print name

    



if __name__ == '__main__':
    #book_tag_lists = ['科普','经典','生活','心灵','文学']
   get_bus_mes()
