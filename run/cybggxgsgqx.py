#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
import time
sys.path.append('/home/yhl2/workspace/xtp_test/mysql')
sys.path.append('/home/yhl2/workspace/xtp_test/Autocase_Result/CYBGGXGSGQX')
sys.path.append('/home/yhl2/workspace/xtp_test/utils')
import runcase_ipo
import CaseService

def runcase_CYBGGXGSGQX():
    runcase_ipo.runCases(path, u'sj_qx.xlsx', u'CYBGGXGSGQX')


if __name__ == '__main__':
    path = '/home/yhl2/workspace/xtp_test/utils'
    runcase_CYBGGXGSGQX()
