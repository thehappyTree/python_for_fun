# -*- coding:utf-8 -*-
import json
from openpyxl import load_workbook,Workbook
import os

class LiaoCheng2Excel:
    def __init__(self,parent_path,excelName=''):
        self.parent_path = parent_path
        self.excelName = excelName
    
    def action(self):
        wb = Workbook()
        ws = wb.active
        pagePath = self.parent_path + '/memberpage'
        title = [u'会员名',u'会员电话',u'卡名称',u'金额',u'总次数',u'剩余次数',u'创建时间']
        ws.append(title)
        for i in xrange(1,100):
            pPath = pagePath + '/page_' + str(i) 
            if not os.path.exists(pPath):
                break
            with open(pPath) as pf:
                pageJson = json.load(pf)
                plist = pageJson['body']['list']
                for p in plist:
                    rFilePath = self.parent_path +'/liaocheng/'+p['code']
                    name = p['customerName']
                    phone = p['mobile']
                    with open(rFilePath) as imf:
                        rj = json.load(imf)
                        rbody = rj['body']
                        for r in rbody:
                            cardName = r['objName']
                            account = int(r['amount'])/100.00
                            buytime = r.get('createdAt','')
                            buytime = buytime[:10] if buytime else ''
                            total = r['totalCount']
                            rem = r['remainCount']
                            ws.append([name,phone,cardName,account,total,rem,buytime])
                    rFilePath = None

        
        wb.save(self.parent_path+'/' + self.parent_path +'_' +self.excelName + '_疗程卡详情.xlsx')






if __name__ == '__main__':
    #getExcelSheet()
    #phone = '18519005765'
    phone = '13675846617'
    #reads()
    #phone = '13915218983'
    rc = LiaoCheng2Excel(phone)
    rc.action()
