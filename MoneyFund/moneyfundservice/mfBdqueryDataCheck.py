#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
import time
from mfFundStkCheck import *
from log import *
from mfCheckDataPrice import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
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
            Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_INSERT_SUBMITTED'],
            Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED'],
            Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_INSERT_REJECTED']):
        logger.info('当前为报单类型data')
        result['报单类型'] = '报单'
        # (委托入参)公共业务检查
        public_result = public_Handle(Api,wt_reqs, data,case_goal)
        if public_result['报单检查状态'] == 'pending' and public_result['测试结果'] == True:
            bdQuery_result = bd_type_Handle(Api, wt_reqs, case_goal, data, error, QueryInit, QueryEnd)
            result['报单检查状态'] = bdQuery_result['报单检查状态']
            result['测试结果'] = bdQuery_result['测试结果']
            result['错误信息'] = bdQuery_result['错误信息']
        else:
            result['报单检查状态'] = public_result['报单检查状态']
            result['测试结果'] = public_result['测试结果']
            result['错误信息'] = public_result['错误信息']
    # --如果报单为撤单类型
    elif data['order_submit_status'] in (
            Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_CANCEL_SUBMITTED'],
            Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_CANCEL_REJECTED'],
            Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_CANCEL_ACCEPTED']):
        logger.info('当前为撤单类型data')
        result['报单类型'] = '撤单'
        # (委托入参)公共业务检查
        public_result = public_Handle(Api,wt_reqs, data,case_goal)
        if public_result['报单检查状态'] == 'pending' and public_result['测试结果'] == True:
            cdQuery_result = cd_type_Handle(Api, wt_reqs, case_goal, data, error, QueryInit, QueryEnd)
            result['报单检查状态'] = cdQuery_result['报单检查状态']
            result['测试结果'] = cdQuery_result['测试结果']
            result['错误信息'] = cdQuery_result['错误信息']
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
    # 逆回购业务中以错误的业务类型，如用'新股申购'下单时买卖方向为'卖'，但报单返回买卖方向为'买',对这种情况做处理
    side_reverse_repo_flag = (wt_reqs['ticker'][0:3] != '204' and wt_reqs['ticker'][0:4] != '1318' and
                              wt_reqs['business_type'] != Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_IPOS'] and
                              wt_reqs['business_type'] != Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_ALLOTMENT'])
    # 定义测试结果参数
    public_result = {
        '报单检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
    }
    #若是新股申购和逆回购，则不用校验价格和价格条件
    if wt_reqs['business_type'] not in (Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_REPO'],
        Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_IPOS'],Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_ALLOTMENT']):
        if checkDataPrice(Api, wt_reqs, data['price'])==False:
            logger.error('报单查询返回的价格验证错误')
        elif data['price_type'] != wt_reqs['price_type']:
            logger.error('错误，报单返回的价格条件与原委托不一致，原委托价格条件和报单回报的价格条件分别是' + str(wt_reqs['price_type']) + ',' + str(data['price_type']))
            public_result['报单检查状态'] = 'end'
            public_result['测试结果'] = False
            public_result['错误信息'] = '报单返回的价格条件与原委托不一致'

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
    elif data['side'] != wt_reqs['side'] and side_reverse_repo_flag:
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

    # # 判断撤单xtp_ID是否一致,注：报单查询，已撤的报单没有显示撤单xtp_ID
    # elif data['order_cancel_xtp_id'] != case_goal['cancel_xtpID']:
    #     logger.error('错误，报单返回的撤单xtpID与期望不一致，期望撤单xtp_ID和报单回报的撤单xtp_ID分别是'+str(case_goal['cancel_xtpID'])+','+str(data['order_cancel_xtp_id']))
    #     bdQuery_result['报单检查状态'] = 'end'
    #     bdQuery_result['测试结果'] = False
    #     bdQuery_result['错误信息'] = '报单返回的撤单xtpID与期望不一致'

    # 判断已成交数量加上待成交数量（撤单数量）是否等于委托数量

    elif data['qty_traded'] + data['qty_left'] != wt_reqs['quantity']:
        logger.error('错误，报单返回的成交数量加上待成交数量（撤单数量）应等于委托数量，委托数量和返回报单的成交数量和待成交数量（撤单数量）分别为'+str(wt_reqs['quantity'])+','+str(data['qty_traded'])+','+str(data['qty_left']))
        bdQuery_result['报单检查状态'] = 'end'
        bdQuery_result['测试结果'] = False
        bdQuery_result['错误信息'] = '报单返回的成交数量加上待成交数量（撤单数量）应等于委托数量'

    # --下面是根据报单的状态调用各自对应的校验方法
    # -如果报单查询是‘初始’状态的执行如下测试结果
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_INIT']:
        if data['order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
            'XTP_ORDER_SUBMIT_STATUS_INSERT_SUBMITTED']:
            logger.info('报单查询状态为初始，'+str(data['order_status'])+','+str(data['order_submit_status']))
            # 如果期望状态是'初始'，执行
            if case_goal['期望状态'] == '初始':
                #检查资金持仓是否正确
                fundstkcheck_rs=fundStkCheck_nomatch(Api, QueryInit, QueryEnd, wt_reqs, case_goal)
                #如果资金持仓检查正确，则执行报单数据检查，否则结束
                if fundstkcheck_rs['检查状态']=='end' and fundstkcheck_rs['测试结果']==True:
                    #报单数据检查
                    rs = statusInit(wt_reqs, data, error)
                    bdQuery_result['报单检查状态'] = rs['报单检查状态']
                    bdQuery_result['测试结果'] = rs['测试结果']
                    bdQuery_result['错误信息'] = rs['错误信息']
                else:
                    bdQuery_result['报单检查状态'] = fundstkcheck_rs['检查状态']
                    bdQuery_result['测试结果'] = fundstkcheck_rs['测试结果']
                    bdQuery_result['错误信息'] = fundstkcheck_rs['错误信息']
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
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_NOTRADEQUEUEING']:
        if data['order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
            'XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
            logger.info('报单查询状态为未成交,提交状态为已提交，'+str(data['order_status'])+','+str(data['order_submit_status']))
            # 如果期望状态是未成交，执行
            if case_goal['期望状态'] == '未成交':
                # 检查资金持仓是否正确
                fundstkcheck_rs = fundStkCheck_nomatch(Api, QueryInit, QueryEnd, wt_reqs, case_goal)
                # 如果资金持仓检查正确，则执行报单数据检查，否则结束
                if fundstkcheck_rs['检查状态'] == 'end' and fundstkcheck_rs['测试结果'] == True:
                    # 报单数据检查
                    rs = no_match(wt_reqs, case_goal, data, error)
                    bdQuery_result['报单检查状态'] = rs['报单检查状态']
                    bdQuery_result['测试结果'] = rs['测试结果']
                    bdQuery_result['错误信息'] = rs['错误信息']
                else:
                    bdQuery_result['报单检查状态'] = fundstkcheck_rs['检查状态']
                    bdQuery_result['测试结果'] = fundstkcheck_rs['测试结果']
                    bdQuery_result['错误信息'] = fundstkcheck_rs['错误信息']
            #如果期望状态是已报待撤,此处不作资金持仓股份检查，在撤单报单那里进行资金股份检查，所以报单状态是True
            elif case_goal['期望状态'] =='已报待撤':
                bdQuery_result['报单检查状态'] = 'end'
                bdQuery_result['测试结果'] = True
                bdQuery_result['错误信息'] = ''

            elif case_goal['期望状态'] in('部成','全成','部撤已报','部撤','已撤','废单','撤废'):
                bdQuery_result['报单检查状态'] = 'pending'
                bdQuery_result['测试结果'] = False
                bdQuery_result['错误信息'] = ''
            elif '是否是新股申购' in case_goal:
                if case_goal['期望状态'] == '初始':
                    # 检查资金持仓是否正确
                    fundstkcheck_rs = fundStkCheck_nomatch(Api, QueryInit, QueryEnd, wt_reqs, case_goal)
                    # 如果资金持仓检查正确，则执行报单数据检查，否则结束
                    if fundstkcheck_rs['检查状态'] == 'end' and fundstkcheck_rs['测试结果'] == True:
                        # 报单数据检查
                        rs = no_match(wt_reqs, case_goal, data, error)
                        bdQuery_result['报单检查状态'] = rs['报单检查状态']
                        bdQuery_result['测试结果'] = rs['测试结果']
                        bdQuery_result['错误信息'] = rs['错误信息']
                    else:
                        bdQuery_result['报单检查状态'] = fundstkcheck_rs['检查状态']
                        bdQuery_result['测试结果'] = fundstkcheck_rs['测试结果']
                        bdQuery_result['错误信息'] = fundstkcheck_rs['错误信息']
            else:
                logger.error('期望状态和报单状态、提交状态不匹配，期望状态、报单状态、提交状态分别为'+str(case_goal['期望状态'])+','+str(data['order_status'])+','+str(data['order_submit_status']))
                bdQuery_result['报单检查状态'] = 'end'
                bdQuery_result['测试结果'] = False
                bdQuery_result['错误信息'] = '期望状态和报单状态、提交状态不匹配'
        else:
            bdQuery_result['报单检查状态'] = 'end'
            bdQuery_result['测试结果'] = False
            bdQuery_result['错误信息'] = '报单提交状态不正确'

    # --如果报单查询是‘部成状态’的，执行如下
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_PARTTRADEDQUEUEING']:
        if data['order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
            'XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
            logger.info('报单查询状态为部分成交，提交状态为已提交'+str(data['order_status'])+','+str(data['order_submit_status']))
            # 期望状态如果是为部成，执行
            if case_goal['期望状态']=='部成':
                rs = part_match(wt_reqs, case_goal, data, error)
                bdQuery_result['报单检查状态'] = rs['报单检查状态']
                bdQuery_result['测试结果'] = rs['测试结果']
                bdQuery_result['错误信息'] = rs['错误信息']

            # 如果期望状态是部撤已报,此处不作资金持仓股份检查，在撤单报单那里进行资金股份检查，所以报单状态是True
            elif case_goal['期望状态'] == '部撤已报':
                bdQuery_result['报单检查状态'] = 'end'
                bdQuery_result['测试结果'] = True
                bdQuery_result['错误信息'] = ''

            elif case_goal['期望状态'] in('全成','部撤','撤废'):
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

    # --如果报单查询是全成状态的，执行如下
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_ALLTRADED']:
        if data['order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
            'XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
            logger.info('报单查询状态为全部成交，提交状态为已提交'+str(data['order_status'])+','+str(data['order_submit_status']))

            # 期望状态如果是为全成，执行
            if case_goal['期望状态'] == '全成':
                rs = all_match(wt_reqs, case_goal, data, error)
                bdQuery_result['报单检查状态'] = rs['报单检查状态']
                bdQuery_result['测试结果'] = rs['测试结果']
                bdQuery_result['错误信息'] = rs['错误信息']
            elif case_goal['期望状态'] == '撤废':
                bdQuery_result['报单检查状态'] = 'pending'
                bdQuery_result['测试结果'] = False
                bdQuery_result['错误cdhb_result信息'] = ''
            else:
                logger.error('期望状态和报单状态、提交状态不匹配，期望状态、报单状态、提交状态分别为'+str(case_goal['期望状态'])+','+str(data['order_status'])+','+str(data['order_submit_status']))
                bdQuery_result['报单检查状态'] = 'end'
                bdQuery_result['测试结果'] = False
                bdQuery_result['错误信息'] = '期望状态和报单状态、提交状态不匹配'
        else:
            bdQuery_result['报单检查状态'] = 'end'
            bdQuery_result['测试结果'] = False
            bdQuery_result['错误信息'] = '报单提交状态不正确'

    # --如果报单是部撤状态的，执行如下
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_PARTTRADEDNOTQUEUEING']:
        if data['order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
            'XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
            logger.info('报单查询状态为部分撤单，'+str(data['order_status'])+','+str(data['order_submit_status']))
            # 期望状态如果是为部撤，执行
            if case_goal['期望状态'] == '部撤':
                # 检查资金持仓是否正确
                fundstkcheck_rs = fundStkCheck_partCancel(Api,QueryInit,QueryEnd,wt_reqs,data)
                # 如果资金持仓检查正确，则执行报单数据检查，否则结束
                if fundstkcheck_rs['检查状态'] == 'end' and fundstkcheck_rs['测试结果'] == True:
                    # 报单数据检查
                    rs = part_cancel(wt_reqs, case_goal, data, error)
                    bdQuery_result['报单检查状态'] = rs['报单检查状态']
                    bdQuery_result['测试结果'] = rs['测试结果']
                    bdQuery_result['错误信息'] = rs['错误信息']
                else:
                    bdQuery_result['报单检查状态'] = fundstkcheck_rs['检查状态']
                    bdQuery_result['测试结果'] = fundstkcheck_rs['测试结果']
                    bdQuery_result['错误信息'] = fundstkcheck_rs['错误信息']
            # 期望状态如果是撤废（部撤后进行撤单），执行
            elif case_goal['期望状态'] == '撤废':
                bdQuery_result['报单检查状态'] = 'pending'
                bdQuery_result['测试结果'] = False
            else:
                logger.error('期望状态和报单状态、提交状态不匹配，期望状态、报单状态、提交状态分别为'+str(case_goal['期望状态'])+','+str(data['order_status'])+','+str(data['order_submit_status']))
                bdQuery_result['报单检查状态'] = 'end'
                bdQuery_result['测试结果'] = False
                bdQuery_result['错误信息'] = '期望状态和报单状态、提交状态不匹配'
        else:
            bdQuery_result['报单检查状态'] = 'end'
            bdQuery_result['测试结果'] = False
            bdQuery_result['错误信息'] = '报单提交状态不正确'

    # --如果是已撤状态的，执行如下
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_CANCELED']:
        if data['order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
            logger.info('报单查询状态为已撤，'+str(data['order_status']))
            # 期望状态如果是为已撤，执行
            if case_goal['期望状态'] in('已撤','内部撤单') :
                # 检查资金持仓是否正确
                fundstkcheck_rs = fundStkCheck_other(QueryInit,QueryEnd)
                # 如果资金持仓检查正确，则执行报单数据检查，否则结束
                if fundstkcheck_rs['检查状态'] == 'end' and fundstkcheck_rs['测试结果'] == True:
                    # 报单数据检查
                    rs = all_cancel(wt_reqs, data, error)
                    bdQuery_result['报单检查状态'] = rs['报单检查状态']
                    bdQuery_result['测试结果'] = rs['测试结果']
                    bdQuery_result['错误信息'] = rs['错误信息']
                else:
                    bdQuery_result['报单检查状态'] = fundstkcheck_rs['检查状态']
                    bdQuery_result['测试结果'] = fundstkcheck_rs['测试结果']
                    bdQuery_result['错误信息'] = fundstkcheck_rs['错误信息']

            # 期望状态如果是撤废（已撤后进行撤单），执行
            elif case_goal['期望状态'] == '撤废':
                bdQuery_result['报单检查状态'] = 'pending'
                bdQuery_result['测试结果'] = False
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

    # --如果是废单状态的，执行如下
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_REJECTED']:
        if data['order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE['XTP_ORDER_SUBMIT_STATUS_INSERT_REJECTED']:
            logger.info('报单查询状态为废单，'+str(data['order_status']))
            # 期望状态如果是为废单，执行
            if case_goal['期望状态'] == '废单':
                # 检查资金持仓是否正确
                fundstkcheck_rs = fundStkCheck_other(QueryInit, QueryEnd)
                # 如果资金持仓检查正确，则执行报单数据检查，否则结束
                if fundstkcheck_rs['检查状态'] == 'end' and fundstkcheck_rs['测试结果'] == True:
                    # 报单数据检查
                    rs = reject(wt_reqs, case_goal, data, error)
                    bdQuery_result['报单检查状态'] = rs['报单检查状态']
                    bdQuery_result['测试结果'] = rs['测试结果']
                    bdQuery_result['错误信息'] = rs['错误信息']
                else:
                    bdQuery_result['报单检查状态'] = fundstkcheck_rs['检查状态']
                    bdQuery_result['测试结果'] = fundstkcheck_rs['测试结果']
                    bdQuery_result['错误信息'] = fundstkcheck_rs['错误信息']
            # 期望状态如果是撤废（已撤后进行撤单），执行
            elif case_goal['期望状态'] == '撤废':
                bdQuery_result['报单检查状态'] = 'pending'
                bdQuery_result['测试结果'] = False
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
#--报单为撤单类型的业务处理
#-----------------------------------------------------------------------------------------------------------------------
def cd_type_Handle(Api,wt_reqs,case_goal,data,error,QueryInit,QueryEnd):
    # 定义测试结果参数
    cdQuery_result = {
        '报单检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
    }
    # --判断报单返回的data
    # 判断撤单报单查询的xtpID是否和撤单xtpID一致
    #未成撤废
    if data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_REJECTED'] and data['order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
            'XTP_ORDER_SUBMIT_STATUS_CANCEL_REJECTED'] and case_goal['期望状态'] == '未成交' and case_goal['是否是撤废'] == '是' and case_goal['是否是集合竞价'] == '否':
        if data['order_xtp_id'] != case_goal['recancel_xtpID']:
            logger.error('错误，撤单报单返回的xtpID与recancel_xtpID不一致，recancel_xtpID和撤单报单回报xtp_ID分别是'+str(case_goal['recancel_xtpID'])+','+str(data['order_xtp_id']))
            cdQuery_result['报单检查状态'] = 'end'
            cdQuery_result['测试结果'] = False
            cdQuery_result['错误信息'] = '撤单报单返回的xtpID与recancel_xtpID不一致'
    else:
        if data['order_xtp_id'] != case_goal['cancel_xtpID']:
            logger.error('错误，撤单报单返回的xtpID与cancel_xtpID不一致，cancel_xtpID和撤单报单回报xtp_ID分别是'+str(case_goal['cancel_xtpID'])+','+str(data['order_xtp_id']))
            cdQuery_result['报单检查状态'] = 'end'
            cdQuery_result['测试结果'] = False
            cdQuery_result['错误信息'] = '撤单报单返回的xtpID与cancel_xtpID不一致'

    # --下面是根据撤单报单的状态调用各自对应的校验方法
    # -如果撤单报单是‘初始’状态的执行如下,通过报单查询
    if data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_INIT']:
        if data['order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
            'XTP_ORDER_SUBMIT_STATUS_CANCEL_SUBMITTED']:
            logger.info('撤单报单状态为初始,提交状态为已提交，'+str(data['order_status'])+','+str(data['order_submit_status']))
            # 如果期望状态是'已报待撤'或'部撤已报'，执行
            if case_goal['期望状态'] in('已报待撤','部撤已报'):
                # 检查资金持仓是否正确
                fundstkcheck_rs = fundStkCheck_other(QueryInit, QueryEnd)
                # 如果资金持仓检查正确，则执行报单数据检查，否则结束
                if fundstkcheck_rs['检查状态'] == 'end' and fundstkcheck_rs['测试结果'] == True:
                    # 报单数据检查
                    rs = cdQuery_init(wt_reqs, data, error)
                    cdQuery_result['报单检查状态']=rs['报单检查状态']
                    cdQuery_result['测试结果'] = rs['测试结果']
                    cdQuery_result['错误信息'] = rs['错误信息']
                else:
                    cdQuery_result['报单检查状态'] = fundstkcheck_rs['检查状态']
                    cdQuery_result['测试结果'] = fundstkcheck_rs['测试结果']
                    cdQuery_result['错误信息'] = fundstkcheck_rs['错误信息']
            elif case_goal['期望状态'] in('部撤','已撤','撤废'):
                cdQuery_result['报单检查状态'] = 'pending'
                cdQuery_result['测试结果'] = False
                cdQuery_result['错误信息'] = ''
            else:
                logger.error('期望状态和报单状态、提交状态不匹配，期望状态、报单状态、提交状态分别为' + str(case_goal['期望状态']) + ',' + str(
                    data['order_status']) + ',' + str(data['order_submit_status']))
                cdQuery_result['报单检查状态'] = 'end'
                cdQuery_result['测试结果'] = False
                cdQuery_result['错误信息'] = '期望状态和撤单报单状态、提交状态不匹配'

    # -如果撤单报单是‘部撤’状态的执行如下,通过报单查询
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_PARTTRADEDNOTQUEUEING']:
        if data['order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
            'XTP_ORDER_SUBMIT_STATUS_CANCEL_ACCEPTED']:
            logger.info('撤单报单状态为部分撤单,提交状态为已提交，'+str(data['order_status'])+','+str(data['order_submit_status']))
            # 如果期望状态是'部撤'，执行
            if case_goal['期望状态'] in('部撤'):
                rs = cdQuery_partCancle(wt_reqs, data, error)
                cdQuery_result['报单检查状态'] = rs['报单检查状态']
                cdQuery_result['测试结果'] = rs['测试结果']
                cdQuery_result['错误信息'] = rs['错误信息']

            elif case_goal['是否是撤废'] =='是':
                cdQuery_result['报单检查状态'] = 'pending'
                cdQuery_result['测试结果'] = False
                cdQuery_result['错误信息'] = ''
            else:
                logger.error('期望状态和报单状态、提交状态不匹配，期望状态、报单状态、提交状态分别为' + str(case_goal['期望状态']) + ',' + str(
                    data['order_status']) + ',' + str(data['order_submit_status']))
                cdQuery_result['报单检查状态'] = 'end'
                cdQuery_result['测试结果'] = False
                cdQuery_result['错误信息'] = '期望状态和撤单报单状态、提交状态不匹配'

    # -如果撤单报单是‘已撤’状态的执行如下,通过报单查询
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_CANCELED']:
        if data['order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
            'XTP_ORDER_SUBMIT_STATUS_CANCEL_ACCEPTED']:

            logger.info('撤单报单查询状态为已撤,提交状态为已提交，'+str(data['order_status'])+','+str(data['order_submit_status']))
            # 如果期望状态是'已撤'，执行
            if case_goal['期望状态'] in('已撤','内部撤单'):
                rs = cdQuery_allCancle(wt_reqs, data, error)
                cdQuery_result['报单检查状态'] = rs['报单检查状态']
                cdQuery_result['测试结果'] = rs['测试结果']
                cdQuery_result['错误信息'] = rs['错误信息']
            elif case_goal['是否是撤废'] =='是':
                cdQuery_result['报单检查状态'] = 'pending'
                cdQuery_result['测试结果'] = False
                cdQuery_result['错误信息'] = ''
            else:
                logger.error('期望状态和报单状态、提交状态不匹配，期望状态、报单状态、提交状态分别为' + str(case_goal['期望状态']) + ',' + str(
                    data['order_status']) + ',' + str(data['order_submit_status']))
                cdQuery_result['报单检查状态'] = 'end'
                cdQuery_result['测试结果'] = False
                cdQuery_result['错误信息'] = '期望状态和撤单报单状态、提交状态不匹配'

    # -如果撤单报单是‘撤废’状态的执行如下,通过报单查询
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_REJECTED']:
        if data['order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
            'XTP_ORDER_SUBMIT_STATUS_CANCEL_REJECTED']:
            logger.info('撤单报单状态为已拒绝,提交状态为撤单已拒绝，'+str(data['order_status'])+','+str(data['order_submit_status']))
            # 如果期望状态是'撤废'，执行
            if case_goal['是否是撤废'] =='是':

                fundstkcheck_rs=fundStkCheck_other(QueryInit, QueryEnd)
                if fundstkcheck_rs['检查状态'] == 'end' and fundstkcheck_rs['测试结果'] == True:
                    # 报单数据检查
                    rs = cdQueryCancleRejected(wt_reqs,case_goal,data,error)
                    cdQuery_result['报单检查状态']=rs['报单检查状态']
                    cdQuery_result['测试结果'] = rs['测试结果']
                    cdQuery_result['错误信息'] = rs['错误信息']
                else:
                    cdQuery_result['报单检查状态'] = fundstkcheck_rs['检查状态']
                    cdQuery_result['测试结果'] = fundstkcheck_rs['测试结果']
                    cdQuery_result['错误信息'] = fundstkcheck_rs['错误信息']
            elif '是否是新股申购' in case_goal:
                if case_goal['是否是新股申购'] == '是':
                    fundstkcheck_rs = fundStkCheck_other(QueryInit, QueryEnd)
                    if fundstkcheck_rs['检查状态'] == 'end' and fundstkcheck_rs['测试结果'] == True:
                        # 报单数据检查
                        rs = cdQueryCancleRejected(wt_reqs, case_goal, data, error)
                        cdQuery_result['报单检查状态'] = rs['报单检查状态']
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


#-----------------------------------------------------------------------------------------------------------------------
#－报单查询－初始－校验-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------

def statusInit(wt_reqs,data,error):
    logger.info('正在进行初始状态的报单查询业务校验')
    bdquery_result={
        '报单检查状态':'init',
        '测试结果':'',
        '错误信息':'',
    }
    #判断成交数量是否为０
    if data['qty_traded']!=0:
        logger.error('初始状态的报单成交数量应该为０，实际成交数量为'+str(data['qty_traded']))
        bdquery_result['报单检查状态']='end'
        bdquery_result['测试结果'] = False
        bdquery_result['错误信息'] = '初始状态的报单成交数量应该为０'
    # 判断成交金额是否为０
    elif data['trade_amount']!=0:
        logger.error('初始状态的报单成交金额应该为０，实际成交数量为'+str(data['trade_amount']))
        bdquery_result['报单检查状态']='end'
        bdquery_result['测试结果'] = False
        bdquery_result['错误信息'] = '初始状态的报单成交金额应该为０'
    #判断剩余数量是否等于委托数量
    elif data['qty_left'] != wt_reqs['quantity']:
        logger.error('初始状态的报单剩余数量和委托数量不相等，委托数量和报单剩余数量分别为'+str(wt_reqs['quantity'])+','+str(data['qty_left']))
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = False
        bdquery_result['错误信息'] = '初始状态的报单剩余数量和委托数量不相等'
    # 判断报单中的委托时间不能为空
    elif data['insert_time'] == 0:
        logger.error('错误，报单委托时间不能为空，报单返回的委托时间为'+str(data['insert_time']))
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = False
        bdquery_result['错误信息'] = '报单委托时间不能为空'
    # 判断其它项：最后修改时间，撤销时间，撤单xtpID,err_code,Err_Msg
    elif data['update_time'] != 0 and data['cancel_time'] != 0 and data['order_cancel_xtp_id'] != 0 and error['error_id'] != 0 and error['error_msg'] != '':
        logger.error('错误，请检查最后修改时间，撤单时间，撤单xtpID,err_code,err_msg!它们的值分别是：' + str(data['update_time']) + ',' + str(
            data['cancel_time']) + ',' + str(data['order_cancel_xtp_id']) + ',' + str(error['error_id']) + ',' + str(error['error_msg']))
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = False
        bdquery_result['错误信息'] = '错误，请检查最后修改时间，撤单时间，撤单xtpID,err_code,err_msg!'
    else:
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = True
        logger.info('初始状态的报单查询业务校验正确')

    return bdquery_result

#-----------------------------------------------------------------------------------------------------------------------
#--报单查询--未成交-校验
#-----------------------------------------------------------------------------------------------------------------------
def no_match(wt_reqs,case_goal,data,error):
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
#--报单查询--部分成交-校验，ＰＳ：部分成交没有报单推送,通过查询报单
# #-----------------------------------------------------------------------------------------------------------------------
def part_match(wt_reqs,case_goal,data,error):
    logger.info('正在进行部分成交状态的报单查询推送校验')
    # 定义测试结果参数
    bdquery_result = {
        '报单检查状态': 'init',
        '测试结果': '',
        '错误信息': '',
    }
    # 判断成交数量是否正确
    if data['qty_traded'] <= 0 or data['qty_traded']>=wt_reqs['quantity']:
        logger.error('部分成交报单查询的数量应大于０小于委托数量，实际成交数量为和委托数量分别是'+str(data['qty_traded'])+','+str(wt_reqs['quantity']))
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = False
        bdquery_result['错误信息'] = '部分成交委托的数量应大于０小于委托数量'
    # 判断成交金额是否大于零
    elif data['trade_amount'] <= 0:
        logger.error('部分成交的报单查询成交金额应该大于０，实际成交数量为'+str(data['trade_amount']))
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = False
        bdquery_result['错误信息'] = '部分成交的报单查询成交金额应该大于０'
    # # 判断剩余数量是否等于委托数量，上面已判断成交数量＋剩余数量＝＝委托数量，所以此处注释
    # elif data['qty_left'] != wt_reqs['quantity']:
    #     logger.error('初始状态的报单剩余数量和委托数量不相等，委托数量和报单剩余数量分别为'+str(wt_reqs['quantity'])+','+str(data['qty_left']))
    #     bdquery_result['报单检查状态'] = 'end'
    #     bdquery_result['测试结果'] = False
    #     bdquery_result['错误信息'] = '初始状态的报单剩余数量和委托数量不相等'
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
            data['cancel_time']) + ',' + str(data['order_cancel_xtp_id']) + ',' + str(error['error_id']) + ',' + str(
            error['error_msg']))
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = False
        bdquery_result['错误信息'] = '错误，请检查报单查询的最后修改时间，撤单时间，撤单xtpID,err_code,err_msg!'
    else:
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = True
        logger.info('部分成交状态的报单查询业务校验正确')

    return bdquery_result


#-----------------------------------------------------------------------------------------------------------------------
#--查询报单（原单）部撤已报-校验
#---------------------------------------------------------------------------------------------------------------------
def bd_bcyb(wt_reqs,case_goal,data,error):
    logger.info('正在进行部撤已报状态的报单查询业务校验')
    #　部撤已报状态的原委托订单和部分成交状态的报单是一样的，所以直接调用部分成交状态的订单
    bdquery_result=part_match(wt_reqs,case_goal,data,error)
    return bdquery_result

# -----------------------------------------------------------------------------------------------------------------------
# --查询报单（原单）已报待撤-校验
#---------------------------------------------------------------------------------------------------------------------
def bd_ybdc(wt_reqs,case_goal,data,error):
    logger.info('正在进行已报待撤状态的报单查询业务校验')
    # 　已报待撤状态的原委托订单和未成交状态的报单是一样的，所以直接调用未成交状态的订单
    bdquery_result = part_match(wt_reqs, case_goal, data, error)
    return bdquery_result



#-----------------------------------------------------------------------------------------------------------------------
#--查询报单（原单）撤废-校验
# #---------------------------------------------------------------------------------------------------------------------
# def part_match(wt_reqs,case_goal,data,error):
#     logger.info('正在进行撤废状态的下单推送业务校验')


#-----------------------------------------------------------------------------------------------------------------------
#--报单查询--全部成交-校验
#-----------------------------------------------------------------------------------------------------------------------
def all_match(wt_reqs,case_goal,data,error):
    logger.info('正在进行全部成交状态的报单查询业务校验')
    # 定义测试结果参数
    bdquery_result = {
        '报单检查状态': 'init',
        '测试结果': '',
        '错误信息': '',
    }
    # 判断成交数量是否正确
    if data['qty_traded'] != wt_reqs['quantity']:
        logger.error('全部成交报单查询的数量应等于委托数量，实际成交数量为和委托数量分别是'+str(data['qty_traded'])+','+str(wt_reqs['quantity']))
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = False
        bdquery_result['错误信息'] = '全部成交报单查询的数量应等于委托数量'
    # 判断成交金额是否大于零
    elif data['trade_amount'] <= 0:
        logger.error('全部成交的报单查询成交金额应该大于０，实际成交数量为'+str(data['trade_amount']))
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = False
        bdquery_result['错误信息'] = '全部成交的报单查询成交金额应该大于０'
    # 判断剩余数量是否等于０
    elif data['qty_left'] != 0:
        logger.error('全部成交状态的报单剩余数量应等于０，实际报单剩余数量分别为'+str(data['qty_left']))
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = False
        bdquery_result['错误信息'] = '全部成交状态的报单剩余数量应等于０'
    # 判断报单中的委托时间不能为空
    elif data['insert_time'] == 0:
        logger.error('错误，报单查询的委托时间不能为空，报单返回的委托时间为' + str(data['insert_time']))
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = False
        bdquery_result['错误信息'] = '报单查询的委托时间不能为空'
    # 判断其它项：最后修改时间，撤销时间，撤单xtpID,err_code,Err_Msg
    elif data['update_time'] != 0 and data['cancel_time'] != 0 and data['order_cancel_xtp_id'] != 0 and error[
        'error_id'] != 0 and error['error_msg'] != '':
        logger.error('错误，请检查最后修改时间，撤单时间，撤单xtpID,err_code,err_msg!它们的值分别是：' + str(data['update_time']) + ',' + str(
            data['cancel_time']) + ',' + str(data['order_cancel_xtp_id']) + ',' + str(error['error_id']) + ','+error['error_msg'])
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = False
        bdquery_result['错误信息'] = '错误，请检查报单查询的最后修改时间，撤单时间，撤单xtpID,err_code,err_msg!'
    else:
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = True
        logger.info('全成状态的报单查询业务校验正确')
    return bdquery_result

#-----------------------------------------------------------------------------------------------------------------------
#--报单查询--（原单）部分撤单-校验
#-----------------------------------------------------------------------------------------------------------------------
def part_cancel(wt_reqs,case_goal,data,error):
    logger.info('正在进行部分撤单状态的报单查询业务校验')
    # 定义测试结果参数
    bdquery_result = {
        '报单检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
    }
    # 判断成交数量是否大于0
    if data['qty_traded'] <= 0:
        logger.error('错误，部分撤单状态的报单查询返回的成交数量应大于0，实际返回的成交数量为'+str(data['qty_traded']))
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = False
        bdquery_result['错误信息'] = '部分撤单状态的报单查询返回的成交数量应大于0'
    # 判断撤单数量是否大于0
    elif data['qty_left'] <= 0:
        logger.error('错误，部分撤单状态的报单查询返回的撤单数量应大于0，实际返回的撤单数量为'+str(data['qty_left']))
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = False
        bdquery_result['错误信息'] = '部分撤单状态的报单查询返回的撤单数量应大于0'
    # 判断成交金额是否大于０
    elif data['trade_amount'] <= 0.0:
        logger.error('错误，部分撤单状态报单查询的成交金额应大于０，返回报单的成交金额为'+str(data['trade_amount']))
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = False
        bdquery_result['错误信息'] = '部分撤单状态报单查询的成交金额应大于０'
    # 判断报单中的委托时间不能为空
    elif data['insert_time'] == 0:
        logger.error('错误，报单查询的委托时间不能为空，报单返回的委托时间为'+str(data['insert_time']))
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = False
        bdquery_result['错误信息'] = '报单查询的委托时间不能为空'
    # 判断报单中的撤单时间不能为空
    elif data['cancel_time'] == 0:
        logger.error('错误，报单查询的撤单时间不能为空，报单返回的撤单时间为'+str(data['cancel_time']))
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = False
        bdquery_result['错误信息'] = '报单查询的撤单时间不能为空'
    #判断撤单xtpID是否正确
    #注：当前报单查询撤单xtpID显示为０，所以验证代码暂且屏蔽
    # elif data['order_cancel_xtp_id']!=case_goal['cancel_xtpID']:
    #     print '报单查询的撤单xtpID不正确，实际显示的撤单xtpID为',data['order_cancel_xtp_id']
    #     bdquery_result['报单检查状态'] = 'end'
    #     bdquery_result['测试结果'] = False
    #     bdquery_result['错误信息'] = '报单查询的撤单xtpID不正确'

    # 判断其它项：最后修改时间,err_code,Err_Msg
    elif data['update_time'] != 0  and error['error_id'] != 0 and error['error_msg'] != '':
        logger.error('错误，请检查最后修改时间，err_code,err_msg!它们的值分别是：'+str(data['update_time'])+','+str(error['error_id'])+','+error['error_msg'])
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = False
        bdquery_result['错误信息'] = '错误，请检查最后修改时间，撤单时间,err_code,err_msg!'

    else:
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = True
        logger.info('部撤状态的报单查询业务校验正确')
    return bdquery_result

#-----------------------------------------------------------------------------------------------------------------------
#--报单推送--已撤-校验
#-----------------------------------------------------------------------------------------------------------------------
def all_cancel(wt_reqs,data,error):
    logger.info('正在进行已撤状态的报单查询业务校验')
    # 定义测试结果参数
    bdquery_result = {
        '报单检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
    }
    # 判断成交数量是否等于0
    if data['qty_traded'] != 0:
        logger.error('错误，已撤状态的报单返回的成交数量应等于0，实际返回的成交数量为'+str(data['qty_traded']))
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = False
        bdquery_result['错误信息'] = '已撤状态的报单返回的成交数量应等于0'
    # 判断撤单数量是否等于委托数量
    elif data['qty_left'] != wt_reqs['quantity']:
        logger.error('错误，已撤状态的报单返回的撤单数量应等于委托数量，原委托数量和实际返回的撤单数量为'+str(wt_reqs['quantity'])+','+str(data['qty_left']))
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = False
        bdquery_result['错误信息'] = '已撤状态的报单返回的撤单数量应等于委托数量'

    # 判断成交金额是否大于０
    elif data['trade_amount'] != 0.0:
        logger.error('错误，已撤成交状态报单的成交金额应等于０，返回报单的成交金额为'+str(data['trade_amount']))
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = False
        bdquery_result['错误信息'] = '已撤成交状态报单的成交金额应等于０'

    # 判断报单中的委托时间不能为空
    elif data['insert_time'] == 0:
        logger.error('错误，报单委托时间不能为空，报单返回的委托时间为'+str(data['insert_time']))
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = False
        bdquery_result['错误信息'] = '报单委托时间不能为空'

    # 判断报单中的撤单时间不能为空
    elif data['cancel_time'] == 0:
        logger.error('错误，报单撤单时间不能为空，报单返回的撤单时间为'+str(data['cancel_time']))
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = False
        bdquery_result['错误信息'] = '报单撤单时间不能为空'

    # 判断撤单xtpID是否正确
    # 注：当前报单查询撤单xtpID显示为０，所以验证代码暂且屏蔽
    # elif data['order_cancel_xtp_id']!=case_goal['cancel_xtpID']:
    #     print '报单查询的撤单xtpID不正确，实际显示的撤单xtpID为',data['order_cancel_xtp_id']
    #     bdquery_result['报单检查状态'] = 'end'
    #     bdquery_result['测试结果'] = False
    #     bdquery_result['错误信息'] = '报单查询的撤单xtpID不正确'

    # 判断其它项：最后修改时间，撤销时间,err_code,Err_Msg
    elif data['update_time'] != 0 and error['error_id'] != 0 and error['error_msg'] != '':
        logger.error('错误，请检查最后修改时间，err_code,err_msg!它们的值分别是：'+str(data['update_time'])+','+str(error['error_id'])+','+error['error_msg'])
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = False
        bdquery_result['错误信息'] = '错误，请检查最后修改时间，撤单时间,err_code,err_msg!'

    else:
        bdquery_result['报单检查状态'] = 'end'
        bdquery_result['测试结果'] = True
        bdquery_result['错误信息'] = ''
        logger.info('已撤状态的报单查询业务校验正确')

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
#--撤单报单查询-状态初始-校验
#-----------------------------------------------------------------------------------------------------------------------
def cdQuery_init(wt_reqs, data, error):
    logger.info('正在进行撤单报单查询初始状态业务校验')
    cdquery_result = {
        '报单检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
    }
    # 初始状态的撤单报单，成交数量、剩余数量、成交金额应该是０
    if data['qty_traded'] != 0:
        logger.error('错误，撤单报单初始状态报单的成交数量应为０，返回报单的成交数量为'+str(data['qty_traded']))
        cdquery_result['报单检查状态'] = 'end'
        cdquery_result['测试结果'] = False
        cdquery_result['错误信息'] = '撤单报单初始状态报单的成交数量应为０'
    # 判断未成交数量是否等于0
    elif data['qty_left'] != 0:
        logger.error('错误，撤单报单初始状态的剩余数量应等于０，返回报单的剩余成交数量是'+str(wt_reqs['quantity'])+','+str(data['qty_left']))
        cdquery_result['报单检查状态'] = 'end'
        cdquery_result['测试结果'] = False
        cdquery_result['错误信息'] = '撤单报单初始状态的剩余数量应等于０'
    # 判断成交金额是否是０
    elif data['trade_amount'] != 0.0:
        logger.error('错误，撤单报单初始状态的成交金额应为０，返回报单的成交金额为'+str(data['trade_amount']))
        cdquery_result['报单检查状态'] = 'end'
        cdquery_result['测试结果'] = False
        cdquery_result['错误信息'] = '撤单报单初始状态的成交金额应为０'
    elif data['insert_time'] == 0:
        logger.error('错误，撤单报单初始状态的委托时间不能为空，报单返回的委托时间为'+str(data['insert_time']))
        cdquery_result['报单检查状态'] = 'end'
        cdquery_result['测试结果'] = False
        cdquery_result['错误信息'] = '撤单报单初始状态的委托时间不能为空'
    # 判断其它项：最后修改时间，撤销时间，撤单xtpID,err_code,Err_Msg
    elif data['update_time'] != 0 and data['cancel_time'] != 0 and data['order_cancel_xtp_id'] != 0 and error[
        'error_id'] != 0 and error['error_msg'] != '':
        logger.error('错误，请检查最后修改时间，撤单时间，撤单xtpID,err_code,err_msg!它们的值分别是：' + str(data['update_time']) + ',' + str(
            data['cancel_time']) + ',' + str(data['order_cancel_xtp_id']) + ',' + str(error['error_id']) + ',' + error['error_msg'])
        cdquery_result['报单检查状态'] = 'end'
        cdquery_result['测试结果'] = False
        cdquery_result['错误信息'] = '错误，请检查初始状态的查询撤单报单的最后修改时间，撤单时间，撤单xtpID,err_code,err_msg!'
    else:
        cdquery_result['报单检查状态'] = 'end'
        cdquery_result['测试结果'] = True
        logger.info('撤单报单查询初始状态业务校验正确')

    return cdquery_result


#-----------------------------------------------------------------------------------------------------------------------
#--撤单报单查询-状态部撤-校验
#-----------------------------------------------------------------------------------------------------------------------
def cdQuery_partCancle(wt_reqs, data, error):
    logger.info('正在进行撤单报单查询部撤状态业务校验')
    cdquery_result = {
        '报单检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
    }
    # 部撤状态的撤单报单，成交数量应大于０小于委托数量
    if data['qty_traded'] <=0 or data['qty_traded']>=wt_reqs['quantity']:
        logger.error('错误，部撤状态的撤单报单，成交数量应大于０小于委托数量，委托数量和返回报单的成交数量分别为'+str(wt_reqs['quantity'])+','+str(data['qty_traded']))
        cdquery_result['报单检查状态'] = 'end'
        cdquery_result['测试结果'] = False
        cdquery_result['错误信息'] = '部撤状态的撤单报单，成交数量应大于０小于委托数量'
    # 判断剩余成交数量是否等于0
    elif data['qty_left'] != 0:
        logger.error('错误，部撤状态的撤单报单查询，剩余数量应等于０，返回报单的剩余成交数量是'+str(wt_reqs['quantity'])+','+str(data['qty_left']))
        cdquery_result['报单检查状态'] = 'end'
        cdquery_result['测试结果'] = False
        cdquery_result['错误信息'] = '部撤状态的撤单报单查询，剩余数量应等于０'
    # 判断成交金额是否是０
    elif data['trade_amount'] != 0.0:
        logger.error('错误，部撤状态的撤单报单查询，成交金额应为０，返回报单的成交金额为'+str(data['trade_amount']))
        cdquery_result['报单检查状态'] = 'end'
        cdquery_result['测试结果'] = False
        cdquery_result['错误信息'] = '部撤状态的撤单报单查询，成交金额应为０'
    elif data['insert_time'] == 0:
        logger.error('错误，部撤状态的撤单报单查询，委托时间不能为空，报单返回的委托时间为'+str(data['insert_time']))
        cdquery_result['报单检查状态'] = 'end'
        cdquery_result['测试结果'] = False
        cdquery_result['错误信息'] = '部撤状态的撤单报单查询，委托时间不能为空'
    #撤销时间不能为０
    elif data['cancel_time']== 0:
        logger.error('错误，部撤状态的撤单报单查询，撤单时间不能为空，报单返回的撤单时间为'+str(data['cancel_time']))
        cdquery_result['报单检查状态'] = 'end'
        cdquery_result['测试结果'] = False
        cdquery_result['错误信息'] = '部撤状态的撤单报单查询，撤单时间不能为空'
    # 判断其它项：最后修改时间，撤单xtpID,err_code,Err_Msg
    elif data['update_time'] != 0 and data['order_cancel_xtp_id'] != 0 and error[
        'error_id'] != 0 and error['error_msg'] != '':
        logger.error('错误，请检查部撤状态的查询撤单报单的最后修改时间，撤单xtpID,err_code,err_msg!它们的值分别是：'+str(data['update_time'])+','+str(data['order_cancel_xtp_id'])+','+str(error['error_id'])+','+error['error_msg'])
        cdquery_result['报单检查状态'] = 'end'
        cdquery_result['测试结果'] = False
        cdquery_result['错误信息'] = '错误，请检查部撤状态的查询撤单报单的最后修改时间，撤单xtpID,err_code,err_msg!'
    else:
        cdquery_result['报单检查状态'] = 'end'
        cdquery_result['测试结果'] = True
        logger.info('撤单报单查询部撤状态业务校验正确')

    return cdquery_result

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
            '错误，报单返回的未成交数量应等于0，返回报单的未成交数量是' + str(wt_reqs['quantity']) )
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


