# -*- coding:utf-8 -*-
import ldap,ldap.modlist

conf = {'server_uri':'ldap://(ladp_id)',
        'server_port':(ldap_port),
        'bind_dn':(bind_dn),
        'bind_base':(bind_base),
        'bind_passwd':(bind_passwd)}

class MyLdap(object):
    def __init__(self):
        self.server_uri = conf['server_uri']
        self.server_port = conf['server_port']
        self.ldap_obj = None
        self.bind_dn = conf['bind_dn']
        self.bind_base = conf['bind_base']
        self.ldap_connect(conf['bind_dn'], conf['bind_passwd'])
        # 可以更改的内容
        self.change_field = ['userPassword','mobile','departmentNumber']
        # 可添加内容
        self.add_field = ['cn','mail','mobile','userPassword','departmentNumber']

    def ldap_connect(self, bind_name='', bind_passwd=''):
        """
        :param bind_name: 绑定的ldap用户，可为空; 添加，删除用户时 bind_name 要有root权限
        :param bind_passwd:
        :return:
        """
        url = self.server_uri + ":" + str(self.server_port)
        conn = ldap.initialize(url)
        # try:
        #     conn.start_tls_s()
        # except ldap.LDAPError as exc:
        #     raise Exception(exc.message)
        if bind_name and not bind_passwd:
            raise Exception("请输入LDAP密码")
        try:
            rest = conn.simple_bind_s(bind_name, bind_passwd)
            print rest
        except ldap.SERVER_DOWN:
            raise Exception("无法连接到LDAP")
        except ldap.INVALID_CREDENTIALS:
            raise Exception("LDAP账号错误")
        except Exception, ex:
            raise Exception(type(ex))
        if rest[0] != 97:  # 97 表示success
            raise Exception(rest[1])
        self.ldap_obj = conn

    def ldap_search(self, email=None, rdn='uid'):
        """
        base: 域 ou=test, dc=test, dc=com
        keyword: 搜索的用户
        rdn: cn/uid
        """
        if not email:
            error_message = u'not found email'
            raise Exception(error_message)
        keyword = email.split('@')[0]
        scope = ldap.SCOPE_SUBTREE
        filter = "%s=%s" % (rdn, keyword)
        retrieve_attributes = None
        try:
            result_id = self.ldap_obj.search(self.bind_base, scope, filter, retrieve_attributes)
            result_type, result_data = self.ldap_obj.result(result_id)
            if not result_data:
                return False, []
        except ldap.LDAPError, error_message:
            raise Exception(error_message)
        return True, result_data

    def add_user(self, add_content):
        add_list = {field:add_content[field] for field in self.add_field if field in add_content }
        if not add_list['mail'] or not add_list['cn']:
            raise Exception('邮箱或者名字不能为空')
        increase_id = self.get_increase_uidNumber()
        email = add_list['mail']
        loginName = email.split('@')[0]
        addDN = "uid=%s,"%loginName + self.bind_base
        attrs = {}
        attrs['uid'] = loginName
        #attrs['mobile']= add_list['mobile']
        attrs['loginShell'] = '/bin/bash'
        #attrs['userPassword'] = add_list['password']
        attrs['uidNumber'] = str(increase_id)
        attrs['objectclass'] = ['inetOrgPerson', 'posixAccount', 'shadowAccount']
        attrs['gidNumber'] = str(increase_id)
        attrs['sn'] = loginName
        attrs['homeDirectory'] = '/home/%s'%loginName
        #attrs['mail'] = add_list['email']
        #attrs['cn'] = add_list['name']
        #attrs['departmentNumber'] = add_list['departmentNumber']
        for key,value in add_list.iteritems():
            attrs[key] = value
        #attrs['givenName'] = name
        #l.unbind_s()
        #print add_record
        print '-------------添加ldap--------'
        print attrs
        print '-------end----------------'
        try:
            ldif = ldap.modlist.addModlist(attrs)
            result = self.ldap_obj.add_s(addDN, ldif)
        except ldap.LDAPError, error_message:
            raise Exception(error_message)
        else:
            if result[0] == 105:
                return True, []
            else:
                return False, result[1]

    def modify_user(self, email, modify_content):
        """
        MOD_ADD: 如果属性存在，这个属性可以有多个值，那么新值加进去，旧值保留
        MOD_DELETE ：如果属性的值存在，值将被删除
        MOD_REPLACE ：这个属性所有的旧值将会被删除，这个值被加进去

        dn: cn=test, ou=magicstack,dc=test, dc=com
        attr_list: [( ldap.MOD_REPLACE, 'givenName', 'Francis' ),
                    ( ldap.MOD_ADD, 'cn', 'Frank Bacon' )
                   ]
        """
        #result,mes = self.ldap_search(email)
        #if not result:
        #    return 
        result,mes = self.ldap_search(email)
        if not result:
            return False,'unsyn'

        loginName = str(email).split('@')[0]
        #dn = 'uid=%s,ou=People,dc=mei1,dc=com' % loginName
        dn = "uid=%s,"%loginName + self.bind_base
        attr_list = [(ldap.MOD_REPLACE,field,modify_content[field] ) for field in self.change_field if field in modify_content] 
        if not attr_list:
            return False,'wrong field'
        try:
            result = self.ldap_obj.modify_s(dn, attr_list)
        except ldap.LDAPError, error_message:
            raise Exception(error_message)
        else:
            if result[0] == 103:
                return True, []
            else:
                return False, result[1]

    def delete_user(self, email):
        """
        dn: cn=test, ou=magicstack,dc=test, dc=com
        """
        result,mes = self.ldap_search(email)
        if not result:
            return True,'unsyn'
        loginName = email.split('@')[0]
        dn = 'uid=%s,'%loginName+self.bind_base
        try:
            result = self.ldap_obj.delete_s(dn)
        except ldap.LDAPError, error_message:
            raise Exception(error_message)
        else:
            if result[0] == 107:
                return True, []
            else:
                return False, result[1]


    def get_increase_uidNumber(self):
        """
        查询 当前最大的uid，这个是在添加用户时，用于自增uid
        :param: None
        :return: max uidNumber
        """
        obj = self.ldap_obj
        obj.protocal_version = ldap.VERSION3
        searchScope = ldap.SCOPE_SUBTREE
        retrieveAttributes = ['uidNumber']
        searchFilter = "uid=*"
        
        try:
            ldap_result = obj.search_s(
                base=self.bind_base,
                scope=searchScope,
                filterstr=searchFilter,
                attrlist=retrieveAttributes
            )
            result_set = []
            for data in ldap_result:
                if data[1]:
                    result_set.append(int(data[1]["uidNumber"][0]))
            if not result_set:
                return False
            return max(result_set) + 1
        except ldap.LDAPError, error_message:
            print (error_message)
            return False

if __name__ == '__main__':
    pass
    #mldap = MyLdap()
    #mldap.modify_user(email=email,modify_content={'mobile':'111111'})
    #userq3 = mldap.ldap_search(email = email)
    #print userq3[1][0][1]['userPassword'][0]
    #print mldap.delete_user(email= email)
    #print mldap.get_increase_uidNumber()

