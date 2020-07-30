#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
from BdtsDataCheck import *
from BdqueryDataCheck import *
from CaseEndCheck import *
from CancelOrderErrorDataCheck import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from log import *
from getTime import *
import ServiceConfig
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from QueryStkpriceDB import *
sys.path.append("/home/yhl2/workspace/xtp_test/StructuredFund/mysql")
from QueryMrcommFjjj import QueryMrcommFjjj


# 定义request_id
request_id=0
# 定义查询报单的requestID
QueryOrder_requestID=0
# 定义查询报单的参数
XTPQueryOrderReq = {
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
    if expectStatus in ('未成交', '废单'):
        result['撤单检查状态'] = 'end'
        result['撤单测试结果'] = True
    else:
        result['撤单检查状态'] = 'init'
        result['撤单测试结果'] = False

    # 下单前初始化　bd_time（各个状态的报单时间）为空
    bdTimeInit()
    # 下单前初始化成交回报测试结果集
    logger.info('ParmIni初始化全局变量完成')

def serviceTest(Api,case_goal,wt_reqs,*component_stk_info_sell):
    # ------------------------------------------------------------------------------------------------------------------
    #　业务回调(成交回报／报单回报／报单查询／撤单废单)-------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # 报单查询业务回调
    def on_QueryOrder(data,error,reqID,is_last):
        logger.info('报单查询回调开始，当前报单xtpID='+str(data['order_xtp_id'])+',报单状态='+str(data['order_status'])+',提交状态='+str(data['order_submit_status']))
        bdQuecyCheck=bdqueryCheck(Api,case_goal,wt_reqs,data)
        logger.info('报单查询-报单状态/提交状态check结果:'+str(bdQuecyCheck['flag'])+','+str(bdQuecyCheck['检查状态'])+','+bdQuecyCheck['remark'])
        global bdquery_rs,cdquery_rs
        if bdQuecyCheck['flag'] and bdQuecyCheck['检查状态']=='end':
            rs=BdqueryDataCheck(Api,wt_reqs,case_goal,data,error,QueryInit,QueryEnd)
            if rs['报单类型']=='报单':
                bdquery_rs=rs
                result['报单检查状态'] = rs['报单检查状态']
                result['报单测试结果'] = rs['测试结果']
                result['报单错误原因'] = rs['错误信息']
            elif rs['报单类型']=='撤单':
                cdquery_rs=rs
                result['撤单检查状态'] = rs['报单检查状态']
                result['撤单测试结果'] = rs['测试结果']
                result['撤单错误原因'] = rs['错误信息']
            else:
                result['报单检查状态'] = 'end'
                result['报单测试结果'] = False
                result['报单错误原因'] = '报单类型无法识别'
                result['撤单检查状态'] = 'end'
                result['撤单测试结果'] = False
                result['撤单错误原因'] = '报单类型无法识别'

        elif bdQuecyCheck['检查状态']=='pending':
            case_goal['cancel_xtpID'] = bdQuecyCheck['cancel_xtpID']
            logger.warning('报单查询等待...,xtpID='+str(data['order_xtp_id']))
            bdquery_rs={
                '检查状态': 'pending'
            }
        elif bdQuecyCheck['检查状态']=='end' and bdQuecyCheck['flag']==False:
            bdquery_rs={
                '检查状态':'end',
                '测试结果':False,
                '错误信息':bdQuecyCheck['remark']
            }
            result['报单检查状态'] = 'end'
            result['用例检查状态'] = 'end'
            result['用例测试结果'] = False
            result['用例错误原因'] = bdQuecyCheck['remark']
            result['用例错误源'] = '报单查询－状态检查'

    # 报单回报业务回调
    def on_order(data, error):
        global bdhb_rs
        bdCheck=bdtsCheck(Api, case_goal, wt_reqs, data)
        logger.info('报单推送-报单状态/提交状态check结果:' + str(bdCheck['flag']) + ','+ bdCheck['remark'])
        if bdCheck['flag'] and bdCheck['status']=='end':
            bdhb_rs = bdtsDataCheck(Api, wt_reqs, case_goal, data, error)
        elif bdCheck['flag'] is False and bdCheck['status']=='end':
            bdhb_rs = {
                '报单检查状态':'end',
                '测试结果':False,
                '错误信息':bdCheck['remark'],
            }
            result['用例检查状态'] = 'end'
            result['用例测试结果'] = False
            result['用例错误原因'] = bdCheck['remark']
            result['用例错误源'] = '报单推送－状态检查'
        else:
            logger.error('状态未知,bdCheck["flag"]:' + str(bdCheck['flag']) + ', bdCheck["status"]:' + str(bdCheck['status']))

        # 校验xtp_mrcomm_fjjj表
        if bdhb_rs['测试结果'] and data['order_local_id'] != '':
            bdhb_rs_mrcomm = mrcomm_check(data, wt_reqs)
            bdhb_rs['测试结果'] = bdhb_rs_mrcomm['测试结果']
            bdhb_rs['错误信息'] = bdhb_rs_mrcomm['错误信息']


    # 撤废业务回调
    def on_cancelorder_error(cancel_info, error_info):
        logger.info('当前为撤废异步回调函数..start')
        time.sleep(0.2)
        if case_goal['是否是撤废'] == '是':
            cancelorder_check(cancel_info, error_info)
        else:
            logger.error('错误，当前撤单为撤废与期望状态不符合，期望状态为' + case_goal['期望状态'])
            result['用例检查状态'] = 'end'
            result['用例错误源'] = '撤单'
            result['用例测试结果'] = False
            result['用例错误原因'] = '当前撤单为撤废与期望状态不符合'

    def cancelorder_check(cancel_info, error_info):
        if cancel_info['order_xtp_id'] != case_goal['xtp_ID']:
            logger.error('错误，当前API返回撤废的原xtpID与当前用例的xtpID不一致，当前API返回的xtpID和此用例的xtpID分别是' + str(
                cancel_info['order_xtp_id']) + ',' + str(case_goal['xtp_ID']))
            result['用例检查状态'] = 'end'
            result['用例错误源'] = '撤单'
            result['用例测试结果'] = False
            result['用例错误原因'] = '当前API返回撤废的原xtpID与当前用例的xtpID不一致'
        else:
            rs = cancelOrderErrorDataCheck(case_goal, error_info)
            result['用例检查状态'] = rs['检查状态']
            result['用例测试结果'] = rs['测试结果']
            result['用例错误原因'] = rs['错误原因']
            if rs['测试结果'] is False:
                result['用例错误源'] = '撤废'
            result['用例错误源'] = ''

    Api.trade.setQueryOrderHandle(on_QueryOrder)
    Api.trade.setOrderEventHandle(on_order)
    Api.trade.setCancelOrderErrorHandle(on_cancelorder_error)

    # ------------------------------------------------------------------------------------------------------------------
    # 查询初始资金和持仓，当期望状态是'初始','未成交','部成','全成','已撤','废单'时，在下单前查询-----------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    if case_goal['期望状态'] in ('未成交', '废单'):
        setQueryInit(Api, wt_reqs)

    # ------------------------------------------------------------------------------------------------------------------
    # 下单---------------------------------------------------------------------------------------------------------------
    # 当期望状态为（部撤已报和已报待撤）时，在开市时间内下单（match程序需要配置为EqualHigh），其它期望状态直接下单
    # ------------------------------------------------------------------------------------------------------------------

    case_goal['xtp_ID'] = Api.trade.InsertOrder(wt_reqs)

    insertOrderTime = getTimestampInt()
    logger.info('下单的xtpID=' + str(case_goal['xtp_ID']))

    if case_goal['xtp_ID'] == 0:
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

    # ------------------------------------------------------------------------------------------------------------------
    # 当报单检查状态非‘end’时，一直休0.5秒,等待报单检查结束
    # ------------------------------------------------------------------------------------------------------------------
    #获取超时时间
    t=getTimePending(case_goal['期望状态'])
    #定义caseEndCheck是否已执行
    endCheckFlag=False
    while getTimestampInt()<=insertOrderTime+t:
        if result['用例检查状态'] == 'end':
            break
        else:
            time.sleep(0.5)
            if result['报单检查状态'] == 'end' and result['撤单检查状态'] == 'end' and endCheckFlag is False:
                rs = caseEndCheck(Api, bdhb_rs, bdquery_rs, cdquery_rs, cjhb_rs, case_goal['期望状态'],
                                  wt_reqs['price_type'])
                result['用例检查状态'] = 'end'
                result['用例测试结果'] = rs['测试结果']
                result['用例错误原因'] = rs['错误原因']
                result['用例错误源'] = rs['错误源']
                endCheckFlag = True

    #超出设置的“超时”时间后
    if result['用例检查状态']== 'init':
        result['用例测试结果'] = False
        result['用例错误原因'] = '用例超时'

    return result

# ----------------------------------------------------------------------------------------------------------------------
# 定义函数：报单推送外层检查，注：根据报单推送的类型和期望状态进行撤单　和　赋值查询
# ----------------------------------------------------------------------------------------------------------------------
def bdtsCheck(Api,case_goal,wt_reqs,data):
    bdCheck={
        'status':'init',
        'flag':False,
        'remark':'',
        'cancel_xtpID':0,
    }

    # 当报单是‘未成交’时，报单已接受，进行报单查询
    if data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_NOTRADEQUEUEING'] and data[
        'order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
        time.sleep(0.1)
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
    global sqbh_cd,xtp_id_init

    bdQuecyCheck={
        '检查状态':'init',
        'flag':False,
        'cancel_xtpID':0,
        'recancel_xtpID':0,
        'remark':'',
    }

    # 当报单查询结果是‘未成交’，报单已接受
    if data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_NOTRADEQUEUEING'] and data['order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
                'XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
        #当期望状态是‘未成交’时，赋值queryEnd，检查报单查询数据
        if case_goal['期望状态'] == '未成交' and case_goal['是否是撤废'] == '否':
            setQueryEnd(Api,wt_reqs)
            bdQuecyCheck['检查状态'] = 'end'
            bdQuecyCheck['flag'] = True
        elif case_goal['期望状态'] == '未成交' and case_goal['是否是撤废'] == '是':
            bdQuecyCheck['cancel_xtpID'] = Api.trade.CancelOrder(case_goal['xtp_ID'])
            bdQuecyCheck['检查状态'] = 'pending'
        else:
            bdQuecyCheck['检查状态'] = 'end'
            bdQuecyCheck['flag']=False
            bdQuecyCheck['remark']='期望状态与报单状态不匹配'

    # 当报单查询结果是‘废单’，报单已拒绝
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_REJECTED']:
        if data['order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_INSERT_REJECTED']:
            #当期望状态是‘废单’，进行报单查询数据处理
            if case_goal['期望状态'] == '废单':
                setQueryEnd(Api, wt_reqs)
                bdQuecyCheck['检查状态'] = 'end'
                bdQuecyCheck['flag'] = True
            else:
                bdQuecyCheck['检查状态'] = 'end'
                bdQuecyCheck['flag'] = False
                bdQuecyCheck['remark'] = '期望状态与报单状态不匹配'
        # 撤单已接受
        elif data['order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_CANCEL_ACCEPTED']:
            bdQuecyCheck['检查状态'] = 'end'
            bdQuecyCheck['flag'] = True

    return bdQuecyCheck

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
        stkasset = stkasset0['data'][wt_reqs['ticker']]['position']
        QueryInit['股票代码'] = stkasset['ticker']
        QueryInit['市场'] = stkasset['market']
        QueryInit['拥股数量'] = stkasset['total_qty']
        QueryInit['可用股份数'] = stkasset['sellable_qty']
        QueryInit['持仓成本'] = stkasset['avg_price']
        QueryInit['浮动盈亏'] = stkasset['unrealized_pnl']
        QueryInit['昨日持仓'] = stkasset['yesterday_position']
        QueryInit['今日可申购赎回持仓'] = stkasset['purchase_redeemable_qty']
    elif stkasset0['data'].has_key(wt_reqs['ticker'] + '  '):
        stkasset = stkasset0['data'][wt_reqs['ticker'] + '  ']['position']
        QueryInit['股票代码'] = stkasset['ticker']
        QueryInit['市场'] = stkasset['market']
        QueryInit['拥股数量'] = stkasset['total_qty']
        QueryInit['可用股份数'] = stkasset['sellable_qty']
        QueryInit['持仓成本'] = stkasset['avg_price']
        QueryInit['浮动盈亏'] = stkasset['unrealized_pnl']
        QueryInit['昨日持仓'] = stkasset['yesterday_position']
        QueryInit['今日可申购赎回持仓'] = stkasset['purchase_redeemable_qty']
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
        stkasset = stkasset9['data'][wt_reqs['ticker']]['position']
        QueryEnd['股票代码'] = stkasset['ticker']
        QueryEnd['市场'] = stkasset['market']
        QueryEnd['拥股数量'] = stkasset['total_qty']
        QueryEnd['可用股份数'] = stkasset['sellable_qty']
        QueryEnd['持仓成本'] = stkasset['avg_price']
        QueryEnd['浮动盈亏'] = stkasset['unrealized_pnl']
        QueryEnd['昨日持仓'] = stkasset['yesterday_position']
        QueryEnd['今日可申购赎回持仓'] = stkasset['purchase_redeemable_qty']
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
    if expectStatus == '未成交':
        time = ServiceConfig.TIMEPENDING['WEICHENGJIAO']
    elif expectStatus == '废单':
        time = ServiceConfig.TIMEPENDING['FEIDAN']
    else:
        pass

    return time

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

# ---------------------------------------------------------------------------------------------
# 定义函数：等待到休市时间＋１秒，返回值为True
#----------------------------------------------------------------------------------------------
def waitCloseTime():
    # 获取当前系统时间的秒数
    if is_exchange_clese is False:
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

def mrcomm_check(data, wt_reqs):
    # 作拆分合并报单不是废单时，对xtp_mrcomm_fjjj表作校验

    if wt_reqs['side'] == Api.const.XTP_SIDE_TYPE['XTP_SIDE_SPLIT']:
        appl_id = '310'
    elif wt_reqs['side'] == Api.const.XTP_SIDE_TYPE['XTP_SIDE_MERGE']:
        appl_id = '311'
    else:
        appl_id = ''
        logger.error('非法的买卖方向:' + str(wt_reqs['side']))
    mrcommon_dict = QueryMrcommFjjj()

    error_msg = ''
    bdhb_rs = {
        '报单检查状态': 'end',
        '测试结果': True,
        '错误信息': error_msg,
    }
    # # 0-未发送至中登,1-发送至中登
    if mrcommon_dict['send_flag'] != 0:
        error_msg = '发送状态send_flag错误，' + str(mrcommon_dict['send_flag'])
        bdhb_rs['测试结果'] = False
        logger.error(error_msg)
    elif mrcommon_dict['appl_id'] != appl_id:
        error_msg = 'appl_id错误，' + str(mrcommon_dict['appl_id'])
        bdhb_rs['测试结果'] = False
        logger.error(error_msg)
    elif mrcommon_dict['memo'] != 'mock':
        error_msg = 'memo错误，' + str(mrcommon_dict['memo'])
        bdhb_rs['测试结果'] = False
        logger.error(error_msg)

    return bdhb_rs



