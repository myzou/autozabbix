#coding=utf-8
from conf import apiconf
from lib  import AutoZabbix
from lib import  log

#登录认证
zabbix=AutoZabbix.AutoZabbix(apiconf.ZABBIX_SERVER,apiconf.ZABBIX_USER,apiconf.ZABBIX_PASSWD)

#日志文件
log=log.LOG("auto_zabbix_test")

all_userids=zabbix.get_all_users()
log.info("所有用户ID: %s" % all_userids)
print(zabbix.get_userid('GNOC'))

#print zabbix.create_usergroup("test01","15",permission)
#print  zabbix.create_user("test01","test01","19","4","test01@findsec.cn")
#print zabbix.user_to_group("8","13")
#print zabbix.group_permission_update("19","2","2")
#print zabbix.update_user_email("8","4","test01@126.com")


#print  zabbix.get_all_groups()
#print  zabbix.get_group_id("findsec")
#print  zabbix.get_host_id("Zabbix server")
#print  zabbix.create_group("apitest")
#print  zabbix.host_to_group("16","10084")
#print  zabbix.create_snmp_host_with_visablename("1.1.1.1","1.1.1.1","16")
#print  zabbix.unlink_clear_host_template("10285","10217")
#print  zabbix.create_host_snmp_interface("10280","10.70.93.172","161")
#print  zabbix.host_interface_delete("22")
#print  zabbix.delete_host("10293")


#print  zabbix.get_template_id("Template App FTP Service")
#print  zabbix.get_template_host("Template OS Linux")
#print   zabbix.template_to_host("10093","10282")
#print  zabbix.unlink_clear_template("10093","10097")
#print  zabbix.clear_template_host("10093")
#print   zabbix.update_item_status("29508","1")
#print zabbix.get_latest_item_value("23299","0")
#print  zabbix.get_host_interfaces("10084")
#print  zabbix.create_item("10084","1","test item","auto.api.item","0","0","60")

#print zabbix.get_trigger_info("16197")
#print zabbix.create_trigger("API告警创建测试","{10.70.93.176:proc.num[,,run].avg(5m)}>60","3")
#print   zabbix.update_trigger_name("16270","API告警创建测试  new ","4")
#print   zabbix.update_trigger_status("16270","1")

#print   zabbix.get_trigger_id("10.70.93.143", "{HOST.NAME}主机最近10分钟的平均进程数为{ITEM.VALUE1}大于1000")

#print  zabbix.create_alert_action("测试告警操作创建",p_subject,p_message,r_subject,r_message,"20","4","17")
#print  zabbix.update_action_msg("14",p_subject,p_message,r_subject,r_message)
#conditions=[{"conditiontype":0,"operator":0,"value":18},{"conditiontype":16,"operator":11,"value":""},{"conditiontype":4,"operator":5,"value":2}]
#print  zabbix.update_action_conditions("14","0",conditions)

#print zabbix.create_http_check("测试web监控","10084","1271","60","3","百度首页","https://www.baidu.com","200","1","5")
#print zabbix.get_web_url("10084")
# print(zabbix.update_web_url("测试web监控","9","120","2","百度new","https://www.baidu.com/test/","302","1","4"))