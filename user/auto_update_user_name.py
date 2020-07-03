#coding=utf-8
from conf import apiconf
from lib  import AutoZabbix
from lib import  log

#登录认证
zabbix=AutoZabbix.AutoZabbix(apiconf.ZABBIX_SERVER,apiconf.ZABBIX_USER,apiconf.ZABBIX_PASSWD)

#日志文件
log=log.LOG("auto_update_user_name")

#配置文件
list_file="../list/auto_update_user_name.txt"

#遍历配置文件
with open(list_file,"r") as f:
    for line in f.readlines():
        old_name=line.split()[0]
        new_name=line.split()[1]

        #判断用户是否存在
        if zabbix.user_exists(old_name):
            user_id=zabbix.get_userid(old_name)
            try:
                zabbix.update_user_name(user_id,new_name)
                log.info("用户%s名称%s --> %s 更改成功" % (old_name,old_name,new_name))
            except Exception as e:
                log.error(("用户%s名称更新异常： %s" % (old_name,e)))

        #用户不存在
        else:
            log.warning("用户%s不存在" % (old_name))