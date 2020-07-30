#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
import os
import time

def runcase_all():
    os.system('python /home/yhl2/workspace/xtp_test/run/run4_option.py')
    os.system('sh /home/yhl2/workspace/xtp_test/Autocase_Result/RESTART/restart.sh')
    os.system('python /home/yhl2/workspace/xtp_test/run/run4_option_exercise.py')
    os.system('sh /home/yhl2/workspace/xtp_test/Autocase_Result/RESTART/restart.sh')
    os.system('python /home/yhl2/workspace/xtp_test/run/run4_option_yz.py')
    os.system('python /home/yhl2/workspace/xtp_test/run/run4_option_exercise_yz.py')
if __name__ == '__main__':
    runcase_all()
