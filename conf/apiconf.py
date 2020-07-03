#!/usr/bin/env python
#coding=utf-8

#zabbix server变量
ZABBIX_SERVER="http://10.122.82.162/zabbix"
ZABBIX_USER="Admin"
ZABBIX_PASSWD="JPrPHPeA"


#用户组对主机组权限
permission="3"


#报警信息
p_subject="new状态:{TRIGGER.STATUS}|机器:{HOST.NAME1}|{TRIGGER.NAME}"
p_message='''
new
<b>报警内容：</b>{TRIGGER.NAME}<br>
<b>当前时间：</b>{DATE} {TIME}<br>
<b>服务器IP：</b>{HOST.HOST1}<br>
<b>报警级别：</b> <font color='red'>{TRIGGER.SEVERITY}</font><br>
<b>报警时间：</b> {DATE} {EVENT.TIME}<br>
<b>确认状态：</b> {EVENT.ACK.STATUS}<br>
<b>监控项名称：</b>{ITEM.NAME1}<br>
<b>最新数据：</b> {ITEM.VALUE1}<br>
'''

r_subject="new 状态:{TRIGGER.STATUS}|机器:{HOST.NAME1}|{TRIGGER.NAME}"
r_message='''
new
<b>报警内容：</b>{TRIGGER.NAME}<br>
<b>当前时间：</b>{DATE} {TIME}<br>
<b>服务器IP：</b>{HOST.HOST1}<br>
<b>报警级别：</b> <font color='red'>{TRIGGER.SEVERITY}</font><br>
<b>报警时间：</b> {DATE} {EVENT.TIME}<br>
<b>故障持续时间：</b> {EVENT.AGE}  <br>
<b>恢复时间：</b> {EVENT.RECOVERY.TIME}  <br>
<b>监控项名称：</b>{ITEM.NAME1}<br>
<b>最新数据：</b> {ITEM.VALUE1}<br>
'''
