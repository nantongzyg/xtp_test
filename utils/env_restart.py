#!/usr/bin/python:
# -*- encoding: utf-8 -*-
import sys
import os
import time
import urllib2
import paramiko
import pexpect
sys.path.append('/home/yhl2/workspace/xtp_test/xtp/api')
import config
sys.path.append('/home/yhl2/workspace/xtp_test/service')
import ServiceConfig
sys.path.append('/home/yhl2/workspace/xtp_test/mysql')
from  SqlData_Transfer import SqlData_Transfer
from mysql_config import *
from database_manager import QueryTable

#执行导出生成xtp_ept_dayorderrec_date表
def excute_ept():
    get_data(ServiceConfig.ept_dayorderrec_sh[0])
    time.sleep(30)

# oms重启
def oms_restart():
    myclient = client_conn()
    oms_print_msg = ''
    if len(ServiceConfig.oms_cmds) > 0:
        for cmd in ServiceConfig.oms_cmds:
            oms_print_msg = exec_cmd(myclient, cmd)
            time.sleep(4)
            oms_print_msg = exec_cmd(myclient, cmd)
        oms_restart_cycle(oms_print_msg, myclient)
    else:
        return False
    myclient.close()

# 上海环境重启，r包含oms
def sh_all_restart():
    sh_restart()
    oms_restart()

# 上海sqlserver 数据库服务关闭
def sqlserver_stop():
    get_data(ServiceConfig.restart_sqlserver_sh[0])
    time.sleep(5)

# 上海sqlserver 数据库服务启动
def sqlserver_start():
    get_data(ServiceConfig.restart_sqlserver_sh[1])
    time.sleep(5)

# 深圳环境重启，包含oms
def sz_restart():
    myclient = client_conn()
    oms_print_msg = ''
    if len(ServiceConfig.sz_cmds) > 0:
        for cmd in ServiceConfig.sz_cmds:
            if cmd.endswith('startall.sh'):
                oms_print_msg = exec_cmd(myclient, cmd)
                time.sleep(4)
            oms_print_msg = exec_cmd(myclient, cmd)
        oms_restart_cycle(oms_print_msg, myclient)
    else:
        return False
    myclient.close()
    #time.sleep(2)

def xogwsz_close():
    myclient = client_conn()
    exec_cmd(myclient, ServiceConfig.sz_close[1])
    myclient.close()
# 所有环境重启
def all_restart():
    sh_restart()
    sz_restart()

# xogwsz深圳报盘重启
def xogwsz_restart():
    myclient = client_conn()
    if len(ServiceConfig.xogwsz_cmds) > 0:
        for cmd in ServiceConfig.xogwsz_cmds:
            exec_cmd(myclient, cmd)
            time.sleep(1)
    else:
        return False
    myclient.close()

def close_ogw():
    for path in ServiceConfig.restart_path_sh:
        if path == ServiceConfig.restart_path_sh[2]:
            print 'path',path
            get_data(path)

# 清除上海接口库数据并且重启上海环境，包含oms
def clear_data_and_restart_sh():
    oms_stop()
    sql_transfer = SqlData_Transfer()
    sql_transfer.truncate_sse()
    sh_restart()
    oms_restart()
    #time.sleep(1)

# 清除深圳接口库数据并且重启深圳环境，包含oms
def clear_data_and_restart_sz():
    oms_stop()
    remove_files()
    sz_restart()

#清除上海 深圳接口库数据，重启环境
def clear_data_and_restart_all():
    print 'coming'
    oms_stop()
    print "oms_stop"
    sql_transfer = SqlData_Transfer()
    print sql_transfer
    sql_transfer.truncate_sse()
    print "truncate_sse"
    remove_files()
    print "rm file"
    sh_restart()
    print "sh restart over"
    sz_restart()
    print "sz restart over"
    #time.sleep(2)

def close_ogwsh():
    for path in ServiceConfig.restart_path_sh:
        if path == ServiceConfig.restart_path_sh[2]:
            print 'path',path
            get_data(path)


# 修改本地match配置文件,market_style="Open",并上传到oms服务器
def update_Open_and_upload_match_xml():
    update_market_style(1)
    doRsync(ServiceConfig.srcMatchAfterUpdate, ServiceConfig.matchDstDir)

# 修改本地match配置文件,market_style="EqualHigh",并上传到oms服务器
def update_Equalhigh_and_upload_match_xml():
    update_market_style(2)
    doRsync(ServiceConfig.srcMatchAfterUpdate, ServiceConfig.matchDstDir)

# 修改oms配置文件中match的market_style,1-Open, 2-EqualHigh
def update_market_style(market_style):
    content = ''
    with open(ServiceConfig.srcMatchBeforeUpdate, 'r') as f:
        for line in f.readlines():
            if line.find('market_style') > 0:
                print line
                if market_style == 1:
                    line = '    <Rule mode="report" index="7" market_style="Open">\n'
                elif market_style == 2:
                    line = '    <Rule mode="report" index="7" market_style="EqualHigh">\n'
                else:
                    return False

            content += line
    with open(ServiceConfig.srcMatchAfterUpdate, 'w') as f:
        f.write(content)

# 将修改后的oms配置文件上传到oms服务器
def doRsync(srcDir, dstDir, timeout=3600):
    #  cmd = "rsync -azPq --delete {srcDir} {rUser}@{rHost}:{dstDir}".format(
    #      rUser = user,rHost=ip,srcDir=srcDir,dstDir=dstDir
    #  )
    # 如果是目录的话，rsync命令中添加'-r'
    if os.path.isdir(srcDir):
        cmd = "rsync -r {srcDir} {rUser}@{rHost}:{dstDir}".format(
            rUser = ServiceConfig.login_info['user_name'],
            rHost = ServiceConfig.login_info['ip'],
            srcDir = srcDir,
            dstDir = dstDir)
    # 其他按文件传输
    else:
        cmd = "rsync {srcDir} {rUser}@{rHost}:{dstDir}".format(
            rUser = ServiceConfig.login_info['user_name'],
            rHost = ServiceConfig.login_info['ip'],
            srcDir = srcDir,
            dstDir = dstDir)
    try:
        ssh = pexpect.spawn(cmd, timeout=timeout)
        i = ssh.expect(['password:', 'continue connecting (yes/no)?'],
                       timeout=5)
        if i == 0:
            ssh.sendline(ServiceConfig.login_info['password'])
        elif i == 1:
            ssh.sendline('yes')
            ssh.expect('password: ')
            ssh.sendline(ServiceConfig.login_info['password'])
        ssh.read()
        ssh.close()
    except:
        # print traceback.format_exc()
        pass

# oms服务关闭
def oms_stop():
    myclient = client_conn()
    exec_cmd(myclient, ServiceConfig.oms_stop_cmds)
    myclient.close()

# 上海环境重启，不包含oms 16版本
# def sh_restart():
#     for path in ServiceConfig.restart_path_sh:
#         get_data(path)
#         time.sleep(3)
#18版本
def sh_restart():
    for path in ServiceConfig.restart_path_sh:
        print 'path',path
        if path == ServiceConfig.restart_path_sh[1]:
            get_data(path)
            time.sleep(10)
        else:
            get_data(path)
            time.sleep(2)

def client_conn():
    myclient = paramiko.SSHClient()
    myclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    myclient.connect(ServiceConfig.login_info['ip'],
                     port=ServiceConfig.login_info['port'],
                     username=ServiceConfig.login_info['user_name'],
                     password=ServiceConfig.login_info['password'])
    return myclient

def exec_cmd(myclient, cmd):
    stdin, stdout, stderr = myclient.exec_command(cmd)
    oms_print_msg = stdout.read()
    time.sleep(2)
    return oms_print_msg

# 若oms服务第一次启动失败，则再启动三次，直到启动成功
def oms_restart_cycle(oms_print_msg, myclient):
    count = 0
    # 若用startall.sh命令启动oms失败，则用startall.sh xoms命令再启三次
    while count <= 3:
        if oms_print_msg.endswith(ServiceConfig.oms_error_msg):
            for c in ServiceConfig.oms_cmds:
                if c.endswith('startall.sh xoms'):
                    oms_print_msg = exec_cmd(myclient, c)
                    time.sleep(3)
                oms_print_msg = exec_cmd(myclient, c)
        else:
            return True
        count += 1

def get_date():
    return time.strftime('%Y%m%d', time.localtime(time.time()))

def get_data(url):
	u = urllib2.urlopen(url)
	return u.read()

# 删除深圳接口库文件
def remove_files():
    myclient = client_conn()
    print ServiceConfig.match_data_path
    print ServiceConfig.ogw_data_path1
    print ServiceConfig.ogw_data_path2
    exec_cmd(myclient, ServiceConfig.match_data_path)
    exec_cmd(myclient, ServiceConfig.ogw_data_path1)
    exec_cmd(myclient, ServiceConfig.ogw_data_path2)
    myclient.close()

# 上海撮合关闭(午休)
def sh_noonclosed():
    get_data(ServiceConfig.restart_path_sh[0])
    time.sleep(1)

# 上海撮合开启(午休)
def sh_noonstart():
    get_data(ServiceConfig.restart_path_sh[1])
    time.sleep(30)

if __name__ == '__main__':
    # update_and_upload_oms_xml('YW_FJJJ_SZSS_030')
    clear_data_and_restart_all()
    #clear_data_and_restart_sz()
    # update_etf_fee_and_upload_oms_xml('YW_ETFSS_SHSG_059')
    #time.sleep(1)
    #excute_ept()
