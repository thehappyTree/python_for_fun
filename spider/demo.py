# _*_ coding:utf-8 _*_
import urllib
import urllib2
import re

def getHtml(url):
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    getImg(response.read())


def getImg(html):
    reg = r'src="(.+?\.jpg)" size'
    imgre = re.compile(reg)
    imglist = re.findall(imgre, html)
    x = 100
    for imgurl in imglist:
        urllib.urlretrieve(imgurl, '{name}.jpg'.format(name=x))
        x+=1
        print x

getHtml("https://tieba.baidu.com/p/5406071122")
#print getImg(html)


