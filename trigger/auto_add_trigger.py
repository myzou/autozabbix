#coding=utf-8
from conf import apiconf
from lib  import AutoZabbix
from lib import  log

#登录认证
zabbix=AutoZabbix.AutoZabbix(apiconf.ZABBIX_SERVER,apiconf.ZABBIX_USER,apiconf.ZABBIX_PASSWD)

#日志文件
log=log.LOG("auto_add_trigger")

#配置文件
list_file="../list/auto_add_trigger.txt"

#触发器的设置
trigger_name="{HOST.NAME}主机最近10分钟的平均进程数为{ITEM.VALUE1}大于1000"
priority=4

#遍历配置文件
with open(list_file,"r") as f:
    for line in f.readlines():
        host_ip=line.split()[0]

        #判断主机是否存在
        if zabbix.host_exists(host_ip):
            host_id=zabbix.get_host_id(host_ip)
            trigger_expression = "{" + host_ip + ":proc.num[]" + ".avg(10m)}>1000"
            #如果trigger不存在则创建
            if not zabbix.trigger_exist(host_ip, trigger_name):
                zabbix.create_trigger(trigger_name,trigger_expression,priority)
                log.info("主机%s触发器%s创建成功" % (host_ip,trigger_expression))
            else:
                log.info("主机%s触发器%s已存在" % (host_ip,trigger_expression))

        #主机不存在
        else:
            log.warning("主机%s未加入监控" % host_ip)