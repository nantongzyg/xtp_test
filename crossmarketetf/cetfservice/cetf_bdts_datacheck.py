#!/usr/bin/python
# -*- encoding: utf-8 -*-
import time
import sys
sys.path.append('/home/yhl2/workspace/xtp_test')
from service.log import *


#获取配置：废单是否校验err_msg
is_check_errMsg=ServiceConfig.IS_CHECK_ERR_MSG_FROM_BDTS
is_check_errID=ServiceConfig.IS_CHECK_ERRID_FROM_BDTS

# 定义各状态报单的时间戳，用于后续判断个状态报单返回先后顺序是否正确
bd_time={
    '未成交':None,
    '全部成交':None,
    '已撤':None,
    '部撤':None,
    '废单':None
}

#初始化全局变量报单时间bd_time 为空
def bdTimeInit():
    """记录各个状态的报单推送过来的时间戳，从而比较各个状态的报单推送顺序是否正确。
    报单推送数据校验函数cetf_bdts_datacheck模块使用"""
    bd_time['未成交'] = None
    bd_time['部分成交'] = None
    bd_time['全部成交'] = None
    bd_time['已撤'] = None
    bd_time['部撤'] = None
    bd_time['废单'] = None

def cetf_bdts_datacheck(Api,wt_reqs,case_goal,data,error,QueryInit,QueryEnd):
    """报单推送数据校验,返回最后一笔报单推送的校验结果和部分数据"""

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
    public_result = cetf_bdts_public_handle(Api,wt_reqs,data)

    if public_result['测试结果'] == True:
        rs = cetf_bdts_type_handle(Api, wt_reqs, case_goal, data, error,
                                   QueryInit, QueryEnd)
        result['报单检查状态'] = rs['报单检查状态']
        result['测试结果'] = rs['测试结果']
        result['错误信息'] = rs['错误信息']

    else:
        result['报单检查状态'] = 'end'
        result['测试结果'] = public_result['测试结果']
        result['错误信息'] = public_result['错误信息']

    logger.info('报单推送数据检查结束，检查结果如下')
    dictLogging(result)

    return result

def cetf_bdts_public_handle(Api,wt_reqs,data):
    """报单推送委托入参公共业务检查，检查推送结果和委托入参wt_reqs是否一致：
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
        logger.error(
            '错误，报单推送的证券代码与原委托不一致，委托证券代码和报单推送证券代码分别是'
            + wt_reqs['ticker'] + ',' + data['ticker'])
        public_result['测试结果'] = False
        public_result['错误信息'] = '报单推送返回的证券代码与原委托不一致'

    # 判断市场是否一致
    elif data['market'] != wt_reqs['market']:
        logger.error('错误，报单推送的市场与原委托不一致，原委托市场和报单推送市场分别是'
                     + str(wt_reqs['market']) + ',' + str(data['market']))
        public_result['测试结果'] = False
        public_result['错误信息'] = '报单推送返回的市场与原委托不一致'

    # 判断委托方向是否一致
    elif data['side'] != wt_reqs['side']:
        logger.error('报单推送返回的委托方向与原委托不一致')
        public_result['测试结果'] = False
        public_result['错误信息'] = '报单返回的委托方向与原委托不一致'

    # 判断价格条件是否正确，ETF申赎市价订单会被自动转化为限价订单
    elif data['price_type'] != \
            Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT']:
        logger.error('错误，报单查询返回的价格条件为:' + str(data['price_type'])
                     + '; ETF申赎的价格类型应为限价！')
        public_result['测试结果'] = False
        public_result['错误信息'] = 'ETF申赎报单查询返回的价格条件非限价'

    # 判断委托数量是否一致
    elif data['quantity'] != wt_reqs['quantity']:
        logger.error('错误，报单返回的委托数量和原委托数量不一致，原委托数量和报单返回的委托数量分别是' + str(
            wt_reqs['quantity']) + ',' + str(data['quantity']))
        public_result['测试结果'] = False
        public_result['错误信息'] = '报单返回的价格条件与原委托不一致'

    else:
        public_result['测试结果'] = True
        public_result['错误信息'] = ''

    return public_result


def cetf_bdts_type_handle(Api,wt_reqs,case_goal,data,error,QueryInit,QueryEnd):
    """报单推送返回的报单类型为'报单'的业务处理"""
    # 定义结果参数
    ts_result = {
        '报单检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
    }
    # --判断报单返回的data
    # 判断xtpID是否一致
    if data['order_xtp_id'] != case_goal['xtp_ID']:
        logger.error('错误，报单推送的xtpID与原委托不一致，'
                     '下单xtp_ID和报单推送xtp_ID分别是' +
                     str(case_goal['xtp_ID']) + ',' + str(data['order_xtp_id']))
        ts_result['报单检查状态'] = 'end'
        ts_result['测试结果'] = False
        ts_result['错误信息'] = '报单推送的xtpID与原委托不一致'

    # 判断已成交数量加上待成交数量（撤单数量）是否等于委托数量
    elif data['qty_traded'] + data['qty_left'] != wt_reqs['quantity']:
        logger.error('错误，报单返回的成交数量加上待成交数量（撤单数量）应等于委托数量'
                     '，委托数量和返回报单的成交数量和待成交数量（撤单数量）分别为'
                     + str(wt_reqs['quantity']) + ',' + str(data['qty_traded'])
                     + ',' + str(data['qty_left']))
        ts_result['报单检查状态'] = 'end'
        ts_result['测试结果'] = False
        ts_result['错误信息'] = '报单推送的成交数量加待成交数(撤单数量)不等于委托数量'

    # --下面是根据报单的状态调用各自对应的校验方法
    # --如果报单是‘未成交’状态的执行如下，通过下单后的报单推送
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE[
        'XTP_ORDER_STATUS_NOTRADEQUEUEING']:
        if data['order_submit_status'] == \
                Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
                    'XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
            bd_time['未成交'] = time.time()
            logger.error('报单推送状态为未成交,提交状态为已接受,' +
                         str(data['order_status']) + ',' + str(
                    data['order_submit_status']))
            # 如果期望状态是未成交，执行
            if case_goal['期望状态'] == '未成交':
                TODO
            elif case_goal['期望状态'] in ('全成', '已撤', '废单'):
                ts_result['报单检查状态'] = 'pending'
                ts_result['测试结果'] = False
                ts_result['错误信息'] = ''
            else:
                logger.error('期望状态和报单状态不匹配，期望状态、报单状态、'
                             '提交状态分别为' + case_goal['期望状态'] + ',' +
                             str(data['order_status']) + ',' + str(
                    data['order_submit_status']))
                ts_result['报单检查状态'] = 'end'
                ts_result['测试结果'] = False
                ts_result['错误信息'] = '期望状态和报单状态不匹配'

        else:
            ts_result['报单检查状态'] = 'end'
            ts_result['测试结果'] = False
            ts_result['错误信息'] = '报单提交状态不正确'

    # --如果报单回报是全成状态的，执行如下
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE[
        'XTP_ORDER_STATUS_ALLTRADED']:
        if data['order_submit_status'] == \
                Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
                    'XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
            bd_time['全部成交'] = time.time()
            logger.info('报单推送状态为全部成交，提交状态为已接受,' +
                        str(data['order_status']) + ',' + str(
                    data['order_submit_status']))
            # 期望状态如果是为全成，执行
            if case_goal['期望状态'] == '全成':
                rs = CHECK1.all_match(wt_reqs, data, error)
                ts_result['报单检查状态'] = rs['报单检查状态']
                ts_result['测试结果'] = rs['测试结果']
                ts_result['错误信息'] = rs['错误信息']
            else:
                logger.error('期望状态和报单状态不匹配，期望状态、报单状态、'
                             '提交状态分别为' + case_goal['期望状态'] + ',' +
                             str(data['order_status']) + ',' + str(
                    data['order_submit_status']))
                ts_result['报单检查状态'] = 'end'
                ts_result['测试结果'] = False
                ts_result['错误信息'] = '期望状态和报单状态不匹配'
        else:
            ts_result['报单检查状态'] = 'end'
            ts_result['测试结果'] = False
            ts_result['错误信息'] = '报单提交状态不正确'
    # --如果是已撤状态的，执行如下
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE[
        'XTP_ORDER_STATUS_CANCELED']:
        if data['order_submit_status'] == \
                Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
                    'XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
            bd_time['已撤'] = time.time()
            logger.info('报单推送回报状态为已撤,' + str(data['order_status']))
            # 期望状态如果是为已撤，执行
            if case_goal['期望状态'] == '内部撤单':
                TODO
            elif case_goal['期望状态'] == '未成交' and \
                            case_goal['是否是撤废'] == '是':
                TODO
            else:
                logger.error('期望状态和报单状态不匹配，期望状态、报单状态、'
                             '提交状态分别为' + case_goal['期望状态'] + ',' +
                             str(data['order_status']) + ',' + str(
                    data['order_submit_status']))
                ts_result['报单检查状态'] = 'end'
                ts_result['测试结果'] = False
                ts_result['错误信息'] = '期望状态和报单状态不匹配'
        else:
            logger.error('报单提交状态不正确')
            ts_result['报单检查状态'] = 'end'
            ts_result['测试结果'] = False
            ts_result['错误信息'] = '报单提交状态不正确'

    # --如果是废单状态的，执行如下
    elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE[
        'XTP_ORDER_STATUS_REJECTED']:
        if data['order_submit_status'] == \
                Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
                    'XTP_ORDER_SUBMIT_STATUS_INSERT_REJECTED']:
            bd_time['废单'] = time.time()
            logger.info('报单推送状态为废单,' + str(data['order_status']))
            # 期望状态如果是为废单，执行
            if case_goal['期望状态'] == '废单':
                ts_result = CHECK1.reject(wt_reqs, case_goal, data, error)
            else:
                logger.error('期望状态和报单状态不匹配，期望状态、报单状态、'
                             '提交状态分别为' + case_goal['期望状态'] + ',' +
                             str(data['order_status']) + ',' + str(
                    data['order_submit_status']))
                ts_result['报单检查状态'] = 'end'
                ts_result['测试结果'] = False
                ts_result['错误信息'] = '期望状态和报单状态不匹配'
        else:
            logger.error('报单提交状态不正确')
            ts_result['报单检查状态'] = 'end'
            ts_result['测试结果'] = False
            ts_result['错误信息'] = '报单提交状态不正确'

    # --如果是未知状态的，执行如下
    else:
        ts_result = CHECK1.unknown(data)
        logger.error('当前报单返回的状态未知,' + str(data['order_status']))
    return ts_result

# 报单推送返回的不同状态进行进一步校验
class check_bdtsdata_by_status(object):
    """根据报单推送的不同状态，分别进行数据校验"""


    def no_match(self,wt_reqs,case_goal,data,error):
        """报单推送--未成交-校验"""
        # TODO:编写cetf_bdts_type_Handle函数，未成交逻辑分支，期望状态未成交时再补充

    def all_match(self,wt_reqs, data, error):
        """报单推送--全部成交-校验"""
        logger.info('这里是全部成交状态的报单推送业务校验')
        # 定义测试结果参数
        ts_result = {
            '报单检查状态': 'init',
            '测试结果': False,
            '错误信息': '',
        }

        # 判断成交数量和委托数量是否一致
        if data['qty_traded'] != wt_reqs['quantity']:
            logger.error('错误，全部成交状态报单的成交数量应和委托数量一致，'
                         '委托数量和返回报单的成交数量分别为' + str(
                wt_reqs['quantity']) + ',' + str(data['qty_traded']))
            ts_result['报单检查状态'] = 'end'
            ts_result['测试结果'] = False
            ts_result['错误信息'] = '全部成交状态报单的成交数量应和委托数量一致'

        # 判断未成交数量是否等于0
        elif data['qty_left'] != 0:
            logger.error(
                '错误，全部成交状态的报单返回的未成交数量应等于0，实际返回的未成交数量为'
                + str(data['qty_left']))
            ts_result['报单检查状态'] = 'end'
            ts_result['测试结果'] = False
            ts_result['错误信息'] = '全部成交状态的报单返回的未成交数量不等于0'

        # 判断成交金额是否大于０
        elif data['trade_amount'] < 0.0:
            logger.error(
                '错误，全部成交状态报单的成交金额应不小于０，返回报单的成交金额为' +
                str(data['trade_amount']))
            ts_result['报单检查状态'] = 'end'
            ts_result['测试结果'] = False
            ts_result['错误信息'] = '全部成交状态报单的成交金额小于０'

        # 判断报单中的委托时间不能为空
        elif data['insert_time'] == 0:
            logger.error('错误，报单委托时间不能为空，报单返回的委托时间为' +
                         str(data['insert_time']))
            ts_result['报单检查状态'] = 'end'
            ts_result['测试结果'] = False
            ts_result['错误信息'] = '报单委托时间为空'

        # 判断其它项：最后修改时间，撤销时间，撤单xtpID,err_code,Err_Msg
        elif data['update_time'] != 0 and data['cancel_time'] != 0 and data[
            'order_cancel_xtp_id'] != 0 and \
                        error['error_id'] != 0 and error['error_msg'] != '':
            logger.error('错误，请检查最后修改时间，撤单时间，撤单xtpID,err_code,'
                         'err_msg!它们的值分别是：' + str(
                    data['update_time']) + ',' + str(
                    data['cancel_time']) + ',' + str(
                    data['order_cancel_xtp_id']) + ',' + str(
                    error['error_id']) + ',' + error['error_msg'])
            ts_result['报单检查状态'] = 'end'
            ts_result['测试结果'] = False
            ts_result['错误信息'] = '错误，请检查最后修改时间，撤单时间，' \
                                  '撤单xtpID,err_code,err_msg!'

        # 判断推送时间
        elif bd_time['全部成交'] <= bd_time['未成交']:
            logger.error('全部成交推送应晚于未成交推送')
            ts_result['报单检查状态'] = 'end'
            ts_result['测试结果'] = False
            ts_result['错误信息'] = '全部成交推送应晚于未成交推送'

        else:
            logger.info('全部成交状态报单回报校验正确！')
            ts_result['报单检查状态'] = 'end'
            ts_result['测试结果'] = True
            ts_result['错误信息'] = ''
        return ts_result

    def all_cancel(self,wt_reqs, data, error):
        """报单推送--已撤-校验"""
        # TODO:编写cetf_bdts_type_Handle函数，已撤逻辑分支，期望状态已撤时再补充

    def reject(self,wt_reqs, case_goal, data, error):
        """报单推送--废单-校验"""
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
            logger.error(
                '错误，废单状态报单的成交数量应为０，返回报单的成交数量为' +
                str(data['qty_traded']))
            bdhb_result['报单检查状态'] = 'end'
            bdhb_result['测试结果'] = False
            bdhb_result['错误信息'] = '废单状态报单的成交数量应为０'

        # 判断未成交数量是否等于委托数量
        elif data['qty_left'] != wt_reqs['quantity']:
            logger.error(
                '错误，报单返回的未成交数量应等于委托数量，'
                '返回报单的未成交数量和原委托数量分别是' + str(
                    wt_reqs['quantity']) + ',' + str(data['qty_left']))
            bdhb_result['报单检查状态'] = 'end'
            bdhb_result['测试结果'] = False
            bdhb_result['错误信息'] = '报单返回的未成交数量应等于委托数量'

        # 判断成交金额是否是０
        elif data['trade_amount'] != 0.0:
            logger.error(
                '错误，废单状态报单的成交金额应为０，返回报单的成交金额为' +
                str(data['trade_amount']))
            bdhb_result['报单检查状态'] = 'end'
            bdhb_result['测试结果'] = False
            bdhb_result['错误信息'] = '废单状态报单的成交金额应为０'

        # 判断其它项：最后修改时间，撤销时间，撤单xtpID
        elif data['update_time'] != 0 and data['cancel_time'] != 0 and data[
            'order_cancel_xtp_id'] != 0:
            logger.error('错误，请检查最后修改时间，撤单时间，' +
                         '撤单xtpID!它们的值分别是：' +
                         str(data['update_time']) + ',' + str(
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
                    logger.error('报单的error_id与用例期望的不一致，' +
                                 '期望和实际的error_id分别是' + str(
                        case_goal['errorID']) + ',' + str(
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
            elif is_check_errID and is_check_errMsg:
                # 判断废单的error_msg与期望的是否一致
                if error['error_id'] != case_goal['errorID']:
                    logger.error('报单的error_id与用例期望的不一致，' +
                                 '期望和实际的error_id分别是' + str(
                        case_goal['errorID']) + ',' + str(
                        error['error_id']))
                    bdhb_result['报单检查状态'] = 'end'
                    bdhb_result['测试结果'] = False
                    bdhb_result['错误信息'] = '报单的error_id与用例期望的不一致'
                elif error['error_msg'] != case_goal['errorMSG']:
                    logger.error(
                        '报单的error_msg与用例期望的不一致，' +
                        '期望和实际的error_msg分别是' + str(
                            case_goal['errorMSG']) + ',' + str(
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

    def unknown(self,data):
        """报单推送-状态未知-校验"""
        # TODO:编写cetf_bdts_type_Handle函数，未知逻辑分支时再补充


CHECK1 = check_bdtsdata_by_status()


