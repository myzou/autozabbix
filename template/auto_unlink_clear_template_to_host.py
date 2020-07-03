#coding=utf-8
from conf import apiconf
from lib  import AutoZabbix
from lib import  log

#登录认证
zabbix=AutoZabbix.AutoZabbix(apiconf.ZABBIX_SERVER,apiconf.ZABBIX_USER,apiconf.ZABBIX_PASSWD)

#日志文件
log=log.LOG("auto_unlink_clear_template_to_host")

#配置文件
list_file="../list/auto_unlink_clear_template_to_host.txt"

#关联的模板名称
template_name="Template Module Generic SNMPv1"

#遍历文件
with open(list_file,"r+") as f:
    #获取模板ID
    template_id=zabbix.get_template_id(template_name)
    #获取主机
    for line in f.readlines():
        host_ip=line.split()[0]
        #主机存在
        if zabbix.host_exists(host_ip):
            host_id=zabbix.get_host_id(host_ip)
            host_id_list={"hostid":host_id}
            monitoered_host=zabbix.get_template_host(template_name)
            #主机已加入模板
            if host_id_list in monitoered_host:
                zabbix.unlink_clear_host_template(host_id,template_id)
                log.info("主机%s成功清理监控模板%s" % (host_ip,template_name))
            #主机未关联模板
            else:
                log.info("主机%s未关联模板%s" % (host_ip,template_name))
        #主机不存在
        else:
            log.info("主机%s不存在" % host_ip)