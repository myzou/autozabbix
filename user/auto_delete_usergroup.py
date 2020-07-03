#coding=utf-8
from conf import apiconf
from lib  import AutoZabbix
from lib import  log

#登录认证
zabbix=AutoZabbix.AutoZabbix(apiconf.ZABBIX_SERVER,apiconf.ZABBIX_USER,apiconf.ZABBIX_PASSWD)

#日志文件
log=log.LOG("auto_delete_usergroup")

#配置文件
list_file="../list/auto_delete_usergroup.txt"


#遍历配置文件
with open(list_file,"r") as f:
    for line in f.readlines():
        group_name=line.split()[0]

        #判断用户组是否存在
        if zabbix.user_group_exists(group_name):
            group_id=zabbix.get_usrgrpid(group_name)
            try:
                zabbix.delete_usergroup(group_id)
                log.info("用户组%s删除成功" % (group_name))
            except Exception as e:
                log.error(("删除用户组%s异常： %s" % (group_name,e)))

        #用户组不存在
        else:
            log.warning("用户组%s不存在" % (group_name))