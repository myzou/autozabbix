#coding=utf-8
from conf import apiconf
from lib  import AutoZabbix
from lib import  log

#登录认证
zabbix=AutoZabbix.AutoZabbix(apiconf.ZABBIX_SERVER,apiconf.ZABBIX_USER,apiconf.ZABBIX_PASSWD)

#日志文件
log=log.LOG("auto_add_item")

#配置文件
list_file="../list/auto_add_item.txt"

#监控项的设置
name="findsec test"
key="findsec.test"
type=4
value_type=3
delay=60
snmp_oid="1.3.6.1.2.1.1.6.0.0.0.0.0"
snmp_community="public"

iterface_type="2"

#遍历配置文件
with open(list_file,"r") as f:
    for line in f.readlines():
        host_ip=line.split()[0]

        #判断主机是否存在
        if zabbix.host_exists(host_ip):
            host_id=zabbix.get_host_id(host_ip)
            #如果item不存在则添加
            if zabbix.item_exits(host_ip, key):
                log.info("主机%s监控项%s已存在" % (host_ip,key))
            else:
                #获取监控接口ID
                all_interfaces=zabbix.get_host_interfaces(host_id)
                if len(all_interfaces) >0:
                    for interface_info in all_interfaces:
                        if interface_info["type"] == iterface_type:
                            interface_id=interface_info["interfaceid"]
                        else:
                            interface_id=""

                #若接口ID不为空，创建item
                if interface_id != "":
                    try:
                        zabbix.create_snmp_item(host_id,interface_id,name,key,type,value_type,delay,snmp_oid,snmp_community)
                        log.info("主机%s添加监控项%s成功" % (host_ip,key))
                    except Exception as e:
                        log.error("主机%s添加监控项%s异常： %s" % (host_ip,key,e))

        #主机不存在
        else:
            log.warning("主机%s未加入监控" % host_ip)