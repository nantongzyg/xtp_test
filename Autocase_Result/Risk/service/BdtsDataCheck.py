#!/usr/bin/python
# -*- encoding: utf-8 -*-
import time
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from log import *
from CheckDataPrice import *
import ServiceConfig
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *

bd_time={
    '未成交':None,
    '全部成交':None,
    '已撤':None,
    '部撤':None,
    '废单':None,
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

#报单推送业务处理方法
def bdtsDataCheck(Api,wt_reqs,case_goal,data,error):
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
    bdhb_result = bd_type_Handle(Api, wt_reqs, case_goal, data, error)
    result['报单检查状态'] = bdhb_result['报单检查状态']
    result['测试结果'] = bdhb_result['测试结果']
    result['错误信息'] = bdhb_result['错误信息']

    logger.info('报单推送数据检查结束，检查结果如下')
    dictLogging(result)
    return result

#-----------------------------------------------------------------------------------------------------------------------
#--报单为报单类型的业务处理
#-----------------------------------------------------------------------------------------------------------------------
def bd_type_Handle(Api,wt_reqs,case_goal,data,error):
    # 定义测试结果参数
    bdhb_result = {
        '报单检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
    }

    # --下面是根据报单的状态调用各自对应的校验方法
    # --如果是废单状态的，执行如下
    if data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_REJECTED']:
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
                logger.error('期望状态和报单状态、提交状态不匹配，期望状态、报单状态、提交状态分别为' + case_goal['期望状态'] + ',' + str(data['order_status']) + ',' + str(data['order_submit_status']))
                bdhb_result['报单检查状态'] = 'end'
                bdhb_result['测试结果'] = False
                bdhb_result['错误信息'] = '期望状态和报单状态、提交状态不匹配'
        else:
            logger.error('报单提交状态不正确')
            bdhb_result['报单检查状态'] = 'end'
            bdhb_result['测试结果'] = False
            bdhb_result['错误信息'] = '报单提交状态不正确'
    else:
        if case_goal['期望状态'] == '废单':
            logger.error('期望状态和报单状态、提交状态不匹配，期望状态、报单状态、提交状态分别为' + case_goal[
                '期望状态'] + ',' + str(data['order_status']) + ',' + str(
                data['order_submit_status']))
        else:
            logger.info('风控校验-非废单提交状态和报单状态正确')

    return bdhb_result

#-----------------------------------------------------------------------------------------------------------------------
#--下单推送--未成交-校验
#-----------------------------------------------------------------------------------------------------------------------
def no_match(wt_reqs,case_goal,data,error):
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
        logger.error('错误，报单返回的未成交数量应等于委托数量，返回报单的未成交数量和原委托数量分别是'+str(wt_reqs['quantity'])+','+str(data['qty_left']))
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '报单返回的未成交数量应等于委托数量'

    # 判断成交金额是否是０
    elif data['trade_amount'] != 0.0:
        logger.error('错误，未成交状态报单的成交金额应为０，返回报单的成交金额为'+str(data['trade_amount']))
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '未成交状态报单的成交金额应为０'

    # 判断报单中的委托时间不能为空
    elif data['insert_time'] == 0:
        logger.error('错误，报单委托时间不能为空，报单返回的委托时间为'+str(data['insert_time']))
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '报单委托时间不能为空'

    # 判断其它项：最后修改时间，撤销时间，撤单xtpID,err_code,Err_Msg
    elif data['update_time'] != 0 and data['cancel_time'] != 0 and data['order_cancel_xtp_id'] != 0 and error[
        'error_id'] != 0 and error['error_msg'] != '':
        logger.error('错误，请检查最后修改时间，撤单时间，撤单xtpID,err_code,err_msg!它们的值分别是：'+str(data['update_time'])+','+str(data['cancel_time'])+','+str(data['order_cancel_xtp_id'])+','+str(error['error_id'])+','+str(error['error_msg']))
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
def all_match(wt_reqs,case_goal,data,error):
    logger.info('这里是全部成交状态的报单推送业务校验')
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
    elif data['trade_amount'] <= 0.0:
        logger.error('错误，全部成交状态报单的成交金额应大于０，返回报单的成交金额为'+str(data['trade_amount']))
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
    elif data['update_time'] != 0 and data['cancel_time'] != 0 and data['order_cancel_xtp_id'] != 0 and error[
        'error_id'] != 0 and error['error_msg'] != '':
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

    return bdhb_result


#-----------------------------------------------------------------------------------------------------------------------
#--下单推送--部分撤单-校验
#-----------------------------------------------------------------------------------------------------------------------
def part_cancel(wt_reqs,case_goal,data,error):
    logger.info('这里是部分撤单状态的报单推送业务校验')
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

    # 判断成交数量是否大于0
    if data['qty_traded'] <= 0:
        logger.error('错误，部分撤单状态的报单返回的成交数量应大于0，实际返回的成交数量为'+str(data['qty_traded']))
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '部分撤单状态的报单返回的成交数量应大于0'

    # 判断撤单数量是否大于0
    elif data['qty_left'] <= 0:
        logger.error('错误，部分撤单状态的报单返回的撤单数量应大于0，实际返回的撤单数量为'+str(data['qty_left']))
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '部分撤单状态的报单返回的撤单数量应大于0'

    # 判断成交金额是否大于０
    elif data['trade_amount'] <= 0.0:
        logger.error('错误，部分撤单状态报单的成交金额应大于０，返回报单的成交金额为'+str(data['trade_amount']))
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '部分撤单状态报单的成交金额应大于０'

    # 判断报单中的委托时间不能为空
    elif data['insert_time'] == 0:
        logger.error('错误，报单委托时间不能为空，报单返回的委托时间为'+str(data['insert_time']))
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '报单委托时间不能为空'

    # 判断报单中的撤单时间不能为空
    elif data['cancel_time'] == 0:
        logger.error('错误，报单撤单时间不能为空，报单返回的撤单时间为'+str(data['cancel_time']))
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '报单撤单时间不能为空'

    # 判断其它项：最后修改时间，撤销时间，撤单xtpID,err_code,Err_Msg
    elif data['update_time'] != 0 and data['order_cancel_xtp_id'] != 0 and error[
        'error_id'] != 0 and error['error_msg'] != '':
        logger.error('错误，请检查最后修改时间，撤单xtpID,err_code,err_msg!它们的值分别是：'+str(data['update_time'])+','+str(data['order_cancel_xtp_id'])+','+str(error['error_id'])+error['error_msg'])
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '错误，请检查最后修改时间，撤单时间，撤单xtpID,err_code,err_msg!'

    # 判断推送时间
    elif bd_time['部撤'] <= bd_time['未成交']:
        logger.error('部撤推送应晚于未成交推送')
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '部撤推送应晚于未成交推送'

    else:
        logger.info('部分撤单状态报单回报校验正确！')
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = True
        bdhb_result['错误信息'] = ''

    return bdhb_result

#-----------------------------------------------------------------------------------------------------------------------
#--下单推送--已撤-校验
#-----------------------------------------------------------------------------------------------------------------------
def all_cancel(wt_reqs,data,error):
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
        logger.error('错误，已撤状态的报单返回的成交数量应等于0，实际返回的成交数量为'+str(data['qty_traded']))
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '已撤状态的报单返回的成交数量应等于0'

    # 判断撤单数量是否等于委托数量
    elif data['qty_left'] != wt_reqs['quantity']:
        logger.error('错误，已撤状态的报单返回的撤单数量应等于委托数量，原委托数量和实际返回的撤单数量为'+str(wt_reqs['quantity'])+','+str(data['qty_left']))
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '已撤状态的报单返回的撤单数量应等于委托数量'

    # 判断成交金额是否大于０
    elif data['trade_amount'] != 0.0:
        logger.error('错误，已撤成交状态报单的成交金额应等于０，返回报单的成交金额为'+str(data['trade_amount']))
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '已撤成交状态报单的成交金额应等于０'

    # 判断报单中的委托时间不能为空
    elif data['insert_time'] == 0:
        logger.error('错误，报单委托时间不能为空，报单返回的委托时间为'+str(data['insert_time']))
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '报单委托时间不能为空'

    # 判断报单中的撤单时间不能为空
    elif data['cancel_time'] == 0:
        logger.error('错误，报单撤单时间不能为空，报单返回的撤单时间为'+str(data['cancel_time']))
        bdhb_result['报单检查状态'] = 'end'
        bdhb_result['测试结果'] = False
        bdhb_result['错误信息'] = '报单撤单时间不能为空'

    # 判断其它项：最后修改时间，撤单xtpID,err_code,Err_Msg
    elif data['update_time'] != 0 and data['order_cancel_xtp_id'] != 0 and error[
        'error_id'] != 0 and error['error_msg'] != '':
        logger.error('错误，请检查最后修改时间，撤单xtpID,err_code,err_msg!它们的值分别是：' + str(data['update_time']) + ',' + str(
            data['order_cancel_xtp_id']) + ',' + str(error['error_id']) + error['error_msg'])
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


#-----------------------------------------------------------------------------------------------------------------------
#--下单推送--废单-校验
#-----------------------------------------------------------------------------------------------------------------------
def reject(wt_reqs,case_goal,data,error):
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

    #校验errID，不校验err_msg
    if is_check_errID and is_check_errMsg is False:
        if error['error_id'] != case_goal['errorID']:
            logger.error('报单的error_id与用例期望的不一致，期望和实际的error_id分别是' + str(case_goal['errorID']) + ',' + str(error['error_id']))
            bdhb_result['报单检查状态'] = 'end'
            bdhb_result['测试结果'] = False
            bdhb_result['错误信息'] = '报单的error_id与用例期望的不一致'
        else:
            logger.info('未成交状态报单回报校验正确！')
            bdhb_result['报单检查状态'] = 'end'
            bdhb_result['测试结果'] = True
            bdhb_result['错误信息'] = ''
    # 校验errID，校验err_msg
    elif is_check_errID and is_check_errMsg:
        # 判断废单的error_msg与期望的是否一致
        if error['error_id'] != case_goal['errorID']:
            logger.error('报单的error_id与用例期望的不一致，期望和实际的error_id分别是' + str(case_goal['errorID']) + ',' + str(error['error_id']))
            bdhb_result['报单检查状态'] = 'end'
            bdhb_result['测试结果'] = False
            bdhb_result['错误信息'] = '报单的error_id与用例期望的不一致'
        elif error['error_msg'] != case_goal['errorMSG']:
            logger.error('报单的error_msg与用例期望的不一致，期望和实际的error_msg分别是'+str(case_goal['errorMSG'])+','+str(error['error_msg']))
            bdhb_result['报单检查状态'] = 'end'
            bdhb_result['测试结果'] = False
            bdhb_result['错误信息'] = '报单的error_msg与用例期望的不一致'
        else:
            logger.info('未成交状态报单回报校验正确！')
            bdhb_result['报单检查状态'] = 'end'
            bdhb_result['测试结果'] = True
            bdhb_result['错误信息'] = ''
    #当errID不校验(err_msg也不校验)
    elif is_check_errID is False:
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
