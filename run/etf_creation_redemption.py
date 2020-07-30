#!/usr/bin/python
# -*- encoding: utf-8 -*-

import os

def runCases():

    #os.system('sh /home/yhl2/workspace/xtp_test/ETF/Creation_SA/creation_sa.sh')
    #os.system('sh /home/yhl2/workspace/xtp_test/ETF/Redemption_SA/redemption_sa.sh')
    os.system('sh /home/yhl2/workspace/xtp_test/ETF/Creation_HA/creation_ha.sh')
    os.system('sh /home/yhl2/workspace/xtp_test/ETF/Redemption_HA/redemption_ha.sh')
    os.system('sh /home/yhl2/workspace/xtp_test/crossmarketetf/crossmarket_creation_HA/cetf_shsg.sh')
    os.system('sh /home/yhl2/workspace/xtp_test/crossmarketetf/crossmarket_redemption_HA/cetf_shsh.sh')

if __name__ == '__main__':
    runCases()
