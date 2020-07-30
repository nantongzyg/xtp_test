#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pexpect
import time
import traceback
import os
from Linux_Upload_config import user, passwd, ip, srcFile, srcDir, dstDir


def doRsync(user, passwd, ip, srcDir, dstDir, timeout=3600):
    #  cmd = "rsync -azPq --delete {srcDir} {rUser}@{rHost}:{dstDir}".format(
    #      rUser = user,rHost=ip,srcDir=srcDir,dstDir=dstDir
    #  )
    # 如果是目录的话，rsync命令中添加'-r'
    if os.path.isdir(srcDir):
        cmd = "rsync -r {srcDir} {rUser}@{rHost}:{dstDir}".format(
            rUser=user, rHost=ip, srcDir=srcDir, dstDir=dstDir)
    # 其他按文件传输
    else:
        cmd = "rsync {srcDir} {rUser}@{rHost}:{dstDir}".format(
            rUser=user, rHost=ip, srcDir=srcDir, dstDir=dstDir)
    print cmd
    try:
        ssh = pexpect.spawn(cmd, timeout=timeout)
        print cmd
        i = ssh.expect(['password:', 'continue connecting (yes/no)?'], timeout=5)
        if i == 0:
            ssh.sendline(passwd)
        elif i == 1:
            ssh.sendline('yes')
            ssh.expect('password: ')
            ssh.sendline(passwd)
        ssh.read()
        ssh.close()
    except:
        # print traceback.format_exc()
        pass


if __name__ == '__main__':
    # 测试传输单个文件
    doRsync(user, passwd, ip, srcFile, dstDir)
    print "Upload File Success!"
    # 测试传输文件夹
    doRsync(user, passwd, ip, srcDir, dstDir)
    print "Upload Dir Success!"
