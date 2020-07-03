#coding=utf-8
from conf import apiconf
from lib  import AutoZabbix
from lib import  log

#登录认证
zabbix=AutoZabbix.AutoZabbix(apiconf.ZABBIX_SERVER,apiconf.ZABBIX_USER,apiconf.ZABBIX_PASSWD)
#日志文件
log=log.LOG("auto_delete_action")

#配置文件
list_file="../list/auto_delete_action.txt"


#遍历配置文件
with open(list_file,"r") as f:
    for line in f.readlines():
        action_name=line.split()[0]

        #操作是否存在
        if zabbix.action_exists(action_name):
            action_id=zabbix.action_filter(action_name)
            zabbix.delete_action(action_id[0])
            log.info("成功删除告警操作%s" % action_name)
        else:
            log.warning("告警操作%s不存在" % action_name)