# -*- coding:utf-8 -*-
import csv
import sys
from serviceAPI import WebAPI
reload(sys)
sys.setdefaultencoding('UTF-8')
import time
class login():
    def __init__(self):
        self.wapi = WebAPI(url='http://erp.mei1.info')
        self.wapi.login(db='odoo_171024',username='admin',password='meiwen666666')
        '''
        self.wapi = WebAPI(url='http://erp.dev.mei1.info')
        self.wapi.login(db='mwodoo10',username='admin',password='meiwen666666')
        '''
    def get_wapi(self):
        return self.wapi

class create_contact():
    def __init__(self, wapi):
        self.wapi = wapi


    def read(self):
        f = open('potential_merchant.csv')
        reader = csv.DictReader(f)
        self.reader = reader


    def action(self):
        for r in self.reader:
            print '-------------------------------------------------'

            company_id = self.wapi.search_read(model='res.partner',domain=[('x_potential_merchant_id','=',r['id'])])
            print '--name:',r['contact_name'],'--phone:',r['contact_phone'],'company_id',company_id[0],r['id']
            print self.wapi.create('res.partner',{'name':r['contact_name'],'phone':r['contact_phone'], 'is_company':False, 'parent_id':company_id[0]})
            break

    def finish(self):
        pass
class create_employee():
    def __init__(self, wapi):
        self.wapi = wapi

    def read(self):
        f = open('t_saas_opt_operator.csv')
        reader = csv.DictReader(f)
        self.reader = reader
    
    def action(self):
        for r in self.reader:
            pass

    def finish(self):
        pass


class create_partner():
    def __init__(self, wapi):
        self.wapi = wapi
        self.optindustry = [('beauty', '1'),('hairdress', '2'), ('nail','3'), ('pedicure', '5'), ('composite','6'), ('other','7'), ('skin', '8'), ('yoga', '9'), ('pet', '10'), ('medical','11'), ('tatto','12'), ('acne','13'), ('postmold','14'), ('fitness','15'), ('dance','16'), ('wedding','17'),('jewel','18')]
        self.industry = {}

    def read(self):
        for ind in self.optindustry:
            self.industry[ind[1]] = ind[0]
        f = open('potential_merchant.csv')
        reader = csv.DictReader(f)
        self.reader = reader
    def action(self):
        for r in self.reader:
            print '------------------'
            print 'insert: x_potential_merchant_id:',r['id'],'--name:',r['customer_name'], '--street2:',r['customer_address'],'--phone:',r['contact_phone'],'--x_industry:',self.industry[r['business_scope_id']]
            self.wapi.create('res.partner', {'x_potential_merchant_id':r['id'], 'name':r['customer_name'], 'street2':r['customer_address'], 'phone':r['contact_phone'], 'x_industry':self.industry[r['business_scope_id']], 'is_company':True})

    def end(self):
        pass

class create_visit():

    def __init__(self, wapi):
        self.wapi = wapi

    def read(self):
        f = open('t_saas_merchant_visit_newplus.csv')
        reader = csv.DictReader(f)
        self.reader = reader

    def action(self):
        i = 0
        c_id = None
        for r in self.reader:
            print '**************************'
            i += 1
            print i,r['potential_merchant_id'],r['submit_time']
            if i <= 0:
                continue
            if r['potential_merchant_id'] == '1906035348685395':
                continue
            company_id = self.wapi.search_read(model='res.partner', domain=[('x_potential_merchant_id','=',r['potential_merchant_id'])])
            print company_id
            if len(r['contact_phone']) == 0:
                r['contact_phone'] = u'未填写'+str(i)
            contact = self.wapi.search_read(model='res.partner', domain=[('is_company','=',False),('phone','=',r['contact_phone']),('parent_id','=',company_id[0])])
            if len(contact) == 0 :
                print r['contact_name'],r['contact_phone'],r['customer_address'],company_id[0],r['potential_merchant_id']
                contact_id = self.wapi.create('res.partner', {'name':r['contact_name'],'phone':r['contact_phone'],"street2":r['customer_address'], 'is_company':False, 'parent_id':company_id[0]})
            #创建congtact:
                c_id = contact_id
            else:
                c_id = contact[0]
        
            print 'contact_name--:',r['contact_name'],c_id,':customer_info:',r['customer_info'],'--first_visit:',r['first_visit'],'--unsign_reason:',r['unsign_reason'],'--potential_merchant_id:',r['potential_merchant_id']
            self.wapi.create('x_visit_record',{'x_visit_parent_id':company_id[0], 'x_contact_id':c_id, 'x_profiling':r['customer_info'], 'x_first_visit':r['first_visit'],'x_unsign_reason':r['unsign_reason'],'x_solution':r['solution'],'x_summary':r['note'], 'x_contact_phone':r['contact_phone'], 'x_address':r['customer_address']})
            print i

class insert():
    def __init__(self):
        self.optindustry = [('beauty', '1'),('hairdress', '2'), ('nail','3'), ('pedicure', '5'), ('composite','6'), ('other','7'), ('skin', '8'), ('yoga', '9'), ('pet', '10'), ('medical','11'), ('tatto','12'), ('acne','13'), ('postmold','14'), ('fitness','15'), ('dance','16'), ('wedding','17'),('jewel','18')]
        self.industry = {}

    def get_industry(self):
        for ind in self.optindustry:
            self.industry[ind[1]] = ind[0]
        #for key,value in reader.iteritems():
        #    print key,value

    def read(self):
        f = open('potential_merchant.csv')
        reader = csv.DictReader(f)
        wapi = WebAPI(url='http://erp.dev.mei1.info')
        wapi.login(db='mwodoo10',username='admin',password='meiwen666666')
        '''
        for r in reader:
            #print 'x_potential_merchant_id--',r['id'], ',name--',r['customer_name'],',street2--', r['customer_address'], ',phone--',r['contact_phone'], ',x_industry--',r['business_scope_id'], r['business_scope_id'],self.industry[r['business_scope_id']]
            ids =  wapi.search_read(model='res.partner', domain=[('name','=',r['customer_name']),('is_company','=',True)])
            if len(ids) > 0:#有此数据
                print ids
                print r['customer_name']
                for i in ids:
                    wapi.update(model='res.partner',up_id=i, val={'x_potential_merchant_id':r['id']})

            else:
        '''
        for r in reader:
            wapi.create('res.partner', {'x_potential_merchant_id':r['id'], 'name':r['customer_name'], 'street2':r['customer_address'], 'phone':r['contact_phone'], 'x_industry':self.industry[r['business_scope_id']], 'is_company':True})
            #wapi.update('res.partner', {'is_company':True})
    


    def rep(self):
		fi = open('t_saas_opt_merchant_visit.csv', 'rb')  
		data = fi.read()  
		fi.close()  
		fo = open('merchant_visit.csv', 'wb')  
		fo.write(data.replace('\x00', ''))  
		fo.close()  

    def insert_visit(self):
        pf = open('potential_merchant.csv')
        preader = csv.DictReader(pf)
        id_saas_name = {}
        for r in preader:
            name_saas_id[r['id']] = r['name']
        f = open('merchant_visit.csv')
        reader = csv.DictReader(f)
        for r in reader:
            #print 'for'
            #print r['id'], r['potential_merchant_id']
            ids = wapi.search_read(model='res.partner', domain=[('x_potential_merchant_id','=',r['potential_merchant_id'])])
            for i in ids:
                contact_id = wapi.create('res.partner', val={'name':r['contact_name'],'phone':r['contact_phone']})
                #wapi.create('x_visit_record', val={'x_contact_id':, 'x_visit_parent_id':i})

class update_city():
    def __init__(self,wapi):
        self.wapi = wapi
        self.row = {}

    def read(self):
        f = open('potential_merchant.csv')
        reader = csv.DictReader(f)
        self.row = {r['id']:r['city_code'] for r in reader}

    def action(self):
        com_ids = self.wapi.search_read(model='res.partner', domain=[('is_company','=',True)], fields={'fields':['x_potential_merchant_id']})
        print com_ids
        '''
        for ci in com_ids:
            self.wapi.search_read(model='x_administrative.area', domain=[('x_code', '=',)])
            self.wapi.update(model='res.partner',up_id=ci, val={'x_addr_prov':})
        ''' 


class update_status():
    def __init__(self, wapi):
        self.wapi = wapi

    def read(self):
        f = open("potential_merchant.csv")
        reader = csv.DictReader(f)
        self.reader = reader
        self.row = {r['id']:r['sign_status'] for r in self.reader}
    def action(self):
        com_ids = self.wapi.search_read(model='res.partner', domain=[('is_company','=',True)], fields={'fields':['x_potential_merchant_id']})
        for di in com_ids:
            status = self.row.get(di['x_potential_merchant_id'],'nodata')
            if status == 'nodata':
                print di['x_potential_merchant_id'],di['id']
            status = 'following' if status == 'unsigned' or status == 'nodata' else 'enter'
            self.wapi.update(model='res.partner', up_id=di['id'], val={'x_merchant_status':status})
            print 'status--',status,'--id:',di['id']

class update_employee():
    def __init__(self,wapi):
        self.wapi = wapi

    def read(self):
        f = open('operator.csv')
        reader = csv.DictReader(f)
        self.reader = reader

    def action(self):
        for r in self.reader:
            print r['name'], r['phone'], r['id'], r['city_code'], r['role_code']
            self.wapi.create('hr.employee', {'name':r['name'], 'work_phone':r['phone'], 'x_saas_operator_id':r['id'], 'x_city_code':r['city_code'], 'x_role_code':r['role_code']})

class update_user():
    def __init__(self, wapi):
        self.wapi = wapi

    def read(self):
        f = open('operator.csv')
        reader = csv.DictReader(f)
        self.reader = reader

    def action(self):
        i = 0
        for r in self.reader:
            print '-----------'
            i += 1
            print i
            if i <= 247:
                print r['phone'],r['name']
                continue
            u_id = self.wapi.create('res.users', val={'name':r['name'], 'login':r['phone']})
            e_ids = self.wapi.search_read(model = 'hr.employee',domain=[('x_saas_operator_id','=',r['id'])])
            self.wapi.update(model='hr.employee', up_id=e_ids[0],val={'user_id':u_id})
            print 'name==',r['name'], 'phone--',r['phone']
            

class realation():
    def __init__(self, wapi):
        self.wapi = wapi
        self.row  = {}


    def read(self):
        f = open('potential_merchant.csv')
        reader = csv.DictReader(f)
        self.row = {r['id']:r['operator_id'] for r in reader}

    def action(self):
        com_ids = self.wapi.search_read(model='res.partner', domain=[('is_company','=',True)], fields={'fields':['x_potential_merchant_id']})
        f = open('nooperator2.csv','w')
        fieldnames = ['par_id']
        writer = csv.DictWriter(f, fieldnames = fieldnames)
        writer.writeheader()

        i = 0
        for di in com_ids:
            i+=1
            print '*******************'
            print i
            if i<21818:
                continue
            employee = self.wapi.search_read(model='hr.employee', domain=[('x_saas_operator_id','=',self.row[di['x_potential_merchant_id']])], fields={'fields':['user_id']})

            if employee == []:
                writer.writerow({'par_id':di['id']})
                continue
            print employee[0]['user_id'][0], di['id']
            self.wapi.update(model='res.partner', up_id=di['id'], val={'user_id':employee[0]['user_id'][0], 'x_modify_flag':True}) 
            #print employee,di['x_potential_merchant_id']

class search_partner():
    def __init__(self, wapi):
        self.wapi = wapi

    def read(self):
        pass
        




class changemaile():
    def __init__(self,wapi):
        self.wapi = wapi
    
    def read(self):
        col = self.wapi.search_read(model='res.users', fields={'fields':['login','name']})
        for c in col:
            print c
class updateEmail():
    def __init__(self,wapi):
        self.wapi = wapi

    def read(self):
        f = open('whole_res_user.csv')
        self.reader = csv.DictReader(f)
        depart = self.wapi.search_read(model='hr.department', fields={'fields':['name']})   
        print depart
        self.de = {d['name']:d['id'] for d in depart}
        employee = self.wapi.search_read(model='hr.employee', fields={'fields':['work_phone']})
        self.em = {e['work_phone']:e['id'] for e in employee}

            

    def action(self):
        '''
        for r in self.reader:
            if self.em.has_key(r['name_related']):
                self.wapi.update(model='hr.employee', up_id=self.em[r['name_related']], val={'department'})
        '''
        for r in self.reader:
            if len(r['work_phone']) == 0:
                r['work_phone'] = '12345678'
            if not self.em.has_key(r['work_phone']):
                #self.wapi.create(model='hr.employee',val={'name':r['name_related'], 'work_phone':r['work_phone'], 'work_email':r['work_email']})
                print 'create',r['name_related'], r['work_phone'], r['work_email']
            else:
                #self.wapi.update(model='hr.employee', up_id=self.em[r['work_phone']], val={'work_email':r['work_email']})
                if len(r['work_email']) == 0:
                
                    print 'update',r['work_email'],r['work_phone'],r['name_related']

class update_user_id():
    def __init__(self,wapi):
        self.wapi = wapi
    def read(self):
        employee = self.wapi.search_read(model='hr.employee', fields={'fields':['user_id','id', 'work_email']})
        for e in employee:
            print e

class readuser1():
    def __init__(self, wapi):
        self.wapi = wapi

    def read(self):
        f = open('whole_res_user1.csv')
        reader = csv.DictReader(f)
        self.row = {r['name']:r['login'] for r in reader}
        emp = self.wapi.search_read(model='hr.employee',fields={'fields':['name']})
        self.emp = {str(e['name']):e['id'] for e in emp}


    def action(self):

        '''
        for name,e_id in self.emp.items():
            name = str(name)
            print name
            print self.row['胡晨']
            if self.row.has_key(str(name)):
                self.wapi.update(model='hr.employee', up_id=e_id, val={'work_emial':self.row[str(name)]})
                print name,e_id
            else:
                self.wapi.create(model='hr.employee',val={'name':name,'work_email':})
        '''
        for name,login in self.row.items():
            if self.emp.has_key(name):
                self.wapi.update(model='hr.employee',up_id=self.emp[name],val={'work_email':login})
                print name
            else:
                self.wapi.create(model='hr.employee', val={'name':name,'work_email':login})
class create_res():
    def __init__(self,wapi):
        self.wapi = wapi
    def read(self):
        self.he = self.wapi.search_read(model='hr.employee',domain=[('user_id','=',False)], fields={'fields':['name','work_email']})
    def action(self):
        for h in self.he:
            print h['work_email'], h['name']
            u_id = self.wapi.create(model = 'res.users', val={'name':h['name'],'login':h['work_email']})
            self.wapi.update('hr.employee', h['id'],{'user_id':u_id})
            print 'name',h['name'],'login',h['work_email']



class hanzi2pinyin():
    def __init__(self, dict_file='word.data'):
        self.word_dict = {}
        self.dict_file = dict_file
        self.email=None
    def load_word(self):
        with file(self.dict_file) as f_obj:
            for f_line in f_obj.readlines():
                print 'kk'
                try:
                    line = f_line.split(' ')
                    self.word_dict[line[0]] = line[1]
                except:
                    line = f_line.split(' ')
                    self.word_dict[line[0]] = line[1]
    def change(self,string):
        for key,value in self.word_dict.items():
            print key,value
            break
        result = []
        if not isinstance(string,unicode):
            string = string.decode('utf-8')
        for char in string:
            key = '%x'%ord(char)
            result.append(self.word_dict.get(key,char).split()[0][:-1].lower())
            print result
        if len(result)==2:
            self.email = result[1]+'.'+result[0]+'@mei1.com'
        if len(result) == 3:
            self.email = result[1]+result[2]+'.'+result[0]+'@mei1.com'
        return self.email

class login2email():
    def __init__(self,wapi):
        self.wapi = wapi

    def read(self):
        i = 0
        employ = self.wapi.search_read(model='hr.employee', fields={'fields':['user_id', 'work_email']})
        self.row = {tuple(e['user_id']):e['work_email'] for e in employ}
        



    def action(self):
        i = 0
        for user_id, work_email in self.row.items():
            i+=1
            print i
            print user_id[1],work_email
            if work_email is False or i <=70:
                continue
            try:
                self.wapi.update('res.users',user_id[0], {'login':work_email})
            except BaseException:
                print '--------------',user_id[1],work_email
                continue
            
class depart():
    def __init__(self, wapi):
        self.wapi = wapi

    def read(self):
        f = open('whole_res_user.csv')
        reader = csv.DictReader(f)
        self.row = {r['name_related']:r['name'] for r in reader}
        departs = self.wapi.search_read(model='hr.department',fields={'fields':['name']})

        self.de = {str(d['name']):d['id'] for d in departs}
        self.employee = self.wapi.search_read(model='hr.employee', fields={'fields':['name']})
        self.em = [(str(e['name']),e['id']) for e in self.employee]
    def r(self):
        for key,value in self.row.items():
            print key,value

    def action(self):
        for key,value in self.de.items():
            print key,value
        for emp in self.em:
            depart = self.row.get(emp[0],'unkown')
            if depart == '':
                depart = 'unkown'
            self.wapi.update(model='hr.employee',up_id=emp[1],val={'department_id':self.de[depart]})
            #print depart,emp[0],emp[1] , self.de[depart]
            print depart
            print emp[0],type(emp[0]),depart,self.de[depart]

            
class get_group():
    def __init__(self,wapi):
        self.wapi = wapi

    def read(self):
        groups = self.wapi.search_read(model='res.groups', fields={'fields':['name']})
        for g in groups:
            
            print g['name'],g['id']

    def action(self):
        self.wapi.update(model='res.groups', up_id=48, val={'user':[1]})
class update_email():
    def __init__(self, wapi):
        self.wapi = wapi 

    def read(self):
        users = self.wapi.search_read(model='res.users',fields={'fields':['partner_id']})
        for u in users:
            print u

    def action(self):
        pass

class find_max_time():
    def __init__(self):
        pass
    def read(self):
        f = open('t_saas_opt_merchant_visit.csv')
        reader = csv.DictReader(f)
        for r in reader:
            print r['id']


if __name__ == '__main__':
    '''
    log = login()
    wapi = log.get_wapi()
    #功能模块
    ue = update_email(wapi)
    ue.read()
    ue.action()
    gg = get_group(wapi)
    gg.read()
    gg.action()
    cv = create_visit(wapi)
    cv.read()
    cv.action()
    cs = update_status(wapi)
    cs.read()
    cs.action()
    ue = update_employee(wapi)
    ue.read()
    ue.action()
    uu = update_user(wapi)
    uu.read()
    uu.action()
    re = realation(wapi)
    re.read()
    re.action()
    uu = update_user_id(wapi)
    uu.read()
    ce = updateEmail(wapi)
    ce.read()
    ce.action()
    ru = readuser1(wapi)
    ru.read()
    ru.action()
    ce = create_res(wapi)
    ce.read()
    ce.action()
    hp = hanzi2pinyin()
    hp.load_word()
    hp.change('李科伟')
    le = login2email(wapi)
    le.read()
    le.action()
    de = depart(wapi)
    de.read()
    de.action()
    de = depart(wapi)
    de.read()
    de.r()
    '''
    fmt = find_max_time()
    fmt.read()
