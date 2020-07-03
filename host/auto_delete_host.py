#coding=utf-8
from conf import apiconf
from lib  import AutoZabbix
from lib import  log

#登录认证
zabbix=AutoZabbix.AutoZabbix(apiconf.ZABBIX_SERVER,apiconf.ZABBIX_USER,apiconf.ZABBIX_PASSWD)

#日志文件
log=log.LOG("auto_delete_host")

#配置文件
list_file="../list/auto_delete_host.txt"

#遍历配置文件
with open(list_file,"r") as f:
    for line in f.readlines():
        host_ip=line.split()[0]

        if zabbix.host_exists(host_ip):
            #主机存在，删除主机
            try:
                host_id=zabbix.get_host_id(host_ip)
                zabbix.delete_host(host_id)
                log.info("成功删除主机%s" % host_ip)
            except Exception as e:
                log.error("删除主机%s异常： %s" % (host_ip,e))

        else:
            log.warning("主机%s不存在" % host_ip)