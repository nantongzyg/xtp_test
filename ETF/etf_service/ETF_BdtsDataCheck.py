#!/usr/bin/python
# -*- encoding: utf-8 -*-
import time
import math
from log import *
from CheckDataPrice import *
import ServiceConfig
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/ETF/etf_mysql")
from QueryEtfNavDB import *
from QueryEtfQty import stkQty

#---定义费率，最低收费
fee_rate_etf_creation = ServiceConfig.FEE_RATE_ETF_CREATION
fee_rate_etf_redemption =ServiceConfig.FEE_RATE_ETF_REDEMPTION
fee_etf_min = ServiceConfig.FEE_ETF_MIN

bd_time={
    '未成交':None,
    '全部成交':None,
    '已撤':None,
    '部撤':None,
    '废单':None
}

#初始化全局变量报单时间bd_time 为空
def bdTimeInit():
    bd_time['未成交'] = None
    bd_time['部分成交'] = None
    bd_time['全部成交'] = None
    bd_time['已撤'] = None
    bd_time['部撤'] = None
    bd_time['废单'] = None
#获取配置：废单是否校验err_msg
is_check_errMsg=ServiceConfig.IS_CHECK_ERR_MSG_FROM_BDTS
is_check_errID=ServiceConfig.IS_CHECK_ERRID_FROM_BDTS

# 定义测试结果参数
bdhb_result = {
    '报单检查状态': 'init',
    '测试结果': False,
    '错误信息': '',
    '报单状态': None,
    '提交状态': None,
    '成交数量': None,
    '成交金额': None,
}

#报单推送业务处理方法
def etf_bdtsDataCheck(Api,wt_reqs,case_goal,data,error,QueryInit,QueryEnd):
    # 定义测试结果参数
    result = {
        '报单检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
        '报单状态': data['order_status'],
        '提交状态': data['order_submit_status'],
        '成交数量': data['qty_traded'],
        '剩余数量': data['qty_left'],
        '成交金额': data['trade_amount'],
        '委托价格': data['price'],
        'xtpID':data['order_xtp_id'],
        '委托时间':data['insert_time'],
        '最后修改时间':data['update_time'],
        '撤销时间':data['cancel_time'],
        'cancel_xtpID':data['order_cancel_xtp_id'],
        'Err_code':error['error_id'],
        'ErrMsg':error['error_msg'],
    }
    #(委托入参)公共业务检查
    public_result=etf_public_Handle(Api,wt_reqs,data)
    global bdhb_result
    if public_result['报单检查状态']=='pending' and public_result['测试结果']==True:
        etf_bd_type_Handle(Api, wt_reqs, case_goal, data, error, QueryInit, QueryEnd)
        result['报单检查状态'] = bdhb_result['报单检查状态']
        result['测试结果'] = bdhb_result['测试结果']
        result['错误信息'] = bdhb_result['错误信息']

    else:
        result['报单检查状态'] = public_result['报单检查状态']
        result['测试结果'] = public_result['测试结果']
        result['错误信息'] = public_result['错误信息']

    logger.info('报单推送数据检查结束，检查结果如下')
    dictLogging(result)

    return result

#-----------------------------------------------------------------------------------------------------------------------
#--定义（委托入参）公共业务检查
#-----------------------------------------------------------------------------------------------------------------------
def etf_public_Handle(Api,wt_reqs,data):
    # 定义测试结果参数
    public_result = {
        '报单检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
    }
    # 判断证券代码是否一致
    if data['ticker'] != wt_reqs['ticker']:
        logger.error('错误，报单返回的证券代码与原委托不一致，委托证券代码和报单回报证券代码分别是'+wt_reqs['ticker']+','+data['ticker'])
        public_result['报单检查状态'] = 'end'
        public_result['测试结果'] = False
        public_result['错误信息'] = '报单返回的证券代码与原委托不一致'

    # 判断市场是否一致
    elif data['market'] != wt_reqs['market']:
        logger.error('错误，报单返回的市场与原委托不一致，原委托市场和报单回报市场分别是' +str(wt_reqs['market']) + ',' +str(data['market']))
        public_result['报单检查状态'] = 'end'
        public_result['测试结果'] = False
        public_result['错误信息'] = '报单返回的市场与原委托不一致'

    # 判断委托方向是否一致
    elif data['side'] != wt_reqs['side']:
        logger.error('报单返回的委托方向与原委托不一致')
        public_result['报单检查状态'] = 'end'
        public_result['测试结果'] = False
        public_result['错误信息'] = '报单返回的委托方向与原委托不一致'

    # 判断价格条件是否一致
    elif data['price_type'] != wt_reqs['price_type'] and \
           wt_reqs['business_type'] != \
           Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_ETF']:
        logger.error('错误，报单返回的价格条件与原委托不一致，原委托价格条件和报单回报的价格条件分别是'+str(wt_reqs['price_type'])+','+str(data['price_type']))
        public_result['报单检查状态'] = 'end'
        public_result['测试结果'] = False
        public_result['错误信息'] = '报单返回的价格条件与原委托不一致'

    # 判断委托数量是否一致
    elif data['quantity'] != wt_reqs['quantity']:
        logger.error('错误，报单返回的委托数量和原委托数量不一致，原委托数量和报单返回的委托数量分别是' + str(wt_reqs['quantity']) + ',' + str(data['quantity']))
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
def etf_bd_type_Handle(Api,wt_reqs,case_goal,data,error,QueryInit,QueryEnd):
    global bdhb_result
    # --判断报单返回的data
    # 判断xtpID是否一致
    if data['order_xtp_id'] != case_goal['xtp_ID']:
        logger.error('错误，报单返回的xtpID与原委托不一致，下单xtp_ID和报单回报xtp_ID分别是'+str(case_goal['xtp_ID'])+','+str(data['order_xtp_id']))
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '报单返回的xtpID与原委托不一致'

    # 判断已成交数量加上待成交数量（撤单数量）是否等于委托数量
    elif data['qty_traded'] + data['qty_left'] != wt_reqs['quantity']:
        logger.error('错误，报单返回的成交数量加上待成交数量（撤单数量）应等于委托数量，委托数量和返回报单的成交数量和待成交数量（撤单数量）分别为'+str(wt_reqs['quantity'])+','+str(data['qty_traded'])+','+str(data['qty_left']))
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '报单返回的成交数量加上待成交数量（撤单数量）应等于委托数量'

    # --下面是根据报单的状态调用各自对应的校验方法
    # --如果报单是‘未成交’状态的执行如下，通过下单后的报单推送
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_NOTRADEQUEUEING']:
        if data['order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
            'XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
            bd_time['未成交'] = time.time()
            logger.error('报单回报状态为未成交,提交状态为已提交,'+str(data['order_status'])+','+str(data['order_submit_status']))
            # 如果期望状态是未成交，执行(‘部成’的报单推送与‘未成交’的一样)
            if case_goal['期望状态'] in ('未成交'):
                bdhb_result = no_match(wt_reqs, case_goal, data, error)
            elif case_goal['期望状态'] in('全成','已撤','废单','撤废'):
                bdhb_result['报单检查状态'] = 'pending'
                bdhb_result['测试结果'] = False
                bdhb_result['错误信息'] = ''
            else:
                logger.error('期望状态和报单状态、提交状态不匹配，期望状态、报单状态、提交状态分别为'+case_goal['期望状态']+','+str(data['order_status'])+','+str(data['order_submit_status']))
                bdhb_result['报单检查状态'] = 'end'
                bdhb_result['测试结果'] = False
                bdhb_result['错误信息'] = '期望状态和报单状态、提交状态不匹配'

        else:
            bdhb_result['报单检查状态'] = 'end'
            bdhb_result['测试结果'] = False
            bdhb_result['错误信息'] = '报单提交状态不正确'

    # --如果报单回报是全成状态的，执行如下
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_ALLTRADED']:
        if data['order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
            'XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
            bd_time['全部成交'] = time.time()
            logger.info('报单回报状态为全部成交，提交状态为已提交,'+str(data['order_status'])+','+str(data['order_submit_status']))
            # 期望状态如果是为全成，执行
            if case_goal['期望状态'] == '全成':
                all_match(Api, wt_reqs, case_goal, data, error, QueryInit, QueryEnd)
            elif case_goal['期望状态'] == '撤废':
                bdhb_result['报单检查状态'] = 'pending'
                bdhb_result['测试结果'] = False
                bdhb_result['错误信息'] = ''
            else:
                logger.error('期望状态和报单状态、提交状态不匹配，期望状态、报单状态、提交状态分别为'+case_goal['期望状态']+','+str(data['order_status'])+','+str(data['order_submit_status']))
                bdhb_result['报单检查状态'] = 'end'
                bdhb_result['测试结果'] = False
                bdhb_result['错误信息'] = '期望状态和报单状态、提交状态不匹配'
        else:
            bdhb_result['报单检查状态'] = 'end'
            bdhb_result['测试结果'] = False
            bdhb_result['错误信息'] = '报单提交状态不正确'
        # --如果是已撤状态的，执行如下
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE[
        'XTP_ORDER_STATUS_CANCELED']:
        if data['order_submit_status'] == \
                Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
                    'XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
            bd_time['已撤'] = time.time()
            logger.info('报单回报状态为已撤,' + str(data['order_status']))
            # 期望状态如果是为已撤，执行
            if case_goal['期望状态'] in ('已撤', '内部撤单'):
                bdhb_result = all_cancel(wt_reqs, data, error)
            # 期望状态如果是撤废（已撤后进行撤单），执行
            elif case_goal['期望状态'] == '撤废':
                bdhb_result['报单检查状态'] = 'pending'
                bdhb_result['测试结果'] = False
                bdhb_result['错误信息'] = ''
            elif case_goal['期望状态'] == '未成交' and case_goal['是否是撤废'] == '是' and \
                            case_goal['是否是集合竞价'] == '否':
                bdhb_result['报单检查状态'] = 'pending'
                bdhb_result['测试结果'] = False
                bdhb_result['错误信息'] = ''
            else:
                logger.error('期望状态和报单状态、提交状态不匹配，期望状态、报单状态、提交状态分别为' + case_goal[
                    '期望状态'] + ',' + str(data['order_status']) + ',' + str(
                    data['order_submit_status']))
                bdhb_result['报单检查状态'] = 'end'
                bdhb_result['测试结果'] = False
                bdhb_result['错误信息'] = '期望状态和报单状态、提交状态不匹配'
        else:
            logger.error('报单提交状态不正确')
            bdhb_result['报单检查状态'] = 'end'
            bdhb_result['测试结果'] = False
            bdhb_result['错误信息'] = '报单提交状态不正确'

    # --如果是废单状态的，执行如下
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_REJECTED']:
        if data['order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
            'XTP_ORDER_SUBMIT_STATUS_INSERT_REJECTED']:
            bd_time['废单'] = time.time()
            logger.info('报单回报状态为废单,' + str(data['order_status']))
            # 期望状态如果是为废单，执行
            if case_goal['期望状态'] == '废单':
                bdhb_result = reject(wt_reqs, case_goal, data, error)
            # 期望状态如果是撤废（已撤后进行撤单），执行
            elif case_goal['期望状态'] == '撤废':
                bdhb_result['报单检查状态'] = 'pending'
                bdhb_result['测试结果'] = False
                bdhb_result['错误信息'] = ''
            else:
                logger.error('期望状态和报单状态、提交状态不匹配，期望状态、报单状态、提交状态分别为' + case_goal['期望状态'] + ',' + str(
                    data['order_status']) + ',' + str(data['order_submit_status']))
                bdhb_result['报单检查状态'] = 'end'
                bdhb_result['测试结果'] = False
                bdhb_result['错误信息'] = '期望状态和报单状态、提交状态不匹配'
        else:
            logger.error('报单提交状态不正确')
            bdhb_result['报单检查状态'] = 'end'
            bdhb_result['测试结果'] = False
            bdhb_result['错误信息'] = '报单提交状态不正确'

    # --如果是未知状态的，执行如下
    else:
        bdhb_result = unknown(data)
        logger.error('当前报单返回的状态未知,' + str(data['order_status']))

# -----------------------------------------------------------------------------------------------------------------------
# --下单推送--未成交-校验
# -----------------------------------------------------------------------------------------------------------------------
def no_match(wt_reqs, case_goal, data, error):
    logger.info('这里是未成交状态的报单推送业务校验')
    # 定义测试结果参数
    bdhb_result = {
        '报单检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
        '报单状态': None,
        '提交状态': None,
        '成交数量': 0,
        '成交金额': 0.00,
    }

    # 判断成交数量是否为０
    if data['qty_traded'] != 0:
        logger.error('错误，未成交状态报单的成交数量应为０，返回报单的成交数量为', str(data['qty_traded']))
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '未成交状态报单的成交数量应为０'

    # 判断未成交数量是否等于委托数量
    elif data['qty_left'] != wt_reqs['quantity']:
        logger.error(
            '错误，报单返回的未成交数量应等于委托数量，返回报单的未成交数量和原委托数量分别是' + str(wt_reqs['quantity']) + ',' + str(data['qty_left']))
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '报单返回的未成交数量应等于委托数量'

    # 判断成交金额是否是０
    elif data['trade_amount'] != 0.0:
        logger.error('错误，未成交状态报单的成交金额应为０，返回报单的成交金额为' + str(data['trade_amount']))
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '未成交状态报单的成交金额应为０'

    # 判断报单中的委托时间不能为空
    elif data['insert_time'] == 0:
        logger.error('错误，报单委托时间不能为空，报单返回的委托时间为' + str(data['insert_time']))
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '报单委托时间不能为空'

    # 判断其它项：最后修改时间，撤销时间，撤单xtpID,err_code,Err_Msg
    elif data['update_time'] != 0 and data['cancel_time'] != 0 and data['order_cancel_xtp_id'] != 0 and error[
        'error_id'] != 0 and error['error_msg'] != '':
        logger.error('错误，请检查最后修改时间，撤单时间，撤单xtpID,err_code,err_msg!它们的值分别是：' + str(data['update_time']) + ',' + str(
            data['cancel_time']) + ',' + str(data['order_cancel_xtp_id']) + ',' + str(
            error['error_id']) + ',' + str(error['error_msg']))
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '错误，请检查最后修改时间，撤单时间，撤单xtpID,err_code,err_msg!'

    else:
        logger.info('未成交状态报单回报校验正确！')
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = True
        bdhb_result['错误信息'] = ''

    return bdhb_result


#-----------------------------------------------------------------------------------------------------------------------
#--下单推送--全部成交-校验
#-----------------------------------------------------------------------------------------------------------------------
def all_match(Api,wt_reqs,case_goal,data,error,QueryInit,QueryEnd):
    logger.info('这里是全部成交状态的报单推送业务校验')
    '''
    --------------------------------------------------------------------------------------------------------------------
    报单信息校验
    --------------------------------------------------------------------------------------------------------------------
    '''
    global bdhb_result
    bdhb_result['报单状态'] = data['order_status']
    bdhb_result['提交状态'] = data['order_submit_status']
    bdhb_result['成交数量'] = data['qty_traded']
    bdhb_result['成交金额'] = data['qty_traded']

    # 判断成交数量和委托数量是否一致
    if data['qty_traded'] != wt_reqs['quantity']:
        logger.error('错误，全部成交状态报单的成交数量应和委托数量一致，委托数量和返回报单的成交数量分别为'+str(wt_reqs['quantity'])+','+str(data['qty_traded']))
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '全部成交状态报单的成交数量应和委托数量一致'

    # 判断未成交数量是否等于0
    elif data['qty_left'] != 0:
        logger.error('错误，全部成交状态的报单返回的未成交数量应等于0，实际返回的未成交数量为'+str(data['qty_left']))
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '全部成交状态的报单返回的未成交数量应等于0'

    # 判断成交金额是否大于０
    elif data['trade_amount'] < 0.0:
        logger.error('错误，全部成交状态报单的成交金额应不小于０，返回报单的成交金额为'+str(data['trade_amount']))
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '全部成交状态报单的成交金额应大于０'

    # 判断报单中的委托时间不能为空
    elif data['insert_time'] == 0:
        logger.error('错误，报单委托时间不能为空，报单返回的委托时间为'+str(data['insert_time']))
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '报单委托时间不能为空'

    # 判断其它项：最后修改时间，撤销时间，撤单xtpID,err_code,Err_Msg
    elif data['update_time'] != 0 and data['cancel_time'] != 0 and data['order_cancel_xtp_id'] != 0 and \
            error['error_id'] != 0 and error['error_msg'] != '':
        logger.error('错误，请检查最后修改时间，撤单时间，撤单xtpID,err_code,err_msg!它们的值分别是：'+str(data['update_time'])+','+str(data['cancel_time'])+','+str(data['order_cancel_xtp_id'])+','+str(error['error_id'])+','+error['error_msg'])
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '错误，请检查最后修改时间，撤单时间，撤单xtpID,err_code,err_msg!'

    # 判断推送时间
    elif bd_time['全部成交'] <= bd_time['未成交']:
        logger.error('全部成交推送应晚于未成交推送')
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '全部成交推送应晚于未成交推送'

    else:
        logger.info('全部成交状态报单回报校验正确！')
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = True
        bdhb_result['错误信息'] = ''

# -----------------------------------------------------------------------------------------------------------------------
# --下单推送--已撤-校验
# -----------------------------------------------------------------------------------------------------------------------
def all_cancel(wt_reqs, data, error):
    logger.info('这里是已撤状态的报单推送业务校验')
    # 定义测试结果参数
    bdhb_result = {
        '报单检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
        '报单状态': data['order_status'],
        '提交状态': data['order_submit_status'],
        '成交数量': data['qty_traded'],
        '成交金额': data['trade_amount'],
    }

    # 判断成交数量是否等于0
    if data['qty_traded'] != 0:
        logger.error(
            '错误，已撤状态的报单返回的成交数量应等于0，实际返回的成交数量为' + str(data['qty_traded']))
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '已撤状态的报单返回的成交数量应等于0'

    # 判断撤单数量是否等于委托数量
    elif data['qty_left'] != wt_reqs['quantity']:
        logger.error('错误，已撤状态的报单返回的撤单数量应等于委托数量，原委托数量和实际返回的撤单数量为' + str(
            wt_reqs['quantity']) + ',' + str(data['qty_left']))
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '已撤状态的报单返回的撤单数量应等于委托数量'

    # 判断成交金额是否大于０
    elif data['trade_amount'] != 0.0:
        logger.error(
            '错误，已撤成交状态报单的成交金额应等于０，返回报单的成交金额为' + str(data['trade_amount']))
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '已撤成交状态报单的成交金额应等于０'

    # 判断报单中的委托时间不能为空
    elif data['insert_time'] == 0:
        logger.error('错误，报单委托时间不能为空，报单返回的委托时间为' + str(data['insert_time']))
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '报单委托时间不能为空'

    # 判断报单中的撤单时间不能为空
    elif data['cancel_time'] == 0:
        logger.error('错误，报单撤单时间不能为空，报单返回的撤单时间为' + str(data['cancel_time']))
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '报单撤单时间不能为空'

    # 判断其它项：最后修改时间，撤单xtpID,err_code,Err_Msg
    elif data['update_time'] != 0 and data['order_cancel_xtp_id'] != 0 and \
                    error[
                        'error_id'] != 0 and error['error_msg'] != '':
        logger.error('错误，请检查最后修改时间，撤单xtpID,err_code,err_msg!它们的值分别是：' + str(
            data['update_time']) + ',' + str(
            data['order_cancel_xtp_id']) + ',' + str(error['error_id']) +
                     error['error_msg'])
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '错误，请检查最后修改时间，撤单时间，撤单xtpID,err_code,err_msg!'

    # 判断推送时间
    elif bd_time['已撤'] <= bd_time['未成交']:
        logger.error('已撤推送应晚于未成交推送')
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '已撤推送应晚于未成交推送'

    else:
        logger.info('已撤状态报单回报校验正确！')
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = True
        bdhb_result['错误信息'] = ''

    return bdhb_result

# -----------------------------------------------------------------------------------------------------------------------
# --下单推送--废单-校验
# -----------------------------------------------------------------------------------------------------------------------
def reject(wt_reqs, case_goal, data, error):
    logger.info('这里是废单状态的报单推送业务校验')
    bdhb_result = {
        '报单检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
        '报单状态': data['order_status'],
        '提交状态': data['order_submit_status'],
        '成交数量': data['qty_traded'],
        '成交金额': data['trade_amount'],
    }
    # 判断成交数量是否为０
    if data['qty_traded'] != 0:
        logger.error('错误，废单状态报单的成交数量应为０，返回报单的成交数量为' + str(data['qty_traded']))
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '废单状态报单的成交数量应为０'

    # 判断未成交数量是否等于委托数量
    elif data['qty_left'] != wt_reqs['quantity']:
        logger.error(
            '错误，报单返回的未成交数量应等于委托数量，返回报单的未成交数量和原委托数量分别是' + str(wt_reqs['quantity']) + ',' + str(data['qty_left']))
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '报单返回的未成交数量应等于委托数量'

    # 判断成交金额是否是０
    elif data['trade_amount'] != 0.0:
        logger.error('错误，废单状态报单的成交金额应为０，返回报单的成交金额为' + str(data['trade_amount']))
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '废单状态报单的成交金额应为０'

    # # 判断报单中的委托时间不能为空
    # elif data['insert_time'] != 0:
    #     logger.error('错误，报单委托时间不能为空，报单返回的委托时间为' + str(data['insert_time']))
    #     bdhb_result['报单检查状态'] = 'end'
    #     bdhb_result['测试结果'] = False
    #     bdhb_result['错误信息'] = '报单委托时间不能为空'

    # 判断其它项：最后修改时间，撤销时间，撤单xtpID
    elif data['update_time'] != 0 and data['cancel_time'] != 0 and data['order_cancel_xtp_id'] != 0:
        logger.error('错误，请检查最后修改时间，撤单时间，撤单xtpID!它们的值分别是：' + str(data['update_time']) + ',' + str(
            data['cancel_time']) + ',' + str(data['order_cancel_xtp_id']))
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '错误，请检查最后修改时间，撤单时间，撤单xtpID!'

    # 判断推送时间
    elif bd_time['废单'] <= bd_time['未成交']:
        logger.error('废单推送应晚于未成交推送')
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '废单推送应晚于未成交推送'

    else:
        # 校验errID，不校验err_msg
        if is_check_errID == True and is_check_errMsg == False:
            if error['error_id'] != case_goal['errorID']:
                logger.error('报单的error_id与用例期望的不一致，期望和实际的error_id分别是' + str(case_goal['errorID']) + ',' + str(
                    error['error_id']))
                bdhb_result['报单检查状态'] = 'end'
                bdhb_result['测试结果'] = False
                bdhb_result['错误信息'] = '报单的error_id与用例期望的不一致'
            else:
                logger.info('未成交状态报单回报校验正确！')
                bdhb_result['报单检查状态'] = 'end'
                bdhb_result['测试结果'] = True
                bdhb_result['错误信息'] = ''
        # 校验errID，校验err_msg
        elif is_check_errID  and is_check_errMsg:
            # 判断废单的error_msg与期望的是否一致
            if error['error_id'] != case_goal['errorID']:
                logger.error('报单的error_id与用例期望的不一致，期望和实际的error_id分别是' + str(case_goal['errorID']) + ',' + str(
                    error['error_id']))
                bdhb_result['报单检查状态'] = 'end'
                bdhb_result['测试结果'] = False
                bdhb_result['错误信息'] = '报单的error_id与用例期望的不一致'
            elif error['error_msg'] != case_goal['errorMSG']:
                logger.error('报单的error_msg与用例期望的不一致，期望和实际的error_msg分别是' + str(case_goal['errorMSG']) + ',' + str(
                    error['error_msg']))
                bdhb_result['报单检查状态'] = 'end'
                bdhb_result['测试结果'] = False
                bdhb_result['错误信息'] = '报单的error_msg与用例期望的不一致'
            else:
                logger.info('未成交状态报单回报校验正确！')
                bdhb_result['报单检查状态'] = 'end'
                bdhb_result['测试结果'] = True
                bdhb_result['错误信息'] = ''
        # 当errID不校验(err_msg也不校验)
        elif is_check_errID == False:
            logger.info('未成交状态报单回报校验正确！')
            bdhb_result['报单检查状态'] = 'end'
            bdhb_result['测试结果'] = True
            bdhb_result['错误信息'] = ''

    return bdhb_result

#-----------------------------------------------------------------------------------------------------------------------
#--下单推送-状态未知-校验
#-----------------------------------------------------------------------------------------------------------------------
def unknown(data):
    bdhb_result = {
        '报单检查状态':'init',
        '测试结果': False,
        '错误信息': '',
        '报单状态': data['order_status'],
        '提交状态': data['order_submit_status'],
        '成交数量': data['qty_traded'],
        '成交金额': data['trade_amount'],
    }

    bdhb_result['报单检查状态'] = 'end'
    bdhb_result['测试结果'] = False
    bdhb_result['错误信息'] = '报单回报状态未知'

    return bdhb_result
