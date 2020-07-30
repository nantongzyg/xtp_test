#!/usr/bin/python
# -*- encoding: utf-8 -*-
import time
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from log import *
from ServiceConfig import *
from getTime import *
from CancelOrderErrorDataCheck import *
sys.path.append("/home/yhl2/workspace/xtp_test/ETF/etf_service")
from ETF_BdtsDataCheck import *
from ETF_CjhbDataCheck import *
from ETF_BdqueryDataCheck import *
from ETF_CaseEndCheck import *
sys.path.append("/home/yhl2/workspace/xtp_test/ETF/etf_mysql")
from QueryEtfComponentsCodeDB import QueryEtfCode1Code2DB
from QueryEtfQty import stkQty
from QueryPreclosePriceDB import QueryCompnentsPreclosePriceDB

# 定义下单前资金持仓全局变量－----------------
QueryInit = {
    '可用资金': 0,
    '买入资金': 0,
    '买入费用': 0,
    '卖出资金': 0,
    '卖出费用': 0,
    '预扣资金': 0,
    '总资产': 0,
    '证券资产': 0,
    '股票代码': None,
    '市场': None,
    '总持仓': 0,
    '可卖持仓': 0,
    '昨日持仓': 0,
    '今日可申购赎回持仓': 0,
    '持仓成本价': 0,
    '浮动盈亏': 0
    }

# 定义下单后的资金持仓全局变量----------------------
QueryEnd = {
    '可用资金': 0,
    '买入资金': 0,
    '买入费用': 0,
    '卖出资金': 0,
    '卖出费用': 0,
    '预扣资金': 0,
    '总资产': 0,
    '证券资产': 0,
    '股票代码': None,
    '市场': None,
    '总持仓': 0,
    '可卖持仓': 0,
    '昨日持仓': 0,
    '今日可申购赎回持仓': 0,
    '持仓成本价': 0,
    '浮动盈亏': 0
    }
# etf申购允许现金替代成分股所需金额
cash_substitute_amount = 0
# etf成分股昨天价
pre_close_prices = {}

# etf撤废前成分股持仓
component_stk_info_reject = {}

# 定义request_id
request_id=0
# 定义报单检查状态、用例测试结果、测试错误原因
result = {
    '用例检查状态':'init',
    '用例测试结果': False,
    '用例错误原因':'',
    '用例错误源': '',
    '报单检查状态':'init',
    '报单测试结果': False,
    '报单错误原因':'',
    '撤单检查状态':'init',
    '撤单测试结果': False,
    '撤单错误原因':'',
}

cdquery_rs=None


cjhb_rs= {
    '成交回报检查状态': 'init',
    'xtp_id': None,
    '市场': None,
    '股票代码': None,
    '买卖方向': None,
    '成交价格': None,
    '成交数量': 0,
    '成交金额': 0.00,
    '成交类型': None,
    '测试结果':0,
    '测试错误原因':None,
}

#初始化全局变量
def EtfParmIni(Api,expectStatus,price_type):
    logger.info('ParmIni初始化全局变量开始..')

    global request_id
    request_id +=1

    QueryInit['可用资金'] = 0
    QueryInit['买入资金'] = 0
    QueryInit['买入费用'] = 0
    QueryInit['卖出资金'] = 0
    QueryInit['卖出费用'] = 0
    QueryInit['预扣资金'] = 0
    QueryInit['总资产'] = 0
    QueryInit['证券资产'] = 0
    QueryInit['股票代码'] = None
    QueryInit['市场'] = None
    QueryInit['总持仓'] = 0
    QueryInit['可卖持仓'] = 0
    QueryInit['昨日持仓'] = 0
    QueryInit['今日可申购赎回持仓'] = 0
    QueryInit['持仓成本价'] = 0.000
    QueryInit['浮动盈亏'] = 0.00

    QueryEnd['可用资金'] = 0
    QueryEnd['买入资金'] = 0
    QueryEnd['买入费用'] = 0
    QueryEnd['卖出资金'] = 0
    QueryEnd['卖出费用'] = 0
    QueryEnd['预扣资金'] = 0
    QueryEnd['总资产'] = 0
    QueryEnd['证券资产'] = 0
    QueryEnd['股票代码'] = None
    QueryEnd['市场'] = None
    QueryEnd['总持仓'] = 0
    QueryEnd['可卖持仓'] = 0
    QueryEnd['昨日持仓'] = 0
    QueryEnd['今日可申购赎回持仓'] = 0
    QueryEnd['持仓成本价'] = 0.000
    QueryEnd['浮动盈亏'] = 0.00

    result['用例检查状态'] = 'init'
    result['用例错误源'] = ''
    result['用例测试结果'] = False
    result['用例错误原因'] = ''
    result['报单检查状态'] = 'init'
    result['报单测试结果'] = False
    result['报单错误原因'] = ''
    result['撤单错误原因'] = ''

    if expectStatus in('初始','未成交','全成','废单'):
        result['撤单检查状态'] = 'end'
        result['撤单测试结果'] = True
    else:
        result['撤单检查状态'] = 'init'
        result['撤单测试结果'] = False

    # 下单前初始化　bd_time（各个状态的报单时间）为空
    bdTimeInit()
    # 下单前初始化成交回报测试结果集
    cjhbDataInit()
    logger.info('ParmIni初始化全局变量完成')

def etfServiceTest(Api,case_goal,wt_reqs,*args):

    def on_QueryOrder(data,error,reqID,is_last):
        logger.info('报单查询回调开始，当前报单xtpID=' + str(data['order_xtp_id']) + ',报单状态=' + str(data['order_status']) + ',提交状态=' + str(data['order_submit_status']))
        bdQuecyCheck = bdqueryCheck(Api, case_goal, wt_reqs, data)
        logger.info('报单查询-报单状态/提交状态check结果:' + str(bdQuecyCheck['flag']) + ',' + str(bdQuecyCheck['检查状态']) + ',' + bdQuecyCheck['remark'])
        global bdquery_rs, cdquery_rs, cash_substitute_amount
        if bdQuecyCheck['flag'] and bdQuecyCheck['检查状态'] == 'end':
            if case_goal['是否是撤废'] == '是':
                component_stk_info_new = component_stk_info_reject
                if len(args) > 1:
                    component_stk_info_new = (component_stk_info_reject,args[1])
            else:
                component_stk_info_new = args

            rs = etf_BdqueryDataCheck(Api, wt_reqs, case_goal, data, error, QueryInit, QueryEnd, component_stk_info_new,cash_substitute_amount)
            if rs['报单类型'] == '报单':
                bdquery_rs = rs
                result['报单检查状态'] = rs['报单检查状态']
                result['报单测试结果'] = rs['测试结果']
                result['报单错误原因'] = rs['错误信息']
            elif rs['报单类型'] == '撤单':
                cdquery_rs = rs
                result['撤单检查状态'] = rs['报单检查状态']
                result['撤单测试结果'] = rs['测试结果']
                result['撤单错误原因'] = rs['错误信息']
                if case_goal['是否是撤废']=='是':
                    if rs['测试结果']:
                        result['用例测试结果'] = True
                        result['用例检查状态'] = 'end'

                    else:
                        result['用例测试结果'] = False
                        result['用例错误原因'] = rs['错误信息']
                        result['用例错误源'] = '撤废-报单查询'
                        result['用例检查状态'] = 'end'
            else:
                result['报单检查状态'] = 'end'
                result['报单测试结果'] = False
                result['报单错误原因'] = '报单类型无法识别'
                result['撤单检查状态'] = 'end'
                result['撤单测试结果'] = False
                result['撤单错误原因'] = '报单类型无法识别'
        elif bdQuecyCheck['检查状态'] == 'pending':
            case_goal['cancel_xtpID'] = bdQuecyCheck['cancel_xtpID']
            logger.warning('报单查询等待...,xtpID='+str(data['order_xtp_id']))
            if case_goal['期望状态'] in ('已报待撤','部撤已报'):
                time.sleep(0.1)
                queryByXtpID(Api, case_goal['xtp_ID'])
                queryByXtpID(Api, case_goal['cancel_xtpID'])
            bdquery_rs={
                '检查状态': 'pending'
            }
        elif bdQuecyCheck['检查状态'] == 'end' and bdQuecyCheck['flag'] == False:
            bdquery_rs = {
                '检查状态': 'end',
                '测试结果': False,
                '错误信息': bdQuecyCheck['remark']
            }
            result['报单检查状态'] = 'end'
            result['用例检查状态'] = 'end'
            result['用例测试结果'] = False
            result['用例错误原因'] = bdQuecyCheck['remark']
            result['用例错误源'] = '报单查询－状态检查'

    def on_order(data, error):
        global bdhb_rs
        bdCheck = etf_bdtsCheck(Api, case_goal, wt_reqs, data)
        logger.info('报单推送-报单状态/提交状态check结果:' + str(bdCheck['flag']) + ',' + bdCheck['remark'])
        if bdCheck['flag'] == True and bdCheck['status'] == 'end':
            bdhb_rs = etf_bdtsDataCheck(Api, wt_reqs, case_goal, data, error, QueryInit, QueryEnd)
        elif bdCheck['flag'] == False and bdCheck['status'] == 'end':
            bdhb_rs = {
                '报单检查状态': 'end',
                '测试结果': False,
                '错误信息': bdCheck['remark'],
            }
            result['用例检查状态'] = 'end'
            result['用例测试结果'] = False
            result['用例错误原因'] = bdCheck['remark']
            result['用例错误源'] = '报单推送－状态检查'
        elif bdCheck['status']=='pending' and case_goal['是否是撤废']=='是':
            case_goal['cancel_xtpID']=bdCheck['cancel_xtpID']

    def on_trade(hb_data):
        logger.info('交易数据回报如下')
        dictLogging(hb_data)
        if case_goal['期望状态'] in ('全成', '未成交'):
            setQueryEnd(Api, wt_reqs) 
            # 收到成交回报后进行业务处理，返回值为为一个dict
            global cjhb_rs
            rs = etf_cjhbDataCheck(case_goal['期望状态'],
                                   Api,
                                   QueryInit,
                                   wt_reqs,
                                   case_goal['xtp_ID'],
                                   QueryEnd,
                                   hb_data,
                                   cash_substitute_amount,
                                   args,
                                   pre_close_prices
                                   )
            cjhb_rs['成交回报检查状态'] = rs['成交回报检查状态']
            cjhb_rs['xtp_id'] = rs['xtp_id']
            cjhb_rs['市场'] = rs['市场']
            cjhb_rs['股票代码'] = rs['股票代码']
            cjhb_rs['买卖方向'] = rs['买卖方向']
            cjhb_rs['成交价格'] = rs['成交价格']
            cjhb_rs['成交数量'] = rs['成交数量']
            cjhb_rs['成交金额'] = rs['成交金额']
            cjhb_rs['成交类型'] = rs['成交类型']
            cjhb_rs['测试结果'] = rs['测试结果']
            cjhb_rs['测试错误原因'] = rs['测试错误原因']
            if cjhb_rs['股票代码'] in ('580241','580242'):
                print '-------------------------'
                print cjhb_rs['股票代码']
        else:
            logger.info('成交回报检查：用例期望状态非【全成】,不做成交回报数据业务检查！')
            cjhb_rs = {
                '成交回报检查状态': 'end',
                '测试结果': True,
            }

        # 'trade_type': 2，一级市场成交回报，保证成交回报都返回后，再作报单查询
        if hb_data['trade_type'] == '2' and case_goal['期望状态'] == '未成交':
            queryByXtpID(Api, case_goal['xtp_ID'])

    def on_cancelorder_error(cancel_info, error_info):
        logger.info('当前为撤废异步回调函数..start')
        time.sleep(0.2)
        if case_goal['是否是撤废'] == '是':
            if cancel_info['order_xtp_id'] != case_goal['xtp_ID']:
                logger.error('错误，当前API返回撤废的原xtpID与当前用例的xtpID不一致，当前API返回的xtpID和此用例的xtpID分别是' + str(
                    cancel_info['order_xtp_id']) + ',' + str(case_goal['xtp_ID']))
                result['用例检查状态'] = 'end'
                result['用例错误源'] = '撤单'
                result['用例测试结果'] = False
                result['用例错误原因'] = '当前API返回撤废的原xtpID与当前用例的xtpID不一致'
            elif cancel_info['order_cancel_xtp_id'] != case_goal['cancel_xtpID']:
                result['用例检查状态'] = 'end'
                result['用例错误源'] = '撤单'
                result['用例测试结果'] = False
                result['用例错误原因'] = '当前API返回撤废的xtpID与当前用例的撤废xtpID不一致'
            else:
                rs = cancelOrderErrorDataCheck(case_goal, error_info)

                if rs['检查状态'] == 'end' and rs['测试结果'] == True:
                    # 报单查询（撤废）
                    queryByXtpID(Api, case_goal['cancel_xtpID'])
                else:
                    result['用例检查状态'] = 'end'
                    result['用例测试结果'] = False
                    result['用例错误原因'] = rs['错误原因']
                    result['用例错误源'] = rs['撤废']

        else:
            logger.error('错误，当前撤单为撤废与期望状态不符合，期望状态为' + case_goal['期望状态'])
            result['用例检查状态'] = 'end'
            result['用例错误源'] = '撤单'
            result['用例测试结果'] = False
            result['用例错误原因'] = '当前撤单为撤废与期望状态不符合'


    Api.trade.setQueryOrderHandle(on_QueryOrder)
    Api.trade.setTradeEventHandle(on_trade)
    Api.trade.setOrderEventHandle(on_order)
    Api.trade.setCancelOrderErrorHandle(on_cancelorder_error)

    '''
    ------------------------------------------------------------------------------------------------------------------
    查询初始资金和持仓，当期望状态是'初始','未成交','部成','全成','已撤','废单'时，在下单前查询
    ------------------------------------------------------------------------------------------------------------------
    '''
    if case_goal['期望状态'] in ('初始', '未成交', '全成', '废单','内部撤单'):
        setQueryInit(Api, wt_reqs)

    # 查询etf一级市场代码
    if case_goal['期望状态'] in ('全成', '未成交'):
        etf_code1_code2 = QueryEtfCode1Code2DB(wt_reqs['ticker'])
        if etf_code1_code2 != {}:
            # 计算允许现金替代金额
            global cash_substitute_amount
            cash_substitute_amount = etf_get_cash_subtitute_amount(
                Api,
                wt_reqs['market'],
                etf_code1_code2['etf_code1'],
                wt_reqs['quantity'] / stkQty['最小申赎单位'])

        global pre_close_prices
        pre_close_prices = QueryCompnentsPreclosePriceDB(wt_reqs['ticker'])
    #下单
    # 如果期望状态为　内部撤单，则需要在休市时下单
    # if case_goal['期望状态'] == '内部撤单':
    # waitCloseTime()
    # case_goal['xtp_ID'] = Api.trade.InsertOrder(wt_reqs)
    case_goal['xtp_ID'] = Api.trade.InsertOrder(wt_reqs)

    insertOrderTime = getTimestampInt()
    logger.info('下单的xtpID=' + str(case_goal['xtp_ID']))

    if case_goal['xtp_ID']==0:
        if case_goal['期望状态']=='废单':
            msg=Api.trade.GetApiLastError()
            dictLogging(msg)
            if case_goal['errorID'] == msg['error_id']:
                logger.info('废单校验正确！')
                result['用例检查状态'] = 'end'
                result['用例测试结果'] = True

            else:
                logger.error('期望的errorID和实际errorID不一致，'+'期望errorID＝'+str(case_goal['errorID'])+'，实际errorID＝'+str(msg['error_id']))
                result['用例检查状态'] = 'end'
                result['用例测试结果'] = False
                result['用例错误原因'] = '期望的errorID和实际errorID不一致'
        else:
            logger.error('下单的xtpID为0')
            result['用例检查状态'] = 'end'
            result['用例测试结果'] = False
            result['用例错误原因'] = '下单的xtpID为0'

    # --如果期望状态是‘初始’,1.赋值queryEnd 2.进行报单查询
    if case_goal['期望状态'] in ('初始', '内部撤单'):
        queryByXtpID(Api, case_goal['xtp_ID'])

    # ------------------------------------------------------------------------------------------------------------------
    # 当报单检查状态非‘end’时，一直休0.5秒,等待报单检查结束
    # ------------------------------------------------------------------------------------------------------------------
    # 获取超时时间
    t = getTimePending(case_goal['期望状态'])

    # 定义caseEndCheck是否已执行
    endCheckFlag = False
    while getTimestampInt() <= insertOrderTime + t:
        if result['用例检查状态'] == 'end':
            break
        else:
            time.sleep(0.5)
            if result['报单检查状态'] == 'end' and result['撤单检查状态'] == 'end' and endCheckFlag == False:
                if case_goal['期望状态'] == '初始':
                    rs = etf_caseEndCheck(Api, None, bdquery_rs, None, None,
                                          case_goal['期望状态'], wt_reqs['price_type'])
                else:
                    rs = etf_caseEndCheck(Api, bdhb_rs, bdquery_rs, cdquery_rs, cjhb_rs,
                                          case_goal['期望状态'], wt_reqs['price_type'])
                result['用例检查状态'] = 'end'
                result['用例测试结果'] = rs['测试结果']
                result['用例错误原因'] = rs['错误原因']
                result['用例错误源'] = rs['错误源']
                endCheckFlag = True

    # 超出设置的“超时”时间后
    if result['用例检查状态'] == 'init':
        result['用例测试结果'] = False
        result['用例错误原因'] = '用例超时'

    return result

# ----------------------------------------------------------------------------------------------------------------------
# 定义函数：报单推送外层检查，注：根据报单推送的类型和期望状态进行撤单　和　赋值查询
# ----------------------------------------------------------------------------------------------------------------------
def etf_bdtsCheck(Api,case_goal,wt_reqs,data):
    bdCheck={
        'status':'init',
        'flag':False,
        'remark':'',
        'cancel_xtpID':0,
    }
    global component_stk_info_reject
    # 当报单是‘未成交’时，报单已接受，进行报单查询
    if data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_NOTRADEQUEUEING'] and data[
        'order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
        if case_goal['期望状态'] in ('全成','内部撤单'):
            logger.info('当前报单推送状态为未成交，等待..')
            bdCheck['status']='pending'
        else:
            time.sleep(0.1)
            bdCheck['status'] = 'end'
            bdCheck['flag'] = True

    # 当报单是‘全部成交’时，报单已接受，进行１.报单业务处理 2.报单查询业务处理
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_ALLTRADED'] and data[
        'order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
        if case_goal['期望状态'] == '全成' and case_goal['是否是撤废']=='是':
            setQueryInit(Api, wt_reqs)
            bdCheck['cancel_xtpID'] = Api.trade.CancelOrder(case_goal['xtp_ID'])
            # -----------查询ETF申购前成分股持仓-------------
            component_stk_info_reject = etf_get_all_component_stk(wt_reqs['ticker'])
            bdCheck['status']='pending'
            logger.info('报单推送penging')

        else:
            queryByXtpID(Api, case_goal['xtp_ID'])
            bdCheck['status'] = 'end'
            bdCheck['flag'] = True

    # 当报单是‘已撤’时，报单已接受，进行１.赋值queryEnd　２.报单业务处理 ３.原单和撤单都进行报单查询业务处理
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_CANCELED'] and \
       data['order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
        if case_goal['期望状态'] == '已撤' and case_goal['是否是撤废'] == '是':
            setQueryInit(Api, wt_reqs)
            # bdCheck['cancelErr_xtpID']=Api.trade.CancelOrder(case_goal['xtp_ID'])
            bdCheck['cancel_xtpID'] = Api.trade.CancelOrder(case_goal['xtp_ID'])
            bdCheck['status'] = 'pending'
        else:
            setQueryEnd(Api, wt_reqs)
            time.sleep(0.1)
            queryByXtpID(Api, case_goal['xtp_ID'])
            # 如果是手动撤单类型的话，需要根据撤单xtpID去查询撤单类型报单
            if getCancelType(Api, wt_reqs['price_type'], case_goal['期望状态']):
                queryByXtpID(Api, case_goal['cancel_xtpID'])
            bdCheck['status'] = 'end'
            bdCheck['flag'] = True

    # 当报单是‘废单’时，报单已拒绝，进行１.赋值queryEnd　２.报单业务处理 ３.报单查询业务处理
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_REJECTED'] and data[
        'order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_INSERT_REJECTED']:
        if case_goal['期望状态']=='废单' and case_goal['是否是撤废']=='是':
            setQueryInit(Api,wt_reqs)
            bdCheck['cancel_xtpID'] = Api.trade.CancelOrder(case_goal['xtp_ID'])
            # -----------查询ETF申购前成分股持仓-------------
            component_stk_info_reject = etf_get_all_component_stk(wt_reqs['ticker'])
            bdCheck['status']='pending'
        else:
            setQueryEnd(Api, wt_reqs)
            queryByXtpID(Api, case_goal['xtp_ID'])
            bdCheck['status'] = 'end'
            bdCheck['flag'] = True

    else:
        logger.error('当前报单推送状态无法识别，'+str(data['order_status'])+','+str(data['order_submit_status']))
        bdCheck['status'] = 'end'
        bdCheck['flag'] = False
        bdCheck['remark']='当前报单推送状态无法识别'

    return bdCheck

#-----------------------------------------------------------------------------------------------------------------------
#-定义函数：报单查询检查，此检查为外层的检查，主要检查查询回来的报单的状态是什么，然后根据状态进行不同的操作
#-----------------------------------------------------------------------------------------------------------------------
def bdqueryCheck(Api,case_goal,wt_reqs,data):

    bdQuecyCheck={
        '检查状态':'init',
        'flag':False,
        'cancel_xtpID':0,
        'remark':'',
    }

    # 当报单查询结果是‘初始’报单已提交
    if data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_INIT'] and data[
        'order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_INSERT_SUBMITTED']:
        # 期望状态是‘初始’，赋值queryEnd，检查报单查询数据
        if case_goal['期望状态'] == '初始':
            setQueryEnd(Api, wt_reqs)
            bdQuecyCheck['检查状态'] = 'end'
            bdQuecyCheck['flag'] = True
        elif case_goal['期望状态'] == '内部撤单':
            # 当撤单xtpID不为０时，说明已经做过撤单申请
            if case_goal['cancel_xtpID'] != 0:
                bdQuecyCheck['检查状态'] = 'end'
                bdQuecyCheck['flag'] = True
            # 当撤单xtpID为０时，说明尚未做过撤单申请
            else:
                # 休市时段内撤单
                bdQuecyCheck['cancel_xtpID'] = Api.trade.CancelOrder(case_goal['xtp_ID'])
                bdQuecyCheck['检查状态'] = 'pending'
        else:
            bdQuecyCheck['检查状态'] = 'end'
            bdQuecyCheck['flag'] = False
            bdQuecyCheck['remark'] = '期望状态与报单状态不匹配'

    # 当报单查询结果是‘未成交’，报单已接受
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_NOTRADEQUEUEING'] and data[
        'order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
        'XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
        # 当期望状态是‘未成交’时，赋值queryEnd，检查报单查询数据
        if case_goal['期望状态'] == '未成交' and case_goal['是否是撤废'] == '否':
            setQueryEnd(Api, wt_reqs)
            bdQuecyCheck['检查状态'] = 'end'
            bdQuecyCheck['flag'] = True
        # 当期望状态是‘已报待撤’，赋值queryInit，然后撤单，然后查询（撤单）报单(返回cancelXTPID后查询)
        elif case_goal['期望状态'] == '已报待撤':
            # 当撤单xtpID不为０时，说明已经做过撤单申请
            if case_goal['cancel_xtpID'] != 0:
                bdQuecyCheck['检查状态'] = 'end'
                bdQuecyCheck['flag'] = True
            # 当撤单xtpID为０时，说明尚未做过撤单申请
            else:
                setQueryInit(Api, wt_reqs)
                # 等待休市时间
                #waitCloseTime()
                time.sleep(0.1)
                # 休市时段内撤单
                bdQuecyCheck['cancel_xtpID'] = Api.trade.CancelOrder(case_goal['xtp_ID'])
                bdQuecyCheck['检查状态'] = 'pending'
        # 当期望状态是’已撤‘,'撤废-交易所撤废'，撤单
        elif case_goal['期望状态'] == '已撤':
            # setQueryInit(Api, wt_reqs)
            bdQuecyCheck['cancel_xtpID'] = Api.trade.CancelOrder(case_goal['xtp_ID'])
            bdQuecyCheck['检查状态'] = 'pending'
        # 当期望状态是’已撤‘,'撤废-交易所撤废'，撤单
        elif case_goal['期望状态'] == '未成交' and case_goal['是否是撤废'] == '是':
            setQueryInit(Api, wt_reqs)
            bdQuecyCheck['cancel_xtpID'] = Api.trade.CancelOrder(case_goal['xtp_ID'])
            bdQuecyCheck['检查状态'] = 'pending'
        # 当期望状态是
        elif case_goal['期望状态'] in ('全成', '内部撤单'):
            bdQuecyCheck['检查状态'] = 'pending'
        else:
            bdQuecyCheck['检查状态'] = 'end'
            bdQuecyCheck['flag'] = False
            bdQuecyCheck['remark'] = '期望状态与报单状态不匹配'

    # 当报单查询结果是‘初始’，撤单已提交
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_INIT'] and data['order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_CANCEL_SUBMITTED']:
        # 当期望状态是‘已报待撤’或‘部撤已报’，赋值queryEnd,检查报单查询数据
        if case_goal['期望状态'] in ('已报待撤'):
            setQueryEnd(Api, wt_reqs)
            time.sleep(0.1)
            bdQuecyCheck['检查状态'] = 'end'
            bdQuecyCheck['flag'] = True
        # 期望状态是'已撤','部撤','撤废'，等待
        elif case_goal['期望状态'] in ('已撤', '撤废'):
            bdQuecyCheck['检查状态'] = 'pending'
        # 其它，终止
        else:
            bdQuecyCheck['检查状态'] = 'end'
            bdQuecyCheck['flag'] = False
            bdQuecyCheck['remark'] = '期望状态与报单状态不匹配'
    #当报单查询结果是‘全成’，报单已接受
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_ALLTRADED'] and data[
        'order_submit_status'] ==Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
        #当期望状态是‘全成’时，检查报单查询数据
        if case_goal['期望状态'] in ('全成'):
            bdQuecyCheck['检查状态'] = 'end'
            bdQuecyCheck['flag'] = True
        else:
            bdQuecyCheck['检查状态'] = 'end'
            bdQuecyCheck['flag'] = False
            bdQuecyCheck['remark'] = '期望状态与报单状态不匹配'

    # 当报单查询结果是‘已撤’
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_CANCELED']:
        # 报单已接受
        if data['order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
            'XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
            if case_goal['期望状态'] in ('已撤', '内部撤单'):
                setQueryEnd(Api, wt_reqs)
                bdQuecyCheck['检查状态'] = 'end'
                bdQuecyCheck['flag'] = True
            else:
                bdQuecyCheck['检查状态'] = 'end'
                bdQuecyCheck['flag'] = False
                bdQuecyCheck['remark'] = '期望状态与报单状态不匹配'

        # 撤单已接受
        elif data['order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
            'XTP_ORDER_SUBMIT_STATUS_CANCEL_ACCEPTED']:
            bdQuecyCheck['检查状态'] = 'end'
            bdQuecyCheck['flag'] = True

    # 当报单查询结果是‘废单’，报单已拒绝
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_REJECTED'] and data[
        'order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_INSERT_REJECTED']:
        # 当期望状态是‘废单’，进行报单查询数据处理
        if case_goal['期望状态'] == '废单':
            setQueryEnd(Api, wt_reqs)
            bdQuecyCheck['检查状态'] = 'end'
            bdQuecyCheck['flag'] = True
        else:
            bdQuecyCheck['检查状态'] = 'end'
            bdQuecyCheck['flag'] = False
            bdQuecyCheck['remark'] = '期望状态与报单状态不匹配'


    # 当报单查询结果是‘撤废’,撤单已拒绝
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_REJECTED'] and data[
        'order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_CANCEL_REJECTED']:
        # 当期望状态是‘撤废’，先进行赋值queryEnd,然后报单查询数据处理
        if case_goal['是否是撤废'] == '是':
            setQueryEnd(Api, wt_reqs)
            bdQuecyCheck['检查状态'] = 'end'
            bdQuecyCheck['flag'] = True
        else:
            bdQuecyCheck['检查状态'] = 'end'
            bdQuecyCheck['flag'] = False
            bdQuecyCheck['remark'] = '期望状态与报单状态不匹配'

    return bdQuecyCheck

#-----------------------------------------------------------------------------------------------------------------------
#定义函数：通过xtpID查询报单
#-----------------------------------------------------------------------------------------------------------------------
def queryByXtpID(Api,xtpID):
    global request_id
    rs_QueryOrder = Api.trade.QueryOrderByXTPID(xtpID, request_id)
    request_id += 1
    # --如果返回的是非０，说明调用报单查询方法失败，需要调用GetApiLastError()获取错误代码
    if rs_QueryOrder != 0:
        logger.info('报单查询出错'+str(rs_QueryOrder))
        # 需要调用GetApiLastError()获取错误代码
        # GetApiLastError()
    else:
        logger.info('正在进行报单查询，xtpID='+str(xtpID))

# -----------------------------------------------------------------------------------------------------------------------
# 定义函数：赋值初始查询的资金和持仓
# -----------------------------------------------------------------------------------------------------------------------
def setQueryInit(Api, wt_reqs):
    # 资金查询及赋值QueryInit-------------------------------------
    fundasset0 = Api.trade.QueryAssetSync()
    if fundasset0['data'] == {}:
        logger.error('未查到资金持仓数据，请检查测试环境')
    elif fundasset0['data']['is_last']:
        QueryInit['可用资金'] = fundasset0['data']['buying_power']
        QueryInit['买入资金'] = fundasset0['data']['fund_buy_amount']
        QueryInit['买入费用'] = fundasset0['data']['fund_buy_fee']
        QueryInit['卖出资金'] = fundasset0['data']['fund_sell_amount']
        QueryInit['卖出费用'] = fundasset0['data']['fund_sell_fee']
        QueryInit['预扣资金'] = fundasset0['data']['withholding_amount']
        QueryInit['总资产'] = fundasset0['data']['total_asset']
        QueryInit['证券资产'] = fundasset0['data']['security_asset']
    else:
        logger.error("初始资金查询：查询的资金返回值非is_last")

    # 持仓查询及赋值QueryInit------------------------------------------
    stkcode = {
        'ticker': ''
    }
    stkasset0 = Api.trade.QueryPositionSync(stkcode)
    if wt_reqs['ticker'] in stkasset0['data']:
        QueryInit['股票代码'] = stkasset0['data'][wt_reqs['ticker']]['position']['ticker']
        QueryInit['市场'] = stkasset0['data'][wt_reqs['ticker']]['position']['market']
        QueryInit['总持仓'] = stkasset0['data'][wt_reqs['ticker']]['position']['total_qty']
        QueryInit['可卖持仓'] = stkasset0['data'][wt_reqs['ticker']]['position']['sellable_qty']
        QueryInit['昨日持仓'] = stkasset0['data'][wt_reqs['ticker']]['position']['yesterday_position']
        QueryInit['今日可申购赎回持仓'] = stkasset0['data'][wt_reqs['ticker']]['position']['purchase_redeemable_qty']
        QueryInit['持仓成本价'] = stkasset0['data'][wt_reqs['ticker']]['position']['avg_price']
        QueryInit['浮动盈亏'] = stkasset0['data'][wt_reqs['ticker']]['position']['unrealized_pnl']
    else:
        QueryInit['股票代码'] = wt_reqs['ticker']
        QueryInit['市场'] = wt_reqs['market']
        QueryInit['总持仓'] = 0
        QueryInit['可卖持仓'] = 0
        QueryInit['昨日持仓'] = 0
        QueryInit['可卖出证券数'] = 0
        QueryInit['持仓成本'] = 0
        QueryInit['浮动盈亏'] = 0
    logger.info('初始资金持仓为:')
    dictLogging(QueryInit)


# -----------------------------------------------------------------------------------------------------------------------
# 定义函数：赋值业务操作后查询的资金和持仓
# -----------------------------------------------------------------------------------------------------------------------
def setQueryEnd(Api, wt_reqs):
    time.sleep(0.5)
    # 查询资金-------------------------------------
    fundasset9 = Api.trade.QueryAssetSync()
    if fundasset9['data'] == {}:
        logger.error('未查到资金持仓数据，请检查测试环境')
    elif fundasset9['data']['is_last']:
        QueryEnd['可用资金'] = fundasset9['data']['buying_power']
        QueryEnd['买入资金'] = fundasset9['data']['fund_buy_amount']
        QueryEnd['买入费用'] = fundasset9['data']['fund_buy_fee']
        QueryEnd['卖出资金'] = fundasset9['data']['fund_sell_amount']
        QueryEnd['卖出费用'] = fundasset9['data']['fund_sell_fee']
        QueryEnd['预扣资金'] = fundasset9['data']['withholding_amount']
        QueryEnd['总资产'] = fundasset9['data']['total_asset']
        QueryEnd['证券资产'] = fundasset9['data']['security_asset']
    else:
        logger.error("收到成交回报资金查询：查询的资金返回值非is_last")

    # 收到成交回报后查询持仓-------------------------------------
    stkcode = {
        'ticker': ''
    }
    stkasset9 = Api.trade.QueryPositionSync(stkcode)
    if wt_reqs['ticker'] in stkasset9['data']:
        QueryEnd['股票代码'] = stkasset9['data'][wt_reqs['ticker']]['position']['ticker']
        QueryEnd['市场'] = stkasset9['data'][wt_reqs['ticker']]['position']['market']
        QueryEnd['总持仓'] = stkasset9['data'][wt_reqs['ticker']]['position']['total_qty']
        QueryEnd['可卖持仓'] = stkasset9['data'][wt_reqs['ticker']]['position']['sellable_qty']
        QueryEnd['昨日持仓'] = stkasset9['data'][wt_reqs['ticker']]['position']['yesterday_position']
        QueryEnd['今日可申购赎回持仓'] = stkasset9['data'][wt_reqs['ticker']]['position']['purchase_redeemable_qty']
        QueryEnd['持仓成本价'] = stkasset9['data'][wt_reqs['ticker']]['position']['avg_price']
        QueryEnd['浮动盈亏'] = stkasset9['data'][wt_reqs['ticker']]['position']['unrealized_pnl']
    else:
        QueryEnd['股票代码'] = wt_reqs['ticker']
        QueryEnd['市场'] = wt_reqs['market']
        QueryEnd['总持仓'] = 0
        QueryEnd['可卖持仓'] = 0
        QueryEnd['昨日持仓'] = 0
        QueryEnd['可卖出证券数'] = 0
        QueryEnd['持仓成本'] = 0
        QueryEnd['浮动盈亏'] = 0
    logger.info('最终资金持仓为:')
    dictLogging(QueryEnd)

#-----------------------------------------------------------------------------------------------------------------------
# 定义函数：根据期望状态返回超时时间（来源：serviceconfig）
#-----------------------------------------------------------------------------------------------------------------------
def getTimePending(expectStatus):
    #默认
    time=ServiceConfig.TIMEPENDING['DEFAULT']
    #各状态
    if expectStatus in ('全成', '未成交', '初始', '内部撤单', '废单'):
        time = ServiceConfig.TIMEPENDING['CREATION']

    return time

#-----------------------------------------------------------------------------------------------------------------------
# 定义函数：等待到休市时间＋１秒，返回值为True
#-----------------------------------------------------------------------------------------------------------------------
def waitCloseTime():
    # 获取当前系统时间的秒数
    if is_exchange_clese==False:
        second = getTimeSecondInt()
        logger.info('等待休市' + str(second))
        # 如果在开市时间(+延时)内，一直等待１秒循环
        while open_time[0][0] <= second <= open_time[0][1] + time_delay or open_time[1][0] <= second <= open_time[1][
            1] + time_delay or open_time[2][0] <= second <= open_time[2][1] + time_delay:
            time.sleep(1)
            second = getTimeSecondInt()
        # 如果在休市时间内返回True
        if close_time[0][0] <= second <= close_time[0][1] or close_time[1][0] <= second <= close_time[1][1] or close_time[2][0] <= second <= close_time[2][1]:
            return True
    else:
        return True

