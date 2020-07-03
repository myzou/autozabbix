#coding=utf-8
from conf import apiconf
from lib  import AutoZabbix
from lib import  log

#登录认证
zabbix=AutoZabbix.AutoZabbix(apiconf.ZABBIX_SERVER,apiconf.ZABBIX_USER,apiconf.ZABBIX_PASSWD)

#日志文件
log=log.LOG("auto_update_item_status")

#配置文件
list_file="../list/auto_update_item_status.txt"

#监控项的设置
key="system.cpu.switches"
status="1"

#遍历配置文件
with open(list_file,"r") as f:
    for line in f.readlines():
        host_ip=line.split()[0]

        #判断主机是否存在
        if zabbix.host_exists(host_ip):
            host_id=zabbix.get_host_id(host_ip)
            #如果item存在则禁用
            if zabbix.item_exits(host_ip, key):
                try:
                    itemid=zabbix.get_host_item(host_id, key)
                    zabbix.update_item_status(itemid[0],status)
                    log.info("主机%s监控项%s已禁用" % (host_ip,key))
                except Exception as e:
                    log.error("主机%s监控项%s状态更新异常: %s" % (host_ip,key,e))
            else:
                log.info("主机%s监控项%s不存在" % (host_ip,key))

        #主机不存在
        else:
            log.warning("主机%s未加入监控" % host_ip)