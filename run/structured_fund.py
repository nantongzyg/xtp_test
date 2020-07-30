#!/usr/bin/python
# -*- encoding: utf-8 -*-
import time
import structured_fund_creation_redemption
import structured_fund_split_merge

if __name__ == '__main__':
    path = '/home/yhl2/workspace/xtp_test/utils'
    structured_fund_creation_redemption.runCases(path, 'structured_fund_creation_redemption.xlsx')
    time.sleep(3)
    structured_fund_split_merge.runCases(path, 'structured_fund_creation_redemption.xlsx')