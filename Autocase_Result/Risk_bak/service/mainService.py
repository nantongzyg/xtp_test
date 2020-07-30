#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
from BdtsDataCheck import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from CaseEndCheck import *
from log import *
from getTime import *
from GetCancelType import *
import ServiceConfig
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from QueryStkpriceDB import *
from order import f
import collections


# 定义request_id
request_id=0
# 定义查询报单的requestID
QueryOrder_requestID=0
# 定义查询报单的参数
XTPQueryOrderReq={
    'ticker' : '00000' ,
    'begin_time' : 0 ,
    'end_time' : 0 ,
}
#　获取是否交易所休市配置
is_exchange_clese=ServiceConfig.IS_EXCHANGE_CLOSE
# 获取开市时间配置
close_time = ServiceConfig.TIME_MARKET_CLOSE
# 获取休市时间配置
open_time = ServiceConfig.TIME_MARKET_OPEN
# 获取开市第4秒开始的时间配置
open_time_four_sec = ServiceConfig.TIME_MARKET_OPEN_FOUR_SEC
#获取延时时间配置
time_delay = ServiceConfig.TIME_DELAY

# 风控测试用到的订单信息，包括订单状态，报单状态，err_code,err_msg
order_info = {}

#程序成交回报数
cjhb_count = 0

#本地报单编号sqbh,撤单的本地报单编号sqbh_cd
sqbh = ''
sqbh_cd = ''

#期望状态为'初始'case的xtp_id,用来和ashare_ordwth表作校验
xtp_id_init = ''

# 定义下单前资金持仓全局变量－----------------
QueryInit = {
    '总资产': 0,
    '可用资金': 0,
    '买入资金': 0,
    '买入费用': 0,
    '卖出资金': 0,
    '卖出费用': 0,
    '预扣资金':0,
    '股票代码': None,
    '市场': None,
    '拥股数量': 0,
    '可用股份数':0,
    '持仓成本': 00,
    '浮动盈亏': 0,
    '昨日持仓': 0,
    '今日可申购赎回持仓': 0,
    }

# 定义下单后的资金持仓全局变量----------------------
QueryEnd = {
    '总资产': 0,
    '可用资金': 0,
    '买入资金': 0,
    '买入费用': 0,
    '卖出资金': 0,
    '卖出费用': 0,
    '预扣资金':0,
    '股票代码': None,
    '市场': None,
    '拥股数量': 0,
    '可用股份数':0,
    '持仓成本': 00,
    '浮动盈亏': 0,
    '昨日持仓': 0,
    '今日可申购赎回持仓': 0,
    }
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
    '成交金额': 0,
    '成交类型': None,
    '测试结果':0,
    '测试错误原因':None,
}
#初始化全局变量
def ParmIni(Api,expectStatus,price_type):
    logger.info('ParmIni初始化全局变量开始..')

    global request_id
    request_id +=1

    QueryInit['总资产'] = 0,
    QueryInit['可用资金'] = 0,
    QueryInit['买入资金'] = 0,
    QueryInit['买入费用'] = 0,
    QueryInit['卖出资金'] = 0,
    QueryInit['卖出费用'] = 0,
    QueryInit['预扣资金'] = 0,
    QueryInit['股票代码'] = None,
    QueryInit['市场'] = None,
    QueryInit['拥股数量'] = 0,
    QueryInit['可用股份数'] = 0,
    QueryInit['持仓成本'] = 0,
    QueryInit['浮动盈亏'] = 0,
    QueryInit['昨日持仓'] = 0,
    QueryInit['今日可申购赎回持仓'] = 0,

    QueryEnd['总资产'] = 0,
    QueryEnd['可用资金'] = 0,
    QueryEnd['买入资金'] = 0,
    QueryEnd['买入费用'] = 0,
    QueryEnd['卖出资金'] = 0,
    QueryEnd['卖出费用'] = 0,
    QueryEnd['预扣资金'] = 0,
    QueryEnd['股票代码'] = None,
    QueryEnd['市场'] = None,
    QueryEnd['拥股数量'] = 0,
    QueryEnd['可用股份数'] = 0,
    QueryEnd['持仓成本'] = 0,
    QueryEnd['浮动盈亏'] = 0,
    QueryEnd['昨日持仓'] = 0,
    QueryEnd['今日可申购赎回持仓'] = 0,

    result['用例检查状态'] = 'init'
    result['用例错误源'] = ''
    result['用例测试结果'] = False
    result['用例错误原因'] = ''
    result['报单检查状态'] = 'init'
    result['报单测试结果'] = False
    result['报单错误原因'] = ''
    result['撤单错误原因'] = ''
    if expectStatus in('初始','未成交','部成','全成','废单'):
        result['撤单检查状态'] = 'end'
        result['撤单测试结果'] = True
    else:
        result['撤单检查状态'] = 'init'
        result['撤单测试结果'] = False

    if getCancelType(Api,price_type,expectStatus) is False:
        result['撤单检查状态'] = 'end'
        result['撤单测试结果'] = True
        result['撤单错误原因'] = ''

    # 下单前初始化　bd_time（各个状态的报单时间）为空
    bdTimeInit()
    # 下单前初始化成交回报测试结果集
    cjhbDataInit()
    logger.info('ParmIni初始化全局变量完成')

def serviceTest(Api,case_goal,wt_reqs,file):
    # ------------------------------------------------------------------------------------------------------------------
    #　业务回调(成交回报／报单回报／报单查询／撤单废单)-------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    # 报单回报业务回调
    def on_order(data, error):
        order = {}
        order['order_xtp_id'] = data['order_xtp_id']
        order['error_id'] = error['error_id']
        order['error_msg'] = error['error_msg']
        order['insert_time'] = data['insert_time']
        order_info = {}
        order_info[data['order_xtp_id']] = order
        save_order(file, str(order_info) + '\n')

    Api.trade.setOrderEventHandle(on_order)
    # ------------------------------------------------------------------------------------------------------------------
    # 下单---------------------------------------------------------------------------------------------------------------
    # 当期望状态为（部撤已报和已报待撤）时，在开市时间内下单（match程序需要配置为EqualHigh），其它期望状态直接下单
    # ------------------------------------------------------------------------------------------------------------------

    case_goal['xtp_ID'] = Api.trade.InsertOrder(wt_reqs)
    #time.sleep(0.01)

    #Api.trade.CancelOrder(case_goal['xtp_ID'])
    #time.sleep(20)

# ----------------------------------------------------------------------------------------------------------------------
# 定义函数：报单推送外层检查，注：根据报单推送的类型和期望状态进行撤单　和　赋值查询
# ----------------------------------------------------------------------------------------------------------------------
def bdtsCheck(Api, case_goal, wt_reqs, data):
    bdCheck={
        'status':'init',
        'flag':False,
        'remark':'',
        'cancel_xtpID':0,
    }

    # 当报单是‘未成交’时，报单已接受，进行报单查询
    if data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_NOTRADEQUEUEING'] and data[
        'order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
        global sqbh
        sqbh = data['order_local_id']
        if '是否是新股申购' not in case_goal:
            if case_goal['期望状态'] in ('全成','内部撤单') or getCancelType(Api,wt_reqs['price_type'],case_goal['期望状态']) is False :
                logger.info('当前报单推送状态为未成交，等待..')
                bdCheck['status']='pending'

            else:
                time.sleep(0.1)
                queryByXtpID(Api, case_goal['xtp_ID'])
                if case_goal['期望状态'] == '未成交' and case_goal['是否是撤废']=='是':
                    bdCheck['status'] = 'pending'
                else:
                    bdCheck['status'] = 'end'
                    bdCheck['flag'] = True
        else:
            time.sleep(0.1)
            queryByXtpID(Api, case_goal['xtp_ID'])
            bdCheck['status'] = 'end'
            bdCheck['flag'] = True

    # 当报单是‘全部成交’时，报单已接受，进行１.报单业务处理 2.报单查询业务处理
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_ALLTRADED'] and data[
        'order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
        if case_goal['期望状态'] == '全成' and case_goal['是否是撤废']=='是':
            setQueryInit(Api,wt_reqs)
            # bdCheck['cancelErr_xtpID']=Api.trade.CancelOrder(case_goal['xtp_ID'])
            bdCheck['cancel_xtpID'] = Api.trade.CancelOrder(case_goal['xtp_ID'])
            bdCheck['status'] = 'pending'
            logger.info('报单推送penging')
        else:
            queryByXtpID(Api, case_goal['xtp_ID'])
            bdCheck['status'] = 'end'
            bdCheck['flag'] = True
    # 当报单是‘部撤’时，报单已接受，进行１.赋值queryEnd　２.报单业务处理 ３.原单和撤单都进行报单查询业务处理
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_PARTTRADEDNOTQUEUEING'] and data[
        'order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
        #如果是部撤后再撤单
        if case_goal['期望状态']=='部撤' and case_goal['是否是撤废']=='是':
            setQueryInit(Api,wt_reqs)
            # bdCheck['cancelErr_xtpID']=Api.trade.CancelOrder(case_goal['xtp_ID'])
            bdCheck['cancel_xtpID'] = Api.trade.CancelOrder(case_goal['xtp_ID'])
            bdCheck['status']='pending'
        else:
            time.sleep(0.1)
            queryByXtpID(Api, case_goal['xtp_ID'])
            # 当委托价格条件是：既成剩撤和五档转撤时不做撤单查询请求
            # if wt_reqs['price_type'] not in(Api.const.XTP_PRICE_TYPE['XTP_PRICE_BEST_OR_CANCEL'],Api.const.XTP_PRICE_TYPE['XTP_PRICE_BEST5_OR_CANCEL']):
            #     queryByXtpID(Api, case_goal['cancel_xtpID'])
            if getCancelType(Api, wt_reqs['price_type'], case_goal['期望状态']):
                queryByXtpID(Api, data['order_cancel_xtp_id'])
            bdCheck['status'] = 'end'
            bdCheck['flag'] = True


    # 当报单是‘已撤’时，报单已接受，进行１.赋值queryEnd　２.报单业务处理 ３.原单和撤单都进行报单查询业务处理
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_CANCELED'] and data[
        'order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:

        if case_goal['期望状态']=='已撤' and case_goal['是否是撤废']=='是':
            setQueryInit(Api,wt_reqs)
            # bdCheck['cancelErr_xtpID']=Api.trade.CancelOrder(case_goal['xtp_ID'])
            bdCheck['cancel_xtpID'] = Api.trade.CancelOrder(case_goal['xtp_ID'])
            bdCheck['status']='pending'
        elif case_goal['期望状态'] == '未成交' and case_goal['是否是撤废']=='是' and case_goal['是否是集合竞价'] == '否':
            setQueryEnd(Api,wt_reqs)
            time.sleep(0.1)
            queryByXtpID(Api, case_goal['cancel_xtpID'])

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
            # bdCheck['cancelErr_xtpID']=Api.trade.CancelOrder(case_goal['xtp_ID'])
            bdCheck['cancel_xtpID'] = Api.trade.CancelOrder(case_goal['xtp_ID'])
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
#定义函数：通过xtpID查询报单
#-----------------------------------------------------------------------------------------------------------------------
def queryByXtpID(Api,xtpID) :
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


#-----------------------------------------------------------------------------------------------------------------------
# 定义函数：赋值初始查询的资金和持仓
#-----------------------------------------------------------------------------------------------------------------------
def setQueryInit(Api,wt_reqs):
    # 资金查询及赋值QueryInit-------------------------------------
    fundasset0 = Api.trade.QueryAssetSync()
    if fundasset0['data'] == {}:
        logger.error('未查到资金持仓数据，请检查测试环境')
    elif fundasset0['data']['is_last']:
        QueryInit['总资产'] = fundasset0['data']['total_asset']
        QueryInit['可用资金'] = fundasset0['data']['buying_power']
        QueryInit['买入资金'] = fundasset0['data']['fund_buy_amount']
        QueryInit['买入费用'] = fundasset0['data']['fund_buy_fee']
        QueryInit['卖出资金'] = fundasset0['data']['fund_sell_amount']
        QueryInit['卖出费用'] = fundasset0['data']['fund_sell_fee']
        QueryInit['预扣资金'] = fundasset0['data']['withholding_amount']
    else:
        logger.error("初始资金查询：查询的资金返回值非is_last")

    # 持仓查询及赋值QueryInit------------------------------------------
    stkcode = {
        'ticker': ''
    }
    stkasset0 = Api.trade.QueryPositionSync(stkcode)
    # print stkasset0
    if stkasset0['data'].has_key(wt_reqs['ticker']):
        QueryInit['股票代码'] = stkasset0['data'][wt_reqs['ticker']]['position']['ticker']
        QueryInit['市场'] = stkasset0['data'][wt_reqs['ticker']]['position']['market']
        QueryInit['拥股数量'] = stkasset0['data'][wt_reqs['ticker']]['position']['total_qty']
        QueryInit['可用股份数'] = stkasset0['data'][wt_reqs['ticker']]['position']['sellable_qty']
        QueryInit['持仓成本'] = stkasset0['data'][wt_reqs['ticker']]['position']['avg_price']
        QueryInit['浮动盈亏'] = stkasset0['data'][wt_reqs['ticker']]['position']['unrealized_pnl']
        QueryInit['昨日持仓'] = stkasset0['data'][wt_reqs['ticker']]['position']['yesterday_position']
        QueryInit['今日可申购赎回持仓'] = stkasset0['data'][wt_reqs['ticker']]['position']['purchase_redeemable_qty']
    elif stkasset0['data'].has_key(wt_reqs['ticker'] + '  '):
        QueryInit['股票代码'] = stkasset0['data'][wt_reqs['ticker'] + '  ']['position']['ticker']
        QueryInit['市场'] = stkasset0['data'][wt_reqs['ticker'] + '  ']['position']['market']
        QueryInit['拥股数量'] = stkasset0['data'][wt_reqs['ticker'] + '  ']['position']['total_qty']
        QueryInit['可用股份数'] = stkasset0['data'][wt_reqs['ticker'] + '  ']['position']['sellable_qty']
        QueryInit['持仓成本'] = stkasset0['data'][wt_reqs['ticker'] + '  ']['position']['avg_price']
        QueryInit['浮动盈亏'] = stkasset0['data'][wt_reqs['ticker'] + '  ']['position']['unrealized_pnl']
        QueryInit['昨日持仓'] = stkasset0['data'][wt_reqs['ticker'] + '  ']['position']['yesterday_position']
        QueryInit['今日可申购赎回持仓'] = stkasset0['data'][wt_reqs['ticker'] + '  ']['position']['purchase_redeemable_qty']
    else:
        QueryInit['股票代码'] = wt_reqs['ticker']
        QueryInit['市场'] = wt_reqs['market']
        QueryInit['拥股数量'] = 0
		
        QueryInit['可用股份数'] = 0
        QueryInit['持仓成本'] = 0
        QueryInit['浮动盈亏'] = 0
        QueryInit['昨日持仓'] = 0
        QueryInit['今日可申购赎回持仓'] = 0
    logger.info('初始资金持仓为:')
    dictLogging(QueryInit)

#-----------------------------------------------------------------------------------------------------------------------
# 定义函数：赋值业务操作后查询的资金和持仓
#-----------------------------------------------------------------------------------------------------------------------
def setQueryEnd(Api,wt_reqs):
    # 查询资金-------------------------------------
    fundasset9 = Api.trade.QueryAssetSync()
    if fundasset9['data'] == {}:
        logger.error('未查到资金持仓数据，请检查测试环境')
    elif fundasset9['data']['is_last']:
        QueryEnd['总资产'] = fundasset9['data']['total_asset']
        QueryEnd['可用资金'] = fundasset9['data']['buying_power']
        QueryEnd['买入资金'] = fundasset9['data']['fund_buy_amount']
        QueryEnd['买入费用'] = fundasset9['data']['fund_buy_fee']
        QueryEnd['卖出资金'] = fundasset9['data']['fund_sell_amount']
        QueryEnd['卖出费用'] = fundasset9['data']['fund_sell_fee']
        QueryEnd['预扣资金'] = fundasset9['data']['withholding_amount']
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
        QueryEnd['昨日持仓'] = stkasset9['data'][wt_reqs['ticker']]['position']['yesterday_position']
        QueryEnd['今日可申购赎回持仓'] = stkasset9['data'][wt_reqs['ticker']]['position']['purchase_redeemable_qty']
    else:
        QueryEnd['股票代码'] = wt_reqs['ticker']
        QueryEnd['市场'] = wt_reqs['market']
        QueryEnd['拥股数量'] = 0
        QueryEnd['可用股份数'] = 0
        QueryEnd['持仓成本'] = 0
        QueryEnd['浮动盈亏'] = 0
        QueryEnd['昨日持仓'] = 0
        QueryEnd['今日可申购赎回持仓'] = 0
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

#-----------------------------------------------------------------------------------------------------------------------
# 定义函数：获取撤单类型（交易所主动撤(False)或自己手动发起撤单(True)）
#-----------------------------------------------------------------------------------------------------------------------
# def getCancelType(Api,price_type,expectStatus):
#     isCancel=True
#     #当价格条件为：全成全撤，即成剩撤，五档转撤(期望状态：非内部撤单)时，对手方最优（期望状态：已撤）不需要手动发起撤
#     if price_type in(Api.const.XTP_PRICE_TYPE['XTP_PRICE_BEST_OR_CANCEL'],Api.const.XTP_PRICE_TYPE['XTP_PRICE_ALL_OR_CANCEL'],Api.const.XTP_PRICE_TYPE['XTP_PRICE_BEST5_OR_CANCEL']) and expectStatus!='内部撤单' or (price_type==Api.const.XTP_PRICE_TYPE['XTP_PRICE_REVERSE_BEST_LIMIT'] and expectStatus=='已撤'):
#         isCancel = False
#     else:
#         isCancel = True
#
#     return isCancel

#-----------------------------------------------------------------------------------------------------------------------
# 定义函数：等待到开市时间，返回值为True
#-----------------------------------------------------------------------------------------------------------------------
def waitOpenTime():
    # 获取当前系统时间的秒数
    second = getTimeSecondInt()
    logger.info('等待开市'+str(second))
    #如果在休市时间内，一直等待１秒循环
    while close_time[0][0] <= second <= close_time[0][1] or close_time[1][0] <= second <= close_time[1][1] or close_time[2][
        0] <= second <= close_time[2][1]:
        time.sleep(1)
        second = getTimeSecondInt()
    #如果在开市时间内,则返回True
    if open_time[0][0] <= second <= open_time[0][1] or open_time[1][0] <= second <= open_time[1][1] or open_time[2][
        0] <= second <= open_time[2][1]:

        return True

# -----------------------------------------------------------------------------------------------------------------------
# 定义函数：等待到开市第4秒，返回值为True
# -----------------------------------------------------------------------------------------------------------------------
def waitOpenTimeFourSec():
    # 获取当前系统时间的秒数
    second = getTimeSecondInt()
    logger.info('等待开市' + str(second))
    # 如果在休市时间内，一直等待１秒循环
    while close_time[0][0] <= second <= close_time[0][1] or close_time[1][0] <= second <= close_time[1][1] or \
                            close_time[2][
                                0] <= second <= close_time[2][1]:
        time.sleep(1)
        second = getTimeSecondInt()
    # 如果在开市时间内,则返回True
    if open_time_four_sec[0][0] <= second <= open_time_four_sec[0][1] or open_time_four_sec[1][0] <= second <= open_time_four_sec[1][1] or open_time_four_sec[2][
        0] <= second <= open_time_four_sec[2][1]:
        return True
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

def save_order(file, orderinfo):
    with open(file, 'a') as f:
        f.write(orderinfo)




