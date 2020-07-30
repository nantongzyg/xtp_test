#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
sys.path.append("/home/yhl2/workspace/xtp_test")
from service.log import *
from cetf_fund_stk_check import fund_stk_check_other

#获取配置参数:废单是否校验errID和err_msg
is_check_errId_bdQuery=ServiceConfig.IS_CHECK_ERRID_FROM_BDQUERY
is_Check_errmsg_bdQuery=ServiceConfig.IS_CHECK_ERRMSG_FROM_BDQUERY

def cetf_bdquery_datacheck(Api,wt_reqs,case_goal,data,error,QueryInit,
                         QueryEnd,component_stk_info,cash_substitute_amount):
    """报单查询结果的业务及数据校验函数"""

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
        '委托价格':data['price'],
        'xtpID':data['order_xtp_id'],
        '委托时间':data['insert_time'],
        '最后修改时间':data['update_time'],
        '撤销时间':data['cancel_time'],
        'cancel_xtpID':data['order_cancel_xtp_id'],
        'Err_code':error['error_id'],
        'ErrMsg':error['error_msg'],
    }

    # --判断查询的报单为报单类型还是撤单类型
    # --如果报单为报单类型
    if data['order_submit_status'] in (
            Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
                'XTP_ORDER_SUBMIT_STATUS_INSERT_SUBMITTED'],
            Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
                'XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED'],
            Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
                'XTP_ORDER_SUBMIT_STATUS_INSERT_REJECTED']):
        logger.info('当前为报单类型data')
        result['报单类型'] = '报单'
        # (委托入参)公共业务检查
        public_result = cetf_bdquery_public_handle(Api, wt_reqs, data)
        # 如果公共业务检查通过，进行报单数据检查；否则结束检查，返回错误信息
        if public_result['测试结果'] == True:
            bdQuery_result = cetf_bdquery_type_Handle(Api, wt_reqs, case_goal, data,
                                                error,QueryInit, QueryEnd,
                                                component_stk_info,
                                                cash_substitute_amount)
            result['报单检查状态'] = bdQuery_result['报单检查状态']
            result['测试结果'] = bdQuery_result['测试结果']
            result['错误信息'] = bdQuery_result['错误信息']
        else:
            result['报单检查状态'] = 'end'
            result['测试结果'] = public_result['测试结果']
            result['错误信息'] = public_result['错误信息']

    # --如果报单为撤单类型
    elif data['order_submit_status'] in (
            Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
                'XTP_ORDER_SUBMIT_STATUS_CANCEL_SUBMITTED'],
            Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
                'XTP_ORDER_SUBMIT_STATUS_CANCEL_REJECTED'],
            Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
                'XTP_ORDER_SUBMIT_STATUS_CANCEL_ACCEPTED']):
        logger.info('当前为撤单类型data')
        result['报单类型'] = '撤单'
        # (委托入参)公共业务检查
        public_result = cetf_bdquery_public_handle(Api, wt_reqs, data)
        # 如果公共业务检查通过，进行报单数据检查；否则结束检查，返回错误信息
        if public_result['测试结果'] == True:
            cdQuery_result = cetf_cdquery_type_handle(Api, wt_reqs, case_goal, data,
                                                 error, QueryInit, QueryEnd,
                                                 component_stk_info)
            result['报单检查状态'] = cdQuery_result['报单检查状态']
            result['测试结果'] = cdQuery_result['测试结果']
            result['错误信息'] = cdQuery_result['错误信息']
        else:
            result['报单检查状态'] = 'end'
            result['测试结果'] = public_result['测试结果']
            result['错误信息'] = public_result['错误信息']
    # 如果非报单和撤单类型，错误
    else:
        result['报单检查状态'] = 'end'
        result['测试结果'] = False
        result['错误信息'] = '报单或撤单的提交状态不存在！'

    logger.info('报单查询数据检查结束，检查结果如下')
    dictLogging(result)
    return result


#-------------------------------------------------------------------------------
#--定义（委托入参）公共业务检查
#-------------------------------------------------------------------------------
def cetf_bdquery_public_handle(Api,wt_reqs,data):
    """报单查询委托入参公共业务检查，检查报单查询返回结果和委托入参wt_reqs是否一致：
    1.判断证券代码是否一致
    2.判断市场是否一致
    3.判断委托方向是否一致
    4.判断价格条件是否是限价(下单后自动转换成限价)
    5.判断委托数量是否一致"""
    # 定义测试结果参数
    public_result = {
        '测试结果': False,
        '错误信息': '',
    }
    # 判断证券代码是否一致
    if data['ticker'] != wt_reqs['ticker']:
        logger.error('错误，报单查询返回的证券代码与原委托不一致，'
                     '原委托证券代码和报单查询证券代码分别是'
                     +wt_reqs['ticker']+data['ticker'])
        public_result['测试结果'] = False
        public_result['错误信息'] = '报单查询返回的证券代码与原委托不一致'

    # 判断市场是否一致
    elif data['market'] != wt_reqs['market']:
        logger.error('错误，报单查询返回的市场与原委托不一致，'
                     '原委托市场和报单查询市场分别是'
                     +str(wt_reqs['market'])+','+str(data['market']))
        public_result['测试结果'] = False
        public_result['错误信息'] = '报单查询返回的市场与原委托不一致'

    # 判断委托方向是否一致
    elif data['side'] != wt_reqs['side']:
        logger.error('报单查询返回的委托方向与原委托不一致')
        public_result['测试结果'] = False
        public_result['错误信息'] = '报单查询返回的市场与原委托不一致'

    # 判断价格条件是否正确，ETF申赎市价订单会被自动转化为限价订单
    elif data['price_type'] != \
            Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT']:
        logger.error('错误，报单查询返回的价格条件为:' + str(data['price_type'])
                     + '; ETF申赎的价格类型应为限价！')
        public_result['测试结果'] = False
        public_result['错误信息'] = 'ETF申赎报单查询返回的价格条件非限价'

    # 判断委托数量是否一致
    elif data['quantity'] != wt_reqs['quantity']:
        logger.error('错误，报单查询返回的委托数量和原委托数量不一致，'
            '原委托数量和报单查询返回的委托数量分别是' + str(wt_reqs['quantity'])
            + ',' + str(data['quantity']))
        public_result['测试结果'] = False
        public_result['错误信息'] = '报单查询返回的价格条件与原委托不一致'

    else:
        public_result['测试结果'] = True
        public_result['错误信息'] = ''

    return public_result


#-------------------------------------------------------------------------------
#--报单为报单类型的业务处理
#-------------------------------------------------------------------------------
def cetf_bdquery_type_Handle(Api,wt_reqs,case_goal,data,error,
                       QueryInit,QueryEnd,component_stk_info,
                       cash_substitute_amount):
    """报单查询返回的报单类型为'报单'的业务处理"""
    # 定义测试结果参数
    bdQuery_result = {
        '报单检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
    }
    # --判断报单返回的data
    # 判断xtpID是否一致
    if data['order_xtp_id'] != case_goal['xtp_ID']:
        logger.error('错误，报单查询返回的xtpID与原委托不一致，'
                     '下单xtp_ID和报单查询的xtp_ID分别是'+str(case_goal['xtp_ID'])
                     +','+str(data['order_xtp_id']))
        bdQuery_result['报单检查状态'] = 'end'
        bdQuery_result['测试结果'] = False
        bdQuery_result['错误信息'] = '报单查询返回的xtpID与原委托不一致'

    # --下面是根据报单的状态调用各自对应的校验方法
    # -如果报单查询是‘初始’状态的执行如下
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE[
        'XTP_ORDER_STATUS_INIT']:
        if data['order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
            'XTP_ORDER_SUBMIT_STATUS_INSERT_SUBMITTED']:
            logger.info('报单查询状态为初始,提交状态为已提交：' + str(
                data['order_status']) + ',' + str(data['order_submit_status']))
            # 如果期望状态是'初始'，执行
            if case_goal['期望状态'] == '初始':
                TODO
            else:
                bdQuery_result['报单检查状态'] = 'pending'
                bdQuery_result['测试结果'] = False
                bdQuery_result['错误信息'] = ''
        else:
            logger.error('报单提交状态不正确')
            bdQuery_result['报单检查状态'] = 'end'
            bdQuery_result['测试结果'] = False
            bdQuery_result['错误信息'] = '报单提交状态不正确'

    # --如果报单查询是‘未成交’状态的执行如下
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE[
        'XTP_ORDER_STATUS_NOTRADEQUEUEING']:
        if data['order_submit_status'] == \
                Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
                    'XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
            logger.info('报单查询状态为未成交,提交状态为已接受，' + str(
                data['order_status']) + ',' + str(
                data['order_submit_status']))
            # 如果期望状态是未成交，执行
            if case_goal['期望状态'] == '未成交':
                TODO
            elif case_goal['期望状态'] == '全成':
                bdQuery_result['报单检查状态'] = 'pending'
                bdQuery_result['测试结果'] = False
                bdQuery_result['错误信息'] = ''
            else:
                logger.error('期望状态和报单状态、提交状态不匹配，期望状态、报单状态、'
                             '提交状态分别为' + str(case_goal['期望状态']) + ','
                             + str(data['order_status']) + ',' + str(
                            data['order_submit_status']))
                bdQuery_result['报单检查状态'] = 'end'
                bdQuery_result['测试结果'] = False
                bdQuery_result['错误信息'] = '期望状态和报单状态、提交状态不匹配'
        else:
            bdQuery_result['报单检查状态'] = 'end'
            bdQuery_result['测试结果'] = False
            bdQuery_result['错误信息'] = '报单提交状态不正确'


    # --如果报单查询是全成状态的，执行如下
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE[
        'XTP_ORDER_STATUS_ALLTRADED']:
        if data['order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
            'XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
            logger.info('报单查询状态为全部成交，提交状态为已接受'+str(
                data['order_status'])+','+str(data['order_submit_status']))
            # 期望状态如果是为全成，执行
            if case_goal['期望状态'] == '全成':
                rs = CHECK.all_match(wt_reqs, data, error)
                bdQuery_result['报单检查状态'] = rs['报单检查状态']
                bdQuery_result['测试结果'] = rs['测试结果']
                bdQuery_result['错误信息'] = rs['错误信息']
            else:
                logger.error('期望状态和报单状态不匹配，期望状态、报单状态、'
                             '提交状态分别为'+str(case_goal['期望状态'])+','+str(
                    data['order_status'])+','+str(data['order_submit_status']))
                bdQuery_result['报单检查状态'] = 'end'
                bdQuery_result['测试结果'] = False
                bdQuery_result['错误信息'] = '期望状态和报单状态不匹配'
        else:
            bdQuery_result['报单检查状态'] = 'end'
            bdQuery_result['测试结果'] = False
            bdQuery_result['错误信息'] = '报单提交状态不正确'

    # --如果是已撤状态的，执行如下
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE[
        'XTP_ORDER_STATUS_CANCELED']:
        if data['order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
            'XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
            logger.info('报单查询状态为已撤，' + str(data['order_status']))
            # 期望状态如果是为内部撤单，执行
            if case_goal['期望状态'] == '内部撤单':
                TODO
            else:
                logger.error('期望状态和报单状态不匹配，期望状态、报单状态、'
                             '提交状态分别为' + str(case_goal['期望状态']) + ','
                             + str(data['order_status']) + ',' + str(
                            data['order_submit_status']))
                bdQuery_result['报单检查状态'] = 'end'
                bdQuery_result['测试结果'] = False
                bdQuery_result['错误信息'] = '期望状态和报单状态不匹配'
        else:
            bdQuery_result['报单检查状态'] = 'end'
            bdQuery_result['测试结果'] = False
            bdQuery_result['错误信息'] = '报单提交状态不正确'

    # --如果是废单状态的，执行如下
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE[
        'XTP_ORDER_STATUS_REJECTED']:
        if data['order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
            'XTP_ORDER_SUBMIT_STATUS_INSERT_REJECTED']:
            logger.info('报单查询状态为废单，' + str(data['order_status']))
            # 期望状态如果是为废单，执行
            if case_goal['期望状态'] == '废单' and case_goal['是否是撤废'] == '是':
                TODO
            # 期望状态如果是撤废（废单后进行撤单），执行
            elif case_goal['期望状态'] == '废单':
                # 检查资金持仓是否正确
                fundstkcheck_rs = fund_stk_check_other(QueryInit, QueryEnd,
                                                     component_stk_info,Api)
                # 如果资金持仓检查正确，则执行报单数据检查，否则结束
                if fundstkcheck_rs['检查状态'] == 'end' and fundstkcheck_rs[
                    '测试结果']:
                    # 报单数据检查
                    rs = CHECK.reject(case_goal, data, error)
                    bdQuery_result['报单检查状态'] = rs['报单检查状态']
                    bdQuery_result['测试结果'] = rs['测试结果']
                    bdQuery_result['错误信息'] = rs['错误信息']
                else:
                    bdQuery_result['报单检查状态'] = fundstkcheck_rs['检查状态']
                    bdQuery_result['测试结果'] = fundstkcheck_rs['测试结果']
                    bdQuery_result['错误信息'] = fundstkcheck_rs['错误信息']

            else:
                logger.error('期望状态和报单状态不匹配，期望状态、报单状态、'
                             '提交状态分别为' + str(case_goal['期望状态']) + ','
                             + str(data['order_status']) + ',' + str(
                    data['order_submit_status']))
                bdQuery_result['报单检查状态'] = 'end'
                bdQuery_result['测试结果'] = False
                bdQuery_result['错误信息'] = '期望状态和报单状态不匹配'
        else:
            bdQuery_result['报单检查状态'] = 'end'
            bdQuery_result['测试结果'] = False
            bdQuery_result['错误信息'] = '报单提交状态不正确'

    # --如果是未知状态的，执行如下
    else:
        rs = CHECK.unknown(data)
        bdQuery_result['报单检查状态'] = rs['报单检查状态']
        bdQuery_result['测试结果'] = rs['测试结果']
        bdQuery_result['错误信息'] = rs['错误信息']
        logger.error('当前报单查询返回的状态未知'+str(data['order_status']))

    return bdQuery_result


#-------------------------------------------------------------------------------
#--报单为撤单类型的业务处理
#-------------------------------------------------------------------------------
def cetf_cdquery_type_handle(Api,wt_reqs,case_goal,data,error,QueryInit,QueryEnd,
                        component_stk_info):
    """报单查询返回的报单类型为'撤单'的业务处理"""
    # 定义测试结果参数
    cdQuery_result = {
        '报单检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
    }

    # --判断报单返回的data
    # 判断撤单报单查询的xtpID是否和撤单xtpID一致
    if data['order_xtp_id'] != case_goal['cancel_xtpID']:
        logger.error('错误，撤单报单返回的xtpID与cancel_xtpID不一致，cancel_xtpID和撤单报单回报xtp_ID分别是'+str(case_goal['cancel_xtpID'])+','+str(data['order_xtp_id']))
        cdQuery_result['报单检查状态'] = 'end'
        cdQuery_result['测试结果'] = False
        cdQuery_result['错误信息'] = '撤单报单返回的xtpID与cancel_xtpID不一致'

    # --下面是根据撤单报单的状态调用各自对应的校验方法
    # -如果撤单报单是‘撤废’状态的执行如下,通过报单查询
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_REJECTED']:
        if data['order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
            'XTP_ORDER_SUBMIT_STATUS_CANCEL_REJECTED']:
            logger.info('撤单报单状态为已拒绝,提交状态为撤单已拒绝，'+str(data['order_status'])+','+str(data['order_submit_status']))
            # 如果期望状态是'撤废'，执行
            if case_goal['是否是撤废'] =='是':
                fundstkcheck_rs=fund_stk_check_other(QueryInit, QueryEnd, component_stk_info,Api)
                if fundstkcheck_rs['检查状态'] == 'end' and fundstkcheck_rs['测试结果'] == True:
                    # 报单数据检查
                    rs = CHECK.cdquery_cancle_rejected(wt_reqs,case_goal,data,error)
                    cdQuery_result['报单检查状态']=rs['报单检查状态']
                    cdQuery_result['测试结果'] = rs['测试结果']
                    cdQuery_result['错误信息'] = rs['错误信息']
                else:
                    cdQuery_result['报单检查状态'] = fundstkcheck_rs['检查状态']
                    cdQuery_result['测试结果'] = fundstkcheck_rs['测试结果']
                    cdQuery_result['错误信息'] = fundstkcheck_rs['错误信息']
            else:
                logger.error('期望状态和报单状态、提交状态不匹配，期望状态、报单状态、提交状态分别为' + str(case_goal['期望状态']) + ',' + str(
                    data['order_status']) + ',' + str(data['order_submit_status']))
                cdQuery_result['报单检查状态'] = 'end'
                cdQuery_result['测试结果'] = False
                cdQuery_result['错误信息'] = '期望状态和撤单报单状态、提交状态不匹配'

    return cdQuery_result


# 报单查询返回的不同状态进行进一步校验
class check_querydata_by_status(object):
    """根据报单查询的不同状态，分别进行数据校验"""


    def no_match(self,wt_reqs,case_goal,data,error,trade_fund):
        """报单查询--未成交-校验"""
        # TODO:编写cetf_bdquery_type_Handle函数，未成交逻辑分支，期望状态未成交时再补充

    def all_match(self,wt_reqs, data, error):
        """报单查询--全部成交-校验"""
        logger.info('正在进行全部成交状态的报单查询业务校验')
        # 定义测试结果参数
        bdquery_result = {
            '报单检查状态': 'init',
            '测试结果': False,
            '错误信息': '',
        }
        # 判断成交数量是否正确
        if data['qty_traded'] != wt_reqs['quantity']:
            logger.error('全部成交报单查询的数量不等于委托数量，实际成交数量为和委托'
                         '数量分别是' + str(data['qty_traded']) + ','
                         + str(wt_reqs['quantity']))
            bdquery_result['报单检查状态'] = 'end'
            bdquery_result['测试结果'] = False
            bdquery_result['错误信息'] = '全部成交报单查询的数量不等于委托数量'
        # 判断成交金额是否大于零
        elif data['trade_amount'] < 0:
            logger.error('全部成交的报单查询成交金额应该不小于０，实际成交金额为'
                         + str(data['trade_amount']))
            bdquery_result['报单检查状态'] = 'end'
            bdquery_result['测试结果'] = False
            bdquery_result['错误信息'] = '全部成交的报单查询成交金额小于０'
        # 判断剩余数量是否等于０
        elif data['qty_left'] != 0:
            logger.error('全部成交状态的报单剩余数量应等于０，实际报单剩余数量为'
                         + str(data['qty_left']))
            bdquery_result['报单检查状态'] = 'end'
            bdquery_result['测试结果'] = False
            bdquery_result['错误信息'] = '全部成交状态的报单剩余数量不等于０'
        # 判断报单中的委托时间不能为空
        elif data['insert_time'] == 0:
            logger.error('错误，报单查询的委托时间不能为空，报单返回的委托时间为'
                         + str(data['insert_time']))
            bdquery_result['报单检查状态'] = 'end'
            bdquery_result['测试结果'] = False
            bdquery_result['错误信息'] = '报单查询的委托时间为空'
        # 判断其它项：最后修改时间，撤销时间，撤单xtpID,err_code,Err_Msg
        elif data['update_time'] != 0 and data['cancel_time'] != 0 and data[
            'order_cancel_xtp_id'] != 0 and error[
            'error_id'] != 0 and error['error_msg'] != '':
            logger.error(
                '错误，请检查最后修改时间，撤单时间，撤单xtpID,err_code,err_msg!'
                '它们的值分别是：' + str(
                    data['update_time']) + ',' + str(
                    data['cancel_time']) + ',' + str(
                    data['order_cancel_xtp_id']) + ',' + str(
                    error['error_id']) + ',' + error['error_msg'])
            bdquery_result['报单检查状态'] = 'end'
            bdquery_result['测试结果'] = False
            bdquery_result['错误信息'] = ('错误，请检查报单查询的最后修改时间，'
                                     + '撤单时间，撤单xtpID,err_code,err_msg!')
        else:
            bdquery_result['报单检查状态'] = 'end'
            bdquery_result['测试结果'] = True
            logger.info('全成状态的报单查询业务校验正确')
        return bdquery_result

    def all_cancel(self,wt_reqs, data, error):
        """报单查询--已撤-校验"""
        # TODO:编写cetf_bdquery_type_Handle函数，已撤逻辑分支，期望状态已撤时再补充

    def reject(self,case_goal, data, error):
        """报单查询--废单-校验"""
        logger.info('正在进行废单状态的报单查询业务校验')
        bdquery_result = {
            '报单检查状态': 'init',
            '测试结果': False,
            '错误信息': '',
        }
        # 判断成交数量是否为０
        if data['qty_traded'] != 0:
            logger.error(
                '错误，废单状态报单的成交数量应为０，返回报单的成交数量为' +
                str(data['qty_traded']))
            bdquery_result['报单检查状态'] = 'end'
            bdquery_result['测试结果'] = False
            bdquery_result['错误信息'] = '废单状态报单的成交数量应为０'

        # 判断成交金额是否是０
        elif data['trade_amount'] != 0.0:
            logger.error(
                '错误，废单状态报单的成交金额应为０，返回报单的成交金额为' +
                str(data['trade_amount']))
            bdquery_result['报单检查状态'] = 'end'
            bdquery_result['测试结果'] = False
            bdquery_result['错误信息'] = '废单状态报单的成交金额应为０'
        # 判断报单中的委托时间不能为空
        elif data['insert_time'] == 0:
            logger.error('错误，报单委托时间不能为空，报单返回的委托时间为' +
                         str(data['insert_time']))
            bdquery_result['报单检查状态'] = 'end'
            bdquery_result['测试结果'] = False
            bdquery_result['错误信息'] = '报单委托时间不能为空'
        # 判断其它项：最后修改时间，撤销时间，撤单xtpID
        elif data['update_time'] != 0 and data['cancel_time'] != 0 and data[
            'order_cancel_xtp_id'] != 0:
            logger.error(
                '错误，请检查最后修改时间，撤单时间，撤单xtpID!它们的值分别是：' + str(
                data['update_time']) + ',' + str(
                data['cancel_time']) + ',' + str(data['order_cancel_xtp_id']))
            bdquery_result['报单检查状态'] = 'end'
            bdquery_result['测试结果'] = False
            bdquery_result['错误信息'] = ('错误，请检查最后修改时间，撤单时间，' +
                                     '撤单xtpID!')
        else:
            # errID和errmsg都不校验
            if is_check_errId_bdQuery is False:
                bdquery_result['报单检查状态'] = 'end'
                bdquery_result['测试结果'] = True
                logger.info('废单状态的报单查询业务校验正确')
            # 只校验errID
            elif is_check_errId_bdQuery and is_Check_errmsg_bdQuery is False:
                # 判断废单的error_id与期望的是否一致
                if error['error_id'] != case_goal['errorID']:
                    logger.error(
                        '报单的error_id与用例期望的不一致，期望和实际的error_id分别是'
                        + str(case_goal['errorID']) + ','
                        + str(error['error_id']))
                    bdquery_result['报单检查状态'] = 'end'
                    bdquery_result['测试结果'] = False
                    bdquery_result['错误信息'] = '报单的error_id与用例期望的不一致'
                else:
                    bdquery_result['报单检查状态'] = 'end'
                    bdquery_result['测试结果'] = True
                    logger.info('废单状态的报单查询业务校验正确')
            # errID和errmsg都校验
            elif is_check_errId_bdQuery and is_Check_errmsg_bdQuery:
                # 判断废单的error_id与期望的是否一致
                if error['error_id'] != case_goal['errorID']:
                    logger.error(
                        '报单的error_id与用例期望的不一致，期望和实际的error_id分别是'
                        + str(case_goal['errorID']) + ','
                        + str(error['error_id']))
                    bdquery_result['报单检查状态'] = 'end'
                    bdquery_result['测试结果'] = False
                    bdquery_result['错误信息'] = '报单的error_id与用例期望的不一致'
                # 判断废单的error_msg与期望的是否一致
                elif error['error_msg'] != case_goal['errorMSG']:
                    logger.error(
                        '报单的error_msg与期望的不一致，期望和实际的error_msg分别是'
                        + case_goal['errorMSG'] + ',' + error['error_msg'])
                    bdquery_result['报单检查状态'] = 'end'
                    bdquery_result['测试结果'] = False
                    bdquery_result['错误信息'] = '报单的error_msg与用例期望的不一致'
                else:
                    bdquery_result['报单检查状态'] = 'end'
                    bdquery_result['测试结果'] = True
                    logger.info('废单状态的报单查询业务校验正确')

        return bdquery_result

    def unknown(self,data):
        """报单查询-状态未知-校验"""
        # TODO:编写cetf_bdquery_type_Handle函数，未知逻辑分支时再补充

    def statusInit(wt_reqs, data, error):
        """报单查询－初始－校验"""
        # TODO:编写cetf_bdquery_type_Handle函数，初始逻辑分支，期望状态初始时再补充

    def cdquery_cancle_rejected(self, wt_reqs, case_goal, data, error):
        """撤单类型报单查询-状态撤废-校验"""
        logger.info('撤单查询废单状态业务处理')
        cdquery_result = {
            '报单检查状态': 'init',
            '测试结果': True,
            '错误信息': '',
        }
        # 判断成交数量是否为０
        if data['qty_traded'] != 0:
            logger.error(
                '错误，废单状态报单的成交数量应为０，返回报单的成交数量为' + str(data['qty_traded']))
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
            logger.error(
                '错误，废单状态报单的成交金额应为０，返回报单的成交金额为' + str(data['trade_amount']))
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
        elif data['update_time'] != 0 and data['cancel_time'] != 0 and data[
            'order_cancel_xtp_id'] != 0:
            logger.error('错误，请检查最后修改时间，撤单时间，撤单xtpID!它们的值分别是：' + str(
                data['update_time']) + ',' + str(
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
                        '报单的error_id与用例期望的不一致，期望和实际的error_id分别是' + str(
                            case_goal['errorID']) + ',' + str(
                            error['error_id']))
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
                        '报单的error_id与用例期望的不一致，期望和实际的error_id分别是' + str(
                            case_goal['errorID']) + ',' + str(
                            error['error_id']))
                    cdquery_result['报单检查状态'] = 'end'
                    cdquery_result['测试结果'] = False
                    cdquery_result['错误信息'] = '报单的error_id与用例期望的不一致'
                # 判断废单的error_msg与期望的是否一致
                elif error['error_msg'] != case_goal['errorMSG']:
                    logger.error(
                        '报单的error_msg与用例期望的不一致，期望和实际的error_msg分别是' + case_goal[
                            'errorMSG'] + ',' + error['error_msg'])
                    cdquery_result['报单检查状态'] = 'end'
                    cdquery_result['测试结果'] = False
                    cdquery_result['错误信息'] = '报单的error_msg与用例期望的不一致'
                else:
                    cdquery_result['报单检查状态'] = 'end'
                    cdquery_result['测试结果'] = True
                    logger.info('废单状态的报单查询业务校验正确')

        return cdquery_result

    def cdquery_init(wt_reqs, data, error):
        """撤单报单查询-状态初始-校验"""
        # TODO:编写cetf_cdquery_type_handle函数时再进行补充

    def cdquery_allcancle(wt_reqs, data, error):
        """撤单报单查询-状态已撤-校验"""
        # TODO:编写cetf_cdquery_type_handle函数时再进行补充

CHECK = check_querydata_by_status()








