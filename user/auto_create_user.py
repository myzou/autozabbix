#coding=utf-8
from conf import apiconf
from lib  import AutoZabbix
from lib import  log

#登录认证
zabbix=AutoZabbix.AutoZabbix(apiconf.ZABBIX_SERVER,apiconf.ZABBIX_USER,apiconf.ZABBIX_PASSWD)

#日志文件
log=log.LOG("auto_create_user")

#用户信息
list_file="../list/auto_create_user.txt"


with open(list_file,"r") as f:
    for line in f.readlines():
        user_name=line.split()[0]
        usrgrp_name=line.split()[1]
        user_email=line.split()[2]
        if not zabbix.user_exists(user_name):
            if zabbix.user_group_exists(usrgrp_name):
                user_group_id=zabbix.get_usrgrpid(usrgrp_name)
                try:
                    zabbix.create_user(user_name, "findsec@123",user_group_id , "4", user_email)
                    log.info("成功创建用户%s" % user_name)
                except Exception as e:
                    log.error("创建用户%s异常： %s" % (user_name,e))

            else:
                log.warning("用户组%s不存在" % usrgrp_name)

        #用户已存在
        else:
            user_id=zabbix.get_userid(user_name)
            #获取用户的用户组
            group_ids=zabbix.get_user_grouplist(user_id)

            #获取用户组ID
            if not  zabbix.user_group_exists(usrgrp_name):
                log.warning("%s用户组不存在" % (usrgrp_name))
                user_group_id=""
            else:
                user_group_id=zabbix.get_usrgrpid(usrgrp_name)

            #判断用户是否在用户组
            if user_group_id != "" and not user_group_id in group_ids:
                #将用户加入对应的用户组
                try:
                    user_id=zabbix.get_userid(user_name)
                    zabbix.user_to_group(user_id, user_group_id)
                    log.info("成功将%s加入%s用户组" %(user_name,usrgrp_name))
                except Exception as e:
                    log.error("将%s加入%s异常：%s" %(user_name,usrgrp_name,e))

            #用户已在用户组
            else:
                log.info("%s用户已存在并在%s用户组中" % (user_name,usrgrp_name))


