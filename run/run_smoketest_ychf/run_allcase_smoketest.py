#!/usr/bin/python
# -*- encoding: utf-8 -*-
import os

def runallcase():
    #os.system('python /home/yhl2/workspace/xtp_test/run/run_smoketest/run1_common_smoketest.py')
    os.system('python /home/yhl2/workspace/xtp_test/run/run_smoketest/run4_option_smoketest.py')
    os.system('sh /home/yhl2/workspace/xtp_test/run/run_smoketest/etf_creation_redemption_smoketest.sh')

if __name__ == '__main__':
    runallcase()

