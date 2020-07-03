#!/usr/bin/env python
#coding=utf-8

'''
by patrick@findsec
通过Zabbix API实现Zabbix的自动化管理
'''
from pyzabbix import ZabbixAPI,ZabbixAPIException

class AutoZabbix:
    '''
    通过Zabbix API实现相关功能自动化
    主机
    用户
    操作

    '''
    def __init__(self,zabbixserver,zabbixuser,zabbixpassword):
        self.server=zabbixserver
        self.user=zabbixuser
        self.password=zabbixpassword

    def _login(self):
        '''
        登录Zabbix，返回token
        :return:
        '''
        zabbixapi=ZabbixAPI(self.server)
        zabbixapi.login(self.user,self.password)
        return zabbixapi

################################User/Usergroup funtions ###################################
    def get_all_users(self):
        '''
        获取所有用户ID
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.user.get()
        result=[]
        for i in range(0,len(response)):
            result.append(response[i])
        return result


    def get_all_usrgrpid(self):
        '''
        获取所有用户组ID
        :return:
        '''

        zabbixapi=self._login()
        response=zabbixapi.usergroup.get(output='usrgrpid')
        result=[]
        for i in range(0,len(response)):
            result.append(response[i]['usrgrpid'])
        return result

    def user_group_exists(self,usergroup):
        '''
        判断用户组是否存在
        :param usergroup:
        :return:
        '''

        zabbixapi=self._login()
        response=zabbixapi.usergroup.get(filter={"name":usergroup})
        if len(response) >0:
            return True
        else:
            return False

    def user_exists(self,username):
        '''
        判断用户是否存在
        :param usergroup:
        :return:
        '''

        zabbixapi=self._login()
        response=zabbixapi.user.get(filter={"alias":username})
        if len(response) >0:
            return True
        else:
            return False

    def get_group_userlist(self,usrgrpid):
        '''
        获取用户组中所有用户
        :param usrgrpid:
        :return:
        '''

        zabbixapi=self._login()
        response=zabbixapi.usergroup.get(selectUsers="userid",filter={"usrgrpid":usrgrpid})
        result=[]
        for i in response[0]['users']:
            result.append(i['userid'])

        return result


    def get_user_grouplist(self,userid):
        '''
        获取用户所在用户组
        :param userid:
        :return:
        '''

        zabbixapi=self._login()
        response=zabbixapi.user.get(selectUsrgrps="usrgrpid",filter={"userid":userid})
        result=[]
        for i in response[0]['usrgrps']:
            result.append(i['usrgrpid'])

        return result


    def  id_to_usergroupname(self,groupid):
        '''
        根据ID获取用户组名称
        :param groupid:
        :return:
        '''

        zabbixapi=self._login()
        response=zabbixapi.usergroup.get(filter={"usrgrpid":groupid,"output":"extend"})
        return response[0]['name']

    def  id_to_username(self,userid):
        '''
        根据ID获取用户名称
        :param groupid:
        :return:
        '''

        zabbixapi=self._login()
        response=zabbixapi.user.get(filter={"userid":userid,"output":"extend"})
        return response[0]['alias']


    def get_usrgrpid(self,usrgrpname):
        '''
        获取用户组ID
        :param usrgrpname:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.usergroup.get(filter={"name":usrgrpname,"output":"usrgrpid"})
        return response[0]['usrgrpid']

    def get_userid(self,username):
        '''
        根据 alias 获取用户ID
        :param usrgrpname:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.user.get(filter={"alias":username,"output":"userid"})
        return response[0]['userid']

    def create_usergroup(self,usergroupname,hostgroupid,permission="2"):
        '''
        创建用户组
        :param usergroupname:
        :param hostgroupid:
        :param permission:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.usergroup.create(name=usergroupname,rights={"permission":permission,"id":hostgroupid})
        return response["usrgrpids"][0]

    def create_user(self,username,passwd,groupid,mailid,mailto,lang="zh_CN",theme="default",type="2"):
        '''
        创建用户
        :param username:
        :param passwd:
        :param groupid:
        :param mailid:
        :param mailto:
        :param lang:
        :param theme:
        :param type:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.user.create(lang=lang,theme=theme,type=type,alias=username,passwd=passwd,usrgrps=[{"usrgrpid":groupid}],user_medias=[{"mediatypeid":mailid,"sendto":mailto,"active": 0,"severity": 63,"period":"1-7,00:00-24:00"}])
        return response["userids"][0]

    def delete_user(self,userid):
        '''
        删除用户
        :param userid:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.user.delete(userid)
        return response["userids"]

    def delete_usergroup(self,usrgroupid):
        '''
        删除用户组
        :param usrgroupid:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.usergroup.delete(usrgroupid)
        return response["usrgrpids"]


    def user_to_group(self,userid,groupid):
        '''
        将用户加入指定用户组
        :param userid:
        :param groupid:
        :return:
        '''
        zabbixapi=self._login()
        all_grp_uids=self.get_group_userlist(groupid)
        all_grp_uids.append(userid)
        response=zabbixapi.usergroup.update(usrgrpid=groupid,userids=all_grp_uids)
        return response["usrgrpids"]

    def get_usrgroup_rights(self,groupid):
        '''
        获取用户组的主机权限
        :param groupid:
        :return:
        '''

        zabbixapi=self._login()
        response=zabbixapi.usergroup.get(selectRights="rights",filter={"usrgrpid":groupid})
        return response[0]["rights"]

    def group_permission_update(self,usrgrpid,permission,hostgroupid):
        '''
        更新用户组权限
        :param usrgrpid:
        :param permission:
        :param hostgroupid:
        :return:
        '''
        zabbixapi=self._login()
        all_group_rights=self.get_usrgroup_rights(usrgrpid)
        all_group_rights.append({"permission":permission,"id":hostgroupid})
        response=zabbixapi.usergroup.update(usrgrpid=usrgrpid,rights=all_group_rights)
        return response["usrgrpids"]

    def update_user_email(self,userid,mailid,mailto):
        '''
        更新用户邮件媒介
        :param userid:
        :param mailid:
        :param mailto:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.user.update(userid=userid,user_medias=[{"mediatypeid":mailid,"sendto":mailto,"active": 0,"severity": 63,"period":"1-7,00:00-24:00"}])
        return response

    def update_user_name(self,userid,name):
        '''
        更新用户名称
        :param userid:
        :param name:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.user.update(userid=userid,alias=name)
        return response['userids']

    def get_media_id(self,medianame):
        '''
        获取指定报警媒介ID
        :param medianame:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.mediatype.get(filter={"description":medianame})
        return response[0]["mediatypeid"]
################################ END  User/Usergroup funtions ###############################


##################### START Host和Host Group函数 ###############################################
    def get_all_groups(self):
        '''
        获取所有组信息
        :return:all_groups
        '''
        zabbixapi=self._login()
        all_groups=zabbixapi.hostgroup.get(output='extend')
        return all_groups

    def get_group_id(self,groupname):
        '''
        获取指定主机组的id
        :param groupname:
        :return:主机组ID
        '''
        zabbixapi=self._login()
        groupinfo=zabbixapi.hostgroup.get(output='extend',filter={"name":groupname})
        return  groupinfo[0]['groupid']

    def host_exists(self,hostname):
        '''
        判断主机是否存在
        :param hostname:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.host.get(filter={"host":hostname})
        if len(response)>0:
            return True
        else:
            return False

    def get_host_id(self,hostname):
        '''
        根据主机名获取主机ID
        :param hostname:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.host.get(output='hostid',filter={"host":hostname})
        return response[0]['hostid']

    def group_exists(self,groupname):
        '''
        判断主机组是否存在
        :param groupname:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.hostgroup.get(filter={'name':groupname})
        if len(response)>0:
            return True
        else:
            return False

    def create_group(self,groupname):
        '''
        创建主机组
        :param groupname:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.hostgroup.create(name=groupname)
        return response

    def delete_group(self,groupid):
        '''
        删除主机组
        :param groupid:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.hostgroup.delete(groupid)
        return response['groupids']

    def host_to_group(self,groupid,hostid):
        '''
        将服务器加入指定主机组
        :param groupid:
        :param hostid:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.hostgroup.massadd(groups={"groupid":groupid},hosts={"hostid":hostid})
        return response['groupids'][0]

    def get_all_host_groupid(self,hostid):
        '''
        获取主机所在所有主机组ID
        :param hostid:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.host.get(output="hostid",selectGroups="extend",filter={'hostid':hostid})
        result=[]
        for i in  range(0,len(response[0]['groups'])):
            result.append(response[0]['groups'][i]['groupid'])
        return result

    def get_all_host(self):
        '''
        获取所有监控主机
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.host.get(output="hostid")
        result=[]
        for i in range(0,len(response)):
            result.append(response[i]['hostid'])
        return result

    def id_to_hostname(self,hostid):
        '''
        根据主机ID获取主机名
        :param hostid:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.host.get(output="extend",filter={'hostid':hostid})
        return response[0]['host']

    def id_to_hostgroup(self,hostgroupid):
        '''
        根据ID获取主机组名称
        :param hostgroupid:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.hostgroup.get(filter={"groupid":hostgroupid},output="extend")
        return response[0]['name']

    def delete_host(self,hostid):
        '''
        删除主机
        :param hostid:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.host.delete(hostid)
        return response['hostids'][0]

    def create_snmp_host_with_visablename(self,hostip,visablename,groupid):
        '''
        创建主机（用于SNMP包含visable name）
        :param hostip:
        :param visablename:
        :param groupid:
        :return:
        '''

        zabbixapi=self._login()
        response=zabbixapi.host.create(host=hostip,name=visablename,interfaces=[{"type":2,"main":1,"useip":1,"ip":hostip,"dns":"","port":161}],groups=[{"groupid":groupid}])
        print(response)

    def get_group_host_list(self,groupname):
        '''
        获取指定主机组的所有
        :param groupname:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.hostgroup.get(selectHosts="hostid",search={'name':groupname})
        if len(response[0]['hosts']) > 0:
            result=[]
            for i in range(0,len(response[0]['hosts'])):
                result.append(response[0]['hosts'][i]['hostid'])
            return result
        else:
            return []

    def unlink_clear_host_template(self,hostid,template_clear):
        '''
        取消和清除主机的模板
        :param hostid:
        :param template_clear:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.host.massupdate(hosts={"hostid":hostid},templates_clear={"templateid":template_clear})
        return response

    def is_host_in_group(self,groupname,hostname):
        '''
        判断主机是否属于主机组
        :param groupname:
        :param hostname:
        :return:
        '''
        zabbixapi=self._login()
        hostid=self.get_host_id(hostname)
        hostlist=self.get_group_host_list(groupname)
        if hostid in hostlist:
            return True
        else:
            return False

    def del_host_from_group(self,groupid,hostid):
        '''
        从主机组中删除主机
        :param groupid:
        :param hostid:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.host.massremove(groupids=groupid,hostids=[hostid])
        return response

    def create_host_snmp_interface(self,hostid,interface_ip,interface_port):
        '''
        主机添加snmp监控接口
        :param hostid:
        :param interface_ip:
        :param interface_port:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.hostinterface.create(hostid=hostid,dns="",ip=interface_ip,main=1,port=interface_port,type=2,useip=1)
        return response['interfaceids']

    def get_host_interfaces(self,hostid):
        '''
        获取主机所有接口信息
        :param hostid:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.hostinterface.get(hostids=hostid,output="extend")
        return response

    def host_interface_exists(self,hostid,interface_ip,interface_port):
        '''
        判断监控接口是否存在
        :param interface_ip:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.hostinterface.get(filter={"hostid":hostid,"ip":interface_ip,"port":interface_port})
        if len(response)>0:
            return True
        else:
            return False

    def host_interface_delete(self,interface_id):
        '''
        删除主机监控接口
        :param interface_id:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.hostinterface.delete(interface_id)
        return response
##################### END Host和Host Group函数 ###############################################

##################### START Template相关函数 ###############################################
    def template_filter(self,templatename):
        '''
        根据模板名称过滤模板
        :param templatename:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.template.get(search={'host':templatename})
        result=[]
        for i in range(0,len(response)):
            result.append(response[i]['templateid'])
        return result

    def template_exists(self,template_name):
        '''
        判断模板是否存在
        :param template_name:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.template.get(filter={"host":template_name})
        if len(response)>0:
            return True
        else:
            return False

    def get_template_id(self,template_name):
        '''
        获取模板ID
        :param template_name:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.template.get(filter={"host":template_name},output="extend")
        return response[0]['templateid']

    def id_to_templatename(self,template_id):
        '''
        根据ID获取模板名称
        :param template_id:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.template.get(filter={"host":template_id},output="name")
        return response

    def get_template_host(self,template_name):
        '''
        获取模板监控主机列表
        :param template_name:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.template.get(filter={"host":template_name},selectHosts="hostid",output="hosts")
        result=[]
        for i in range(0,len(response[0]['hosts'])):
            result.append(response[0]['hosts'][i])
        return result


    def clear_template_host(self,templateid):
        '''
        清空模板对应的主机
        :param templateid:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.template.massupdate(templates={"templateid":templateid},hosts={"hostids":[]})
        return response['templateids'][0]

    def template_to_host(self,templateid,hostids):
        '''
        应用模板到主机
        :param templateid:
        :param hostids:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.template.massupdate(templates={"templateid":templateid},hosts=hostids)
        return response['templateids'][0]

    def unlink_clear_template(self,templateid,template_clear):
        '''
        取消和清除模板链接
        :param templateid:
        :param template_clear:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.template.massupdate(templates={"templateid":templateid},templates_clear={"templateid":template_clear})
        return response

    def get_all_template(self):
        '''
        获取所有的模版
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.template.get()
        result=[]
        for i in range(0,len(response)):
            result.append(response[i]['templateid'])
        return result

##################### END Template相关函数 ###############################################

##################### START Item相关函数 ###############################################
    def get_host_item(self,hostid,keyname):
        '''
        获取主机指定名称的item id
        :param hostid:
        :param keyname:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.item.get(output=["itemid"],hostids=hostid,search={"key_":keyname.decode('UTF-8')},sortfield="itemid")
        result=[]
        for i in range(0,len(response)):
            result.append(response[i]['itemid'])
        return result

    def update_item_status(self,itemid,status):
        '''
        启用/禁用监控项
        :param itemid:
        :param status:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.item.update(itemid=itemid,status=status)
        return response['itemids'][0]

    def get_latest_item_value(self,itemid,history_type):
        '''
        获取指定监控项的监控数据
        :param itemid:
        :param history_type:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.history.get(output="extend",history=history_type,itemids=itemid,sortfield="clock",sortorder="DESC",limit=1)
        result=[]
        for i in range(0,len(response)):
            result.append(response[i]['value'])
        return result

    def create_item(self,hostid,interfaceid,name,key,type,value_type,delay):
        '''
        创建监控项
        :param hostid:
        :param name:
        :param key:
        :param type:
        :param value_type:
        :param delay:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.item.create(hostid=hostid,interfaceid=interfaceid,name=name,key_=key,type=type,value_type=value_type,delay=delay)
        return response['itemids'][0]

    def item_exits(self,hostname,itemkey):
        '''
        判断监控项是否存在
        :param hostname:
        :param itemkey:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.item.get(filter={"host":hostname,"key_":itemkey})
        if len(response)>0:
            return True
        else:
            return False


    def get_item_id(self,hostname,itemkey):
        '''
        获取item id
        :param hostname:
        :param itemkey:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.item.get(filter={'host':hostname},search={'name':itemkey})
        if response:
            return response[0]['itemid']

    def update_item_key(self,itemid,itemkey):
        '''
        更新item key
        :param itemid:
        :param itemkey:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.item.update(key_=itemkey,itemid=itemid)
        return response

    def update_item_app(self,itemid,appid):
        '''
        更新Item所属应用程序
        :param itemid:
        :param appid:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.item.update(itemid=itemid,applications=[appid])
        return response

    def delete_item(self,itemid):
        '''
        删除item
        :param itemid:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.item.delete(itemid)
        return response

    def create_snmp_item(self,hostid,interfaceid,name,key,type,value_type,delay,snmp_oid,snmp_community):
        '''
        创建SNMP监控项
        :param hostid:
        :param name:
        :param key:
        :param type:
        :param value_type:
        :param delay:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.item.create(hostid=hostid,interfaceid=interfaceid,name=name,key_=key,type=type,value_type=value_type,delay=delay,snmp_oid=snmp_oid,snmp_community=snmp_community)
        return response['itemids'][0]
##################### END Item相关函数 ###############################################

##################### START Trigger相关函数 ###############################################

    def get_trigger_info(self,triggerid):
        '''
        根据triggerid获取trigger相关信息
        :param triggerid:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.trigger.get(filter={"triggerid":triggerid},sortfield="priority",sortorder="DESC",output=["description","priority"],selectHosts=["host"])
        return response

    def get_recent_problem_trigger(self):
        '''
        获取当前problem报警
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.trigger.get(filter={"value":1},sortfield="priority",sortorder="DESC",output=["description","priority"],selectHosts=["host"],only_true=True,active=True,monitored=True,selectLastEvent="lastEvent")
        return response

    def create_trigger(self,description,expression,priority=4):
        '''
        创建触发器
        :param description:
        :param expression:
        :param priority:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.trigger.create(description=description,expression=expression,priority=priority)
        return response

    def get_trigger_id(self,hostname,triggername):
        '''
        获取triggerid
        :param hostname:
        :param triggername:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.trigger.get(filter={'host':hostname},search={'description':triggername})
        return response[0]['triggerid']

    def update_trigger_name(self,triggerid,trigger_name,priority=4):
        '''
        更新trigger的名称
        :param triggerid:
        :param trigger_name:
        :param priority:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.trigger.update(triggerid=triggerid,description=trigger_name,priority=priority)
        return response['triggerids'][0]

    def delete_trigger(self,triggerid):
        '''
        删除trigger
        :param triggerid:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.trigger.delete(triggerid)
        return response

    def trigger_exist(self,host,trigger_description):
        '''
        判断trigger是否存在
        :param trigger_expression:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.trigger.get(filter={"host":host,"description":trigger_description})
        if len(response) >0:
            return True
        else:
            return False

    def update_trigger_status(self,triggerid,status):
        '''
        更新trigger状态
        :param triggerid:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.trigger.update(triggerid=triggerid,status=status)
        return response

    def get_trigger_expression(self,triggerid):
        '''
        根据triggerid获取trigger表达式
        :param triggerid:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.trigger.get(filter={"triggerid":triggerid},sortfield="priority",sortorder="DESC",output="functions",selectHosts=["host"],selectFunctions=["function","parameter"])
        return response[0]['functions'][0]['function'] + "(" + response[0]['functions'][0]['parameter'] +")"

    def get_discovery_trigger_expression(self,triggerid):
        '''
        根据discovery triggerid获取trigger表达式
        :param triggerid:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.triggerprototype.get(filter={"triggerid":triggerid},sortfield="priority",sortorder="DESC",output="functions",selectHosts=["host"],selectFunctions=["function","parameter"])
        return response[0]['functions'][0]['function'] + "(" + response[0]['functions'][0]['parameter'] +")"
##################### END Trigger相关函数 ###############################################

##################### START Action相关函数 ###############################################
    def create_alert_action(self,actionname,p_subject,p_message,r_subject,r_message,msg_usrgrpid,mediatypeid,value,op_conditiontype="14",op_operator="0",op_value="0",eventsource="0",evaltype="0",esc_period="3600",status="0",r_status="1",conditiontype="0",operator="0",operationtype="0",action_esc_period="0",esc_step_from="1",esc_step_to="1",action_evaltype="0",default_msg="1"):
        '''
        创建报警操作
        :param actionname:
        :param p_subject:
        :param p_message:
        :param r_subject:
        :param r_message:
        :param msg_usrgrpid:
        :param mediatypeid:
        :param value:
        :param op_conditiontype:
        :param op_operator:
        :param op_value:
        :param eventsource:
        :param evaltype:
        :param esc_period:
        :param status:
        :param r_status:
        :param conditiontype:
        :param operator:
        :param operationtype:
        :param action_esc_period:
        :param esc_step_from:
        :param esc_step_to:
        :param action_evaltype:
        :param default_msg:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.action.create(name=actionname,eventsource=eventsource,evaltype=evaltype,esc_period=esc_period,status=status,def_shortdata=p_subject,def_longdata=p_message,r_shortdata=r_subject,r_longdata=r_message,recovery_msg=r_status,filter={"evaltype":0,"conditions":[{"conditiontype":conditiontype,"operator":operator,"value":value}]},operations=[{"operationtype":operationtype,"esc_period":action_esc_period,"esc_step_from":esc_step_from,"esc_step_to":esc_step_to,"evaltype":action_evaltype,"opmessage_grp":[{"usrgrpid":msg_usrgrpid}],"opmessage":{"default_msg":default_msg,"mediatypeid":mediatypeid},"opconditions":[{"conditiontype":op_conditiontype,"operator":op_operator,"value":op_value}]}])
        return response["actionids"]

    def action_exists(self,actionname):
        '''
        判断报警操作是否存在
        :param actionname:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.action.get(filter={"name":actionname})
        if len(response)>0:
            return True
        else:
            return False

    def action_filter(self,name):
        '''
        过滤报警操作
        :param name:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.action.get(search={'name':name})
        result=[]
        for i in range(0,len(response)):
            result.append(response[i]['actionid'])
        return result

    def update_action_msg(self,actionid,p_subject,p_message,r_subject,r_message):
        '''
        更新报警内容信息
        :param actionid:
        :param p_subject:
        :param p_message:
        :param r_subject:
        :param r_message:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.action.update(actionid=actionid,def_shortdata=p_subject,def_longdata=p_message,r_shortdata=r_subject,r_longdata=r_message)
        return response['actionids']

    def action_status(self,actionid,status):
        '''
        启用或禁用报警操作
        :param actionid:
        :param status:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.action.update(actionid=actionid,status=status)
        return response['actionids']

    def update_action_conditions(self,actionid,evaltype,conditions):
        '''
        更新报警条件
        :param actionid:
        :param conditiontype1:
        :param operator1:
        :param value1:
        :param conditiontype2:
        :param operator2:
        :param value2:
        :param conditiontype3:
        :param operator3:
        :param value3:
        :param conditiontype4:
        :param operator4:
        :param value4:
        :param conditiontype5:
        :param operator5:
        :param value5:
        :param conditiontype6:
        :param operator6:
        :param value6:
        :param conditiontype7:
        :param operator7:
        :param value7:
        :param conditiontype8:
        :param operator8:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.action.update(actionid=actionid,filter={"evaltype": evaltype,"conditions":conditions})
        return response['actionids']

    def id_to_actionname(self,actionid):
        '''
        根据ID获取操作名称
        :param actionid:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.action.get(filter={'actionid':actionid},output="extend")
        return response[0]['name']

    def chg_recovery_mgs_status(self,actionid,r_status):
        '''
        启用关闭恢复消息
        :param actionid:
        :param r_status:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.action.update(actionid=actionid,recovery_msg=r_status)
        return response['actionids']

    def  get_all_actionid(self):
        '''
        获取所有操作ID
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.action.get()
        result=[]
        for i in range(0,len(response)):
            result.append(response[i]['actionid'])
        return result


    def delete_action(self,actionid):
        '''
        删除报警操作
        :param actionid:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.action.delete(actionid=actionid)
        return response['actionids']
##################### END Action相关函数 ###############################################

##################### START Web相关函数 ###############################################
    def create_http_check(self,http_name,hostid,applicationid,delay,retries,step_name,step_url,step_status,step_no,step_timeout,posts="",required=""):
        '''
        创建web监控
        :param http_name:
        :param hostid:
        :param applicationid:
        :param delay:
        :param retries:
        :param step_name:
        :param step_url:
        :param step_status:
        :param step_no:
        :param step_timeout:
        :param posts:
        :param required:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.httptest.create(name=http_name,hostid=hostid,applicationid=applicationid,delay=delay,retries=retries,steps=[{"name":step_name,"url":step_url,"status_codes":step_status,"no":step_no,"timeout":step_timeout,"posts":posts,"required":required}])
        return response['httptestids'][0]

    def create_http_check_with_require_string(self,http_name,hostid,applicationid,delay,retries,step_name,step_url,step_status,step_no,step_timeout,required):
        '''
        创建web监控(包含require值)
        :param http_name:
        :param hostid:
        :param applicationid:
        :param delay:
        :param retries:
        :param step_name:
        :param step_url:
        :param step_status:
        :param step_no:
        :param step_timeout:
        :param required:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.httptest.create(name=http_name,hostid=hostid,applicationid=applicationid,delay=delay,retries=retries,steps=[{"name":step_name,"url":step_url,"status_codes":step_status,"no":step_no,"timeout":step_timeout,"required":required}])
        return response['httptestids'][0]


    def get_app_id(self,hostid,appname):
        '''
        获取应用程序ID
        :param hostid:
        :param appname:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.application.get(filter={'hostid':hostid},search={'name':appname})
        return response[0]['applicationid']

    def create_app(self,hostid,appname):
        '''
        创建应用程序
        :param hostid:
        :param appname:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.application.create(name=appname,hostid=hostid)
        return response['applicationids'][0]

    def app_exists(self,hostid,appname):
        '''
        判断应用程序是否存在
        :param hostid:
        :param appname:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.application.get(filter={"name":appname,"hostid":hostid})
        if len(response) >0:
            return True
        else:
            return False

    def  get_web_id(self,hostid,applicationids):
        '''
        获取web监控id
        :param hostid:
        :param applicationids:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.httptest.get(filter={'hostid':hostid},search={'applicationids':applicationids})
        result=[]
        for i in range(0,len(response)):
            result.append(response[i]['httptestid'])
        return result

    def get_web_url(self,hostid):
        '''
        获取wbe监控url
        :param hostid:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.httptest.get(selectSteps=["url"],filter={'hostid':hostid})
        result=[]
        for i in range(0,len(response)):
            result.append(response[i]['steps'][0]['url'])
        return result

    def update_web_url(self,http_name,httptestid,delay,retries,step_name,step_url,step_status,step_no,step_timeout,posts="",required=""):
        '''
        更新web监控内容
        :param http_name:
        :param hostid:
        :param httptestid:
        :param delay:
        :param retries:
        :param step_name:
        :param step_url:
        :param step_status:
        :param step_no:
        :param step_timeout:
        :param posts:
        :param required:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.httptest.update(name=http_name,httptestid=httptestid,delay=delay,retries=retries,steps=[{"name":step_name,"url":step_url,"status_codes":step_status,"no":step_no,"timeout":step_timeout,"posts":posts,"required":required}])
        return response

    def update_web_url_status(self,httptestid,step_status):
        '''
        更新Web监控状态
        :param hostid:
        :param httptestid:
        :param step_status:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.httptest.update(httptestid=httptestid,steps=[{"status_codes":step_status}])
        return response

    def  delete_web_url(self,httptestid):
        '''
        删除web
        :param httptestid:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.httptest.delete(httptestid)
        return response

    def  get_url_id(self,hostid,url):
        '''
        获取web  url监控id
        :param hostid:
        :param url:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.httptest.get(selectSteps=["url"],filter={"hostid":hostid},search=[{"url":url}])
        for i in range(0,len(response)):
            web_url=response[i]['steps'][0]['url']
            if web_url == url:
                return response[i]['httptestid']

    def get_host_web_count(self,hostid):
        '''
        主机web监控个数
        :param hostid:
        :return:
        '''
        zabbixapi=self._login()
        response=zabbixapi.httptest.get(filter={'hostid':hostid},countOutput="True")
        return response
##################### END Web相关函数 ###############################################