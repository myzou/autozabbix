#coding=utf-8
from conf import apiconf
from lib  import AutoZabbix
from lib import  log

#登录认证
zabbix=AutoZabbix.AutoZabbix(apiconf.ZABBIX_SERVER,apiconf.ZABBIX_USER,apiconf.ZABBIX_PASSWD)

#日志文件
log=log.LOG("auto_create_user_group")

#用户组信息
list_file="../list/auto_create_user_group.txt"


with open(list_file,"r") as f:
    for line in f.readlines():
        usrgrp_name=line.split()[0]
        hostgrp_name=line.split()[1]
        if not zabbix.user_group_exists(usrgrp_name):
            #创建zabbix用户组
            try:
                host_groupid=zabbix.get_group_id(hostgrp_name)
                zabbix.create_usergroup(usrgrp_name,host_groupid,permission)
                log.info("创建%s用户组" % (usrgrp_name))
            except Exception as e:
                log.error("创建%s用户组异常: %s" % (usrgrp_name,e))
        else:
            log.info("%s用户组已存在" % (usrgrp_name))