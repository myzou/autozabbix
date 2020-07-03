#coding=utf-8
from conf import apiconf
from lib  import AutoZabbix
from lib import  log

#登录认证
zabbix=AutoZabbix.AutoZabbix(apiconf.ZABBIX_SERVER,apiconf.ZABBIX_USER,apiconf.ZABBIX_PASSWD)

#日志文件
log=log.LOG("auto_add_host_to_group")

#配置文件
list_file="../list/auto_add_host_to_group.txt"

#遍历配置文件
with open(list_file,"r") as f:
    for line in f.readlines():
        host_ip=line.split()[0]
        host_group=line.split()[1]

        # 主机组不存在
        if not zabbix.group_exists(host_group):
            try:
                #创建主机组
                zabbix.create_group(host_group)
                log.info("成功创建主机组%s" % (host_group))
            except Exception as e:
                log.error("创建主机组%s异常：%s" % (host_group,e))

        #判断主机是否存在
        if zabbix.host_exists(host_ip):
            host_id=zabbix.get_host_id(host_ip)
            group_id=zabbix.get_group_id(host_group)
            try:
                zabbix.host_to_group(group_id,host_id)
                log.info("成功将主机%s加入主机组%s" % (host_ip,host_group))
            except Exception as e:
                log.error("主机%s加入主机组%s异常： %s" % (host_ip,host_group,e))
        #主机不存在
        else:
            log.warning("主机%s未加入监控" % host_ip)