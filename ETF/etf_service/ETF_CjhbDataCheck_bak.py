#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
from decimal import Decimal
from decimal import ROUND_HALF_UP
sys.path.append("/home/yhl2/workspace/xtp_test/service")
import ServiceConfig
from log import *
from CheckDataPrice import *
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/ETF/etf_mysql")
from QueryEtfNavDB import *
from QueryEtfComponentsDB import *
from QueryEtfComponentsCodeDB import *
from QueryEtfNavDB import *
import QueryEtfQty
from QueryEtfQty import stkQty


#---定义费率，最低收费
fee_rate_etf_creation = ServiceConfig.FEE_RATE_ETF_CREATION
fee_rate_etf_redemption =ServiceConfig.FEE_RATE_ETF_REDEMPTION
fee_etf_min = ServiceConfig.FEE_ETF_MIN


cjhb_reslut = {
    '成交回报检查状态': 'init',
    'xtp_id': None,
    '市场': None,
    '股票代码': None,
    '买卖方向': None,
    '成交价格': None,
    '成交数量': 0,
    '成交金额': 0.00,
    '成交类型': None,
    '测试结果': 0,
    '测试错误原因': None,
}

#---业务判断程序：买或是卖，及全成或是部成
def etf_cjhbDataCheck(expectStatus, Api, QueryInit, wt_reqs, xtp_id, QueryEnd, hb_data, amount_ava):
    #-----如果委托方向是etf申购，执行如下－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
    component_codes = QueryEtfComponentsCodeDB(hb_data['ticker'])
    if wt_reqs['side'] == Api.const.XTP_SIDE_TYPE['XTP_SIDE_PURCHASE'] :
        #--委托数据和成交数据比较
        if wt_reqs['ticker'] == hb_data['ticker']:
            cjhb_reslut['xtp_id'] = hb_data['order_xtp_id']
            cjhb_reslut['市场'] = hb_data['market']
            cjhb_reslut['股票代码'] = hb_data['ticker']
            cjhb_reslut['买卖方向'] = hb_data['side']
            cjhb_reslut['成交价格'] = hb_data['price']
            cjhb_reslut['成交类型'] = hb_data['trade_type']
            cjhb_reslut['成交数量'] = hb_data['quantity']
            cjhb_reslut['成交金额'] = hb_data['trade_amount']

            #沪A市场ETF申购成交回报返回的买卖方向为XTP_SIDE_BUY,所以不判断买卖方向
            side_flag = True
            if wt_reqs['market'] == Api.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A']:
                side_flag = (xtp_id == hb_data['order_xtp_id']
                             and wt_reqs['market'] == hb_data['market']
                             and wt_reqs['side'] == hb_data['side'])
            else:
                side_flag = (xtp_id == hb_data['order_xtp_id']
                             and wt_reqs['market'] == hb_data['market'])

            if side_flag:
                if  abs(hb_data['trade_amount']-round(hb_data['price'] * hb_data['quantity'],2)) < 0.01:
                    #全成,部成和错误处理
                    if cjhb_reslut['成交数量'] == wt_reqs['quantity']:
                        if expectStatus == '全成':
                            logger.info('成交回报检查：全部成交业务数据开始检查!')
                            ETF_CJHB_QC_B(QueryInit, QueryEnd, wt_reqs, amount_ava)
                        else:
                            logger.error('成交回报检查：错误,成交回报数量累计已经全部成交！')
                            cjhb_reslut['成交回报检查状态'] = 'end'
                            cjhb_reslut['测试结果'] = False
                            cjhb_reslut['测试错误原因'] = '成交回报数量累计已经全部成交！'
                    elif cjhb_reslut['成交数量'] < wt_reqs['quantity']:
                        logger.info('成交回报检查：当前成交回报状态为未全部成交！')
                        cjhb_reslut['成交回报检查状态'] = 'pending'
                    else:
                        logger.error('成交回报错误，总成交数量大于委托数量')
                        cjhb_reslut['成交回报检查状态'] = 'end'
                        cjhb_reslut['测试结果'] = False
                        cjhb_reslut['测试错误原因'] = '成交回报错误，总成交数量大于委托数量'
                else:
                    logger.error('成交回报有问题：价格×数量不等于成交金额'+
                                 str(hb_data['price']* hb_data['quantity'])+
                                 ','+str(hb_data['trade_amount']))
                    cjhb_reslut['成交回报检查状态'] = 'end'
                    cjhb_reslut['测试结果'] = False
                    cjhb_reslut['测试错误原因'] = '成交回报有问题：价格×数量不等于成交金额'
            else:
                logger.error('成交回报和委托信息不一致，如：xtpid,market,ticker,side,price')
                cjhb_reslut['成交回报检查状态'] = 'end'
                cjhb_reslut['测试结果'] = False
                cjhb_reslut['测试错误原因'] = '成交回报和委托信息不一致，如：xtpid,market,ticker,side,price'
        elif hb_data['ticker'] in component_codes:
            if abs(hb_data['trade_amount'] - round(hb_data['price']*hb_data['quantity'], 2)) < 0.01:
                component_share = QueryEtfComponentsDB(wt_reqs['ticker'], hb_data['ticker'])  # etf成分股数量
                creation_quantity = ServiceConfig.CREATION_QUANTITY    #etf申购单位数

                #全成,部成和错误处理
                if hb_data['quantity'] == component_share*creation_quantity:
                    if expectStatus == '全成':
                        logger.info('成分股成交数量正确！')
                    else:
                        logger.error('成交回报检查：错误,成交回报数量累计已经全部成交！')
                        cjhb_reslut['成交回报检查状态'] = 'end'
                        cjhb_reslut['测试结果'] = False
                        cjhb_reslut['测试错误原因'] = '成交回报数量累计已经全部成交！'
                elif hb_data['quantity'] < component_share*creation_quantity:
                    logger.info('成交回报检查：当前成交回报状态为未全部成交！')
                    cjhb_reslut['成交回报检查状态'] = 'pending'
                else:
                    logger.error('成交回报错误，总成交数量大于委托数量')
                    cjhb_reslut['成交回报检查状态'] = 'end'
                    cjhb_reslut['测试结果'] = False
                    cjhb_reslut['测试错误原因'] = '成交回报错误，总成交数量大于委托数量'
            else:
                logger.error('成交回报有问题：价格×数量不等于成交金额'+
                             str(hb_data['price']* hb_data['quantity'])+
                             ','+str(hb_data['trade_amount']))
                cjhb_reslut['成交回报检查状态'] = 'end'
                cjhb_reslut['测试结果'] = False
                cjhb_reslut['测试错误原因'] = '成交回报有问题：价格×数量不等于成交金额'
        else:
            #资金回报处理
            pass

    #--如果委托方向是赎回，执行如下－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
    elif wt_reqs['side'] == Api.const.XTP_SIDE_TYPE['XTP_SIDE_REDEMPTION'] :
        # --委托数据和成交数据比较
        if wt_reqs['ticker'] == hb_data['ticker']:
            cjhb_reslut['xtp_id'] = hb_data['order_xtp_id']
            cjhb_reslut['市场'] = hb_data['market']
            cjhb_reslut['股票代码'] = hb_data['ticker']
            cjhb_reslut['买卖方向'] = hb_data['side']
            cjhb_reslut['成交价格'] = hb_data['price']
            cjhb_reslut['成交类型'] = hb_data['trade_type']
            cjhb_reslut['成交数量'] = hb_data['quantity']
            cjhb_reslut['成交金额'] = hb_data['trade_amount']

            # 沪A市场ETF申购成交回报返回的买卖方向为XTP_SIDE_BUY,所以不判断买卖方向
            side_flag = True
            if wt_reqs['market'] == Api.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A']:
                side_flag = (xtp_id == hb_data['order_xtp_id']
                             and wt_reqs['market'] == hb_data['market']
                             and wt_reqs['side'] == hb_data['side'])
            else:
                side_flag = (xtp_id == hb_data['order_xtp_id']
                             and wt_reqs['market'] == hb_data['market'])

            if side_flag:
                if  abs(hb_data['trade_amount']-round(hb_data['price'] * hb_data['quantity'],2)) < 0.01:
                    # 全成,部成和错误处理
                    if cjhb_reslut['成交数量'] == wt_reqs['quantity']:
                        if expectStatus == '全成':
                            logger.info('成交回报检查：全部成交业务数据开始检查')
                            ETF_CJHB_QC_S(QueryInit, QueryEnd, wt_reqs)
                        else:
                            logger.error('成交回报检查：错误,成交回报数量累计已经全部成交！')
                            cjhb_reslut['成交回报检查状态'] = 'end'
                            cjhb_reslut['测试结果'] = False
                            cjhb_reslut['测试错误原因'] = '成交回报数量累计已经全部成交！'
                    elif cjhb_reslut['成交数量'] < wt_reqs['quantity']:
                        logger.info('成交回报检查：当前成交回报状态为未全部成交！')
                        cjhb_reslut['成交回报检查状态'] = 'pending'
                    else:
                        logger.error('成交回报错误，总成交数量大于委托数量')
                        cjhb_reslut['成交回报检查状态'] = 'end'
                        cjhb_reslut['测试结果'] = False
                        cjhb_reslut['测试错误原因'] = '成交回报错误，总成交数量大于委托数量'
                else:
                    logger.error('成交回报有问题：价格×数量不等于成交金额'+
                                 str(hb_data['price']* hb_data['quantity'])+
                                 ','+str(hb_data['trade_amount']))
                    cjhb_reslut['成交回报检查状态'] = 'end'
                    cjhb_reslut['测试结果'] = False
                    cjhb_reslut['测试错误原因'] = '成交回报有问题：价格×数量不等于成交金额'
            else:
                logger.error('成交回报和委托信息不一致，如：xtpid,market,ticker,side,price')
                cjhb_reslut['成交回报检查状态'] = 'end'
                cjhb_reslut['测试结果'] = False
                cjhb_reslut['测试错误原因'] = '成交回报和委托信息不一致，如：xtpid,market,ticker,side,price'
        else:
            if abs(hb_data['trade_amount']-round(hb_data['price'] * hb_data['quantity'],2)) < 0.01:
                component_share = 0   #etf成分股数量
                component_share = QueryEtfComponentsDB(wt_reqs['ticker'],hb_data['ticker'])
                redemption_unit = ServiceConfig.REDEMPTION_QUANTITY   #etf赎回单位数

                # 全成,部成和错误处理
                if hb_data['quantity'] == component_share*redemption_unit:
                    if expectStatus == '全成':
                        logger.info('成交回报检查：成分股成交数量正确！')
                    else:
                        logger.error('成交回报检查：错误,成交回报数量累计已经全部成交！')
                        cjhb_reslut['成交回报检查状态'] = 'end'
                        cjhb_reslut['测试结果'] = False
                        cjhb_reslut['测试错误原因'] = '成交回报数量累计已经全部成交！'
                elif hb_data['quantity'] < component_share*redemption_unit:
                    logger.info('成交回报检查：当前成交回报状态为未全部成交！')
                    cjhb_reslut['成交回报检查状态'] = 'pending'
                else:
                    print hb_data['ticker']
                    print wt_reqs['ticker']
                    logger.error('成交回报错误，总成交数量大于委托数量')
                    cjhb_reslut['成交回报检查状态'] = 'end'
                    cjhb_reslut['测试结果'] = False
                    cjhb_reslut['测试错误原因'] = '成交回报错误，总成交数量大于委托数量'
            else:
                logger.error('成交回报有问题：价格×数量不等于成交金额'+
                             str(hb_data['price']* hb_data['quantity'])+
                             ','+str(hb_data['trade_amount']))
                cjhb_reslut['成交回报检查状态'] = 'end'
                cjhb_reslut['测试结果'] = False
                cjhb_reslut['测试错误原因'] = '成交回报有问题：价格×数量不等于成交金额'

    return cjhb_reslut


# 禁止现金替代
def etf_cjhbDataCheck_forbidden():
    # -----如果委托方向是etf申购，执行如下－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
    component_codes = QueryEtfComponentsCodeDB(hb_data['ticker'])
    if wt_reqs['side'] == Api.const.XTP_SIDE_TYPE['XTP_SIDE_PURCHASE']:
        # --委托数据和成交数据比较
        if wt_reqs['ticker'] == hb_data['ticker']:
            cjhb_reslut['xtp_id'] = hb_data['order_xtp_id']
            cjhb_reslut['市场'] = hb_data['market']
            cjhb_reslut['股票代码'] = hb_data['ticker']
            cjhb_reslut['买卖方向'] = hb_data['side']
            cjhb_reslut['成交价格'] = hb_data['price']
            cjhb_reslut['成交类型'] = hb_data['trade_type']
            cjhb_reslut['成交数量'] = hb_data['quantity']
            cjhb_reslut['成交金额'] = hb_data['trade_amount']

            # 沪A市场ETF申购成交回报返回的买卖方向为XTP_SIDE_BUY,所以不判断买卖方向
            side_flag = True
            if wt_reqs['market'] == Api.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A']:
                side_flag = (xtp_id == hb_data['order_xtp_id']
                             and wt_reqs['market'] == hb_data['market']
                             and wt_reqs['side'] == hb_data['side'])
            else:
                side_flag = (xtp_id == hb_data['order_xtp_id']
                             and wt_reqs['market'] == hb_data['market'])

            if side_flag:
                if abs(hb_data['trade_amount'] - round(
                                hb_data['price'] * hb_data['quantity'],
                                2)) < 0.01:
                    # 全成,部成和错误处理
                    if cjhb_reslut['成交数量'] == wt_reqs['quantity']:
                        if expectStatus == '全成':
                            logger.info('成交回报检查：全部成交业务数据开始检查!')
                            ETF_CJHB_QC_B(QueryInit, QueryEnd, wt_reqs,
                                          amount_ava)
                        else:
                            logger.error('成交回报检查：错误,成交回报数量累计已经全部成交！')
                            cjhb_reslut['成交回报检查状态'] = 'end'
                            cjhb_reslut['测试结果'] = False
                            cjhb_reslut['测试错误原因'] = '成交回报数量累计已经全部成交！'
                    elif cjhb_reslut['成交数量'] < wt_reqs['quantity']:
                        logger.info('成交回报检查：当前成交回报状态为未全部成交！')
                        cjhb_reslut['成交回报检查状态'] = 'pending'
                    else:
                        logger.error('成交回报错误，总成交数量大于委托数量')
                        cjhb_reslut['成交回报检查状态'] = 'end'
                        cjhb_reslut['测试结果'] = False
                        cjhb_reslut['测试错误原因'] = '成交回报错误，总成交数量大于委托数量'
                else:
                    logger.error('成交回报有问题：价格×数量不等于成交金额' +
                                 str(hb_data['price'] * hb_data['quantity']) +
                                 ',' + str(hb_data['trade_amount']))
                    cjhb_reslut['成交回报检查状态'] = 'end'
                    cjhb_reslut['测试结果'] = False
                    cjhb_reslut['测试错误原因'] = '成交回报有问题：价格×数量不等于成交金额'
            else:
                logger.error('成交回报和委托信息不一致，如：xtpid,market,ticker,side,price')
                cjhb_reslut['成交回报检查状态'] = 'end'
                cjhb_reslut['测试结果'] = False
                cjhb_reslut[
                    '测试错误原因'] = '成交回报和委托信息不一致，如：xtpid,market,ticker,side,price'
        elif hb_data['ticker'] in component_codes:
            if abs(hb_data['trade_amount'] - round(
                            hb_data['price'] * hb_data['quantity'], 2)) < 0.01:
                component_share = QueryEtfComponentsDB(wt_reqs['ticker'],
                                                       hb_data[
                                                           'ticker'])  # etf成分股数量
                creation_quantity = ServiceConfig.CREATION_QUANTITY  # etf申购单位数

                # 全成,部成和错误处理
                if hb_data['quantity'] == component_share * creation_quantity:
                    if expectStatus == '全成':
                        logger.info('成分股成交数量正确！')
                    else:
                        logger.error('成交回报检查：错误,成交回报数量累计已经全部成交！')
                        cjhb_reslut['成交回报检查状态'] = 'end'
                        cjhb_reslut['测试结果'] = False
                        cjhb_reslut['测试错误原因'] = '成交回报数量累计已经全部成交！'
                elif hb_data['quantity'] < component_share * creation_quantity:
                    logger.info('成交回报检查：当前成交回报状态为未全部成交！')
                    cjhb_reslut['成交回报检查状态'] = 'pending'
                else:
                    logger.error('成交回报错误，总成交数量大于委托数量')
                    cjhb_reslut['成交回报检查状态'] = 'end'
                    cjhb_reslut['测试结果'] = False
                    cjhb_reslut['测试错误原因'] = '成交回报错误，总成交数量大于委托数量'
            else:
                logger.error('成交回报有问题：价格×数量不等于成交金额' +
                             str(hb_data['price'] * hb_data['quantity']) +
                             ',' + str(hb_data['trade_amount']))
                cjhb_reslut['成交回报检查状态'] = 'end'
                cjhb_reslut['测试结果'] = False
                cjhb_reslut['测试错误原因'] = '成交回报有问题：价格×数量不等于成交金额'
        else:
            # 资金回报处理
            pass

    # --如果委托方向是赎回，执行如下－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
    elif wt_reqs['side'] == Api.const.XTP_SIDE_TYPE['XTP_SIDE_REDEMPTION']:
        # --委托数据和成交数据比较
        if wt_reqs['ticker'] == hb_data['ticker']:
            cjhb_reslut['xtp_id'] = hb_data['order_xtp_id']
            cjhb_reslut['市场'] = hb_data['market']
            cjhb_reslut['股票代码'] = hb_data['ticker']
            cjhb_reslut['买卖方向'] = hb_data['side']
            cjhb_reslut['成交价格'] = hb_data['price']
            cjhb_reslut['成交类型'] = hb_data['trade_type']
            cjhb_reslut['成交数量'] = hb_data['quantity']
            cjhb_reslut['成交金额'] = hb_data['trade_amount']

            # 沪A市场ETF申购成交回报返回的买卖方向为XTP_SIDE_BUY,所以不判断买卖方向
            side_flag = True
            if wt_reqs['market'] == Api.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A']:
                side_flag = (xtp_id == hb_data['order_xtp_id']
                             and wt_reqs['market'] == hb_data['market']
                             and wt_reqs['side'] == hb_data['side'])
            else:
                side_flag = (xtp_id == hb_data['order_xtp_id']
                             and wt_reqs['market'] == hb_data['market'])

            if side_flag:
                if abs(hb_data['trade_amount'] - round(
                                hb_data['price'] * hb_data['quantity'],
                                2)) < 0.01:
                    # 全成,部成和错误处理
                    if cjhb_reslut['成交数量'] == wt_reqs['quantity']:
                        if expectStatus == '全成':
                            logger.info('成交回报检查：全部成交业务数据开始检查')
                            ETF_CJHB_QC_S(QueryInit, QueryEnd, wt_reqs)
                        else:
                            logger.error('成交回报检查：错误,成交回报数量累计已经全部成交！')
                            cjhb_reslut['成交回报检查状态'] = 'end'
                            cjhb_reslut['测试结果'] = False
                            cjhb_reslut['测试错误原因'] = '成交回报数量累计已经全部成交！'
                    elif cjhb_reslut['成交数量'] < wt_reqs['quantity']:
                        logger.info('成交回报检查：当前成交回报状态为未全部成交！')
                        cjhb_reslut['成交回报检查状态'] = 'pending'
                    else:
                        logger.error('成交回报错误，总成交数量大于委托数量')
                        cjhb_reslut['成交回报检查状态'] = 'end'
                        cjhb_reslut['测试结果'] = False
                        cjhb_reslut['测试错误原因'] = '成交回报错误，总成交数量大于委托数量'
                else:
                    logger.error('成交回报有问题：价格×数量不等于成交金额' +
                                 str(hb_data['price'] * hb_data['quantity']) +
                                 ',' + str(hb_data['trade_amount']))
                    cjhb_reslut['成交回报检查状态'] = 'end'
                    cjhb_reslut['测试结果'] = False
                    cjhb_reslut['测试错误原因'] = '成交回报有问题：价格×数量不等于成交金额'
            else:
                logger.error('成交回报和委托信息不一致，如：xtpid,market,ticker,side,price')
                cjhb_reslut['成交回报检查状态'] = 'end'
                cjhb_reslut['测试结果'] = False
                cjhb_reslut[
                    '测试错误原因'] = '成交回报和委托信息不一致，如：xtpid,market,ticker,side,price'
        else:
            if abs(hb_data['trade_amount'] - round(
                            hb_data['price'] * hb_data['quantity'], 2)) < 0.01:
                component_share = 0  # etf成分股数量
                component_share = QueryEtfComponentsDB(wt_reqs['ticker'],
                                                       hb_data['ticker'])
                redemption_unit = ServiceConfig.REDEMPTION_QUANTITY  # etf赎回单位数

                # 全成,部成和错误处理
                if hb_data['quantity'] == component_share * redemption_unit:
                    if expectStatus == '全成':
                        logger.info('成交回报检查：成分股成交数量正确！')
                    else:
                        logger.error('成交回报检查：错误,成交回报数量累计已经全部成交！')
                        cjhb_reslut['成交回报检查状态'] = 'end'
                        cjhb_reslut['测试结果'] = False
                        cjhb_reslut['测试错误原因'] = '成交回报数量累计已经全部成交！'
                elif hb_data['quantity'] < component_share * redemption_unit:
                    logger.info('成交回报检查：当前成交回报状态为未全部成交！')
                    cjhb_reslut['成交回报检查状态'] = 'pending'
                else:
                    print hb_data['ticker']
                    print wt_reqs['ticker']
                    logger.error('成交回报错误，总成交数量大于委托数量')
                    cjhb_reslut['成交回报检查状态'] = 'end'
                    cjhb_reslut['测试结果'] = False
                    cjhb_reslut['测试错误原因'] = '成交回报错误，总成交数量大于委托数量'
            else:
                logger.error('成交回报有问题：价格×数量不等于成交金额' +
                             str(hb_data['price'] * hb_data['quantity']) +
                             ',' + str(hb_data['trade_amount']))
                cjhb_reslut['成交回报检查状态'] = 'end'
                cjhb_reslut['测试结果'] = False
                cjhb_reslut['测试错误原因'] = '成交回报有问题：价格×数量不等于成交金额'

    return cjhb_reslut


# 可现金替代
def etf_cjhbDataCheck_optional():
    # -----如果委托方向是etf申购，执行如下－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
    component_codes = QueryEtfComponentsCodeDB(hb_data['ticker'])

    if wt_reqs['side'] == Api.const.XTP_SIDE_TYPE['XTP_SIDE_PURCHASE']:
        # --委托数据和成交数据比较
        if wt_reqs['ticker'] == hb_data['ticker']:
            cjhb_reslut['xtp_id'] = hb_data['order_xtp_id']
            cjhb_reslut['市场'] = hb_data['market']
            cjhb_reslut['股票代码'] = hb_data['ticker']
            cjhb_reslut['买卖方向'] = hb_data['side']
            cjhb_reslut['成交价格'] = hb_data['price']
            cjhb_reslut['成交类型'] = hb_data['trade_type']
            cjhb_reslut['成交数量'] = hb_data['quantity']
            cjhb_reslut['成交金额'] = hb_data['trade_amount']

            # 沪A市场ETF申购成交回报返回的买卖方向为XTP_SIDE_BUY,所以不判断买卖方向
            side_flag = True
            if wt_reqs['market'] == Api.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A']:
                side_flag = (xtp_id == hb_data['order_xtp_id']
                             and wt_reqs['market'] == hb_data['market']
                             and wt_reqs['side'] == hb_data['side'])
            else:
                side_flag = (xtp_id == hb_data['order_xtp_id']
                             and wt_reqs['market'] == hb_data['market'])

            if side_flag:
                if abs(hb_data['trade_amount'] - round(
                                hb_data['price'] * hb_data['quantity'],
                                2)) < 0.01:
                    # 全成,部成和错误处理
                    if cjhb_reslut['成交数量'] == wt_reqs['quantity']:
                        if expectStatus == '全成':
                            logger.info('成交回报检查：全部成交业务数据开始检查!')
                            ETF_CJHB_QC_B(QueryInit, QueryEnd, wt_reqs,
                                          amount_ava)
                        else:
                            logger.error('成交回报检查：错误,成交回报数量累计已经全部成交！')
                            cjhb_reslut['成交回报检查状态'] = 'end'
                            cjhb_reslut['测试结果'] = False
                            cjhb_reslut['测试错误原因'] = '成交回报数量累计已经全部成交！'
                    elif cjhb_reslut['成交数量'] < wt_reqs['quantity']:
                        logger.info('成交回报检查：当前成交回报状态为未全部成交！')
                        cjhb_reslut['成交回报检查状态'] = 'pending'
                    else:
                        logger.error('成交回报错误，总成交数量大于委托数量')
                        cjhb_reslut['成交回报检查状态'] = 'end'
                        cjhb_reslut['测试结果'] = False
                        cjhb_reslut['测试错误原因'] = '成交回报错误，总成交数量大于委托数量'
                else:
                    logger.error('成交回报有问题：价格×数量不等于成交金额' +
                                 str(hb_data['price'] * hb_data['quantity']) +
                                 ',' + str(hb_data['trade_amount']))
                    cjhb_reslut['成交回报检查状态'] = 'end'
                    cjhb_reslut['测试结果'] = False
                    cjhb_reslut['测试错误原因'] = '成交回报有问题：价格×数量不等于成交金额'
            else:
                logger.error('成交回报和委托信息不一致，如：xtpid,market,ticker,side,price')
                cjhb_reslut['成交回报检查状态'] = 'end'
                cjhb_reslut['测试结果'] = False
                cjhb_reslut[
                    '测试错误原因'] = '成交回报和委托信息不一致，如：xtpid,market,ticker,side,price'
        elif hb_data['ticker'] in component_codes:
            if abs(hb_data['trade_amount'] - \
                    round(hb_data['price'] * hb_data['quantity'], 2)) < 0.01:
                component_share = QueryEtfComponentsDB(wt_reqs['ticker'],
                                                       hb_data['ticker'])  # etf成分股数量
                creation_quantity = ServiceConfig.CREATION_QUANTITY  # etf申购单位数

                # 全成,部成和错误处理
                if hb_data['quantity'] == component_share * creation_quantity:
                    if expectStatus == '全成':
                        logger.info('成分股成交数量正确！')
                    else:
                        logger.error('成交回报检查：错误,成交回报数量累计已经全部成交！')
                        cjhb_reslut['成交回报检查状态'] = 'end'
                        cjhb_reslut['测试结果'] = False
                        cjhb_reslut['测试错误原因'] = '成交回报数量累计已经全部成交！'
                elif hb_data['quantity'] < component_share * creation_quantity:
                    logger.info('成交回报检查：当前成交回报状态为未全部成交！')
                    cjhb_reslut['成交回报检查状态'] = 'pending'
                else:
                    logger.error('成交回报错误，总成交数量大于委托数量')
                    cjhb_reslut['成交回报检查状态'] = 'end'
                    cjhb_reslut['测试结果'] = False
                    cjhb_reslut['测试错误原因'] = '成交回报错误，总成交数量大于委托数量'
            else:
                logger.error('成交回报有问题：价格×数量不等于成交金额' +
                             str(hb_data['price'] * hb_data['quantity']) +
                             ',' + str(hb_data['trade_amount']))
                cjhb_reslut['成交回报检查状态'] = 'end'
                cjhb_reslut['测试结果'] = False
                cjhb_reslut['测试错误原因'] = '成交回报有问题：价格×数量不等于成交金额'
        else:
            # 资金回报处理
            pass

    # --如果委托方向是赎回，执行如下－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
    elif wt_reqs['side'] == Api.const.XTP_SIDE_TYPE['XTP_SIDE_REDEMPTION']:
        # --委托数据和成交数据比较
        if wt_reqs['ticker'] == hb_data['ticker']:
            cjhb_reslut['xtp_id'] = hb_data['order_xtp_id']
            cjhb_reslut['市场'] = hb_data['market']
            cjhb_reslut['股票代码'] = hb_data['ticker']
            cjhb_reslut['买卖方向'] = hb_data['side']
            cjhb_reslut['成交价格'] = hb_data['price']
            cjhb_reslut['成交类型'] = hb_data['trade_type']
            cjhb_reslut['成交数量'] = hb_data['quantity']
            cjhb_reslut['成交金额'] = hb_data['trade_amount']

            # 沪A市场ETF申购成交回报返回的买卖方向为XTP_SIDE_BUY,所以不判断买卖方向
            side_flag = True
            if wt_reqs['market'] == Api.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A']:
                side_flag = (xtp_id == hb_data['order_xtp_id']
                             and wt_reqs['market'] == hb_data['market']
                             and wt_reqs['side'] == hb_data['side'])
            else:
                side_flag = (xtp_id == hb_data['order_xtp_id']
                             and wt_reqs['market'] == hb_data['market'])

            if side_flag:
                if abs(hb_data['trade_amount'] - round(
                                hb_data['price'] * hb_data['quantity'],
                                2)) < 0.01:
                    # 全成,部成和错误处理
                    if cjhb_reslut['成交数量'] == wt_reqs['quantity']:
                        if expectStatus == '全成':
                            logger.info('成交回报检查：全部成交业务数据开始检查')
                            ETF_CJHB_QC_S(QueryInit, QueryEnd, wt_reqs)
                        else:
                            logger.error('成交回报检查：错误,成交回报数量累计已经全部成交！')
                            cjhb_reslut['成交回报检查状态'] = 'end'
                            cjhb_reslut['测试结果'] = False
                            cjhb_reslut['测试错误原因'] = '成交回报数量累计已经全部成交！'
                    elif cjhb_reslut['成交数量'] < wt_reqs['quantity']:
                        logger.info('成交回报检查：当前成交回报状态为未全部成交！')
                        cjhb_reslut['成交回报检查状态'] = 'pending'
                    else:
                        logger.error('成交回报错误，总成交数量大于委托数量')
                        cjhb_reslut['成交回报检查状态'] = 'end'
                        cjhb_reslut['测试结果'] = False
                        cjhb_reslut['测试错误原因'] = '成交回报错误，总成交数量大于委托数量'
                else:
                    logger.error('成交回报有问题：价格×数量不等于成交金额' +
                                 str(hb_data['price'] * hb_data['quantity']) +
                                 ',' + str(hb_data['trade_amount']))
                    cjhb_reslut['成交回报检查状态'] = 'end'
                    cjhb_reslut['测试结果'] = False
                    cjhb_reslut['测试错误原因'] = '成交回报有问题：价格×数量不等于成交金额'
            else:
                logger.error('成交回报和委托信息不一致，如：xtpid,market,ticker,side,price')
                cjhb_reslut['成交回报检查状态'] = 'end'
                cjhb_reslut['测试结果'] = False
                cjhb_reslut[
                    '测试错误原因'] = '成交回报和委托信息不一致，如：xtpid,market,ticker,side,price'
        else:
            if abs(hb_data['trade_amount'] - round(
                            hb_data['price'] * hb_data['quantity'], 2)) < 0.01:
                component_share = 0  # etf成分股数量
                component_share = QueryEtfComponentsDB(wt_reqs['ticker'],
                                                       hb_data['ticker'])
                redemption_unit = ServiceConfig.REDEMPTION_QUANTITY  # etf赎回单位数

                # 全成,部成和错误处理
                if hb_data['quantity'] == component_share * redemption_unit:
                    if expectStatus == '全成':
                        logger.info('成交回报检查：成分股成交数量正确！')
                    else:
                        logger.error('成交回报检查：错误,成交回报数量累计已经全部成交！')
                        cjhb_reslut['成交回报检查状态'] = 'end'
                        cjhb_reslut['测试结果'] = False
                        cjhb_reslut['测试错误原因'] = '成交回报数量累计已经全部成交！'
                elif hb_data['quantity'] < component_share * redemption_unit:
                    logger.info('成交回报检查：当前成交回报状态为未全部成交！')
                    cjhb_reslut['成交回报检查状态'] = 'pending'
                else:
                    print hb_data['ticker']
                    print wt_reqs['ticker']
                    logger.error('成交回报错误，总成交数量大于委托数量')
                    cjhb_reslut['成交回报检查状态'] = 'end'
                    cjhb_reslut['测试结果'] = False
                    cjhb_reslut['测试错误原因'] = '成交回报错误，总成交数量大于委托数量'
            else:
                logger.error('成交回报有问题：价格×数量不等于成交金额' +
                             str(hb_data['price'] * hb_data['quantity']) +
                             ',' + str(hb_data['trade_amount']))
                cjhb_reslut['成交回报检查状态'] = 'end'
                cjhb_reslut['测试结果'] = False
                cjhb_reslut['测试错误原因'] = '成交回报有问题：价格×数量不等于成交金额'

    return cjhb_reslut


# 全部现金替代
def etf_cjhbDataCheck_all(wt_reqs, hb_data, Api, xtp_id, expectStatus):
    # -----如果委托方向是etf申购，执行如下－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
    etf_code1_code2 = QueryEtfCode1Code2DB()
    cjhb_reslut['xtp_id'] = hb_data['order_xtp_id']
    cjhb_reslut['市场'] = hb_data['market']
    cjhb_reslut['股票代码'] = hb_data['ticker']
    cjhb_reslut['买卖方向'] = hb_data['side']
    cjhb_reslut['成交价格'] = hb_data['price']
    cjhb_reslut['成交类型'] = hb_data['trade_type']
    cjhb_reslut['成交数量'] = hb_data['quantity']
    cjhb_reslut['成交金额'] = hb_data['trade_amount']
    if wt_reqs['side'] == Api.const.XTP_SIDE_TYPE['XTP_SIDE_PURCHASE']:
        # --委托数据和成交数据比较
        if wt_reqs['ticker'] == hb_data['ticker']:
            # 沪A市场ETF申购成交回报返回的买卖方向为XTP_SIDE_BUY,所以不判断买卖方向
            side_flag = True
            if wt_reqs['market'] == Api.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A']:
                side_flag = (xtp_id == hb_data['order_xtp_id']
                             and wt_reqs['market'] == hb_data['market']
                             and wt_reqs['side'] == hb_data['side'])
            else:
                side_flag = (xtp_id == hb_data['order_xtp_id']
                             and wt_reqs['market'] == hb_data['market'])

            if side_flag:
                if abs(hb_data['trade_amount'] - round(
                                hb_data['price'] * hb_data['quantity'],
                                2)) < 0.01:
                    # 全成,部成和错误处理
                    if cjhb_reslut['成交数量'] == wt_reqs['quantity']:
                        if expectStatus == '全成':
                            logger.info('成交回报检查：全部成交业务数据开始检查!')
                            # fund_is_check:1-校验可用资金,0-不校验可用资金
                            fund_is_check = 1
                            ETF_CJHB_QC_B(QueryInit, QueryEnd, wt_reqs, fund_is_check)
                        else:
                            logger.error('成交回报检查：错误,成交回报数量累计已经全部成交！')
                            cjhb_reslut['成交回报检查状态'] = 'end'
                            cjhb_reslut['测试结果'] = False
                            cjhb_reslut['测试错误原因'] = '成交回报数量累计已经全部成交！'
                    elif cjhb_reslut['成交数量'] < wt_reqs['quantity']:
                        logger.info('成交回报检查：当前成交回报状态为未全部成交！')
                        cjhb_reslut['成交回报检查状态'] = 'pending'
                    else:
                        logger.error('成交回报错误，总成交数量大于委托数量')
                        cjhb_reslut['成交回报检查状态'] = 'end'
                        cjhb_reslut['测试结果'] = False
                        cjhb_reslut['测试错误原因'] = '成交回报错误，总成交数量大于委托数量'
                else:
                    logger.error('成交回报有问题：价格×数量不等于成交金额' +
                                 str(hb_data['price'] * hb_data['quantity']) +
                                 ',' + str(hb_data['trade_amount']))
                    cjhb_reslut['成交回报检查状态'] = 'end'
                    cjhb_reslut['测试结果'] = False
                    cjhb_reslut['测试错误原因'] = '成交回报有问题：价格×数量不等于成交金额'
            else:
                logger.error('成交回报和委托信息不一致，如：xtpid,market,ticker,side,price')
                cjhb_reslut['成交回报检查状态'] = 'end'
                cjhb_reslut['测试结果'] = False
                cjhb_reslut[
                    '测试错误原因'] = '成交回报和委托信息不一致，如：xtpid,market,ticker,side,price'
        elif hb_data['ticker'] == etf_code1_code2['etf_code1']:
            if abs(hb_data['trade_amount'] - \
                    round(hb_data['price'] * hb_data['quantity'], 2)) < 0.01:
                # 全成,部成和错误处理
                if hb_data['quantity'] == wt_reqs['quantity']:
                    if expectStatus == '全成':
                        logger.info('成分股成交数量正确！')
                        # fund_is_check:1-校验可用资金,0-不校验可用资金
                        fund_is_check = 0
                        ETF_CJHB_QC_B(QueryInit, QueryEnd, wt_reqs, fund_is_check)
                    else:
                        logger.error('成交回报检查：错误,成交回报数量累计已经全部成交！')
                        cjhb_reslut['成交回报检查状态'] = 'end'
                        cjhb_reslut['测试结果'] = False
                        cjhb_reslut['测试错误原因'] = '成交回报数量累计已经全部成交！'
                elif hb_data['quantity'] < wt_reqs['quantity']:
                    logger.info('成交回报检查：当前成交回报状态为未全部成交！')
                    cjhb_reslut['成交回报检查状态'] = 'pending'
                else:
                    logger.error('成交回报错误，总成交数量大于委托数量')
                    cjhb_reslut['成交回报检查状态'] = 'end'
                    cjhb_reslut['测试结果'] = False
                    cjhb_reslut['测试错误原因'] = '成交回报错误，总成交数量大于委托数量'
            else:
                logger.error('成交回报有问题：价格×数量不等于成交金额' +
                             str(hb_data['price'] * hb_data['quantity']) +
                             ',' + str(hb_data['trade_amount']))
                cjhb_reslut['成交回报检查状态'] = 'end'
                cjhb_reslut['测试结果'] = False
                cjhb_reslut['测试错误原因'] = '成交回报有问题：价格×数量不等于成交金额'
        elif hb_data['ticker'] == etf_code1_code2['etf_code2']:
            if abs(hb_data['trade_amount'] -
                    round(hb_data['price'] * hb_data['quantity'], 2)) < 0.01:
                # 全成,部成和错误处理
                if hb_data['quantity'] == wt_reqs['quantity']:
                    if expectStatus == '全成':
                        logger.info('成分股成交数量正确！')
                        # fund_is_check:1-校验可用资金,0-不校验可用资金
                        fund_is_check = 1
                        ETF_CJHB_QC_B(QueryInit, QueryEnd, wt_reqs, fund_is_check)
                    else:
                        logger.error('成交回报检查：错误,成交回报数量累计已经全部成交！')
                        cjhb_reslut['成交回报检查状态'] = 'end'
                        cjhb_reslut['测试结果'] = False
                        cjhb_reslut['测试错误原因'] = '成交回报数量累计已经全部成交！'
                elif hb_data['quantity'] < wt_reqs['quantity']:
                    logger.info('成交回报检查：当前成交回报状态为未全部成交！')
                    cjhb_reslut['成交回报检查状态'] = 'pending'
                else:
                    logger.error('成交回报错误，总成交数量大于委托数量')
                    cjhb_reslut['成交回报检查状态'] = 'end'
                    cjhb_reslut['测试结果'] = False
                    cjhb_reslut['测试错误原因'] = '成交回报错误，总成交数量大于委托数量'
            else:
                logger.error('成交回报有问题：价格×数量不等于成交金额' +
                             str(hb_data['price'] * hb_data['quantity']) +
                             ',' + str(hb_data['trade_amount']))
                cjhb_reslut['成交回报检查状态'] = 'end'
                cjhb_reslut['测试结果'] = False
                cjhb_reslut['测试错误原因'] = '成交回报有问题：价格×数量不等于成交金额'

        else:
            logger.error('成交回报返回未知代码： ' + hb_data['ticker'])

    # --如果委托方向是赎回，执行如下－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
    elif wt_reqs['side'] == Api.const.XTP_SIDE_TYPE['XTP_SIDE_REDEMPTION']:
        # --委托数据和成交数据比较
        if wt_reqs['ticker'] == hb_data['ticker']:
            cjhb_reslut['xtp_id'] = hb_data['order_xtp_id']
            cjhb_reslut['市场'] = hb_data['market']
            cjhb_reslut['股票代码'] = hb_data['ticker']
            cjhb_reslut['买卖方向'] = hb_data['side']
            cjhb_reslut['成交价格'] = hb_data['price']
            cjhb_reslut['成交类型'] = hb_data['trade_type']
            cjhb_reslut['成交数量'] = hb_data['quantity']
            cjhb_reslut['成交金额'] = hb_data['trade_amount']

            # 沪A市场ETF申购成交回报返回的买卖方向为XTP_SIDE_BUY,所以不判断买卖方向
            side_flag = True
            if wt_reqs['market'] == Api.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A']:
                side_flag = (xtp_id == hb_data['order_xtp_id']
                             and wt_reqs['market'] == hb_data['market']
                             and wt_reqs['side'] == hb_data['side'])
            else:
                side_flag = (xtp_id == hb_data['order_xtp_id']
                             and wt_reqs['market'] == hb_data['market'])

            if side_flag:
                if abs(hb_data['trade_amount'] - round(
                                hb_data['price'] * hb_data['quantity'],
                                2)) < 0.01:
                    # 全成,部成和错误处理
                    if cjhb_reslut['成交数量'] == wt_reqs['quantity']:
                        if expectStatus == '全成':
                            logger.info('成交回报检查：全部成交业务数据开始检查')
                            ETF_CJHB_QC_S(QueryInit, QueryEnd, wt_reqs)
                        else:
                            logger.error('成交回报检查：错误,成交回报数量累计已经全部成交！')
                            cjhb_reslut['成交回报检查状态'] = 'end'
                            cjhb_reslut['测试结果'] = False
                            cjhb_reslut['测试错误原因'] = '成交回报数量累计已经全部成交！'
                    elif cjhb_reslut['成交数量'] < wt_reqs['quantity']:
                        logger.info('成交回报检查：当前成交回报状态为未全部成交！')
                        cjhb_reslut['成交回报检查状态'] = 'pending'
                    else:
                        logger.error('成交回报错误，总成交数量大于委托数量')
                        cjhb_reslut['成交回报检查状态'] = 'end'
                        cjhb_reslut['测试结果'] = False
                        cjhb_reslut['测试错误原因'] = '成交回报错误，总成交数量大于委托数量'
                else:
                    logger.error('成交回报有问题：价格×数量不等于成交金额' +
                                 str(hb_data['price'] * hb_data['quantity']) +
                                 ',' + str(hb_data['trade_amount']))
                    cjhb_reslut['成交回报检查状态'] = 'end'
                    cjhb_reslut['测试结果'] = False
                    cjhb_reslut['测试错误原因'] = '成交回报有问题：价格×数量不等于成交金额'
            else:
                logger.error('成交回报和委托信息不一致，如：xtpid,market,ticker,side,price')
                cjhb_reslut['成交回报检查状态'] = 'end'
                cjhb_reslut['测试结果'] = False
                cjhb_reslut[
                    '测试错误原因'] = '成交回报和委托信息不一致，如：xtpid,market,ticker,side,price'
        else:
            if abs(hb_data['trade_amount'] - round(
                            hb_data['price'] * hb_data['quantity'], 2)) < 0.01:
                component_share = 0  # etf成分股数量
                component_share = QueryEtfComponentsDB(wt_reqs['ticker'],
                                                       hb_data['ticker'])
                redemption_unit = ServiceConfig.REDEMPTION_QUANTITY  # etf赎回单位数

                # 全成,部成和错误处理
                if hb_data['quantity'] == component_share * redemption_unit:
                    if expectStatus == '全成':
                        logger.info('成交回报检查：成分股成交数量正确！')
                    else:
                        logger.error('成交回报检查：错误,成交回报数量累计已经全部成交！')
                        cjhb_reslut['成交回报检查状态'] = 'end'
                        cjhb_reslut['测试结果'] = False
                        cjhb_reslut['测试错误原因'] = '成交回报数量累计已经全部成交！'
                elif hb_data['quantity'] < component_share * redemption_unit:
                    logger.info('成交回报检查：当前成交回报状态为未全部成交！')
                    cjhb_reslut['成交回报检查状态'] = 'pending'
                else:
                    print hb_data['ticker']
                    print wt_reqs['ticker']
                    logger.error('成交回报错误，总成交数量大于委托数量')
                    cjhb_reslut['成交回报检查状态'] = 'end'
                    cjhb_reslut['测试结果'] = False
                    cjhb_reslut['测试错误原因'] = '成交回报错误，总成交数量大于委托数量'
            else:
                logger.error('成交回报有问题：价格×数量不等于成交金额' +
                             str(hb_data['price'] * hb_data['quantity']) +
                             ',' + str(hb_data['trade_amount']))
                cjhb_reslut['成交回报检查状态'] = 'end'
                cjhb_reslut['测试结果'] = False
                cjhb_reslut['测试错误原因'] = '成交回报有问题：价格×数量不等于成交金额'

    return cjhb_reslut


# -----------------------------------------------------------------------------------------------------------------------
#--etf申购--全部成交--费用持仓检查－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
def ETF_CJHB_QC_B(QueryInit, QueryEnd, wt_reqs, fund_is_check):
    logger.info('成交回报－买－全部成交－费用持仓检查')
    # ----计算费用
    nav_per_cu = QueryEtfNavDB(wt_reqs['ticker'])  # etf最小申赎单位净值
    fee = wt_reqs['quantity'] * fee_rate_etf_creation * (nav_per_cu / 10000) / stkQty['最小申赎单位']  # 申赎费用
    if  fee <= fee_etf_min :
        fee = fee_etf_min
    else:
        fee = float(Decimal(Decimal(str(fee)).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)))

    # ----判断可用资金是否正确-----
    if fund_is_check == 1 \
            and abs(QueryInit['可用资金'] - cjhb_reslut['成交金额'] - fee - QueryEnd['可用资金']) > 0.00001:
        logger.error('可用资金计算有错,原可用资金、成交金额、费用、现可用资金分别是' + str(
            QueryInit['可用资金']) + ',' + str(cjhb_reslut['成交金额']) + ',' + str(
            fee) + ',' + str(QueryEnd['可用资金']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['可用资金计算有错', {
            '原可用资金': QueryInit['可用资金'],
            '成交金额': cjhb_reslut['成交金额'],
            '费用': fee,
            '现可用资金': QueryEnd['可用资金']
        }]
    # -----判断下单前后股票代码、市场是否一致-------
    if QueryEnd['股票代码'] !=QueryInit['股票代码'] or QueryEnd['市场'] !=QueryInit['市场']:
        logger.error('下单前后查询的市场股票代码信息不一致,下单前查询的市场和股票代码是'+
                     str(QueryInit['市场'])+
                     ','+str(QueryInit['股票代码'])+
                     ',下单后查询的市场和股票代码是'+
                     str(QueryEnd['市场'])+
                     ','+str(QueryEnd['股票代码']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['下单前后查询的市场股票代码信息不一致', {
            '下单前查询的市场是': QueryInit['市场'],
            '下单前查询的股票代码是': QueryEnd['股票代码'],
            '下单后查询的市场是': QueryInit['市场'],
            '下单后查询的股票代码是': QueryEnd['股票代码'],
        }]
    # ---－判断总持仓是否正确
    elif abs(QueryEnd['总持仓'] - QueryInit['总持仓'] - cjhb_reslut['成交数量']) > 0.00001:
        logger.error('总持仓不正确，原总持仓，成交数量，现总持仓分别是'+
                     str(QueryInit['总持仓'])+
                     ','+str(cjhb_reslut['成交数量'])+
                     ','+str(QueryEnd['总持仓']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['总持仓不正确', {
            '原总持仓': QueryInit['总持仓'],
            '成交数量': cjhb_reslut['成交数量'],
            '现总持仓': QueryEnd['总持仓'],
        }]
    # --判断可卖持仓是否正确
    elif QueryEnd['可卖持仓'] -QueryInit['可卖持仓'] - cjhb_reslut['成交数量'] > 0.00001:
        logger.error('可卖持仓不正确，原可卖持仓，现可卖持仓，成交数量分别是'+
                     str(QueryInit['可卖持仓'])+
                     ','+str(QueryEnd['可卖持仓'])+
                     ','+str(cjhb_reslut['成交数量']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['可卖持仓不正确', {
            '原可卖持仓': QueryInit['可卖持仓'],
            '现可卖持仓':  QueryEnd['可卖持仓'],
            '成交数量': cjhb_reslut['成交数量']
        }]
    # --判断昨日持仓是否正确
    elif QueryEnd['昨日持仓'] != QueryInit['昨日持仓']:
        logger.error('昨日持仓不正确，原昨日持仓，现昨日持仓分别是'+
                     str(QueryInit['昨日持仓'])+
                     ','+str(QueryEnd['昨日持仓']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['昨日持仓不正确', {
            '原昨日持仓': QueryInit['昨日持仓'],
            '现昨日持仓':  QueryEnd['昨日持仓']
        }]
    # --判断可赎回证券数是否正确
    elif QueryEnd['今日可申购赎回持仓'] != QueryInit['今日可申购赎回持仓']:
        logger.error('今日可申购赎回持仓不正确，原今日可申购赎回持仓，现今日可申购赎回持仓分别是'+
                     str(QueryInit['今日可申购赎回持仓'])+
                     ','+str(QueryEnd['今日可申购赎回持仓']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['今日可申购赎回持仓不正确', {
            '原今日可申购赎回持仓': QueryInit['今日可申购赎回持仓'],
            '现今日可申购赎回持仓':  QueryEnd['今日可申购赎回持仓']
        }]
    else:
        logger.info('买_全成_成交回报_业务校验正确！')
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = True


# -----------------------------------------------------------------------------------------------------------------------
#--etf申购--全部成交--费用持仓检查----------------------------------------------------------------------------------------------
def ETF_CJHB_QC_S(QueryInit,QueryEnd,wt_reqs):
    logger.info('成交回报－卖－全部成交－费用持仓检查')
    # -----判断下单前后股票代码、市场是否一致-------
    if QueryEnd['股票代码'] != QueryInit['股票代码'] or \
                    QueryEnd['市场'] != QueryInit['市场']:
        logger.error('下单前后查询的市场股票代码信息不一致', '下单前查询的市场和股票代码是' +
                     str(QueryInit['市场']) + ',' + str(
            QueryInit['股票代码']) + ',下单后查询的市场和股票代码是' +
                     str(QueryEnd['市场']) + ',' + str(QueryEnd['股票代码']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['下单前后查询的市场股票代码信息不一致', {
            '下单前查询的市场是': QueryInit['市场'],
            '下单前查询的股票代码是': QueryEnd['股票代码'],
            '下单后查询的市场是': QueryInit['市场'],
            '下单后查询的股票代码是': QueryEnd['股票代码'],
        }]
    # ---－判断拥股数量是否正确
    elif abs(QueryInit['拥股数量'] - QueryEnd['拥股数量'] - cjhb_reslut['成交数量']) > 0.00001:
        logger.error(
            '拥股数量不正确，原拥股数量，成交数量，现拥股数量分别是' +
            str(QueryInit['拥股数量']) +
            ',' + str(cjhb_reslut['成交数量']) +
            ',' + str(QueryEnd['拥股数量']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['拥股数量不正确', {
            '原拥股数量': QueryInit['拥股数量'],
            '成交数量': cjhb_reslut['成交数量'],
            '现拥股数量': QueryEnd['拥股数量'],
        }]
    # --判断可卖出证券数是否正确
    elif QueryInit['可卖出证券数'] - QueryEnd['可卖出证券数'] - cjhb_reslut['成交数量'] > 0.00001:
        logger.error('可卖出证券数不正确，原可卖出证券数，现可卖出证券数，成交数量分别是' +
                     str(QueryInit['可卖出证券数']) +
                     ',' + str(QueryEnd['可卖出证券数']) +
                     ',' + str(cjhb_reslut['成交数量']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['可卖出证券数不正确', {
            '原可卖出证券数': QueryInit['可卖出证券数'],
            '现可卖出证券数': QueryEnd['可卖出证券数'],
            '成交数量': cjhb_reslut['成交数量']
        }]
    # --判断可用于申购证券数是否正确
    elif QueryEnd['可用于申购证券数'] != QueryInit['可用于申购证券数']:
        logger.error(
            '可用于申购证券数不正确，原可用于申购证券数，现可用于申购证券数分别是' +
            str(QueryInit['可用于申购证券数']) +
            ',' + str(QueryEnd['可用于申购证券数']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['可用于申购证券数不正确', {
            '原可用于申购证券数': QueryInit['可用于申购证券数'],
            '现可用于申购证券数': QueryEnd['可用于申购证券数']
        }]
    # --判断可赎回证券数是否正确
    elif QueryInit['可赎回证券数'] - QueryEnd['可赎回证券数'] - cjhb_reslut['成交数量'] > 0.00001:
        logger.error('可赎回证券数不正确，原可赎回证券数，现可赎回证券数，成交数量分别是' +
                     str(QueryInit['可赎回证券数']) +
                     ',' + str(QueryEnd['可赎回证券数']) +
                     ',' + str(cjhb_reslut['成交数量']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['可赎回证券数不正确', {
            '原可赎回证券数': QueryInit['可赎回证券数'],
            '现可赎回证券数': QueryEnd['可赎回证券数']
        }]
    else:
        logger.info('买_全成_成交回报_业务校验正确！')
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = True


# 初始化成交回报测试结果集
def cjhbDataInit():
    cjhb_reslut['成交回报检查状态']='init'
    cjhb_reslut['xtp_id'] = None
    cjhb_reslut['市场'] = None
    cjhb_reslut['股票代码'] = None
    cjhb_reslut['买卖方向'] = None
    cjhb_reslut['成交价格'] = None
    cjhb_reslut['成交数量'] = 0
    cjhb_reslut['成交金额'] = 0.00
    cjhb_reslut['成交类型'] = None
    cjhb_reslut['测试结果'] = 0
    cjhb_reslut['测试错误原因'] = None

