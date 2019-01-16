# -*- coding:utf-8 -*-
import ConfigParser
import os
'''
ColMember，Recharge，LiaoCheng为爬虫相关类
需要在联网的情况下爬取
'''
#note:ColMember仅爬取/clerk/customerProfile/listNew接口的数据
#params:
#   phone:商户pc端电话（作为目录用一切数据都存放在其中）
#   count:/clerk/customerProfile/listNew接口中的会员数量从pad端收银可见
#pad端收银会员列表爬取,rechargpage.txt为接口的必要request
from spidertools.member_all import ColMember 
# 储值卡爬取
#note Recharge 为/card/objRecharge/list 接口拉取储值卡数据
#params:
#   parent_path:pc端代码目录
#pad端爬取储值卡数据 配置 接口request的json在配置文件字段chargeReq配置文件名(无须路径)
from spidertools.recharge2json import Recharge
#note:Liaocheng为/card/objCourseCard/list接口数据
#params:
#   parent_path:pc端代码目录
#pad端爬取储值卡数据 配置 接口request的json在文件配置liaochengReq配置文件名(无须路径)
from spidertools.liaocheng2json import LiaoCheng #疗程卡数据爬取

'''
Exchange : pad端价格表四个列表数据转换类(转成excel)
Recharge2Excel,LiaoCheng2Excel将json转换为excel
爬取完成的情况下运行
'''
#Exchange直接转换相应json即可
#item=
#产品
#product=
#套卡
#taocard=
#充值卡
#recharge=
from spidertools.jsonParse import Exchange # pad端价格表四个列表数据转换类(转成excel)
from spidertools.recharge2excel import Recharge2Excel #储值卡转换为excel
from spidertools.liaocheng2excel import LiaoCheng2Excel #疗程卡转换为excel

#根据配置文件获取内容
class Configure:
    def __init__(self, section):
        self.section = section

    def getConfig(self,key):
        config = ConfigParser.ConfigParser()
        path = os.path.split('./spiderConfig.conf')
        config.read(path)
        return config.get(self.section, key)

def pullData(phone):
    cf = Configure(phone)
    #价目表处理
    print "处理价目项数据"
    item = cf.getConfig('item')
    product = cf.getConfig('product')
    taocard = cf.getConfig('taocard')
    recharge = cf.getConfig('recharge')
    #parent_path,item,product,taocard,recharge
    ec = Exchange(phone, item, product, taocard, recharge)
    ec.action()

    print "价目表处理完成"


    # 会员信息
    print "会员开始"
    count = int(cf.getConfig('count'))
    memberReq = cf.getConfig('memberReq')
    cm = ColMember(phone,count,memberReq)
    cm.action()
    print "会员完成"

    #充值卡
    chargeReq = cf.getConfig('chargeReq')
    rc = Recharge(phone,chargeReq)
    rc.action()
    rce = Recharge2Excel(phone)
    rce.action()

    #疗程卡
    liaochengReq = cf.getConfig('liaochengReq')
    lc = LiaoCheng(phone,liaochengReq)
    lc.action()
    lce = LiaoCheng2Excel(phone)
    lce.action()

if __name__ == '__main__':
    #cof = Confiure('')
    phone = '18768174001'
    pullData(phone)
