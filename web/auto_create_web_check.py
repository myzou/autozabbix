#coding=utf-8
from conf import apiconf
from lib  import AutoZabbix
from lib import  log

#登录认证
zabbix=AutoZabbix.AutoZabbix(apiconf.ZABBIX_SERVER,apiconf.ZABBIX_USER,apiconf.ZABBIX_PASSWD)
#日志文件
log=log.LOG("auto_create_web_check")

#配置文件
list_file="../list/auto_create_web_check.txt"

#WEB参数
web_app="Web"
delay="300"
retries="3"
status_code="200,301,302,304"
timeout="15"
step_no="1"

with open(list_file,"r+") as f:
    for line  in f.readlines():
        host_name=line.split()[0]
        #port=line.split()[1]
        #urlpath=line.split()[2]
        random_int=random.randint(0,10000)
        #web_name="web_" + port + "_" + str(random_int)
        web_name = "web_" + str(random_int)
        #check_url="http://" + host_name + ":" + port + urlpath
        check_url=line.split()[1]
        #如果监控url的状态非200和30X，则不创建监控
        http_code,time_namelookup,time_connect,time_total= os.popen('''curl -L -o /dev/null -s -w "%{http_code} %{time_namelookup} %{time_connect} %{time_total}" ''' + check_url).readlines()[0].split()
        if http_code == "200" or http_code == "302" or http_code == "301":
            #判断主机是否监控
            if not zabbix.host_exists(host_name):
                log.info("主机%s未加入zabbix监控" % host_name)
            else:
                hostid=zabbix.get_host_id(host_name)
                #判断web应用程序是否存在
                if not zabbix.app_exists(hostid,web_app):
                    app_id=zabbix.create_app(hostid,web_app)
                    log.info("主机%s %s应用集创建成功" % (host_name,web_app))
                #web存在
                app_id=zabbix.get_app_id(hostid,web_app)
                #web监控是否存在
                url_exists=zabbix.get_web_url(hostid)
                if check_url in url_exists:
                    log.info("主机%s %s监控已存在" % (host_name,check_url))
                #web监控不存在，创建监控
                else:
                    zabbix.create_http_check(web_name,hostid,app_id,delay,retries,web_name,check_url,status_code,step_no,timeout)
                    log.info("主机%s %s监控创建成功" % (host_name,check_url))
                    #创建报警策略
                    triggername="主机{HOST.NAME}url:" + check_url + "访问失败"
                    triggerexpression="{" + host_name + ":web.test.error[" + web_name + "].nodata(5m)}=0"
                    zabbix.create_trigger(triggername,triggerexpression)
                    log.info("主机%s web监控trigger创建成功." % host_name)
        else:
            log.info("主机%s %s状态码为%s,非200和30X" % (host_name,check_url,http_code))