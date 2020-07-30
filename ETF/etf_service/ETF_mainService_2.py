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
from CaseEndCheck import *
from BdqueryDataCheck import *
sys.path.append("/home/yhl2/workspace/xtp_test/ETF/etf_service")
from ETF_BdtsDataCheck import *

# 定义下单前资金持仓全局变量－----------------
QueryInit = {
    '可用资金': 0.00,
    '买入资金': 0.00,
    '买入费用': 0.00,
    '卖出资金': 0.00,
    '卖出费用': 0.00,
    'ETF申购占用资金':0.00,
    'ETF申购交易费用':0.00,
    'ETF赎回所得资金':0.00,
    'ETF赎回交易费用':0.00,
    '股票代码': None,
    '市场': None,
    '拥股数量': 0,
    '可卖出证券数':0,
    '可用于申购证券数':0,
    '可赎回证券数':0,
    '持仓成本': 0.000,
    '浮动盈亏': 0
    }

# 定义下单后的资金持仓全局变量----------------------
QueryEnd = {
    '可用资金': 0.00,
    '买入资金': 0.00,
    '买入费用': 0.00,
    '卖出资金': 0.00,
    '卖出费用': 0.00,
    'ETF申购占用资金':0.00,
    'ETF申购交易费用':0.00,
    'ETF赎回所得资金':0.00,
    'ETF赎回交易费用':0.00,
    '股票代码': None,
    '市场': None,
    '拥股数量': 0,
    '可卖出证券数':0,
    '可用于申购证券数':0,
    '可赎回证券数':0,
    '持仓成本': 0.000,
    '浮动盈亏': 0
    }

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

#初始化全局变量
def ParmIni(Api,expectStatus,price_type):
    logger.info('ParmIni初始化全局变量开始..')

    global request_id
    request_id +=1

    QueryInit['可用资金'] = 0.00,
    QueryInit['买入资金'] = 0.00,
    QueryInit['买入费用'] = 0.00,
    QueryInit['卖出资金'] = 0.00,
    QueryInit['卖出费用'] = 0.00,
    QueryInit['ETF申购占用资金'] = 0.00,
    QueryInit['ETF申购交易费用'] = 0.00,
    QueryInit['ETF赎回所得资金'] = 0.00,
    QueryInit['ETF赎回交易费用'] = 0.00,
    QueryInit['股票代码'] = None,
    QueryInit['市场'] = None,
    QueryInit['拥股数量'] = 0,
    QueryInit['可卖出证券数'] = 0,
    QueryInit['可用于申购证券数'] = 0,
    QueryInit['可赎回证券数'] = 0,
    QueryInit['持仓成本'] = 0.000,
    QueryInit['浮动盈亏'] = 0.00,

    QueryEnd['可用资金'] = 0.00,
    QueryEnd['买入资金'] = 0.00,
    QueryEnd['买入费用'] = 0.00,
    QueryEnd['卖出资金'] = 0.00,
    QueryEnd['卖出费用'] = 0.00,
    QueryEnd['ETF申购占用资金'] = 0.00,
    QueryEnd['ETF申购交易费用'] = 0.00,
    QueryEnd['ETF赎回所得资金'] = 0.00,
    QueryEnd['ETF赎回交易费用'] = 0.00,
    QueryEnd['股票代码'] = None,
    QueryEnd['市场'] = None,
    QueryEnd['拥股数量'] = 0,
    QueryEnd['可卖出证券数'] = 0,
    QueryEnd['可用于申购证券数'] = 0,
    QueryEnd['可赎回证券数'] = 0,
    QueryEnd['持仓成本'] = 0.000,
    QueryEnd['浮动盈亏'] = 0.00,

    result['用例检查状态'] = 'init'
    result['用例错误源'] = ''
    result['用例测试结果'] = False
    result['用例错误原因'] = ''
    result['报单检查状态'] = 'init'
    result['报单测试结果'] = False
    result['报单错误原因'] = ''
    result['撤单错误原因'] = ''
    #以下状态待确认
    result['撤单检查状态'] = 'init'
    result['撤单测试结果'] = False



def etf_serviceTest(Api,case_goal,wt_reqs):

    def on_QueryOrder(data,error,reqID,is_last):
        print '这里是on_QueryOrder'
        print data

    def on_order(data, error):
        print '这里是on_order'
        print data



    def on_trade(hb_data):
        print '这里是on_trade'
        print hb_data

    def on_cancelorder_error(cancel_info, error_info):
        print '这里是on_cancelorder_error'
        print cancel_info
        print error_info


    Api.trade.setQueryOrderHandle(on_QueryOrder)
    Api.trade.setTradeEventHandle(on_trade)
    Api.trade.setOrderEventHandle(on_order)
    Api.trade.setCancelOrderErrorHandle(on_cancelorder_error)

    # ------------------------------------------------------------------------------------------------------------------
    # 查询初始资金和持仓，当期望状态是'初始','未成交','部成','全成','已撤','废单'时，在下单前查询-----------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    if case_goal['期望状态'] in ('全成'):
        setQueryInit(Api, wt_reqs)

    #下单
    case_goal['xtp_ID'] = Api.trade.InsertOrder(wt_reqs)

    insertOrderTime = getTimeInt()
    logger.info('下单的xtpID=' + str(case_goal['xtp_ID']))

    if case_goal['xtp_ID']==0:
        logger.error('下单的xtpID为0')
        result['用例检查状态'] = 'end'
        result['用例测试结果'] = False
        result['用例错误原因'] = '下单的xtpID为0'

    # ------------------------------------------------------------------------------------------------------------------
    # 当报单检查状态非‘end’时，一直休0.5秒,等待报单检查结束
    # ------------------------------------------------------------------------------------------------------------------
    # 获取超时时间
    t = getTimePending(case_goal['期望状态'])
    # 定义caseEndCheck是否已执行
    endCheckFlag = False
    while getTimeInt() <= insertOrderTime + t:
        if result['用例检查状态'] == 'end':
            break
        else:
            time.sleep(0.5)
            if result['报单检查状态'] == 'end' and result['撤单检查状态'] == 'end' and endCheckFlag == False:
                if case_goal['期望状态'] == '初始':
                    rs = caseEndCheck(Api, None, bdquery_rs, None, None, case_goal['期望状态'], wt_reqs['price_type'])
                elif getCancelType(Api, wt_reqs['price_type'], case_goal['期望状态']) == False and case_goal[
                    '是否是撤废'] == '否':
                    rs = caseEndCheck(Api, bdhb_rs, bdquery_rs, None, cjhb_rs, case_goal['期望状态'],
                                      wt_reqs['price_type'])
                elif case_goal['是否是撤废'] == '否':
                    rs = caseEndCheck(Api, bdhb_rs, bdquery_rs, cdquery_rs, cjhb_rs, case_goal['期望状态'],
                                      wt_reqs['price_type'])
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
    # 当报单是‘未成交’时，报单已接受，进行报单查询
    if data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_NOTRADEQUEUEING'] and data[
        'order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
        # 当后续报单是主动推送过来的不用做报单查询：1.全成，２.部撤（既成剩撤，五档转撤）３.已撤（全成全撤，对手方最优）
        # if case_goal['期望状态'] in('全成','内部撤单')  or (case_goal['期望状态'] == '部撤' and wt_reqs['price_type'] in (
        # Api.const.XTP_PRICE_TYPE['XTP_PRICE_BEST_OR_CANCEL'],
        # Api.const.XTP_PRICE_TYPE['XTP_PRICE_BEST5_OR_CANCEL'])) or (
        #         case_goal['期望状态'] == '已撤' and wt_reqs['price_type'] in(Api.const.XTP_PRICE_TYPE['XTP_PRICE_ALL_OR_CANCEL'],Api.const.XTP_PRICE_TYPE['XTP_PRICE_REVERSE_BEST_LIMIT'])):
        if case_goal['期望状态'] in('全成'):
            logger.info('当前报单推送状态为未成交，等待..')
            bdCheck['status']='pending'

    # 当报单是‘全部成交’时，报单已接受，进行１.报单业务处理 2.报单查询业务处理
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_ALLTRADED'] and data[
        'order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
        queryByXtpID(Api, case_goal['xtp_ID'])
        bdCheck['status'] = 'end'
        bdCheck['flag'] = True

    # 当报单是‘废单’时，报单已拒绝，进行１.赋值queryEnd　２.报单业务处理 ３.报单查询业务处理
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_REJECTED'] and data[
        'order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_INSERT_REJECTED']:
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
        bdQuecyCheck['检查状态'] = 'end'
        bdQuecyCheck['flag'] = False
        bdQuecyCheck['remark'] = '期望状态与报单状态不匹配'

    # 当报单查询结果是‘未成交’，报单已接受
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_NOTRADEQUEUEING'] and data['order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
                'XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
        #当期望状态是‘未成交’时，赋值queryEnd，检查报单查询数据
        if case_goal['期望状态'] == '未成交':
            setQueryEnd(Api,wt_reqs)
            bdQuecyCheck['检查状态'] = 'end'
            bdQuecyCheck['flag'] = True
        #当期望状态是
        elif case_goal['期望状态'] in('全成'):
            bdQuecyCheck['检查状态']='pending'
        else:
            bdQuecyCheck['检查状态'] = 'end'
            bdQuecyCheck['flag']=False
            bdQuecyCheck['remark']='期望状态与报单状态不匹配'

    # 当报单查询结果是‘全成’，报单已接受
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
        if data['order_submit_status'] ==Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
            bdQuecyCheck['检查状态'] = 'end'
            bdQuecyCheck['flag'] = False
            bdQuecyCheck['remark'] = '期望状态与报单状态不匹配'

        # 撤单已接受
        elif data['order_submit_status'] ==Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_CANCEL_ACCEPTED']:
            bdQuecyCheck['检查状态'] = 'end'
            bdQuecyCheck['flag'] = True


    # 当报单查询结果是‘废单’，报单已拒绝
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_REJECTED'] and data['order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_INSERT_REJECTED']:
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
    elif fundasset0['data']['is_last'] == True:
        QueryInit['可用资金'] = fundasset0['data']['buying_power']
        QueryInit['买入资金'] = fundasset0['data']['fund_buy_amount']
        QueryInit['买入费用'] = fundasset0['data']['fund_buy_fee']
        QueryInit['卖出资金'] = fundasset0['data']['fund_sell_amount']
        QueryInit['卖出费用'] = fundasset0['data']['fund_sell_fee']
    else:
        logger.error("初始资金查询：查询的资金返回值非is_last")

    # 持仓查询及赋值QueryInit------------------------------------------
    stkcode = {
        'ticker': ''
    }
    stkasset0 = Api.trade.QueryPositionSync(stkcode)
    if stkasset0['data'].has_key(wt_reqs['ticker']):
        QueryInit['股票代码'] = stkasset0['data'][wt_reqs['ticker']]['position']['ticker']
        QueryInit['市场'] = stkasset0['data'][wt_reqs['ticker']]['position']['market']
        QueryInit['拥股数量'] = stkasset0['data'][wt_reqs['ticker']]['position']['total_qty']
        QueryInit['可用股份数'] = stkasset0['data'][wt_reqs['ticker']]['position']['sellable_qty']
        QueryInit['持仓成本'] = stkasset0['data'][wt_reqs['ticker']]['position']['avg_price']
        QueryInit['浮动盈亏'] = stkasset0['data'][wt_reqs['ticker']]['position']['unrealized_pnl']
    else:
        QueryInit['股票代码'] = wt_reqs['ticker']
        QueryInit['市场'] = wt_reqs['market']
        QueryInit['拥股数量'] = 0

        QueryInit['可用股份数'] = 0
        QueryInit['持仓成本'] = 0
        QueryInit['浮动盈亏'] = 0
    logger.info('初始资金持仓为:')
    dictLogging(QueryInit)


# -----------------------------------------------------------------------------------------------------------------------
# 定义函数：赋值业务操作后查询的资金和持仓
# -----------------------------------------------------------------------------------------------------------------------
def setQueryEnd(Api, wt_reqs):
    # 查询资金-------------------------------------
    fundasset9 = Api.trade.QueryAssetSync()
    if fundasset9['data'] == {}:
        logger.error('未查到资金持仓数据，请检查测试环境')
    elif fundasset9['data']['is_last'] == True:
        QueryEnd['可用资金'] = fundasset9['data']['buying_power']
        QueryEnd['买入资金'] = fundasset9['data']['fund_buy_amount']
        QueryEnd['买入费用'] = fundasset9['data']['fund_buy_fee']
        QueryEnd['卖出资金'] = fundasset9['data']['fund_sell_amount']
        QueryEnd['卖出费用'] = fundasset9['data']['fund_sell_fee']
    else:
        logger.error("收到成交回报资金查询：查询的资金返回值非is_last")

    # 收到成交回报后查询持仓-------------------------------------
    stkcode = {
        'ticker': ''
    }
    stkasset9 = Api.trade.QueryPositionSync(stkcode)
    if stkasset9['data'].has_key(wt_reqs['ticker']):
        QueryEnd['股票代码'] = stkasset9['data'][wt_reqs['ticker']]['position']['ticker']
        QueryEnd['市场'] = stkasset9['data'][wt_reqs['ticker']]['position']['market']
        QueryEnd['拥股数量'] = stkasset9['data'][wt_reqs['ticker']]['position']['total_qty']
        QueryEnd['可用股份数'] = stkasset9['data'][wt_reqs['ticker']]['position']['sellable_qty']
        QueryEnd['持仓成本'] = stkasset9['data'][wt_reqs['ticker']]['position']['avg_price']
        QueryEnd['浮动盈亏'] = stkasset9['data'][wt_reqs['ticker']]['position']['unrealized_pnl']
    else:
        QueryEnd['股票代码'] = wt_reqs['ticker']
        QueryEnd['市场'] = wt_reqs['market']
        QueryEnd['拥股数量'] = 0
        QueryEnd['可用股份数'] = 0
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
    if expectStatus == '初始':
        time = ServiceConfig.TIMEPENDING['CHUSHI']
    elif expectStatus == '未成交':
        time = ServiceConfig.TIMEPENDING['WEICHENGJIAO']
    elif expectStatus == '部成':
        time = ServiceConfig.TIMEPENDING['BUCHENG']
    elif expectStatus == '全成':
        time = ServiceConfig.TIMEPENDING['QUANCHENG']
    elif expectStatus == '部撤':
        time = ServiceConfig.TIMEPENDING['BUCHE']
    elif expectStatus == '已撤':
        time = ServiceConfig.TIMEPENDING['YICHE']
    elif expectStatus == '废单':
        time = ServiceConfig.TIMEPENDING['FEIDAN']
    elif expectStatus == '已报待撤':
        time = ServiceConfig.TIMEPENDING['YIBAODAICHE']
    elif expectStatus == '部撤已报':
        time = ServiceConfig.TIMEPENDING['BUCHEYIBAO']
    elif expectStatus == '撤废':
        time = ServiceConfig.TIMEPENDING['CHEFEI']
    elif expectStatus == '内部撤单':
        time = ServiceConfig.TIMEPENDING['NEIBUCHEDAN']

    return time

