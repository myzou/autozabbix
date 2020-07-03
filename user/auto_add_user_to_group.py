#coding=utf-8
from conf import apiconf
from lib  import AutoZabbix
from lib import  log

#登录认证
zabbix=AutoZabbix.AutoZabbix(apiconf.ZABBIX_SERVER,apiconf.ZABBIX_USER,apiconf.ZABBIX_PASSWD)

#日志文件
log=log.LOG("auto_add_user_to_group")

#配置文件
list_file="../list/auto_add_user_to_group.txt"

#遍历配置文件
with open(list_file,"r") as f:
    for line in f.readlines():
        user_name=line.split()[0]
        group_name=line.split()[1]

        #判断用户是否存在
        if zabbix.user_exists(user_name):
            #判断用户组是否存在
            if zabbix.user_group_exists(group_name):
                user_id=zabbix.get_userid(user_name)
                group_id=zabbix.get_usrgrpid(group_name)
                #将用户加入用户组
                try:
                    zabbix.user_to_group(user_id,group_id)
                    log.info("用户%s加入组%s成功" % (user_name,group_name))
                except Exception as e:
                    log.error("将用户%s加入组%s异常: %s" % (user_name,group_name,e))

            #用户组不存在
            else:
                log.warning("用户组%s不存在" % group_name)

        #用户不存在
        else:
            log.warning("用户%s不存在" % user_name)