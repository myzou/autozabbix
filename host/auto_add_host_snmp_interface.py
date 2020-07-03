#coding=utf-8
from conf import apiconf
from lib  import AutoZabbix
from lib import  log

#登录认证
zabbix=AutoZabbix.AutoZabbix(apiconf.ZABBIX_SERVER,apiconf.ZABBIX_USER,apiconf.ZABBIX_PASSWD)

#日志文件
log=log.LOG("auto_add_host_snmp_interface")

#配置文件
list_file="../list/auto_add_host_snmp_interface.txt"

#遍历文件
with open(list_file,"r+") as f:
    #获取主机和snmp信息
    for line in f.readlines():
        host_ip=line.split()[0]
        snmp_ip=line.split()[1]
        snmp_port=line.split()[2]

        #判断主机是否存在
        if zabbix.host_exists(host_ip):

            #获取主机ID
            host_id=zabbix.get_host_id(host_ip)
            #监控接口已存在
            if zabbix.host_interface_exists(host_id,snmp_ip,snmp_port):
                log.info("%s - %s - SNMP监控接口已存在" % (host_ip,snmp_ip))
            else:
                #监控接口不存在
                zabbix.create_host_snmp_interface(host_id,snmp_ip,snmp_port)
                log.info("%s - %s - SNMP监控接口添加成功" % (host_ip,snmp_ip))

        #主机不存在
        else:
            log.info("主机%s未加入监控" % host_ip)