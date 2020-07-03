#coding=utf-8
from conf import apiconf
from lib  import AutoZabbix
from lib import  log

#登录认证
zabbix=AutoZabbix.AutoZabbix(apiconf.ZABBIX_SERVER,apiconf.ZABBIX_USER,apiconf.ZABBIX_PASSWD)
#日志文件
log=log.LOG("auto_update_trigger_name")

#配置文件
list_file="../list/auto_update_trigger_name.txt"

#触发器的设置
trigger_name="{HOST.NAME}主机最近10分钟的平均进程数为{ITEM.VALUE1}大于1000"
new_trigger_name="主机最近10分钟的平均进程数为{ITEM.VALUE1}大于1000"
priority=2

#遍历配置文件
with open(list_file,"r") as f:
    for line in f.readlines():
        host_ip=line.split()[0]

        #判断主机是否存在
        if zabbix.host_exists(host_ip):
            host_id=zabbix.get_host_id(host_ip)
            #如果触发器存在则更新
            if zabbix.trigger_exist(host_ip, trigger_name):
                triggerid=zabbix.get_trigger_id(host_ip, trigger_name)
                zabbix.update_trigger_name(triggerid,new_trigger_name,priority)
                log.info("主机%s触发器%s已更新为%s" % (host_ip,trigger_name,new_trigger_name))
            else:
                log.info("主机%s触发器%s不存在" % (host_ip,trigger_name))

        #主机不存在
        else:
            log.warning("主机%s未加入监控" % host_ip)