#coding=utf-8
from conf import apiconf
from lib  import AutoZabbix
from lib import  log

#登录认证
zabbix=AutoZabbix.AutoZabbix(apiconf.ZABBIX_SERVER,apiconf.ZABBIX_USER,apiconf.ZABBIX_PASSWD)

#日志文件
log=log.LOG("auto_create_action")

#配置文件
list_file="../list/auto_create_action.txt"


#获取报警媒介的ID
MAIL_ALERT_ID=zabbix.get_media_id("邮件告警")


with open(list_file,"r+") as f:
    for line in f.readlines():
        zabbix_group=line.split()[0]
        user_group=line.split()[1]

        #判断主机组是否存在
        if not zabbix.group_exists(zabbix_group):
            zabbix.create_group(zabbix_group)
            host_groupid = zabbix.get_group_id(zabbix_group)
        else:
            host_groupid=zabbix.get_group_id(zabbix_group)

        #用户是否存在
        if not zabbix.user_group_exists(user_group):
            zabbix.create_usergroup(user_group,host_groupid)
            usrgrpid=zabbix.get_usrgrpid(user_group)
        else:
            usrgrpid=zabbix.get_usrgrpid(user_group)


        #创建邮件报警操作
        actionname=zabbix_group + "-" + "Mail"
        #邮件发送给用户组
        msg_usrgrpid=usrgrpid
        mediatypeid=MAIL_ALERT_ID
        #默认针对主机组发送报警，主机组ID
        value=host_groupid
        #操作调节，没有ACK发送报警
        op_conditiontype="14"
        op_operator="0"
        op_value="0"
        #默认事件源为trigger
        eventsource="0"
        #操作条件，默认AND/OR
        evaltype="0"
        #操作步骤持续时间，默认3600
        esc_period="3600"
        #操作启用状态，默认启用
        status="0"
        #恢复消息状态，(0-disable,1-enable)
        r_status="0"
        #操作条件，默认针对主机组
        conditiontype="0"
        operator="0"
        #操作类型，默认发送消息
        operationtype="0"
        #步骤持续时间，0为默认值
        action_esc_period="0"
        #步骤的起和终
        esc_step_from="1"
        esc_step_to="1"
        #步骤的条件，默认AND/OR
        action_evaltype="0"
        #默认信息
        default_msg="1"

        if not zabbix.action_exists(actionname):
            zabbix.create_alert_action(actionname,apiconf.p_subject,apiconf.p_message,apiconf.r_subject,apiconf.r_message,msg_usrgrpid,mediatypeid,value,op_conditiontype,op_operator,op_value,eventsource,evaltype,esc_period,status,r_status,conditiontype,operator,operationtype,action_esc_period,esc_step_from,esc_step_to,action_evaltype,default_msg)
            log.info("成功创建告警操作%s" % actionname)
        else:
            log.info("告警操作%s已存在" % actionname)