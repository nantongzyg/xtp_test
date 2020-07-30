#!/usr/bin/python
# -*- encoding: utf-8 -*-
import CaseService
import CaseServiceStructuredFundCreation
import CaseServiceAllotmentPayment
import CaseServiceSplitMerge
import CaseServiceIpo
import CaseServiceOption
import CaseServiceRzrqYchf
import CaseServiceMoneyFund
import CaseServiceKCB
from test_CaseService_kcb import *
# import CaseServiceQuote
# import CaseServiceMultPbu
import os.path

#生成深圳市场测试用例
def testcase_SZ():
    test_CaseService(u'普通业务自动化用例.xlsx',u'深圳限价','GPMM')
    test_CaseService(u'普通业务自动化用例.xlsx',u'深圳市价','GPMM')
    # test_CaseService(u'ETF买卖.xlsx',u'深圳限价单市场','ETFMM_D')
    # test_CaseService(u'ETF买卖.xlsx',u'深圳市价单市场','ETFMM_D')
    # test_CaseService(u'ETF买卖.xlsx',u'深圳限价跨市场','ETFMM_K')
    # test_CaseService(u'ETF买卖.xlsx',u'深圳市价跨市场','ETFMM_K')
    # test_CaseService(u'普通业务自动化用例.xlsx',u'分级子基金深圳限价','FJZJJMM')
    # test_CaseService(u'普通业务自动化用例.xlsx',u'分级子基金深圳市价','FJZJJMM')
    # test_CaseService(u'普通业务自动化用例.xlsx', u'逆回购_深圳','ReverseRepo')
    test_CaseServiceIpo(u'普通业务自动化用例.xlsx',u'新股申购_深圳','IPO')
    # test_CaseServiceAllotmentPayment(u'普通业务自动化用例.xlsx',u'配股缴款_深圳','AllotmentPayment')
    # test_CaseServiceMultPbu(u'普通业务自动化用例.xlsx', u'深圳限价', 'GPMM_MULT_PBU')

#生成深圳市场测试用例(新增)
def testcase_SZ_ADD():
    #test_CaseService(u'普通业务自动化用例_新增.xlsx',u'深圳限价','GPMM')
    #test_CaseService(u'普通业务自动化用例_新增.xlsx',u'深圳市价','GPMM')
    #test_CaseServiceIpo(u'普通业务自动化用例_新增.xlsx',u'新股申购_深圳','IPO')
    test_CaseService(u'ETF买卖_新增.xlsx',u'深圳限价单市场','ETFMM_D')
    test_CaseService(u'ETF买卖_新增.xlsx',u'深圳市价单市场','ETFMM_D')
    test_CaseService(u'ETF买卖_新增.xlsx',u'深圳限价跨市场','ETFMM_K')
    test_CaseService(u'ETF买卖_新增.xlsx',u'深圳市价跨市场','ETFMM_K')

#生成上海市场测试用用例(新增)
def testcase_SH_ADD():
    #test_CaseService(u'普通业务自动化用例_新增.xlsx',u'上海限价','GPMM')
    #test_CaseService(u'普通业务自动化用例_新增.xlsx',u'上海市价','GPMM')
    #test_CaseServiceIpo(u'普通业务自动化用例_新增.xlsx',u'新股申购_上海','IPO')
    #test_CaseServiceMoneyFund(u'普通业务自动化用例_新增.xlsx',u'交易型货币基金买卖上海限价','XjShHBJJMM')
    #test_CaseServiceMoneyFund(u'普通业务自动化用例_新增.xlsx',u'交易型货币基金买卖上海市价','SjShHBJJMM')
    test_CaseService(u'ETF买卖_新增.xlsx',u'上海限价单市场','ETFMM_D')
    test_CaseService(u'ETF买卖_新增.xlsx',u'上海市价单市场','ETFMM_D')
    test_CaseService(u'ETF买卖_新增.xlsx',u'上海限价跨市场','ETFMM_K')
    test_CaseService(u'ETF买卖_新增.xlsx',u'上海市价跨市场','ETFMM_K')

#生成上海市场测试用用例
def testcase_SH():
    test_CaseService(u'普通业务自动化用例.xlsx',u'上海限价','GPMM')
    test_CaseService(u'普通业务自动化用例.xlsx',u'上海市价','GPMM')
    #test_CaseService(u'普通业务自动化用例.xlsx',u'休市下单','MIDDLEBREAK')
    # test_CaseService(u'ETF买卖.xlsx',u'上海限价单市场','ETFMM_D')
    # test_CaseService(u'ETF买卖.xlsx',u'上海市价单市场','ETFMM_D')
    # test_CaseService(u'ETF买卖.xlsx',u'上海限价跨市场','ETFMM_K')
    # test_CaseService(u'ETF买卖.xlsx',u'上海市价跨市场','ETFMM_K')
    # test_CaseService(u'普通业务自动化用例.xlsx',u'逆回购_上海','ReverseRepo')
    test_CaseServiceIpo(u'普通业务自动化用例.xlsx',u'新股申购_上海','IPO')
    # test_CaseServiceAllotmentPayment(u'普通业务自动化用例.xlsx',u'配股缴款_上海','AllotmentPayment')
    # test_CaseServiceOption(u'个股期权自动化用例.xlsx', u'权利方限价_沪市', 'XjShRightSide')
    # test_CaseServiceOption(u'个股期权自动化用例.xlsx', u'权利方市价_沪市', 'SjShRightSide')
    # test_CaseServiceOption(u'个股期权自动化用例.xlsx', u'义务方限价（认购合约）_沪市', 'XjShObligationCall')
    # test_CaseServiceOption(u'个股期权自动化用例.xlsx', u'义务方市价（认购合约）_沪市', 'SjShObligationCall')
    # test_CaseServiceOption(u'个股期权自动化用例.xlsx', u'义务方限价（认沽合约）_沪市', 'XjShObligationPut')
    # test_CaseServiceOption(u'个股期权自动化用例.xlsx', u'义务方市价（认沽合约）_沪市', 'SjShObligationPut')
    # test_CaseServiceOption(u'个股期权自动化用例.xlsx', u'行权', 'Exercise')
    test_CaseServiceMoneyFund(u'普通业务自动化用例.xlsx',u'交易型货币基金买卖上海限价','XjShHBJJMM')
    test_CaseServiceMoneyFund(u'普通业务自动化用例.xlsx',u'交易型货币基金买卖上海市价','SjShHBJJMM')
    # test_CaseServiceCollateral(u'融资融券业务.xlsx',u'担保品买入限价_深圳','XjSzDBPMR')
    # test_CaseServiceCollateral(u'融资融券业务.xlsx',u'担保品买入市价_深圳','SjSzDBPMR')
    # test_CaseServiceCollateral(u'融资融券业务.xlsx',u'担保品买入限价_上海','XjShDBPMR')
    # test_CaseServiceCollateral(u'融资融券业务.xlsx',u'担保品买入市价_上海','SjShDBPMR')
    # test_CaseServiceCollateral(u'融资融券业务.xlsx',u'担保品卖出限价_上海','XjShDBPMC')
    # test_CaseServiceCollateral(u'融资融券业务.xlsx',u'担保品卖出限价_深圳','XjSzDBPMC')
    # test_CaseServiceCollateral(u'融资融券业务.xlsx',u'担保品卖出市价_深圳','SjSzDBPMC')
    # test_CaseServiceCollateral(u'融资融券业务.xlsx',u'担保品卖出市价_上海','SjShDBPMC')
    # test_CaseServiceFinancing(u'融资融券业务.xlsx',u'融资买入限价_深圳','XjSzRZMR')
    # test_CaseServiceFinancing(u'融资融券业务.xlsx',u'融资买入市价_深圳','SjSzRZMR')
    # test_CaseServiceFinancing(u'融资融券业务.xlsx',u'融资买入限价_上海','XjShRZMR')
    # test_CaseServiceFinancing(u'融资融券业务.xlsx',u'融资买入市价_上海','SjShRZMR')
    # test_CaseServiceShortSelling(u'融资融券业务.xlsx',u'融券卖出限价_上海','XjShRQMC')
    # test_CaseServiceShortSelling(u'融资融券业务.xlsx',u'融券卖出限价_深圳','XjSzRQMC')
    # test_CaseServiceSaleVoucher(u'融资融券业务.xlsx',u'卖券还款限价_上海','XjShMQHK')
    # test_CaseServiceSaleVoucher(u'融资融券业务.xlsx',u'卖券还款市价_上海','SjShMQHK')
    # test_CaseServiceSaleVoucher(u'融资融券业务.xlsx',u'卖券还款限价_深圳','XjSzMQHK')
    # test_CaseServiceSaleVoucher(u'融资融券业务.xlsx',u'卖券还款市价_深圳','SjSzMQHK')
    # test_CaseServiceBuyVoucher(u'融资融券业务.xlsx',u'买券还券限价_上海','XjShMQHQ')
    # test_CaseServiceBuyVoucher(u'融资融券业务.xlsx',u'买券还券市价_上海','SjShMQHQ')
    # test_CaseServiceBuyVoucher(u'融资融券业务.xlsx',u'买券还券限价_深圳','XjSzMQHQ')
    # test_CaseServiceBuyVoucher(u'融资融券业务.xlsx',u'买券还券市价_深圳','SjSzMQHQ')

def testcase_medium():
    test_CaseService(u'mediumm.xlsx',u'深圳限价','MEDIUM')
    test_CaseService(u'mediumm.xlsx',u'深圳市价','MEDIUM')
    test_CaseService(u'mediumm.xlsx',u'深圳市价_验资','MEDIUM')
    test_CaseService(u'mediumm.xlsx',u'深圳限价_验资','MEDIUM')

def testcase_gem():
    test_CaseService(u'gem.xlsx',u'深圳限价','GEM')
    test_CaseService(u'gem.xlsx',u'深圳市价','GEM')
    test_CaseService(u'gem.xlsx',u'深圳市价_验资','GEM')
    test_CaseService(u'gem.xlsx',u'深圳限价_验资','GEM')

def testcase_gem_register():
    #test_CaseServiceIpo(u'gem_register.xlsx',u'新股申购_深圳','GEM_REGISTER_IPO')
    test_CaseService(u'gem_register.xlsx',u'深圳限价','GEM_REGISTER')
    test_CaseService(u'gem_register.xlsx',u'深圳市价','GEM_REGISTER')
    test_CaseService(u'gem_register.xlsx',u'深圳市价_验资','GEM_REGISTER')
    test_CaseService(u'gem_register.xlsx',u'深圳限价_验资','GEM_REGISTER')

def testcase_fxjsmm():
    #test_CaseService(u'fxjsmm.xlsx',u'深圳限价','FXJSMM')
    #test_CaseService(u'fxjsmm.xlsx',u'深圳限价_验资','FXJSMM')
    #test_CaseService(u'fxjsmm.xlsx',u'上海限价','FXJSMM')
    test_CaseService(u'fxjsmm.xlsx',u'上海限价_验资','FXJSMM')
def testcase_tszlmm():
    test_CaseService(u'tszlmm.xlsx',u'深圳限价','TSZLMM')
    test_CaseService(u'tszlmm.xlsx',u'上海限价','TSZLMM')
    test_CaseService(u'tszlmm.xlsx',u'深圳限价_验资','TSZLMM')
    test_CaseService(u'tszlmm.xlsx',u'上海限价_验资','TSZLMM')


#生成市价单权限测试用例
def testcase_SJQX():
    test_CaseServiceAllotmentPayment(u'sj_qx.xlsx',u'CYBGGPGQX','CYBGGPGQX')
    #test_CaseServiceIpo(u'sj_qx.xlsx',u'CYBGGXGSGQX','CYBGGXGSGQX')
    #test_CaseService(u'sj_qx.xlsx',u'CYBGGQX','CYBGGQX')
    #test_CaseService(u'sj_qx.xlsx',u'SJQX','SJQX')
    #test_CaseService(u'sj_qx.xlsx',u'FXJSQX','FXJSQX')
    #test_CaseService(u'sj_qx.xlsx',u'TSZLQX','TSZLQX')
    #test_CaseService(u'sj_qx.xlsx',u'CYBQX','CYBQX')
    #test_CaseService(u'sj_qx.xlsx',u'KCBQX','KCBQX')
    #test_CaseService(u'sj_qx.xlsx',u'KCBQX','KSCETFQX')
    #test_CaseServiceKCB(u'sj_qx.xlsx',u'KCBXGSGQX','KCBXGSGQX')
    #test_CaseServiceKCB(u'sj_qx.xlsx',u'KCBPGJKQX','KCBPGJKQX')

def testcase_DBPMR_Ychf():
    test_CaseServiceRzrqYchf(u'YchfDbpmr.xlsx',u'OMS','YchfOmsDbpmr')
    print"over"
def testcase_quote():
    # test_CaseServiceQuote(u'行情自动化用例.xlsx', 'quote16', 'Quote16')
    test_CaseServiceQuote(u'行情自动化用例.xlsx', 'quote18', 'Quote18')

#生成分级基金申赎用例、分级基金拆分合并用例
def testcase_structured_Fund():
    excel_file = u'structured_fund_creation_redemption.xlsx'
    CaseService0 = CaseServiceStructuredFundCreation.CaseService(excel_file)
    CaseService0.gen_all_casepy()
    CaseService0 = CaseServiceSplitMerge.CaseService(excel_file)
    CaseService0.gen_all_casepy()

#将深圳手写的脚本拷贝到Autocase_Result目录
def copy_case_SZ():
    pass

#生成所有测试用例
def testcase_all():
    testcase_SZ()
    testcase_SH()


#生成货币基金买卖用例
def test_CaseServiceMoneyFund(excel_file,sheet_name,casepath):
    CaseService0 = CaseServiceMoneyFund.CaseService(excel_file,sheet_name)
    CaseService0.gen_all_casepy(casepath)


#生成担保品买卖用例
def test_CaseServiceCollateral(excel_file,sheet_name,casepath):
    CaseService0 = CaseServiceCollateral.CaseService(excel_file,sheet_name)
    CaseService0.gen_all_casepy(casepath)

#融资买入用例
def test_CaseServiceFinancing(excel_file,sheet_name,casepath):
    CaseService0 = CaseServiceFinancing.CaseService(excel_file,sheet_name)
    CaseService0.gen_all_casepy(casepath)

#融券卖出用例
def test_CaseServiceShortSelling(excel_file,sheet_name,casepath):
    CaseService0 = CaseServiceShortSelling.CaseService(excel_file,sheet_name)
    CaseService0.gen_all_casepy(casepath)

#卖券还款用例
def test_CaseServiceSaleVoucher(excel_file,sheet_name,casepath):
    CaseService0 = CaseServiceSaleVoucher.CaseService(excel_file,sheet_name)
    CaseService0.gen_all_casepy(casepath)

#买券还券用例
def test_CaseServiceBuyVoucher(excel_file,sheet_name,casepath):
    CaseService0 = CaseServiceBuyVoucher.CaseService(excel_file,sheet_name)
    CaseService0.gen_all_casepy(casepath)

#生成货币基金买卖自动化用例
def test_CaseService(excel_file,sheet_name,casepath):
    CaseService0 = CaseService.CaseService(excel_file,sheet_name)
    CaseService0.gen_all_casepy(casepath)

def test_CaseServiceMultPbu(excel_file,sheet_name,casepath):
    CaseService0 = CaseServiceMultPbu.CaseService(excel_file,sheet_name)
    CaseService0.gen_all_casepy(casepath)

#生成新股申购自动化用例
def test_CaseServiceIpo(excel_file,sheet_name,casepath):
    CaseService1 = CaseServiceIpo.CaseService(excel_file,sheet_name)
    CaseService1.gen_all_casepy(casepath)

#生成配股缴款自动化用例
def test_CaseServiceAllotmentPayment(excel_file,sheet_name,casepath):
    CaseService2 = CaseServiceAllotmentPayment.CaseService(excel_file,sheet_name)
    CaseService2.gen_all_casepy(casepath)

def test_CaseServiceOption(excel_file,sheet_name,casepath):
    caseService = CaseServiceOption.CaseService(excel_file,sheet_name)
    caseService.gen_all_casepy(casepath)

def test_CaseServiceQuote(excel_file, sheet_name, casepath):
    caseService = CaseServiceQuote.CaseService(excel_file, sheet_name)
    caseService.gen_all_casepy(casepath)

#生成融资融券异常恢复自动化用例
def test_CaseServiceRzrqYchf(excel_file,sheet_name,casepath):
    print "test_CaseServiceRzrqYchf"
    CaseService2 = CaseServiceRzrqYchf.CaseService(excel_file,sheet_name)
    print (excel_file)
    print(sheet_name)
    CaseService2.gen_all_casepy(excel_file,casepath)
    print (casepath)

if __name__ == '__main__':
    # testcase_quote()
    #testcase_SH()
    # testcase_structured_Fund()
    # testcase_DBPMR_Ychf()
    # testcase_medium()
    testcase_gem()
    #testcase_gem_register()
    #testcase_fxjsmm()
    #testcase_tszlmm()
    #testcase_SJQX()
    #testcase_SZ_ADD()
    #testcase_SH_ADD()



