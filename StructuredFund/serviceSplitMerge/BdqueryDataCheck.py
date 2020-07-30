#!/usr/bin/python
# -*- encoding: utf-8 -*-
import time
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/StructuredFund/serviceSplitMerge")
from FundStkCheckSplitMerge import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from log import *
import ServiceConfig
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *

#获取配置参数:废单是否校验errID和err_msg
is_check_errId_bdQuery=ServiceConfig.IS_CHECK_ERRID_FROM_BDQUERY
is_Check_errmsg_bdQuery=ServiceConfig.IS_CHECK_ERRMSG_FROM_BDQUERY

#报单查询结果业务处理方法
def BdqueryDataCheck(Api,wt_reqs,case_goal,data,error,QueryInit,QueryEnd):
    # 定义测试结果参数
    result = {
        '报单检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
        '报单类型':'',
        '报单状态': data['order_status'],
        '提交状态': data['order_submit_status'],
        '成交数量': data['qty_traded'],
        '剩余数量': data['qty_left'],
        '成交金额': data['trade_amount'],
        '委托价格': data['price'],
        'xtpID': data['order_xtp_id'],
        '委托时间': data['insert_time'],
        '最后修改时间': data['update_time'],
        '撤销时间': data['cancel_time'],
        'cancel_xtpID': data['order_cancel_xtp_id'],
        'Err_code': error['error_id'],
        'ErrMsg': error['error_msg'],
    }
    # --判断查询的报单为报单类型还是撤单类型
    # --如果报单为报单类型
    if data['order_submit_status'] in (
            Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_INSERT_SUBMITTED'],
            Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED'],
            Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_INSERT_REJECTED']):
        logger.info('当前为报单类型data')
        result['报单类型'] = '报单'
        # (委托入参)公共业务检查
        public_result = public_Handle(Api,wt_reqs, data,case_goal)
        if public_result['报单检查状态'] == 'pending' and public_result['测试结果']:
            bdQuery_result = bd_type_Handle(Api, wt_reqs, case_goal, data, error, QueryInit, QueryEnd)
            result['报单检查状态'] = bdQuery_result['报单检查状态']
            result['测试结果'] = bdQuery_result['测试结果']
            result['错误信息'] = bdQuery_result['错误信息']
        else:
            result['报单检查状态'] = public_result['报单检查状态']
            result['测试结果'] = public_result['测试结果']
            result['错误信息'] = public_result['错误信息']
    else:
        result['报单检查状态'] = 'end'
        result['测试结果'] = False
        result['错误信息'] = '报单或撤单的提交状态不存在！'

    logger.info('报单查询数据检查结束，检查结果如下')
    dictLogging(result)
    return result

#-----------------------------------------------------------------------------------------------------------------------
#--定义（委托入参）公共业务检查
#-----------------------------------------------------------------------------------------------------------------------
def public_Handle(Api,wt_reqs,data,case_goal):
    # 定义测试结果参数
    public_result = {
        '报单检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
    }

    # 判断证券代码是否一致
    if data['ticker'] != wt_reqs['ticker']:
        logger.error('错误，报单返回的证券代码与原委托不一致，委托证券代码和报单回报证券代码分别是'+wt_reqs['ticker']+data['ticker'])
        public_result['报单检查状态'] = 'end'
        public_result['测试结果'] = False
        public_result['错误信息'] = '报单返回的证券代码与原委托不一致'

    # 判断市场是否一致
    elif data['market'] != wt_reqs['market']:
        logger.error('错误，报单返回的市场与原委托不一致，原委托市场和报单回报市场分别是'+str(wt_reqs['market'])+','+str(data['market']))
        public_result['报单检查状态'] = 'end'
        public_result['测试结果'] = False
        public_result['错误信息'] = '报单返回的市场与原委托不一致'

    # 判断委托方向是否一致
    elif data['side'] != wt_reqs['side']:
        logger.error('报单返回的委托方向与原委托不一致')
        public_result['报单检查状态'] = 'end'
        public_result['测试结果'] = False
        public_result['错误信息'] = '报单返回的市场与原委托不一致'

    # 判断委托数量是否一致
    elif data['quantity'] != wt_reqs['quantity']:
        logger.error(
            '错误，报单返回的委托数量和原委托数量不一致，原委托数量和报单返回的委托数量分别是' + str(wt_reqs['quantity']) + ',' + str(data['quantity']))
        public_result['报单检查状态'] = 'end'
        public_result['测试结果'] = False
        public_result['错误信息'] = '报单返回的价格条件与原委托不一致'
    else:
        public_result['报单检查状态'] = 'pending'
        public_result['测试结果'] = True
        public_result['错误信息'] = ''

    return public_result

#-----------------------------------------------------------------------------------------------------------------------
#--报单为报单类型的业务处理
#-----------------------------------------------------------------------------------------------------------------------
def bd_type_Handle(Api,wt_reqs,case_goal,data,error,QueryInit,QueryEnd):
    # 定义测试结果参数
    bdQuery_result = {
        '报单检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
    }
    # --判断报单返回的data
    # 判断xtpID是否一致
    if data['order_xtp_id'] != case_goal['xtp_ID']:
        logger.error('错误，报单返回的xtpID与原委托不一致，下单xtp_ID和报单回报xtp_ID分别是'+str(case_goal['xtp_ID'])+','+str(data['order_xtp_id']))
        bdQuery_result['报单检查状态'] = 'end'
        bdQuery_result['测试结果'] = False
        bdQuery_result['错误信息'] = '报单返回的xtpID与原委托不一致'

    # --如果报单查询是‘未成交’状态的执行如下
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_NOTRADEQUEUEING']:
        if data['order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
            'XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
            logger.info('报单查询状态为未成交,提交状态为已提交，'+str(data['order_status'])+','+str(data['order_submit_status']))
            # 如果期望状态是未成交，执行
            if case_goal['期望状态'] == '未成交':
                # 检查资金持仓是否正确
                fundstkcheck_rs = fundStkCheck_nomatch(Api, QueryInit, QueryEnd, wt_reqs, case_goal)
                # 如果资金持仓检查正确，则执行报单数据检查，否则结束
                if fundstkcheck_rs['检查状态'] == 'end' and fundstkcheck_rs['测试结果']:
                    # 报单数据检查
                    rs = no_match(wt_reqs, case_goal, data, error)
                    bdQuery_result['报单检查状态'] = rs['报单检查状态']
                    bdQuery_result['测试结果'] = rs['测试结果']
                    bdQuery_result['错误信息'] = rs['错误信息']
                else:
                    bdQuery_result['报单检查状态'] = fundstkcheck_rs['检查状态']
                    bdQuery_result['测试结果'] = fundstkcheck_rs['测试结果']
                    bdQuery_result['错误信息'] = fundstkcheck_rs['错误信息']
            elif case_goal['期望状态'] in ('废单'):
                bdQuery_result['报单检查状态'] = 'pending'
                bdQuery_result['测试结果'] = False
                bdQuery_result['错误信息'] = ''
            else:
                logger.error('期望状态和报单状态、提交状态不匹配，期望状态、报单状态、提交状态分别为'+str(case_goal['期望状态'])+','+str(data['order_status'])+','+str(data['order_submit_status']))
                bdQuery_result['报单检查状态'] = 'end'
                bdQuery_result['测试结果'] = False
                bdQuery_result['错误信息'] = '期望状态和报单状态、提交状态不匹配'
        else:
            bdQuery_result['报单检查状态'] = 'end'
            bdQuery_result['测试结果'] = False
            bdQuery_result['错误信息'] = '报单提交状态不正确'

    # --如果是废单状态的，执行如下
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_REJECTED']:
        if data['order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_INSERT_REJECTED']:
            logger.info('报单查询状态为废单，'+str(data['order_status']))
            # 期望状态如果是为废单，执行
            if case_goal['期望状态'] == '废单':
                # 检查资金持仓是否正确
                fundstkcheck_rs = fundStkCheck_other(QueryInit, QueryEnd)
                # 如果资金持仓检查正确，则执行报单数据检查，否则结束
                if fundstkcheck_rs['检查状态'] == 'end' and fundstkcheck_rs['测试结果']:
                    # 报单数据检查
                    rs = reject(wt_reqs, case_goal, data, error)
                    bdQuery_result['报单检查状态'] = rs['报单检查状态']
                    bdQuery_result['测试结果'] = rs['测试结果']
                    bdQuery_result['错误信息'] = rs['错误信息']
                else:
                    bdQuery_result['报单检查状态'] = fundstkcheck_rs['检查状态']
                    bdQuery_result['测试结果'] = fundstkcheck_rs['测试结果']
                    bdQuery_result['错误信息'] = fundstkcheck_rs['错误信息']
            else:
                logger.error('期望状态和报单状态、提交状态不匹配，期望状态、报单状态、提交状态分别为' + str(case_goal['期望状态']) + ',' + str(
                    data['order_status']) + ',' + str(data['order_submit_status']))
                bdQuery_result['报单检查状态'] = 'end'
                bdQuery_result['测试结果'] = False
                bdQuery_result['错误信息'] = '期望状态和报单状态、提交状态不匹配'
        else:
            bdQuery_result['报单检查状态'] = 'end'
            bdQuery_result['测试结果'] = False
            bdQuery_result['错误信息'] = '报单提交状态不正确'

    # --如果是未知状态的，执行如下
    else:
        rs = unknown(data)
        bdQuery_result['报单检查状态'] = rs['报单检查状态']
        bdQuery_result['测试结果'] = rs['测试结果']
        bdQuery_result['错误信息'] = rs['错误信息']
        logger.error('当前报单查询返回的状态未知'+str(data['order_status']))

    return bdQuery_result

#-----------------------------------------------------------------------------------------------------------------------
#--报单查询--未成交-校验
#-----------------------------------------------------------------------------------------------------------------------
def no_match(wt_reqs, case_goal, data, error):
    logger.info('正在进行未成交状态的报单查询业务校验')
    # 定义测试结果参数
    bdquery_result = {
        '报单检查状态': 'init',
        '测试结果': '',
        '错误信息': '',
    }
    # 判断成交数量是否为０
    if data['qty_traded'] != 0:
        logger.error('未成交状态的报单查询的成交数量应该为０，实际成交数量为'+str(data['qty_traded']))
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = False
        bdquery_result['错误信息'] = '未成交状态的报单查询的成交数量应该为０'
    # 判断成交金额是否为０
    elif data['trade_amount'] != 0:
        logger.error('未成交状态的报单成交金额应该为０，实际成交数量为'+str(data['trade_amount']))
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = False
        bdquery_result['错误信息'] = '未成交状态的报单查询的成交金额应该为０'
    # 判断剩余数量是否等于委托数量
    elif data['qty_left'] != wt_reqs['quantity']:
        logger.error('未成交状态的报单剩余数量和委托数量不相等，委托数量和报单剩余数量分别为'+str( wt_reqs['quantity'])+','+str(data['qty_left']))
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = False
        bdquery_result['错误信息'] = '未成交状态的报单查询的剩余数量和委托数量不相等'
    # 判断报单中的委托时间不能为空
    elif data['insert_time'] == 0:
        logger.error('错误，报单查询的委托时间不能为空，报单返回的委托时间为'+str(data['insert_time']))
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = False
        bdquery_result['错误信息'] = '报单查询的委托时间不能为空'
    # 判断其它项：最后修改时间，撤销时间，撤单xtpID,err_code,Err_Msg
    elif data['update_time'] != 0 and data['cancel_time'] != 0 and data['order_cancel_xtp_id'] != 0 and error[
        'error_id'] != 0 and error['error_msg'] != '':
        logger.error('错误，请检查最后修改时间，撤单时间，撤单xtpID,err_code,err_msg!它们的值分别是：' + str(data['update_time']) + ',' + str(
            data['cancel_time']) + ',' + str(data['order_cancel_xtp_id']) + ',' + str(error['error_id']) + ',' + str(error['error_msg']))
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = False
        bdquery_result['错误信息'] = '错误，请检查报单查询的最后修改时间，撤单时间，撤单xtpID,err_code,err_msg!'
    else:
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = True
        logger.info('未成交状态的报单查询业务校验正确')
    return bdquery_result

#-----------------------------------------------------------------------------------------------------------------------
#--报单查询--废单-校验
#-----------------------------------------------------------------------------------------------------------------------
def reject(wt_reqs,case_goal,data,error):
    logger.info('正在进行废单状态的报单查询业务校验')
    bdquery_result = {
        '报单检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
    }
    # 判断成交数量是否为０
    if data['qty_traded'] != 0:
        logger.error('错误，废单状态报单的成交数量应为０，返回报单的成交数量为'+str(data['qty_traded']))
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = False
        bdquery_result['错误信息'] = '废单状态报单的成交数量应为０'
    # 判断未成交数量是否等于委托数量
    elif data['qty_left'] != wt_reqs['quantity']:
        logger.error('错误，报单返回的未成交数量应等于委托数量，返回报单的未成交数量和原委托数量分别是'+str(wt_reqs['quantity'])+','+str(data['qty_left']))
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = False
        bdquery_result['错误信息'] = '报单返回的未成交数量应等于委托数量'
    # 判断成交金额是否是０
    elif data['trade_amount'] != 0.0:
        logger.error('错误，废单状态报单的成交金额应为０，返回报单的成交金额为'+str(data['trade_amount']))
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = False
        bdquery_result['错误信息'] = '废单状态报单的成交金额应为０'
    # 判断报单中的委托时间不能为空
    elif data['insert_time'] == 0:
        logger.error('错误，报单委托时间不能为空，报单返回的委托时间为'+str(data['insert_time']))
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = False
        bdquery_result['错误信息'] = '报单委托时间不能为空'
    # 判断其它项：最后修改时间，撤销时间，撤单xtpID
    elif data['update_time'] != 0 and data['cancel_time'] != 0 and data['order_cancel_xtp_id'] != 0:
        logger.error('错误，请检查最后修改时间，撤单时间，撤单xtpID!它们的值分别是：'+str(data['update_time'])+','+str(data['cancel_time'])+','+str(data['order_cancel_xtp_id']))
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = False
        bdquery_result['错误信息'] = '错误，请检查最后修改时间，撤单时间，撤单xtpID!'
    else:
        #errID和errmsg都不校验
        if is_check_errId_bdQuery==False:
            bdquery_result['报单检查状态'] = 'end'
            bdquery_result['测试结果'] = True
            logger.info('废单状态的报单查询业务校验正确')
        #只校验errID
        elif is_check_errId_bdQuery==True and is_Check_errmsg_bdQuery==False:
            #判断废单的error_id与期望的是否一致
            if error['error_id'] != case_goal['errorID']:
                logger.error('报单的error_id与用例期望的不一致，期望和实际的error_id分别是'+str(case_goal['errorID'])+','+str(error['error_id']))
                bdquery_result['报单检查状态'] = 'end'
                bdquery_result['测试结果'] = False
                bdquery_result['错误信息'] = '报单的error_id与用例期望的不一致'
            else:
                bdquery_result['报单检查状态'] = 'end'
                bdquery_result['测试结果'] = True
                logger.info('废单状态的报单查询业务校验正确')
        # errID和errmsg都校验
        elif is_check_errId_bdQuery == True and is_Check_errmsg_bdQuery == True:
            # 判断废单的error_id与期望的是否一致
            if error['error_id'] != case_goal['errorID']:
                logger.error('报单的error_id与用例期望的不一致，期望和实际的error_id分别是' + str(case_goal['errorID']) + ',' + str(error['error_id']))
                bdquery_result['报单检查状态'] = 'end'
                bdquery_result['测试结果'] = False
                bdquery_result['错误信息'] = '报单的error_id与用例期望的不一致'
            #判断废单的error_msg与期望的是否一致
            elif error['error_msg'] != case_goal['errorMSG']:
                logger.error('报单的error_msg与用例期望的不一致，期望和实际的error_msg分别是'+case_goal['errorMSG']+','+error['error_msg'])
                bdquery_result['报单检查状态'] = 'end'
                bdquery_result['测试结果'] = False
                bdquery_result['错误信息'] = '报单的error_msg与用例期望的不一致'
            else:
                bdquery_result['报单检查状态'] = 'end'
                bdquery_result['测试结果'] = True
                logger.info('废单状态的报单查询业务校验正确')

    return bdquery_result


#-----------------------------------------------------------------------------------------------------------------------
#--报单查询-状态未知-校验
#-----------------------------------------------------------------------------------------------------------------------
def unknown(data):
    bdquery_result = {
        '报单检查状态':'init',
        '测试结果': False,
        '错误信息': '',
    }

    bdquery_result['报单检查状态'] = 'end'
    bdquery_result['测试结果'] = False
    bdquery_result['错误信息'] = '报单回报状态未知'

    return bdquery_result

#-----------------------------------------------------------------------------------------------------------------------
#--撤单报单查询-状态已撤-校验
#-----------------------------------------------------------------------------------------------------------------------
def cdQuery_allCancle(wt_reqs, data, error):
    logger.info('正在进行撤单报单查询已撤状态业务校验')
    cdquery_result = {
        '报单检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
    }
    # 已撤状态的撤单报单，成交数量应等于委托数量
    if data['qty_traded'] != wt_reqs['quantity']:
        logger.error('错误，已撤状态的撤单报单，成交数量应等于委托数量，委托数量和返回报单的成交数量分别为'+str(wt_reqs['quantity'])+','+str(data['qty_traded']))
        cdquery_result['报单检查状态'] = 'end'
        cdquery_result['测试结果'] = False
        cdquery_result['错误信息'] = '已撤状态的撤单报单，成交数量应等于委托数量'
    # 判断剩余成交数量是否等于0
    elif data['qty_left'] != 0:
        logger.error('错误，已撤状态的撤单报单查询，剩余数量应等于０，返回报单的剩余成交数量是'+str(wt_reqs['quantity'])+','+str(data['qty_left']))
        cdquery_result['报单检查状态'] = 'end'
        cdquery_result['测试结果'] = False
        cdquery_result['错误信息'] = '已撤状态的撤单报单查询，剩余数量应等于０'
    # 判断成交金额是否是０
    elif data['trade_amount'] != 0.0:
        logger.error('错误，已撤状态的撤单报单查询，成交金额应为０，返回报单的成交金额为'+str(data['trade_amount']))
        cdquery_result['报单检查状态'] = 'end'
        cdquery_result['测试结果'] = False
        cdquery_result['错误信息'] = '已撤状态的撤单报单查询，成交金额应为０'
    elif data['insert_time'] == 0:
        logger.error('错误，已撤状态的撤单报单查询，委托时间不能为空，报单返回的委托时间为'+str(data['insert_time']))
        cdquery_result['报单检查状态'] = 'end'
        cdquery_result['测试结果'] = False
        cdquery_result['错误信息'] = '已撤状态的撤单报单查询，委托时间不能为空'
    # 撤销时间不能为０
    elif data['cancel_time'] == 0:
        logger.error('错误，已撤状态的撤单报单查询，撤单时间不能为空，报单返回的撤单时间为'+str(data['cancel_time']))
        cdquery_result['报单检查状态'] = 'end'
        cdquery_result['测试结果'] = False
        cdquery_result['错误信息'] = '已撤状态的撤单报单查询，撤单时间不能为空'
    # 判断其它项：最后修改时间，撤单xtpID,err_code,Err_Msg
    elif data['update_time'] != 0 and data['order_cancel_xtp_id'] != 0 and error[
        'error_id'] != 0 and error['error_msg'] != '':
        logger.error(
            '错误，请检查部撤状态的查询撤单报单的最后修改时间，撤单xtpID,err_code,err_msg!它们的值分别是：' + str(data['update_time']) + ',' + str(
                data['order_cancel_xtp_id']) + ',' + str(error['error_id']) + ',' + error['error_msg'])
        cdquery_result['报单检查状态'] = 'end'
        cdquery_result['测试结果'] = False
        cdquery_result['错误信息'] = '错误，请检查已撤状态的查询撤单报单的最后修改时间，撤单xtpID,err_code,err_msg!'
    else:
        cdquery_result['报单检查状态'] = 'end'
        cdquery_result['测试结果'] = True
        logger.info('撤单报单查询已撤状态业务校验正确')

    return cdquery_result

#-----------------------------------------------------------------------------------------------------------------------
#--撤单类型报单查询-状态撤废-校验
#-----------------------------------------------------------------------------------------------------------------------
def cdQueryCancleRejected(wt_reqs,case_goal,data,error):
    logger.info('撤单查询废单状态业务处理')
    cdquery_result = {
        '报单检查状态': 'init',
        '测试结果': True,
        '错误信息': '',
    }
    # 判断成交数量是否为０
    if data['qty_traded'] != 0:
        logger.error('错误，废单状态报单的成交数量应为０，返回报单的成交数量为' + str(data['qty_traded']))
        cdquery_result['报单检查状态'] = 'end'
        cdquery_result['测试结果'] = False
        cdquery_result['错误信息'] = '废单状态报单的成交数量应为０'
    # 判断未成交数量是否等于委托数量
    elif data['qty_left'] != 0:
        logger.error(
            '错误，报单返回的未成交数量应等于0，返回报单的未成交数量是' + str(wt_reqs['quantity']))
        cdquery_result['报单检查状态'] = 'end'
        cdquery_result['测试结果'] = False
        cdquery_result['错误信息'] = '报单返回的未成交数量应等于0'
    # 判断成交金额是否是０
    elif data['trade_amount'] != 0.0:
        logger.error('错误，废单状态报单的成交金额应为０，返回报单的成交金额为' + str(data['trade_amount']))
        cdquery_result['报单检查状态'] = 'end'
        cdquery_result['测试结果'] = False
        cdquery_result['错误信息'] = '废单状态报单的成交金额应为０'
    # 判断报单中的委托时间不能为空
    elif data['insert_time'] == 0:
        logger.error('错误，报单委托时间不能为空，报单返回的委托时间为' + str(data['insert_time']))
        cdquery_result['报单检查状态'] = 'end'
        cdquery_result['测试结果'] = False
        cdquery_result['错误信息'] = '报单委托时间不能为空'
    # 判断其它项：最后修改时间，撤销时间，撤单xtpID
    elif data['update_time'] != 0 and data['cancel_time'] != 0 and data['order_cancel_xtp_id'] != 0:
        logger.error('错误，请检查最后修改时间，撤单时间，撤单xtpID!它们的值分别是：' + str(data['update_time']) + ',' + str(
            data['cancel_time']) + ',' + str(data['order_cancel_xtp_id']))
        cdquery_result['报单检查状态'] = 'end'
        cdquery_result['测试结果'] = False
        cdquery_result['错误信息'] = '错误，请检查最后修改时间，撤单时间，撤单xtpID!'
    else:
        # errID和errmsg都不校验
        if is_check_errId_bdQuery == False:
            cdquery_result['报单检查状态'] = 'end'
            cdquery_result['测试结果'] = True
            logger.info('废单状态的报单查询业务校验正确')
        # 只校验errID
        elif is_check_errId_bdQuery == True and is_Check_errmsg_bdQuery == False:
            # 判断废单的error_id与期望的是否一致
            if error['error_id'] != case_goal['errorID']:
                logger.error(
                    '报单的error_id与用例期望的不一致，期望和实际的error_id分别是' + str(case_goal['errorID']) + ',' + str(error['error_id']))
                cdquery_result['报单检查状态'] = 'end'
                cdquery_result['测试结果'] = False
                cdquery_result['错误信息'] = '报单的error_id与用例期望的不一致'
            else:
                cdquery_result['报单检查状态'] = 'end'
                cdquery_result['测试结果'] = True
                logger.info('废单状态的报单查询业务校验正确')
        # errID和errmsg都校验
        elif is_check_errId_bdQuery == True and is_Check_errmsg_bdQuery == True:
            # 判断废单的error_id与期望的是否一致
            if error['error_id'] != case_goal['errorID']:
                logger.error(
                    '报单的error_id与用例期望的不一致，期望和实际的error_id分别是' + str(case_goal['errorID']) + ',' + str(error['error_id']))
                cdquery_result['报单检查状态'] = 'end'
                cdquery_result['测试结果'] = False
                cdquery_result['错误信息'] = '报单的error_id与用例期望的不一致'
            # 判断废单的error_msg与期望的是否一致
            elif error['error_msg'] != case_goal['errorMSG']:
                logger.error(
                    '报单的error_msg与用例期望的不一致，期望和实际的error_msg分别是' + case_goal['errorMSG'] + ',' + error['error_msg'])
                cdquery_result['报单检查状态'] = 'end'
                cdquery_result['测试结果'] = False
                cdquery_result['错误信息'] = '报单的error_msg与用例期望的不一致'
            else:
                cdquery_result['报单检查状态'] = 'end'
                cdquery_result['测试结果'] = True
                logger.info('废单状态的报单查询业务校验正确')

    return cdquery_result


