#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/service")
import ServiceConfig
from log import *
from mfCjhbDataCheck import *
from mfBdtsDataCheck import *
from mfBdqueryDataCheck import *
from mfCaseEndCheck import *
from mfCancelOrderErrorDataCheck import *
from mfgetTime import *
from mfGetCancelType import *
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *

sys.path.append("/home/yhl2/workspace/xtp_test/MoneyFund/moneyfundmysql")
from mfQueryStkpriceDB import *


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

    # if price_type in (Api.const.XTP_PRICE_TYPE['XTP_PRICE_BEST_OR_CANCEL'],Api.const.XTP_PRICE_TYPE['XTP_PRICE_BEST5_OR_CANCEL'],Api.const.XTP_PRICE_TYPE['XTP_PRICE_ALL_OR_CANCEL'],Api.const.XTP_PRICE_TYPE['XTP_PRICE_REVERSE_BEST_LIMIT']):
    #     result['撤单检查状态'] = 'end'
    #     result['撤单测试结果'] = True
    #     result['撤单错误原因'] = ''
    if getCancelType(Api,price_type,expectStatus) is False:
        result['撤单检查状态'] = 'end'
        result['撤单测试结果'] = True
        result['撤单错误原因'] = ''

    # 下单前初始化　bd_time（各个状态的报单时间）为空
    bdTimeInit()
    # 下单前初始化成交回报测试结果集
    cjhbDataInit()
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
        if bdQuecyCheck['flag']==True and bdQuecyCheck['检查状态']=='end':
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
                if case_goal['是否是撤废']=='是' or ('是否是新股申购' in case_goal and case_goal['期望状态'] == '废单'):
                    if rs['测试结果']==True:
                        result['用例测试结果'] = True
                        result['用例检查状态'] = 'end'
                        result['用例错误源'] = ''

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

        elif bdQuecyCheck['检查状态']=='pending':
            case_goal['cancel_xtpID'] = bdQuecyCheck['cancel_xtpID']
            if case_goal['期望状态'] == '未成交' and case_goal['是否是撤废'] =='是' and case_goal['是否是集合竞价'] == '否':
                case_goal['recancel_xtpID'] = bdQuecyCheck['recancel_xtpID']
            logger.warning('报单查询等待...,xtpID='+str(data['order_xtp_id']))
            # if case_goal['期望状态'] == '未成交' and case_goal['是否是撤废'] == '是':
            #     time.sleep(0.1)
            #     queryByXtpID(Api, case_goal['cancel_xtpID'])
            if case_goal['期望状态'] in ('已报待撤','部撤已报'):
                time.sleep(0.1)
                queryByXtpID(Api, case_goal['xtp_ID'])
                queryByXtpID(Api, case_goal['cancel_xtpID'])
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
        if bdCheck['flag']==True and bdCheck['status']=='end':
            bdhb_rs = bdtsDataCheck(Api, wt_reqs, case_goal, data, error)
        elif bdCheck['flag']==False and bdCheck['status']=='end':
            bdhb_rs={
                '报单检查状态':'end',
                '测试结果':False,
                '错误信息':bdCheck['remark'],
            }
            result['用例检查状态'] = 'end'
            result['用例测试结果'] = False
            result['用例错误原因'] = bdCheck['remark']
            result['用例错误源'] = '报单推送－状态检查'
        elif '是否是新股申购' not in case_goal:
            if bdCheck['status']=='pending' and case_goal['期望状态'] != '未成交' and case_goal['是否是撤废']=='是':
                case_goal['cancel_xtpID']=bdCheck['cancel_xtpID']
        else:
            if case_goal['是否是新股申购'] == '是' and case_goal['期望状态'] == '废单':
                case_goal['cancel_xtpID'] = bdCheck['cancel_xtpID']



    # 成交回报业务回调
    def on_trade(hb_data):
        global cjhb_count
        cjhb_count += 1
        logger.info('交易数据回报如下')
        dictLogging(hb_data)
        if case_goal['期望状态']in('部成','全成'):
            setQueryEnd(Api, wt_reqs)
            #收到成交回报后进行业务处理，返回值为为一个dict
            global cjhb_rs
            rs = cjhbDataCheck(case_goal['期望状态'],Api, QueryInit, wt_reqs, case_goal['xtp_ID'], QueryEnd, hb_data)
            cjhb_rs['成交回报检查状态']=rs['成交回报检查状态']
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
        else:
            logger.info('成交回报检查：用例期望状态非【全成】或【部成】,不做成交回报数据业务检查！')
            cjhb_rs={
                '成交回报检查状态': 'end',
                '测试结果':True,
            }

    # 撤废业务回调
    def on_cancelorder_error(cancel_info, error_info):
        logger.info('当前为撤废异步回调函数..start')
        time.sleep(0.2)
        if '是否是新股申购' in case_goal:
            if case_goal['是否是新股申购'] == '是' and case_goal['期望状态'] == '废单':
                cancelorder_check(cancel_info, error_info)
        elif case_goal['是否是撤废'] == '是':
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
        elif case_goal['期望状态'] != '未成交' and cancel_info['order_cancel_xtp_id'] != case_goal['cancel_xtpID']:
            result['用例检查状态'] = 'end'
            result['用例错误源'] = '撤单'
            result['用例测试结果'] = False
            result['用例错误原因'] = '当前API返回撤废的xtpID与当前用例的撤废xtpID不一致'
        elif case_goal['期望状态'] == '未成交' and case_goal['是否是集合竞价'] == '否' and cancel_info['order_cancel_xtp_id'] != \
                case_goal['recancel_xtpID']:
            result['用例检查状态'] = 'end'
            result['用例错误源'] = '撤单'
            result['用例测试结果'] = False
            result['用例错误原因'] = '当前API返回撤废的xtpID与当前用例的撤废xtpID不一致'
        else:
            rs = cancelOrderErrorDataCheck(case_goal, error_info)
            if rs['检查状态'] == 'end' and rs['测试结果'] == True:
                # 报单查询（撤废）
                if case_goal['期望状态'] == '未成交' and case_goal['是否是撤废'] == '是' and case_goal['是否是集合竞价'] == '否':
                    queryByXtpID(Api, case_goal['recancel_xtpID'])
                else:
                    queryByXtpID(Api, case_goal['cancel_xtpID'])
            else:
                result['用例检查状态'] = 'end'
                result['用例测试结果'] = False
                result['用例错误原因'] = rs['错误原因']
                result['用例错误源'] = rs['撤废']

    Api.trade.setQueryOrderHandle(on_QueryOrder)
    Api.trade.setTradeEventHandle(on_trade)
    Api.trade.setOrderEventHandle(on_order)
    Api.trade.setCancelOrderErrorHandle(on_cancelorder_error)


    # ------------------------------------------------------------------------------------------------------------------
    # 查询初始资金和持仓，当期望状态是'初始','未成交','部成','全成','已撤','废单'时，在下单前查询-----------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    if case_goal['期望状态'] in ('初始', '未成交', '部成', '全成', '部撤', '已撤', '废单','内部撤单'):
        setQueryInit(Api, wt_reqs)


    # ------------------------------------------------------------------------------------------------------------------
    # 下单---------------------------------------------------------------------------------------------------------------
    # 当期望状态为（部撤已报和已报待撤）时，在开市时间内下单（match程序需要配置为EqualHigh），其它期望状态直接下单
    # ------------------------------------------------------------------------------------------------------------------


    if case_goal['期望状态'] in ('已报待撤','部撤已报'):
        waitOpenTime()
        case_goal['xtp_ID'] = Api.trade.InsertOrder(wt_reqs)
    #如果期望状态为　内部撤单，则需要在休市时下单
    elif case_goal['期望状态']=='内部撤单':
        waitCloseTime()
        case_goal['xtp_ID'] = Api.trade.InsertOrder(wt_reqs)
    elif case_goal['期望状态'] == '未成交' and case_goal['是否是撤废']=='是' and case_goal['是否是集合竞价'] == '否':
        waitOpenTime()
        case_goal['xtp_ID'] = Api.trade.InsertOrder(wt_reqs)
        sleep(2)
    else:
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
    if case_goal['期望状态'] in ('初始','内部撤单'):
        queryByXtpID(Api,case_goal['xtp_ID'])


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
                if case_goal['期望状态'] == '初始':
                    if '是否是新股申购' in case_goal:
                        if 'bdhb_rs' in locals().keys():
                            rs = caseEndCheck(Api, bdhb_rs, bdquery_rs, None, None, case_goal['期望状态'], wt_reqs['price_type'])
                        else:
                            rs = caseEndCheck(Api, None, bdquery_rs, None, None, case_goal['期望状态'], wt_reqs['price_type'])
                            sleep(15)
                    else:
                        rs = caseEndCheck(Api, None, bdquery_rs, None, None, case_goal['期望状态'], wt_reqs['price_type'])
                elif getCancelType(Api, wt_reqs['price_type'],case_goal['期望状态']) is False and case_goal['是否是撤废'] == '否':
                    rs = caseEndCheck(Api, bdhb_rs, bdquery_rs, None, cjhb_rs, case_goal['期望状态'], wt_reqs['price_type'])
                elif case_goal['是否是撤废'] == '否':
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
        global sqbh
        sqbh = data['order_local_id']
        if '是否是新股申购' not in case_goal:
            if case_goal['期望状态'] in ('全成','内部撤单') or getCancelType(Api,wt_reqs['price_type'],case_goal['期望状态'])==False :
                logger.info('当前报单推送状态为未成交，等待..')
                bdCheck['status']='pending'

            else:
                time.sleep(2)
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

    # 当报单查询结果是‘初始’报单已提交
    if data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_INIT'] and data[
        'order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_INSERT_SUBMITTED']:
        # 期望状态是‘初始’，赋值queryEnd，检查报单查询数据
        if case_goal['期望状态']=='初始':
            xtp_id_init = data['order_xtp_id']
            setQueryEnd(Api,wt_reqs)
            bdQuecyCheck['检查状态'] = 'end'
            bdQuecyCheck['flag']=True
        elif case_goal['期望状态']=='内部撤单':
            # 当撤单xtpID不为０时，说明已经做过撤单申请
            if case_goal['cancel_xtpID'] != 0:
                bdQuecyCheck['检查状态'] = 'end'
                bdQuecyCheck['flag'] = True
            # 当撤单xtpID为０时，说明尚未做过撤单申请
            else:
                # 等待休市时间
                waitCloseTime()
                # 休市时段内撤单
                bdQuecyCheck['cancel_xtpID'] = Api.trade.CancelOrder(case_goal['xtp_ID'])
                bdQuecyCheck['检查状态'] = 'pending'
        else:
            bdQuecyCheck['检查状态'] = 'end'
            bdQuecyCheck['flag'] = False
            bdQuecyCheck['remark'] = '期望状态与报单状态不匹配'

    # 当报单查询结果是‘未成交’，报单已接受
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_NOTRADEQUEUEING'] and data['order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
                'XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:

        if '是否是新股申购' in case_goal:
            if case_goal['期望状态'] == '废单' and case_goal['是否是撤废'] == '否' and case_goal['是否是新股申购'] == '是':
                bdQuecyCheck['cancel_xtpID'] = Api.trade.CancelOrder(case_goal['xtp_ID'])
                bdQuecyCheck['检查状态'] = 'pending'
            else:
                setQueryEnd(Api, wt_reqs)
                bdQuecyCheck['检查状态'] = 'end'
                bdQuecyCheck['flag'] = True
        else:
            #当期望状态是‘未成交’时，赋值queryEnd，检查报单查询数据
            if case_goal['期望状态'] == '未成交' and case_goal['是否是撤废']=='否':
                setQueryEnd(Api,wt_reqs)
                bdQuecyCheck['检查状态'] = 'end'
                bdQuecyCheck['flag'] = True
            #当期望状态是‘已报待撤’，赋值queryInit，然后撤单，然后查询（撤单）报单(返回cancelXTPID后查询)
            elif case_goal['期望状态'] == '已报待撤':
                #当撤单xtpID不为０时，说明已经做过撤单申请
                if case_goal['cancel_xtpID']!=0:
                    bdQuecyCheck['检查状态'] = 'end'
                    bdQuecyCheck['flag'] = True
                #当撤单xtpID为０时，说明尚未做过撤单申请
                else:
                    setQueryInit(Api, wt_reqs)
                    #等待休市时间
                    waitCloseTime()
                    time.sleep(0.1)
                    #休市时段内撤单
                    bdQuecyCheck['cancel_xtpID'] = Api.trade.CancelOrder(case_goal['xtp_ID'])
                    bdQuecyCheck['检查状态'] = 'pending'
            # 当期望状态是’已撤‘,'撤废-交易所撤废'，撤单
            elif case_goal['期望状态'] == '已撤':
                #setQueryInit(Api, wt_reqs)
                bdQuecyCheck['cancel_xtpID']=Api.trade.CancelOrder(case_goal['xtp_ID'])
                bdQuecyCheck['检查状态'] = 'pending'
            elif '是否是新股申购' in case_goal:
                if case_goal['是否是新股申购'] == '是' and case_goal['期望状态'] == '未成交' and case_goal['是否是撤废']=='是':
                    setQueryInit(Api, wt_reqs)
                    bdQuecyCheck['cancel_xtpID'] = Api.trade.CancelOrder(case_goal['xtp_ID'])
                    bdQuecyCheck['检查状态'] = 'pending'

            # 当期望状态是’已撤‘,'撤废-交易所撤废'，撤单
            elif case_goal['期望状态'] == '未成交' and case_goal['是否是撤废']=='是' and case_goal['是否是集合竞价'] == '否':
                # 等待休市时间
                waitCloseTime()
                bdQuecyCheck['cancel_xtpID']=Api.trade.CancelOrder(case_goal['xtp_ID'])
                sleep(0.5)
                bdQuecyCheck['recancel_xtpID'] = Api.trade.CancelOrder(case_goal['xtp_ID'])
                bdQuecyCheck['检查状态'] = 'pending'
            elif case_goal['期望状态'] == '未成交' and case_goal['是否是撤废']=='是' and case_goal['是否是集合竞价'] == '是':
                setQueryInit(Api, wt_reqs)
                bdQuecyCheck['cancel_xtpID'] = Api.trade.CancelOrder(case_goal['xtp_ID'])
                bdQuecyCheck['检查状态'] = 'pending'
            #当期望状态是
            elif case_goal['期望状态'] in('部成','全成','部撤','部撤已报','内部撤单'):
                bdQuecyCheck['检查状态']='pending'
            elif case_goal['期望状态'] == '初始':
                if '是否是新股申购' in case_goal:
                    setQueryEnd(Api, wt_reqs)
                    bdQuecyCheck['检查状态'] = 'end'
                    bdQuecyCheck['flag'] = True
            else:
                bdQuecyCheck['检查状态'] = 'end'
                bdQuecyCheck['flag']=False
                bdQuecyCheck['remark']='期望状态与报单状态不匹配'

    # 当报单查询结果是‘部分成交’，报单已接受
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_PARTTRADEDQUEUEING'] and data[
        'order_submit_status'] ==Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
        #当期望状态是‘部成’时，检查报单查询数据
        if case_goal['期望状态'] == '部成':
            bdQuecyCheck['检查状态'] = 'end'
            bdQuecyCheck['flag'] = True
        #当期望状态是‘部撤已报’时，赋值queryInit，然后撤单，然后查询（撤单）报单
        elif case_goal['期望状态'] == '部撤已报':
            # 当撤单xtpID不为０时，说明已经做过撤单申请
            if case_goal['cancel_xtpID'] != 0:
                bdQuecyCheck['检查状态'] = 'end'
                bdQuecyCheck['flag'] = True
            # 当撤单xtpID为０时，说明尚未做过撤单申请
            else:
                setQueryInit(Api, wt_reqs)
                # 等待休市时间
                waitCloseTime()
                # 休市时段内撤单
                bdQuecyCheck['cancel_xtpID'] = Api.trade.CancelOrder(case_goal['xtp_ID'])
                bdQuecyCheck['检查状态'] = 'pending'
        # 当期望状态是‘部撤’时,撤单
        elif case_goal['期望状态'] == '部撤':
            if getCancelType(Api,wt_reqs['price_type'],case_goal['期望状态']):
                bdQuecyCheck['cancel_xtpID'] = Api.trade.CancelOrder(case_goal['xtp_ID'])
            bdQuecyCheck['检查状态'] = 'pending'
        #当期望状态是’全成，撤废‘，pending
        elif case_goal['期望状态'] in ('全成','撤废'):
            bdQuecyCheck['检查状态'] = 'pending'
        #其它
        else:
            bdQuecyCheck['检查状态'] = 'end'
            bdQuecyCheck['flag']=False
            bdQuecyCheck['remark']='期望状态与报单状态不匹配'

    # 当报单查询结果是‘初始’，撤单已提交
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_INIT'] and data['order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_CANCEL_SUBMITTED']:
        # 当期望状态是‘已报待撤’或‘部撤已报’，赋值queryEnd,检查报单查询数据
        if case_goal['期望状态'] in('已报待撤','部撤已报'):
            setQueryEnd(Api, wt_reqs)
            time.sleep(0.1)
            bdQuecyCheck['检查状态'] = 'end'
            bdQuecyCheck['flag'] = True
        #期望状态是'已撤','部撤','撤废'，等待
        elif case_goal['期望状态'] in('已撤','部撤','撤废'):
            bdQuecyCheck['检查状态'] = 'pending'
        #其它，终止
        else:
            bdQuecyCheck['检查状态'] = 'end'
            bdQuecyCheck['flag'] = False
            bdQuecyCheck['remark'] = '期望状态与报单状态不匹配'

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
            if case_goal['期望状态'] in('已撤','内部撤单') :
                setQueryEnd(Api,wt_reqs)
                bdQuecyCheck['检查状态'] = 'end'
                bdQuecyCheck['flag'] = True
            else:
                bdQuecyCheck['检查状态'] = 'end'
                bdQuecyCheck['flag'] = False
                bdQuecyCheck['remark'] = '期望状态与报单状态不匹配'

        # 撤单已接受
        elif data['order_submit_status'] ==Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_CANCEL_ACCEPTED']:
                sqbh_cd = data['order_local_id']
                bdQuecyCheck['检查状态'] = 'end'
                bdQuecyCheck['flag'] = True

    # 当报单查询结果是‘部撤’，
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_PARTTRADEDNOTQUEUEING']:
        # 报单已接受
        if data['order_submit_status'] ==Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
            if case_goal['期望状态'] == '部撤':
                setQueryEnd(Api,wt_reqs)
                bdQuecyCheck['检查状态'] = 'end'
                bdQuecyCheck['flag'] = True
            else:
                bdQuecyCheck['检查状态'] = 'end'
                bdQuecyCheck['flag'] = False
                bdQuecyCheck['remark'] = '期望状态与报单状态不匹配'
        # 撤单已接受
        elif data['order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_CANCEL_ACCEPTED']:
            sqbh_cd = data['order_local_id']
            bdQuecyCheck['检查状态'] = 'end'
            bdQuecyCheck['flag'] = True

    # 当报单查询结果是‘撤废’,撤单已拒绝
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_REJECTED'] and data['order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_CANCEL_REJECTED']:
            # 当期望状态是‘撤废’，先进行赋值queryEnd,然后报单查询数据处理
            if case_goal['是否是撤废'] == '是':
                setQueryEnd(Api, wt_reqs)
                bdQuecyCheck['检查状态'] = 'end'
                bdQuecyCheck['flag'] = True
            elif '是否是新股申购' in case_goal:
                if case_goal['是否是新股申购'] == '是':
                    setQueryEnd(Api, wt_reqs)
                    bdQuecyCheck['检查状态'] = 'end'
                    bdQuecyCheck['flag'] = True
            else:
                bdQuecyCheck['检查状态'] = 'end'
                bdQuecyCheck['flag'] = False
                bdQuecyCheck['remark'] = '期望状态与报单状态不匹配'

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
    # print stkasset0['data']
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

#-----------------------------------------------------------------------------------------------------------------------
# 定义函数：（撤废）根据case_goal来判断当报单推送是未成交时，是否进行报单查询，返回值为True或False
#----------------------------------------------------------------------------------------------------------------------
# def isQueryOrder_For_NoMatch(Api,price_type,case_goal):
#     flag=False
#     if case_goal['期望状态'] in('全成','内部撤单'):
#         flag=True
#     else:
#         if getCancelType(Api,price_type,case_goal['期望状态'])==False:
#             flag=True
#         else:


