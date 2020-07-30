#!/usr/bin/python
# -*- encoding: utf-8 -*-

#import CaseServiceRisk
import CaseService
#import CaseServiceMoneyFund
#import CaseServiceCollateral
#import CaseServiceFinancing
#import CaseServiceShortSelling
#import CaseServiceSaleVoucher
#import CaseServiceBuyVoucher
#import CaseServiceStructuredFundCreation
#import CaseServiceAllotmentPayment
#import CaseServiceSplitMerge
#import CaseServiceIpo
#import CaseServiceOption
import CaseServiceRzrqYchf
import CaseServiceKCB
#import CaseServiceQpqcYchf
# import CaseServiceQuote
# import CaseServiceMultPbu
import os.path

#生成深圳市场测试用例
def testcase_SZ():
    test_CaseService(u'普通业务自动化用例.xlsx',u'深圳限价','GPMM')
    test_CaseService(u'普通业务自动化用例.xlsx',u'深圳市价','GPMM')
    test_CaseService(u'ETF买卖.xlsx',u'深圳限价单市场','ETFMM_D')
    test_CaseService(u'ETF买卖.xlsx',u'深圳市价单市场','ETFMM_D')
    test_CaseService(u'ETF买卖.xlsx',u'深圳限价跨市场','ETFMM_K')
    test_CaseService(u'ETF买卖.xlsx',u'深圳市价跨市场','ETFMM_K')
    test_CaseService(u'普通业务自动化用例.xlsx',u'分级子基金深圳限价','FJZJJMM')
    test_CaseService(u'普通业务自动化用例.xlsx',u'分级子基金深圳市价','FJZJJMM')
    test_CaseService(u'普通业务自动化用例.xlsx', u'逆回购_深圳','ReverseRepo')
    test_CaseServiceIpo(u'普通业务自动化用例.xlsx',u'新股申购_深圳','IPO')
    test_CaseServiceAllotmentPayment(u'普通业务自动化用例.xlsx',u'配股缴款_深圳','AllotmentPayment')
    # test_CaseServiceMultPbu(u'普通业务自动化用例.xlsx', u'深圳限价', 'GPMM_MULT_PBU')

#生成上海市场测试用用例
def testcase_SH():
    # test_CaseService(u'普通业务自动化用例.xlsx',u'上海限价','GPMM')
    # test_CaseService(u'普通业务自动化用例.xlsx',u'上海市价','GPMM')
    # test_CaseService(u'ETF买卖.xlsx',u'上海限价单市场','ETFMM_D')
    # test_CaseService(u'ETF买卖.xlsx',u'上海市价单市场','ETFMM_D')
    # test_CaseService(u'ETF买卖.xlsx',u'上海限价跨市场','ETFMM_K')
    # test_CaseService(u'ETF买卖.xlsx',u'上海市价跨市场','ETFMM_K')
    # test_CaseService(u'普通业务自动化用例.xlsx',u'逆回购_上海','ReverseRepo')
    # test_CaseServiceIpo(u'普通业务自动化用例.xlsx',u'新股申购_上海','IPO')
    # test_CaseServiceAllotmentPayment(u'普通业务自动化用例.xlsx',u'配股缴款_上海','AllotmentPayment')
    # test_CaseServiceOption(u'个股期权自动化用例.xlsx', u'权利方限价_沪市', 'XjShRightSide')
    # test_CaseServiceOption(u'个股期权自动化用例.xlsx', u'权利方市价_沪市', 'SjShRightSide')
    # test_CaseServiceOption(u'个股期权自动化用例.xlsx', u'义务方限价（认购合约）_沪市', 'XjShObligationCall')
    # test_CaseServiceOption(u'个股期权自动化用例.xlsx', u'义务方市价（认购合约）_沪市', 'SjShObligationCall')
    # test_CaseServiceOption(u'个股期权自动化用例.xlsx', u'义务方限价（认沽合约）_沪市', 'XjShObligationPut')
    # test_CaseServiceOption(u'个股期权自动化用例.xlsx', u'义务方市价（认沽合约）_沪市', 'SjShObligationPut')
    # test_CaseServiceOption(u'个股期权自动化用例.xlsx', u'行权', 'Exercise')
    # test_CaseServiceMoneyFund(u'普通业务自动化用例.xlsx',u'交易型货币基金买卖上海限价','XjShHBJJMM')
    # test_CaseServiceMoneyFund(u'普通业务自动化用例.xlsx',u'交易型货币基金买卖上海市价','SjShHBJJMM')
    test_CaseServiceCollateral(u'融资融券业务.xlsx',u'担保品买入限价_深圳','XjSzDBPMR')
    test_CaseServiceCollateral(u'融资融券业务.xlsx',u'担保品买入市价_深圳','SjSzDBPMR')
    test_CaseServiceCollateral(u'融资融券业务.xlsx',u'担保品买入限价_上海','XjShDBPMR')
    test_CaseServiceCollateral(u'融资融券业务.xlsx',u'担保品买入市价_上海','SjShDBPMR')
    test_CaseServiceCollateral(u'融资融券业务.xlsx',u'担保品卖出限价_上海','XjShDBPMC')
    test_CaseServiceCollateral(u'融资融券业务.xlsx',u'担保品卖出限价_深圳','XjSzDBPMC')
    test_CaseServiceCollateral(u'融资融券业务.xlsx',u'担保品卖出市价_深圳','SjSzDBPMC')
    test_CaseServiceCollateral(u'融资融券业务.xlsx',u'担保品卖出市价_上海','SjShDBPMC')
    test_CaseServiceFinancing(u'融资融券业务.xlsx',u'融资买入限价_深圳','XjSzRZMR')
    test_CaseServiceFinancing(u'融资融券业务.xlsx',u'融资买入市价_深圳','SjSzRZMR')
    test_CaseServiceFinancing(u'融资融券业务.xlsx',u'融资买入限价_上海','XjShRZMR')
    test_CaseServiceFinancing(u'融资融券业务.xlsx',u'融资买入市价_上海','SjShRZMR')
    test_CaseServiceShortSelling(u'融资融券业务.xlsx',u'融券卖出限价_上海','XjShRQMC')
    test_CaseServiceShortSelling(u'融资融券业务.xlsx',u'融券卖出限价_深圳','XjSzRQMC')
    test_CaseServiceSaleVoucher(u'融资融券业务.xlsx',u'卖券还款限价_上海','XjShMQHK')
    test_CaseServiceSaleVoucher(u'融资融券业务.xlsx',u'卖券还款市价_上海','SjShMQHK')
    test_CaseServiceSaleVoucher(u'融资融券业务.xlsx',u'卖券还款限价_深圳','XjSzMQHK')
    test_CaseServiceSaleVoucher(u'融资融券业务.xlsx',u'卖券还款市价_深圳','SjSzMQHK')
    test_CaseServiceBuyVoucher(u'融资融券业务.xlsx',u'买券还券限价_上海','XjShMQHQ')
    test_CaseServiceBuyVoucher(u'融资融券业务.xlsx',u'买券还券市价_上海','SjShMQHQ')
    test_CaseServiceBuyVoucher(u'融资融券业务.xlsx',u'买券还券限价_深圳','XjSzMQHQ')
    test_CaseServiceBuyVoucher(u'融资融券业务.xlsx',u'买券还券市价_深圳','SjSzMQHQ')

def testcase_DBPMR_Ychf():
    #test_CaseServiceRzrqYchf(u'YchfRqmc.xlsx',u'OMS','YchfOmsRqmc')
    #test_CaseServiceRzrqYchf(u'YchfRqmc.xlsx',u'Oms','Oms')
    #test_CaseServiceRzrqYchf(u'YchfRqmc.xlsx',u'Shbp','Shbp')
    #test_CaseServiceRzrqYchf(u'YchfRqmc.xlsx',u'Szbp','Szbp')
    #test_CaseServiceRzrqYchf(u'YchrfRzmr.xlsx',u'Oms','Oms')
    filenames=['YchfDbpmr','YchfDbpmc','YchfDbpzc','YchfDbpzr',
               'YchfRqmc','YchfRzmr','YchfYqhz',
               'YchfXqhq','YchfMqhq','YchfMqhk']      #'YchfRqmc','YchfRzmr',YchfRqmc
    '''
    
    '''
    sheetnames=['Oms','Szbp','Shbp','OmsShOffer','OmsSzOffer'] #,'OmsShOffer','OmsSzOffer'
    for file in filenames:
        for sheet in sheetnames:
            test_CaseServiceRzrqYchf(file+'.xlsx', sheet, sheet)
   #test_CaseServiceRzrqYchf(u'YchfYqhz.xlsx', u'Oms', 'Oms')
   #test_CaseServiceRzrqYchf(u'YchfYqhz.xlsx',u'Szbp','Szbp')
   #test_CaseServiceRzrqYchf(u'YchfYqhz.xlsx',u'Shbp','Shbp')
   #test_CaseServiceRzrqYchf(u'YchfYqhz.xlsx', u'OmsShOffer', 'OmsShOffer')
   #test_CaseServiceRzrqYchf(u'YchfYqhz.xlsx', u'OmsSzOffer', 'OmsSzOffer')
    #test_CaseServiceRzrqYchf(u'YchfYqhz.xlsx',u'Oms','Oms')
    #test_CaseServiceRzrqYchf(u'YchfYqhz.xlsx',u'Shbp','Shbp')
    #test_CaseServiceRzrqYchf(u'YchfYqhz.xlsx',u'Szbp','Szbp')
    #test_CaseServiceRzrqYchf(u'YchfYqhz.xlsx',u'OmsSzOffer','OmsSzOffer')
    #test_CaseServiceRzrqYchf(u'YchfYqhz.xlsx',u'Oms','Oms')
    #test_CaseServiceRzrqYchf(u'YchfRqmc.xlsx',u'Oms','Oms')
    print 'over!'

def testcase_KCB():
    #test_CaseServiceKCB(u'1_KCB_HASPRICELIMIT.xlsx',u'XTP_PRICE_BEST5_OR_LIMIT','Kcb') 
    #test_CaseServiceKCB(u'1_KCB_HASPRICELIMIT.xlsx',u'XTP_PRICE_BEST5_OR_CANCEL','Kcb')

    #test_CaseServiceKCB(u'2_KCB_HASNOPRICELIMIT.xlsx',u'XTP_PRICE_BEST5_OR_LIMIT','Kcb')
    #test_CaseServiceKCB(u'2_KCB_HASNOPRICELIMIT.xlsx',u'XTP_PRICE_BEST5_OR_CANCEL','Kcb')

    #test_CaseServiceKCB(u'5_KCB_XGSG.xlsx', u'KCB_XGSG', 'Kcb')
    #
    #test_CaseServiceKCB(u'6_KCB_ALLOTMENT.xlsx',u'KCB_ALLOTMENT', 'Kcb')

    #test_CaseServiceKCB(u'10_KCB_YCHF.xlsx', u'OMS', 'Kcb')
    #test_CaseServiceKCB(u'10_KCB_YCHF.xlsx', u'SHOffer', 'Kcb')
    #test_CaseServiceKCB(u'10_KCB_YCHF.xlsx', u'OMS_SHOffer', 'Kcb')


    test_CaseServiceKCB(u'KCB_YCHF_XGSG.xlsx', u'OMS', 'Kcb')
    #test_CaseServiceKCB(u'KCB_YCHF_XGSG.xlsx', u'SHOffer', 'Kcb')
    #test_CaseServiceKCB(u'KCB_YCHF_XGSG.xlsx', u'OMS_SHOffer', 'Kcb')


    #test_CaseServiceKCB(u'KCB_YCHF_ALLOTMENT.xlsx', u'OMS', 'Kcb')
    #test_CaseServiceKCB(u'KCB_YCHF_ALLOTMENT.xlsx', u'SHOffer', 'Kcb')
    #test_CaseServiceKCB(u'KCB_YCHF_ALLOTMENT.xlsx', u'OMS_SHOffer', 'Kcb')



def testcase_Qpqc_Ychf():
    '''filepath,sheetname,casepath(folder)'''
    #test_CaseServiceQpqcYchf(u'YchfQpqc.xlsx',u'Shbp','Shbp')
    #test_CaseServiceQpqcYchf(u'YchfQpqc.xlsx',u'Szbp','Szbp')
    #test_CaseServiceQpqcYchf(u'YchfQpqc.xlsx', u'OmsShOffer', 'OmsShOffer')
    #test_CaseServiceQpqcYchf(u'YchfQpqc.xlsx', u'OmsSzOffer', 'OmsSzOffer')
    test_CaseServiceQpqcYchf(u'YchfQpqc.xlsx', u'Szbp', 'Szbp')
    print 'over!'

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

# 科创板
def test_CaseServiceKCB(excel_file,sheet_name,casepath):
    CaseService0 = CaseServiceKCB.CaseService(excel_file,sheet_name)
    CaseService0.gen_all_casepy(casepath, sheet_name, excel_file)

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
    print (excel_file)
    print(sheet_name)
    CaseService2 = CaseServiceRzrqYchf.CaseService(excel_file,sheet_name)
    CaseService2.gen_all_casepy(excel_file,casepath)

#生成融资融券异常恢复强平强撤自动化用例
def test_CaseServiceQpqcYchf(excel_file,sheet_name,casepath):
    print "test_CaseServiceQpqcYchf"
    caseService3 = CaseServiceQpqcYchf.CaseService(excel_file,sheet_name)
    caseService3.logger.warning("HAHAH"+excel_file)
    caseService3.logger.debug(sheet_name)
    caseService3.gen_all_casepy(excel_file,casepath)
    print (casepath)

if __name__ == '__main__':
    # testcase_quote()
    # testcase_SH()
    # testcase_structured_Fund()
    #testcase_DBPMR_Ychf()#异常恢复
    testcase_KCB()  #科创板


