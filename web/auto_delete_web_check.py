#coding=utf-8
from conf import apiconf
from lib  import AutoZabbix
from lib import  log

#登录认证
zabbix=AutoZabbix.AutoZabbix(apiconf.ZABBIX_SERVER,apiconf.ZABBIX_USER,apiconf.ZABBIX_PASSWD)

#日志文件
log=log.LOG("auto_delete_web_check")

#配置文件
list_file="../list/auto_delete_web_check.txt"


with open(list_file,"r+") as f:
    for line  in f.readlines():
        host_name=line.split()[0]
        check_url=line.split()[1]

        # 判断主机是否监控
        if not zabbix.host_exists(host_name):
            log.info("主机%s未加入zabbix监控" % host_name)
        else:
            hostid = zabbix.get_host_id(host_name)

            # web监控是否存在
            url_exists = zabbix.get_web_url(hostid)
            if check_url in url_exists:
                url_id=zabbix.get_url_id(hostid,check_url)
                zabbix.delete_web_url(url_id)
                log.info("主机%s %s监控已删除" % (host_name, check_url))
            # web监控不存在
            else:
                log.info("主机%s web监控不存在." % host_name)