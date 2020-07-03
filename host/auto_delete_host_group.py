#coding=utf-8
from conf import apiconf
from lib  import AutoZabbix
from lib import  log

#登录认证
zabbix=AutoZabbix.AutoZabbix(apiconf.ZABBIX_SERVER,apiconf.ZABBIX_USER,apiconf.ZABBIX_PASSWD)

#日志文件
log=log.LOG("auto_delete_host_group")

#配置文件
list_file="../list/auto_delete_host_group.txt"

#遍历配置文件
with open(list_file,"r") as f:
    for line in f.readlines():
        host_group=line.split()[0]

        if zabbix.group_exists(host_group):
            #主机组存在，删除主机组
            try:
                group_id=zabbix.get_group_id(host_group)
                zabbix.delete_group(group_id)
                log.info("成功删除主机组%s" % host_group)
            except Exception as e:
                log.error("删除主机组%s异常： %s" % (host_group,e))

        else:
            log.warning("主机组%s不存在" % host_group)