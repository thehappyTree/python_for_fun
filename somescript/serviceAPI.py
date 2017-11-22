# -*- coding:utf-8 -*-
import xmlrpclib
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')
class WebAPI():
    def __init__(self, url=None):
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
        report = xmlrpclib.ServerProxy('{}/xmlrpc/2/report'.format(url))
        self.exc = models.execute_kw
        self.common = common
        self.report = report
        self.uid = None
        self.loginMes = {}


    def getModels(self):
	    return self.models

    
    #获取db下的username password 的 id
    def login(self, db=None, username=None, password=None, val={} ):
        uid = self.common.authenticate(db, username, password, {})
        self.uid = uid
        self.loginMes = {'db':db, 'username':username, 'password':password}
        return uid
    
    #版本号
    def version(self):
        return self.common.version()
    
    #search
    def search_read(self,model, domain=[], optional={}, fields={}):
        db, password,uid = self.loginMes['db'],self.loginMes['password'], self.uid
        if domain != []:domain = [[d[0], d[1], d[2]] for d in domain]
        ids = self.exc(db, uid, password,\
                    model, 'search',\
                    [domain],\
                    optional)
        ins = ids if fields == {} else  self.exc(db, uid, password, model, 'read', [ids], fields)
        return ins
     
    #read
    def read(self, model, ids, fields={}):
        db, password,uid = self.loginMes['db'],self.loginMes['password'], self.uid
        instances = self.exc(db, uid, password, model, 'read', [ids], fields)
        return instances

    #create
    def create(self, model, val={}):
        db, password, uid = self.loginMes['db'],self.loginMes['password'], self.uid
        id  = self.exc(db, uid, password, model, 'create', [val])
        return id

    #update
    def update(self, model, up_id, val={}):
        db, password, uid = self.loginMes['db'],self.loginMes['password'], self.uid
        self.exc( db, uid, password, model, 'write',[[up_id], val] )

    def unlink(self, model, d_id):
        db, password, uid = self.loginMes['db'],self.loginMes['password'], self.uid
        self.exc( db, uid, password, model, 'unlink', [[d_id]])

    def fields_get(self, model, fields={}):
        db, password, uid = self.loginMes['db'],self.loginMes['password'], self.uid
        fields_mes = self.exc( db, uid, password, model, 'fields_get', [],fields )
        return fields_mes


    def search_count(self , model, domain = []):
        db, password, uid = self.loginMes['db'],self.loginMes['password'], self.uid
        if domain != []:domain = [[d[0], d[1], d[2]] for d in domain]
        count = self.exc( db, uid, password,\
                model, 'search_count',\
                [domain]
                )
        return count
        

    #创建数据库{'field_name':field_type|(field_type,required)}
    #创建数据库要求model必须以x_开头，fields必须以x_
    def create_model(self, model_descript, model, fields={}):
        model_record = self.search('ir.model', [('model', '=' , model )])
        db, password, uid = self.loginMes['db'],self.loginMes['password'], self.uid
        '''
        如果该model已存在则取model_id,如果不存在创建数据库
        '''
        id = self.exc( db, uid, password, 'ir.model', \
                'create', [{'name':model_descript, \
                'model':model, 'state': 'manual',}]) if model_record == [] else model_record[0]
        for name, attr in fields.items():
            ttype,required = (attr,True) if isinstance(attr,str) else (attr[0], attr[1])
            self.exc( db, uid, password, 'ir.model.fields', 'create', [{
                        'model_id': id,
                        'name': name,
                        'ttype': ttype,
                        'state': 'manual',
                        'required': required,
                    }])

    
    def sreport(self):
        db, password, uid = self.loginMes['db'],self.loginMes['password'], self.uid
        invoice_ids = self.search('account.invoice', [('type', '=', 'out_invoice'), ('state', '=', 'open')])
        result = self.report.render_report(\
        db, uid, password, 'account.report_invoice', invoice_ids)
        return result['result'].decode('base64')


def testweb():
    wapi = WebAPI(url=url)
    wapi.login(db=dbname,username=db_username,password=db_password)
    #print wapi.fields_get('res.partner',fields = {'attributes': ['string', 'help', 'type']})
    print wapi.search_read( model='res.groups' )
    print wapi.search_read( model = 'res.groups', fields = {'fields':['name']})
    print wapi.search_read( model ='res.groups.users.rel')

    #print wapi.fields_get(model='res.users')

    #update(self, model, up_id, val={}):
    #print wapi.sreport()
    #print wapi.fields_get('res.partner',fields = {'attributes': ['string', 'help', 'type']})
    #print wapi.search('ir.model',[('model','=','x_testmodel8')])
    #wapi.create_model('test model', 'x_testmodel8', {'x_iphone':'char'})
    #ids = wapi.search(model='res.partner',domain = [['name', '=', 'apikewei']])
    #print ids
    #ins = wapi.read(model='res.partner', ids=ids, fields={'fields': ['name', 'country_id', 'comment']})
    #print ins 
    #wapi.create('res.partner', {'name': "apikewei",})
    #wapi.unlink('res.partner', 37973)
    #print wapi.fileds_get('res.partner', {'attributes': ['string', 'help', 'type']})


    
if __name__ == "__main__":
    testweb()
