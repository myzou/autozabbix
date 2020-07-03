#coding=utf-8
from conf import apiconf
from lib  import AutoZabbix
from lib import  log

#登录认证
zabbix=AutoZabbix.AutoZabbix(apiconf.ZABBIX_SERVER,apiconf.ZABBIX_USER,apiconf.ZABBIX_PASSWD)
#日志文件
log=log.LOG("auto_delete_user")

#配置文件
list_file="../list/auto_delete_user.txt"


#遍历配置文件
with open(list_file,"r") as f:
    for line in f.readlines():
        user_name=line.split()[0]

        #判断用户是否存在
        if zabbix.user_exists(user_name):
            user_id=zabbix.get_userid(user_name)
            try:
                zabbix.delete_user(user_id)
                log.info("用户%s删除成功" % (user_name))
            except Exception as e:
                log.error(("删除用户%s异常： %s" % (user_name,e)))

        #用户不存在
        else:
            log.warning("用户%s不存在" % (user_name))