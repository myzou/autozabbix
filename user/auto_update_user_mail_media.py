#coding=utf-8
from conf import apiconf
from lib  import AutoZabbix
from lib import  log

#登录认证
zabbix=AutoZabbix.AutoZabbix(apiconf.ZABBIX_SERVER,apiconf.ZABBIX_USER,apiconf.ZABBIX_PASSWD)

#日志文件
log=log.LOG("auto_update_user_mail_media")

#配置文件
list_file="../list/auto_update_user_mail_media.txt"

#告警媒介ID
mail_type_id="4"

#遍历配置文件
with open(list_file,"r") as f:
    for line in f.readlines():
        user_name=line.split()[0]
        new_mail=line.split()[1]

        #判断用户是否存在
        if zabbix.user_exists(user_name):
            user_id=zabbix.get_userid(user_name)
            try:
                zabbix.update_user_email(user_id,mail_type_id,new_mail)
                log.info("用户%s邮箱更新为%s" % (user_name,new_mail))
            except Exception as e:
                log.error(("用户%s邮件告警更新异常： %s" % (user_name,e)))

        #用户不存在
        else:
            log.warning("用户%s不存在" % (user_name))