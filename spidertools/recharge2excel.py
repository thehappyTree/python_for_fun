# -*- coding:utf-8 -*-
import json
from openpyxl import load_workbook,Workbook
import os

class Recharge2Excel:
    def __init__(self,parent_path):
        self.parent_path = parent_path


    
    def action(self):
        wb = Workbook()
        ws = wb.active
        pagePath = self.parent_path + '/memberpage'
        title = [u'会员名',u'会员电话',u'卡名称',u'充值金额',u'剩余金额',u'折扣',u'购买时间']
        ws.append(title)
        for i in xrange(1,100):
            pPath = pagePath + '/page_' + str(i) 
            if not os.path.exists(pPath):
                break
            with open(pPath) as pf:
                pageJson = json.load(pf)
                plist = pageJson['body']['list']
                for p in plist:
                    rFilePath = self.parent_path +'/recharg/'+p['code']
                    print rFilePath
                    name = p['customerName']
                    phone = p['mobile']
                    with open(rFilePath) as imf:
                        rj = json.load(imf)
                        rbody = rj['body']
                        for r in rbody:
                            cardName = r['objName']
                            originAmount = int(r['originAmount'])/100.00
                            account = int(r['account'])/100.00
                            singleDiscount = r['singleDiscount']
                            buytime = r.get('createTime','')
                            buytime = buytime[:10] if buytime else ''
                            ws.append([name,phone,cardName,originAmount,account,singleDiscount,buytime,p['code']])
                    rFilePath = None

        
        wb.save(self.parent_path+'/recharge.xlsx')






if __name__ == '__main__':
    #getExcelSheet()
    #phone = '18519005765'
    #phone = '13675846617'
    #reads()
    phone = '13915218983'
    rc = Recharge2Excel(phone)
    rc.action()
