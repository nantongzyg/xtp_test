#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
#sys.path.append('/home/yhl2/workspace/xtp_test/StructuredFund/creationRedemption')
#sys.path.append('/home/yhl2/workspace/xtp_test/StructuredFund/splitMerge')
sys.path.append('/home/yhl2/workspace/xtp_test/StructuredFund/serviceCreationRedemption')
sys.path.append('/home/yhl2/workspace/xtp_test/StructuredFund/serviceSplitMerge')
sys.path.append('/home/yhl2/workspace/xtp_test/utils')
import CaseServiceStructuredFundCreation

path = '/home/yhl2/workspace/xtp_test/utils'

def runcase_StructuredFund_SS():
    import structured_fund_creation_redemption as a
    a.runCases(path, 'structured_fund_creation_redemption.xlsx', u'申赎')

def runcase_StructuredFund_Split_Merge():
    import structured_fund_split_merge as a
    a.runCases(path, 'structured_fund_creation_redemption.xlsx', u'拆分合并')

if __name__ == '__main__':
    runcase_StructuredFund_SS()
    #runcase_StructuredFund_Split_Merge()
