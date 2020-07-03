#coding=utf-8
from conf import apiconf
from lib  import AutoZabbix
from lib import  log

#登录认证
zabbix=AutoZabbix.AutoZabbix(apiconf.ZABBIX_SERVER,apiconf.ZABBIX_USER,apiconf.ZABBIX_PASSWD)

#日志文件
log=log.LOG("auto_create_host_with_snmp_interface")

#配置文件
list_file="../list/auto_create_host_with_snmp_interface.txt"

#遍历配置文件
with open(list_file,"r") as f:
    for line in f.readlines():
        host_ip=line.split()[0]
        snmp_ip=line.split()[1]
        snmp_port=line.split()[2]
        host_group=line.split()[3]

        #判断主机是否存在
        if zabbix.host_exists(host_ip):
            #判断主机组是否存在
            if zabbix.group_exists(host_group):
                #将主机加入到主机组
                host_id=zabbix.get_host_id(host_ip)
                host_group_id=zabbix.get_group_id(host_group)
                try:
                    zabbix.host_to_group(host_group_id,host_id)
                    log.info("成功将主机%s加入主机组%s" % (host_ip,host_group))
                except Exception as e:
                    log.error("将主机%s加入主机组%s异常： %s" % (host_ip,host_group,e))

            #主机组不存在
            else:
                #创建主机组
                try:
                    zabbix.create_group(host_group)
                    log.info("成功创建主机组%s" % host_group)
                except Exception as e:
                    log.error("创建主机组%s异常: %s" % (host_group,e))

                #将主机加入到主机组
                host_id=zabbix.get_host_id(host_ip)
                host_group_id=zabbix.get_group_id(host_group)
                try:
                    zabbix.host_to_group(host_group_id,host_id)
                    log.info("成功将主机%s加入主机组%s" % (host_ip,host_group))
                except Exception as e:
                    log.error("将主机%s加入主机组%s异常： %s" % (host_ip,host_group,e))

        #主机不存在
        else:
            #若主机组不存在则创建
            if not zabbix.group_exists(host_group):
                try:
                    zabbix.create_group(host_group)
                    log.info("成功创建主机组%s" % host_group)
                except Exception as e:
                    log.error("创建主机组%s异常: %s" % (host_group,e))

            #获取主机组ID
            host_group_id = zabbix.get_group_id(host_group)

            #创建主机
            try:
                zabbix.create_snmp_host_with_visablename(host_ip,host_ip,host_group_id)
                log.info("创建主机%s成功" % host_ip)

            except Exception as e:
                log.error("创建主机%s失败: %s" % (host_ip,e))