#coding=utf-8
from conf import apiconf
from lib  import AutoZabbix
from lib import  log

#登录认证
zabbix=AutoZabbix.AutoZabbix(apiconf.ZABBIX_SERVER,apiconf.ZABBIX_USER,apiconf.ZABBIX_PASSWD)

#日志文件
log=log.LOG("auto_create_host_group")

#配置文件
list_file="../list/auto_create_host_group.txt"

#遍历配置文件
with open(list_file,"r") as f:
    for line in f.readlines():
        group_name=line.split()[0]

        # 判断主机组是否存在
        if zabbix.group_exists(group_name):
            log.info("主机组%s已存在" % group_name)
        else:
            #创建主机组
            try:
                zabbix.create_group(group_name)
                log.info("成功创建主机组%s" % group_name)
            except Exception as e:
                log.error("创建主机组%s异常： %s" % (group_name,e))