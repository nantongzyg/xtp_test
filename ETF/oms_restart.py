#!/usr/bin/python
# -*- encoding: utf-8 -*-
import subprocess
import paramiko
import os
import wmi_client_wrapper as wmi

def oms_restart():
    user_id = '5'
    myclient = paramiko.SSHClient()
    myclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    myclient.connect('10.26.134.192', port = 22, username = 'xtp-test-' + user_id, password = 'xtp-test-' + user_id)
    cmd = '/xtp/deploy/lastsf/bin/xoms -f ~/oms/xoms_config.xml'
    stdin, stdout, stderr = myclient.exec_command(cmd)
    print stdout.read()
    # myclient.exec_command('su root')
    # stdin, stdout, stderr = myclient.exec_command('/sbin/serviceCreationRedemption oms.test' + user_id + ' restart')
    print cmd
    # print stdout.read()

if __name__ == '__main__':
    oms_restart()