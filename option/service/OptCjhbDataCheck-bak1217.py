#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
import time
import json
from decimal import *
from OptCheckDataPrice import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
import ServiceConfig
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from config import CONST_TRADE_USER
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/option/mysql")
from OptGetUpOrDownPrice import *
from opt_database_manager import QueryTable
from OptUtils import cal_margin_call
from OptUtils import cal_margin_put

#---定义个股期权费用
fee_rate_option_buy_open = ServiceConfig.FEE_RATE_OPTION_BUY_OPEN
fee_rate_option_sell_close =ServiceConfig.FEE_RATE_OPTION_SELL_CLOSE
fee_rate_option_sell_open = ServiceConfig.FEE_RATE_OPTION_SELL_OPEN
fee_rate_option_buy_close =ServiceConfig.FEE_RATE_OPTION_BUY_CLOSE
fee_rate_option_execute = ServiceConfig.FEE_RATE_OPTION_EXECUTE

today = time.strftime('%Y%m%d', time.localtime(time.time()))

#--持仓成本，保留小数位
avg_price_DecimalPlaces_option = ServiceConfig.AVG_PRICE_DECIMALPLACES_OPTION

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
    '测试结果':0,
    '测试错误原因':None,
}

#---业务判断程序：买或是卖，及全成或是部成
def cjhbDataCheck(expectStatus, Api, QueryInit, wt_reqs,
                  xtp_id, QueryEnd, hb_data, etf_sell_flag = 0):
    '''

    :param expectStatus: 期望状态
    :param Api: Api实例
    :param QueryInit: 初始资金持仓情况
    :param wt_reqs: 委托参数
    :param xtp_id: 下单编号
    :param QueryEnd: 当前资金持仓情况
    :param hb_data: 成交回报数据
    :param etf_sell_flag: 用来判断卖出etf前是否作了etf申购，如果是则为1，否则默认为0
    :return: cjhb_reslut
    '''
    #根据证券代码获取涨停和跌停价
    upPrice = getUpPrice(wt_reqs['ticker'])
    downPrice = getDownPrice(wt_reqs['ticker'])

    # 获取合约单位
    rs = QueryTable('xtp_opt_cntrt_info_' + today, ['cntrt_mul_unit'],
                                {'cntrt_id': wt_reqs['ticker']}, 2)
    trade_amount_expect = round(hb_data['price'] * hb_data['quantity'] * rs['cntrt_mul_unit'],2)
    #-----如果委托方向是普通买，执行如下－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
    if wt_reqs['side'] == Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY']:
        #--委托数据和成交数据比较
        if check_order(xtp_id, hb_data, wt_reqs, Api):
            if  abs(hb_data['trade_amount'] - trade_amount_expect) < 0.01:
                cjhb_reslut['xtp_id'] = hb_data['order_xtp_id']
                cjhb_reslut['市场'] = hb_data['market']
                cjhb_reslut['股票代码'] = hb_data['ticker']
                cjhb_reslut['买卖方向'] = hb_data['side']
                cjhb_reslut['成交价格'] = hb_data['price']
                cjhb_reslut['成交类型'] = hb_data['trade_type']
                cjhb_reslut['成交数量'] += hb_data['quantity']
                cjhb_reslut['成交金额'] += hb_data['trade_amount']

                # 部分成交－－－－－－－－－－－－－
                if cjhb_reslut['成交数量'] < wt_reqs['quantity']:
                    if expectStatus == '部成':
                        logger.info('成交回报检查：部分成交业务数据开始检查')
                        if wt_reqs['position_effect'] == Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_OPEN']:
                            CJHB_BC_B_OPEN(QueryInit, wt_reqs, QueryEnd, upPrice)
                        else:
                            wt_price = wt_reqs['price']
                            if wt_reqs['price_type'] != Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT']:
                                wt_price = upPrice
                            CJHB_BC_B_CLOSE(QueryInit, wt_reqs, QueryEnd, wt_price)
                    elif expectStatus == '全成':
                        logger.info('成交回报检查：当前成交回报累计成交数量为部分成交，请等待全部成交！')
                        cjhb_reslut['成交回报检查状态']='pending'

                # 全部成交－－－－－－－－－－－－－
                elif cjhb_reslut['成交数量'] == wt_reqs['quantity']:
                    if expectStatus == '全成':
                        logger.info('成交回报检查：全部成交业务数据开始检查')
                        if wt_reqs['position_effect'] == Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_OPEN']:
                            CJHB_QC_B_OPEN(QueryInit, QueryEnd, wt_reqs)
                        else:
                            CJHB_QC_B_CLOSE(QueryInit, QueryEnd, wt_reqs)
                    elif expectStatus == '部成':
                        logger.error('成交回报检查：错误,期待状态为部成，但成交回报数量累计已经全部成交！')
                        cjhb_reslut['成交回报检查状态'] = 'end'
                        cjhb_reslut['测试结果'] = False
                        cjhb_reslut['测试错误原因'] = '期待状态为部成，但成交回报数量累计已经全部成交！'

                # 错误：成交数量>委托数量
                elif cjhb_reslut['成交数量'] > wt_reqs['quantity']:
                    logger.error('成交回报错误，总成交数量大于委托数量')
                    cjhb_reslut['成交回报检查状态'] = 'end'
                    cjhb_reslut['测试结果'] = False
                    cjhb_reslut['测试错误原因'] = '成交回报错误，总成交数量大于委托数量'

            else:
                trade_amount_expect = float(Decimal(Decimal(str(hb_data['price']* hb_data['quantity'])).quantize(Decimal('.01'),
                          rounding=ROUND_HALF_UP)))
                logger.error('成交回报有问题：价格×数量不等于成交金额'+str(trade_amount_expect)+','+str(hb_data['trade_amount']))
                cjhb_reslut['成交回报检查状态'] = 'end'
                cjhb_reslut['测试结果'] = False
                cjhb_reslut['测试错误原因'] = '成交回报有问题：价格×数量不等于成交金额'
        else:
            logger.error('成交回报和委托信息不一致，如：xtpid,market,ticker,side,price')
            cjhb_reslut['成交回报检查状态'] = 'end'
            cjhb_reslut['测试结果'] = False
            cjhb_reslut['测试错误原因'] = '成交回报和委托信息不一致，如：xtpid,market,ticker,side,price'

    #--如果委托方向是卖，执行如下－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
    elif wt_reqs['side'] == Api.const.XTP_SIDE_TYPE['XTP_SIDE_SELL']:
        # --委托数据和成交数据比较
        if check_order(xtp_id, hb_data, wt_reqs, Api):
            if abs(hb_data['trade_amount'] - trade_amount_expect) < 0.01:
                cjhb_reslut['xtp_id'] = hb_data['order_xtp_id']
                cjhb_reslut['市场'] = hb_data['market']
                cjhb_reslut['股票代码'] = hb_data['ticker']
                cjhb_reslut['买卖方向'] = hb_data['side']
                cjhb_reslut['成交价格'] = hb_data['price']
                cjhb_reslut['成交类型'] = hb_data['trade_type']
                cjhb_reslut['成交数量'] += hb_data['quantity']
                cjhb_reslut['成交金额'] += hb_data['trade_amount']

                # 部分成交－－－－－－－－－－－－－
                if cjhb_reslut['成交数量'] < wt_reqs['quantity']:
                    if expectStatus == '部成':
                        logger.info('成交回报检查：部分成交业务数据开始检查')
                        quantity_left = wt_reqs['quantity'] - hb_data['quantity']
                        if wt_reqs['position_effect'] == Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_OPEN']:
                            CJHB_BC_S_OPEN(QueryInit, wt_reqs, QueryEnd)
                        else:
                            Prefreezing = quantity_left * fee_rate_option_sell_close - \
                                          quantity_left * downPrice * rs['cntrt_mul_unit']
                            Prefreezing = Prefreezing if Prefreezing > 0 else 0
                            CJHB_BC_S_CLOSE(QueryInit, wt_reqs, QueryEnd, Prefreezing)

                    elif expectStatus == '全成':
                        logger.info('成交回报检查：当前成交回报累计成交数量为部分成交，请等待全部成交！')
                        cjhb_reslut['成交回报检查状态'] = 'pending'

                # 全部成交－－－－－－－－－－－－－
                elif cjhb_reslut['成交数量'] == wt_reqs['quantity']:
                    if expectStatus == '全成':
                        logger.info('成交回报检查：全部成交业务数据开始检查')
                        if wt_reqs['position_effect'] == Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_OPEN']:
                            CJHB_QC_S_OPEN(QueryInit, QueryEnd, wt_reqs)
                        else:
                            CJHB_QC_S_CLOSE(QueryInit, QueryEnd, wt_reqs)
                    elif expectStatus == '部成':
                        logger.error('成交回报检查：错误,期待状态为部成，但成交回报数量累计已经全部成交！')
                        cjhb_reslut['成交回报检查状态'] = 'end'
                        cjhb_reslut['测试结果'] = False
                        cjhb_reslut['测试错误原因'] = '期待状态为部成，但成交回报数量累计已经全部成交！'

                # 错误：成交数量>委托数量
                elif cjhb_reslut['成交数量'] > wt_reqs['quantity']:
                    logger.error('成交回报错误，总成交数量大于委托数量')
                    cjhb_reslut['成交回报检查状态'] = 'end'
                    cjhb_reslut['测试结果'] = False
                    cjhb_reslut['测试错误原因'] = '成交回报错误，总成交数量大于委托数量'

            else:
                logger.error('成交回报有问题：价格×数量不等于成交金额'+str(hb_data['price'])+','+str(hb_data['quantity'])+','+str(hb_data['trade_amount']))
                cjhb_reslut['成交回报检查状态'] = 'end'
                cjhb_reslut['测试结果'] = False
                cjhb_reslut['测试错误原因'] = '成交回报有问题：价格×数量不等于成交金额'
        else:
            logger.error('成交回报和委托信息不一致，如：xtpid,market,ticker,side,price')
            cjhb_reslut['成交回报检查状态'] = 'end'
            cjhb_reslut['测试结果'] = False
            cjhb_reslut['测试错误原因'] = '成交回报和委托信息不一致，如：xtpid,market,ticker,side,price'

    return cjhb_reslut

#--买开--全部成交--费用持仓检查－－－－－－－－－－－
def CJHB_QC_B_OPEN(QueryInit,QueryEnd,wt_reqs):
    '''
        校验下单前后资金和持仓
    '''
    logger.info('成交回报－买开－全部成交－费用持仓检查')

    fee = get_fee(cjhb_reslut['成交数量'], wt_reqs)

    # 获取合约单位
    rs = QueryTable('xtp_opt_cntrt_info_' + today, ['cntrt_mul_unit'],
                    {'cntrt_id': wt_reqs['ticker']}, 2)

    #--计算期待持仓成本
    price_avg = (QueryInit['持仓成本'] * QueryInit['拥股数量'] * rs['cntrt_mul_unit'] +
                 cjhb_reslut['成交金额'] + fee)/ \
                ((QueryInit['拥股数量'] + cjhb_reslut['成交数量']) * rs['cntrt_mul_unit'])

    market_type = Api.const.XTP_MARKET_TYPE
    market_init = 2 if QueryInit['市场'] == market_type['XTP_MKT_SZ_A'] else 1
    market_end = 2 if QueryEnd['市场'] == market_type['XTP_MKT_SZ_A'] else 1

    check_item = {
        '可用资金': [[QueryInit['可用资金'], cjhb_reslut['成交金额'], fee, QueryEnd['可用资金'], 0.01],
                 ['-', '-', '-', '>'], ['原可用资金', '成交金额', '费用', '现可用资金'], '%f'],
        '总资产': [[QueryInit['总资产'], cjhb_reslut['成交金额'], fee, QueryEnd['总资产'], 0.01],
                ['-', '-', '-', '>'], ['原总资产', '成交金额', '费用', '现总资产'], '%f'],
        '证券资产': [[QueryInit['证券资产'], QueryEnd['证券资产']],
                 ['!='], ['原证券资产', '现证券资产'], '%f'],
        '预扣资金': [[QueryInit['预扣资金'], QueryEnd['预扣资金']],
                 ['!='], ['原预扣资金', '现预扣资金'], '%f'],
        '买入资金': [[QueryEnd['买入资金'], QueryInit['买入资金'], cjhb_reslut['成交金额'], 0.01],
                 ['-', '-', '>'], ['现买入资金', '原买入资金', '成交金额'], '%f'],
        '买入费用': [[QueryEnd['买入费用'], QueryInit['买入费用'], fee, 0.01],
                 ['-', '-', '>'], ['现买入费用', '原买入费用', '费用'], '%f'],
        '卖出资金': [[QueryInit['卖出资金'], QueryEnd['卖出资金']],
                 ['!='], ['原卖出资金', '现卖出资金'], '%f'],
        '卖出费用': [[QueryInit['卖出费用'], QueryEnd['卖出费用']],
                 ['!='], ['原卖出费用', '现卖出费用'], '%f'],
        '冻结保证金': [[QueryInit['冻结保证金'], QueryEnd['冻结保证金']],
                  ['!='], ['原冻结保证金', '现冻结保证金'], '%f'],
        '行权冻结资金': [[QueryInit['行权冻结资金'], QueryEnd['行权冻结资金']],
                   ['!='], ['原行权冻结资金', '现行权冻结资金'], '%f'],
        '行权费用': [[QueryInit['行权费用'], QueryEnd['行权费用']],
                 ['!='], ['原行权费用', '现行权费用'], '%f'],
        '垫付资金': [[QueryInit['垫付资金'], QueryEnd['垫付资金']],
                 ['!='], ['原垫付资金', '现垫付资金'], '%f'],
        '预垫付资金': [[QueryInit['预垫付资金'], QueryEnd['预垫付资金']],
                  ['!='], ['原预垫付资金', '现预垫付资金'], '%f'],
        '昨日余额': [[QueryInit['昨日余额'], QueryEnd['昨日余额']],
                 ['!='], ['原昨日余额', '现昨日余额'], '%f'],
        '当前余额': [[QueryInit['当前余额'], QueryEnd['当前余额']],
                 ['!='], ['原当前余额', '现当前余额'], '%f'],
        '当天出入金': [[QueryInit['当天出入金'], QueryEnd['当天出入金']],
                  ['!='], ['原当天出入金', '现当天出入金'], '%f'],
        '当日交易资金扎差': [[QueryInit['当日交易资金扎差'], cjhb_reslut['成交金额'], fee, QueryEnd['当日交易资金扎差'], 0.01],
                     ['-', '-', '-', '>'], ['现当日交易资金扎差', '成交金额', '费用', '原当日交易资金扎差'], '%f'],
        '资金资产': [[QueryInit['资金资产'], cjhb_reslut['成交金额'], fee, QueryEnd['资金资产'], 0.01],
                 ['-', '-', '-', '>'], ['原资金资产', '成交金额', '费用', '现资金资产'], '%f'],
        '证券代码': [[QueryInit['证券代码'], QueryEnd['证券代码']],
                 ['!='], ['原证券代码', '现证券代码'], '%s'],
        '市场': [[market_init, market_end],
               ['!='], ['原市场', '现市场'], '%s'],
        '拥股数量': [[QueryEnd['拥股数量'], QueryInit['拥股数量'], cjhb_reslut['成交数量'], 0],
                 ['-', '-', '>'], ['现拥股数量', '原拥股数量', '成交数量'], '%d'],
        '可用股份数': [[QueryEnd['可用股份数'], QueryInit['可用股份数'], cjhb_reslut['成交数量'], 0],
                  ['-', '-', '>'], ['现可用股份数', '原可用股份数', '成交数量'], '%d'],
        '持仓成本': [[price_avg, QueryEnd['持仓成本'], 0.0001],
                 ['-', '>'], ['实际持仓成本', '查询的持仓成本'], '%f'],
        '浮动盈亏': [[QueryInit['浮动盈亏'], QueryEnd['浮动盈亏']],
                 ['!='], ['原浮动盈亏', '现浮动盈亏'], '%f'],
        '昨日持仓': [[QueryInit['昨日持仓'], QueryEnd['昨日持仓']],
                 ['!='], ['原昨日持仓', '现昨日持仓'], '%d'],
        '今日可申购赎回持仓': [[QueryInit['今日可申购赎回持仓'], QueryEnd['今日可申购赎回持仓']],
                      ['!='], ['原今日可申购赎回持仓', '现今日可申购赎回持仓'], '%d'],
        # #'持仓方向' TODO
        '可行权合约': [[QueryInit['可行权合约'], QueryEnd['可行权合约']],
                  ['!='], ['原可行权合约', '现可行权合约'], '%d'],
        '可锁定标的': [[QueryInit['可锁定标的'], QueryEnd['可锁定标的']],
                  ['!='], ['原可锁定标的', '现可锁定标的'], '%d'],
        '可行权标的': [[QueryInit['可行权标的'], QueryEnd['可行权标的']],
                  ['!='], ['原可行权标的', '现可行权标的'], '%d'],
        '已锁定标的': [[QueryInit['已锁定标的'], QueryEnd['已锁定标的']],
                  ['!='], ['原已锁定标的', '现已锁定标的'], '%d'],
        '可用已锁定标的': [[QueryInit['可用已锁定标的'], QueryEnd['可用已锁定标的']],
                    ['!='], ['原可用已锁定标的', '现可用已锁定标的'], '%d'],
    }

    check_fund_stk_cjhb(check_item)

#--买平--全部成交--费用持仓检查－－－－－－－－－－－
def CJHB_QC_B_CLOSE(QueryInit,QueryEnd,wt_reqs):
    '''
        校验下单前后资金和持仓
    '''
    logger.info('成交回报－买平－全部成交－费用持仓检查')

    # 获取合约单位
    rs = QueryTable('xtp_opt_cntrt_info_' + today, ['cntrt_mul_unit', 'call_or_put'],
                    {'cntrt_id': wt_reqs['ticker']}, 2)
    # 释放的保证金
    if rs['call_or_put'] == 'C':
        margin = cal_margin_call(wt_reqs['ticker'], wt_reqs['quantity'], QueryInit['昨日持仓'])
    else:
        margin = cal_margin_put(wt_reqs['ticker'], wt_reqs['quantity'], QueryInit['昨日持仓'])

    fee = get_fee(cjhb_reslut['成交数量'], wt_reqs)

    market_type = Api.const.XTP_MARKET_TYPE
    market_init = 2 if QueryInit['市场'] == market_type['XTP_MKT_SZ_A'] else 1
    market_end = 2 if QueryEnd['市场'] == market_type['XTP_MKT_SZ_A'] else 1

    check_item = {
        '可用资金': [[QueryInit['可用资金'], cjhb_reslut['成交金额'], margin, fee, QueryEnd['可用资金'], 0.01],
                 ['-', '+', '-', '-', '>'], ['原可用资金', '成交金额', '冻结保证金', '费用', '现可用资金'], '%f'],
        '总资产': [[QueryInit['总资产'], cjhb_reslut['成交金额'], fee, QueryEnd['总资产'], 0.01],
                ['-', '-', '-', '>'], ['原总资产', '成交金额', '费用', '现总资产'], '%f'],
        '证券资产': [[QueryInit['证券资产'], QueryEnd['证券资产']],
                 ['!='], ['原证券资产', '现证券资产'], '%f'],
        '预扣资金': [[QueryInit['预扣资金'], QueryEnd['预扣资金']],
                 ['!='], ['原预扣资金', '现预扣资金'], '%f'],
        '买入资金': [[QueryEnd['买入资金'], QueryInit['买入资金'], cjhb_reslut['成交金额'], 0.01],
                 ['-', '-', '>'], ['现买入资金', '原买入资金', '成交金额'], '%f'],
        '买入费用': [[QueryEnd['买入费用'], QueryInit['买入费用'], fee, 0.01],
                 ['-', '-', '>'], ['现买入费用', '原买入费用', '费用'], '%f'],
        '卖出资金': [[QueryInit['卖出资金'], QueryEnd['卖出资金']],
                 ['!='], ['原卖出资金', '现卖出资金'], '%f'],
        '卖出费用': [[QueryInit['卖出费用'], QueryEnd['卖出费用']],
                 ['!='], ['原卖出费用', '现卖出费用'], '%f'],
        '冻结保证金': [[QueryInit['冻结保证金'], margin, QueryEnd['冻结保证金'], 0.01],
                  ['-', '-', '>'], ['原冻结保证金', '冻结保证金', '现冻结保证金'], '%f'],
        '行权冻结资金': [[QueryInit['行权冻结资金'], QueryEnd['行权冻结资金']],
                   ['!='], ['原行权冻结资金', '现行权冻结资金'], '%f'],
        '行权费用': [[QueryInit['行权费用'], QueryEnd['行权费用']],
                 ['!='], ['原行权费用', '现行权费用'], '%f'],
        '垫付资金': [[QueryInit['垫付资金'], QueryEnd['垫付资金']],
                 ['!='], ['原垫付资金', '现垫付资金'], '%f'],
        '预垫付资金': [[QueryInit['预垫付资金'], QueryEnd['预垫付资金']],
                  ['!='], ['原预垫付资金', '现预垫付资金'], '%f'],
        '昨日余额': [[QueryInit['昨日余额'], QueryEnd['昨日余额']],
                 ['!='], ['原昨日余额', '现昨日余额'], '%f'],
        '当前余额': [[QueryInit['当前余额'], QueryEnd['当前余额']],
                 ['!='], ['原当前余额', '现当前余额'], '%f'],
        '当天出入金': [[QueryInit['当天出入金'], QueryEnd['当天出入金']],
                  ['!='], ['原当天出入金', '现当天出入金'], '%f'],
        '当日交易资金扎差': [[QueryInit['当日交易资金扎差'], cjhb_reslut['成交金额'], fee, QueryEnd['当日交易资金扎差'], 0.01],
                     ['-', '-', '-', '>'], ['现当日交易资金扎差', '成交金额', '费用', '原当日交易资金扎差'], '%f'],
        '资金资产': [[QueryInit['资金资产'], cjhb_reslut['成交金额'], fee, QueryEnd['资金资产'], 0.01],
                 ['-', '-', '-', '>'], ['原资金资产', '成交金额', '费用', '现资金资产'], '%f'],
        '证券代码': [[QueryInit['证券代码'], QueryEnd['证券代码']],
                 ['!='], ['原证券代码', '现证券代码'], '%s'],
        '市场': [[market_init, market_end],
               ['!='], ['原市场', '现市场'], '%s'],
        '拥股数量': [[QueryEnd['拥股数量'], QueryInit['拥股数量'], cjhb_reslut['成交数量'], 0],
                 ['-', '+', '>'], ['现拥股数量', '原拥股数量', '成交数量'], '%d'],
        '可用股份数': [[QueryEnd['可用股份数'], QueryInit['可用股份数'], cjhb_reslut['成交数量'], 0],
                  ['-', '+', '>'], ['现可用股份数', '原可用股份数', '成交数量'], '%d'],
        '持仓为0-持仓成本': [[QueryInit['持仓成本'], QueryEnd['持仓成本'], QueryEnd['可用股份数'], 0],
                 ['!=', ' and ', '!='], ['原持仓成本', '现持仓成本', '可用股份数'], '%f'],
        '持仓不为0-持仓成本': [[QueryEnd['持仓成本'], 0, QueryEnd['可用股份数'], 0],
                  ['!=', ' and ', '=='], ['现持仓成本', '实际持仓成本', '可用股份数'], '%f'],
        '浮动盈亏': [[QueryInit['浮动盈亏'], QueryEnd['浮动盈亏']],
                 ['!='], ['原浮动盈亏', '现浮动盈亏'], '%f'],
        '昨日持仓': [[QueryInit['昨日持仓'], QueryEnd['昨日持仓']],
                 ['!='], ['原昨日持仓', '现昨日持仓'], '%d'],
        '今日可申购赎回持仓': [[QueryInit['今日可申购赎回持仓'], QueryEnd['今日可申购赎回持仓']],
                      ['!='], ['原今日可申购赎回持仓', '现今日可申购赎回持仓'], '%d'],
        # #'持仓方向' TODO
        '可行权合约': [[QueryInit['可行权合约'], QueryEnd['可行权合约']],
                  ['!='], ['原可行权合约', '现可行权合约'], '%d'],
        '可锁定标的': [[QueryInit['可锁定标的'], QueryEnd['可锁定标的']],
                  ['!='], ['原可锁定标的', '现可锁定标的'], '%d'],
        '可行权标的': [[QueryInit['可行权标的'], QueryEnd['可行权标的']],
                  ['!='], ['原可行权标的', '现可行权标的'], '%d'],
        '已锁定标的': [[QueryInit['已锁定标的'], QueryEnd['已锁定标的']],
                  ['!='], ['原已锁定标的', '现已锁定标的'], '%d'],
        '可用已锁定标的': [[QueryInit['可用已锁定标的'], QueryEnd['可用已锁定标的']],
                    ['!='], ['原可用已锁定标的', '现可用已锁定标的'], '%d'],
    }

    check_fund_stk_cjhb(check_item)

#--买开--部分成交--费用持仓检查－－－－－－－－－－－－－－－－
def CJHB_BC_B_OPEN(QueryInit, wt_reqs, QueryEnd, upPrice):
    logger.info('成交回报－买开－部分成交－费用持仓检查')

    fee = get_fee(cjhb_reslut['成交数量'], wt_reqs)

    # 获取合约单位
    rs = QueryTable('xtp_opt_cntrt_info_' + today, ['cntrt_mul_unit'],
                    {'cntrt_id': wt_reqs['ticker']}, 2)

    # --计算期待持仓成本
    price_avg = ((QueryInit['持仓成本'] * QueryInit['拥股数量'] * rs['cntrt_mul_unit'] +
                 cjhb_reslut['成交金额']) + fee)/ \
                ((QueryInit['拥股数量'] + cjhb_reslut['成交数量']) * rs['cntrt_mul_unit'])

    #---如果委托类型为限价的，那么计算费用的价格＝委托的价格；如果为市价的，计算费用的价格＝涨停价
    if wt_reqs['price_type'] == Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT']:
        wt_price = wt_reqs['price']
    else:
        wt_price = upPrice

    #--待成交数量为
    nomatch_qty = wt_reqs['quantity'] - cjhb_reslut['成交数量']
    # 冻结资金
    frozen_amount = nomatch_qty * wt_price * rs['cntrt_mul_unit'] + \
                    nomatch_qty * fee
    frozen_amount = float(Decimal(Decimal(str(frozen_amount)).quantize(Decimal('.01'),
                          rounding=ROUND_HALF_UP)))

    market_type = Api.const.XTP_MARKET_TYPE
    market_init = 2 if QueryInit['市场'] == market_type['XTP_MKT_SZ_A'] else 1
    market_end = 2 if QueryEnd['市场'] == market_type['XTP_MKT_SZ_A'] else 1

    check_item = {
        '可用资金': [[QueryInit['可用资金'], cjhb_reslut['成交金额'], fee, frozen_amount, QueryEnd['可用资金'], 0.01],
                 ['-', '-', '-', '-', '>'], ['原可用资金', '成交金额', '费用', '冻结资金', '现可用资金'], '%f'],
        '总资产': [[QueryInit['总资产'], cjhb_reslut['成交金额'], fee, QueryEnd['总资产'], 0.01],
                ['-', '-', '-', '>'], ['原总资产', '成交金额', '费用', '现总资产'], '%f'],
        '证券资产': [[QueryInit['证券资产'], QueryEnd['证券资产']],
                 ['!='], ['原证券资产', '现证券资产'], '%f'],
        '预扣资金': [[QueryInit['预扣资金'], frozen_amount, QueryEnd['预扣资金'], 0.01],
                 ['+', '-', '>'], ['原预扣资金', '冻结资金', '现预扣资金'], '%f'],
        '买入资金': [[QueryInit['买入资金'], cjhb_reslut['成交金额'], QueryEnd['买入资金'], 0.01],
                 ['+', '-', '>'], ['原买入资金', '成交金额', '现买入资金'], '%f'],
        '买入费用': [[QueryInit['买入费用'], fee, QueryEnd['买入费用'], 0.01],
                 ['+', '-', '>'], ['原买入费用', '费用', '现买入费用'], '%f'],
        '卖出资金': [[QueryEnd['卖出资金'], QueryInit['卖出资金']],
                 ['!='], ['现卖出资金', '原卖出资金'], '%f'],
        '卖出费用': [[QueryEnd['卖出费用'], QueryInit['卖出费用']],
                 ['!='], ['现卖出费用', '原卖出费用'], '%f'],
        '冻结保证金': [[QueryInit['冻结保证金'], QueryEnd['冻结保证金']],
                  ['!='], ['原冻结保证金', '现冻结保证金'], '%f'],
        '行权冻结资金': [[QueryInit['行权冻结资金'], QueryEnd['行权冻结资金']],
                   ['!='], ['原行权冻结资金', '现行权冻结资金'], '%f'],
        '行权费用': [[QueryInit['行权费用'], QueryEnd['行权费用']],
                 ['!='], ['原行权费用', '现行权费用'], '%f'],
        '垫付资金': [[QueryInit['垫付资金'], QueryEnd['垫付资金']],
                 ['!='], ['原垫付资金', '现垫付资金'], '%f'],
        '预垫付资金': [[QueryInit['预垫付资金'], QueryEnd['预垫付资金']],
                  ['!='], ['原预垫付资金', '现预垫付资金'], '%f'],
        '昨日余额': [[QueryInit['昨日余额'], QueryEnd['昨日余额']],
                 ['!='], ['原昨日余额', '现昨日余额'], '%f'],
        '当前余额': [[QueryInit['当前余额'], QueryEnd['当前余额']],
                 ['!='], ['原当前余额', '现当前余额'], '%f'],
        '当天出入金': [[QueryInit['当天出入金'], QueryEnd['当天出入金']],
                  ['!='], ['原当天出入金', '现当天出入金'], '%f'],
        '当日交易资金扎差': [[QueryEnd['当日交易资金扎差'], cjhb_reslut['成交金额'], fee, QueryInit['当日交易资金扎差'], 0.01],
                     ['+', '+', '-', '>'], ['现当日交易资金扎差', '成交金额', '费用', '原当日交易资金扎差'], '%f'],
        '资金资产': [[QueryInit['资金资产'], cjhb_reslut['成交金额'], fee, QueryEnd['资金资产'], 0.01],
                 ['-', '-', '-', '>'], ['原资金资产', '成交金额', '费用', '现资金资产'], '%f'],
        '证券代码': [[QueryInit['证券代码'], QueryEnd['证券代码']],
                 ['!='], ['原证券代码', '现证券代码'], '%s'],
        '市场': [[market_init, market_end],
               ['!='], ['原市场', '现市场'], '%s'],
        '拥股数量': [[QueryInit['拥股数量'], cjhb_reslut['成交数量'], QueryEnd['拥股数量'], 0],
                 ['+', '-', '>'], ['原拥股数量', '成交数量', '现拥股数量'], '%d'],
        '可用股份数': [[QueryInit['可用股份数'], cjhb_reslut['成交数量'], QueryEnd['可用股份数'], 0],
                  ['+', '-', '>'], ['原可用股份数', '成交数量', '现可用股份数'], '%d'],
        '持仓成本': [[price_avg, QueryEnd['持仓成本'], 0.0001],
                 ['-', '>'], ['期望持仓成本', '实际持仓成本'], '%f'],
        '浮动盈亏': [[QueryInit['浮动盈亏'], QueryEnd['浮动盈亏']],
                 ['!='], ['原浮动盈亏', '现浮动盈亏'], '%f'],
        '昨日持仓': [[QueryInit['昨日持仓'], QueryEnd['昨日持仓']],
                 ['!='], ['原昨日持仓', '现昨日持仓'], '%d'],
        '今日可申购赎回持仓': [[QueryInit['今日可申购赎回持仓'], QueryEnd['今日可申购赎回持仓']],
                      ['!='], ['原今日可申购赎回持仓', '现今日可申购赎回持仓'], '%d'],
        # #'持仓方向' TODO
        '可行权合约': [[QueryInit['可行权合约'], QueryEnd['可行权合约']],
                  ['!='], ['原可行权合约', '现可行权合约'], '%d'],
        '可锁定标的': [[QueryInit['可锁定标的'], QueryEnd['可锁定标的']],
                  ['!='], ['原可锁定标的', '现可锁定标的'], '%d'],
        '可行权标的': [[QueryInit['可行权标的'], QueryEnd['可行权标的']],
                  ['!='], ['原可行权标的', '现可行权标的'], '%d'],
        '已锁定标的': [[QueryInit['已锁定标的'], QueryEnd['已锁定标的']],
                  ['!='], ['原已锁定标的', '现已锁定标的'], '%d'],
        '可用已锁定标的': [[QueryInit['可用已锁定标的'], QueryEnd['可用已锁定标的']],
                    ['!='], ['原可用已锁定标的', '现可用已锁定标的'], '%d'],
    }

    check_fund_stk_cjhb(check_item)

#--买平--部分成交--费用持仓检查－－－－－－－－－－－－－－－
def CJHB_BC_B_CLOSE(QueryInit, wt_reqs, QueryEnd, wt_price):
    logger.info('成交回报－买平－部分成交－费用持仓检查')

    # 获取合约单位和认购认沽类型
    rs = QueryTable('xtp_opt_cntrt_info_' + today, ['cntrt_mul_unit', 'call_or_put'],
                    {'cntrt_id': wt_reqs['ticker']}, 2)
    # 释放的保证金
    if rs['call_or_put'] == 'C':
        margin = cal_margin_call(wt_reqs['ticker'], cjhb_reslut['成交数量'], QueryInit['昨日持仓'])
    else:
        margin = cal_margin_put(wt_reqs['ticker'], cjhb_reslut['成交数量'], QueryInit['昨日持仓'])

    fee = get_fee(cjhb_reslut['成交数量'], wt_reqs)

    market_type = Api.const.XTP_MARKET_TYPE
    market_init = 2 if QueryInit['市场'] == market_type['XTP_MKT_SZ_A'] else 1
    market_end = 2 if QueryEnd['市场'] == market_type['XTP_MKT_SZ_A'] else 1

    quantity_left = wt_reqs['quantity'] - cjhb_reslut['成交数量']
    Prefreezing = quantity_left * wt_price * rs['cntrt_mul_unit'] + \
                  get_fee(quantity_left, wt_reqs) - margin
    Prefreezing = Prefreezing if Prefreezing > 0 else 0

    check_item = {
        '可用资金': [[QueryInit['可用资金'], cjhb_reslut['成交金额'], Prefreezing, fee, margin, QueryEnd['可用资金'], 0.01],
                 ['-', '-', '-', '+', '-', '>'],
                 ['原可用资金', '成交金额', '预扣资金', '费用', '冻结保证金', '现可用资金'], '%f'],
        '总资产': [[QueryInit['总资产'], cjhb_reslut['成交金额'], fee, QueryEnd['总资产'], 0.01],
                ['-', '-', '-', '>'], ['原总资产', '成交金额', '费用', '现总资产'], '%f'],
        '证券资产': [[QueryInit['证券资产'], QueryEnd['证券资产']],
                 ['!='], ['原证券资产', '现证券资产'], '%f'],
        '预扣资金': [[QueryInit['预扣资金'], Prefreezing, QueryEnd['预扣资金'], 0.01],
                 ['+', '-', '>'], ['原预扣资金', '预扣资金', '现预扣资金'], '%f'],
        '买入资金': [[QueryInit['买入资金'], cjhb_reslut['成交金额'], QueryEnd['买入资金'], 0.01],
                 ['+', '-', '>'], ['原买入资金', '成交金额', '现买入资金'], '%f'],
        '买入费用': [[QueryInit['买入费用'], fee, QueryEnd['买入费用'], 0.01],
                 ['+', '-', '>'], ['原买入费用', '费用', '现买入费用'], '%f'],
        '卖出资金': [[QueryEnd['卖出资金'], QueryInit['卖出资金']],
                 ['!='], ['现卖出资金', '原卖出资金'], '%f'],
        '卖出费用': [[QueryEnd['卖出费用'], QueryInit['卖出费用']],
                 ['!='], ['现卖出费用', '原卖出费用'], '%f'],
        '冻结保证金': [[QueryInit['冻结保证金'], margin, QueryEnd['冻结保证金'], 0.01],
                  ['-', '-', '>'], ['原冻结保证金', '冻结保证金', '现冻结保证金'], '%f'],
        '行权冻结资金': [[QueryInit['行权冻结资金'], QueryEnd['行权冻结资金']],
                   ['!='], ['原行权冻结资金', '现行权冻结资金'], '%f'],
        '行权费用': [[QueryInit['行权费用'], QueryEnd['行权费用']],
                 ['!='], ['原行权费用', '现行权费用'], '%f'],
        '垫付资金': [[QueryInit['垫付资金'], QueryEnd['垫付资金']],
                 ['!='], ['原垫付资金', '现垫付资金'], '%f'],
        '预垫付资金': [[QueryInit['预垫付资金'], QueryEnd['预垫付资金']],
                  ['!='], ['原预垫付资金', '现预垫付资金'], '%f'],
        '昨日余额': [[QueryInit['昨日余额'], QueryEnd['昨日余额']],
                 ['!='], ['原昨日余额', '现昨日余额'], '%f'],
        '当前余额': [[QueryInit['当前余额'], QueryEnd['当前余额']],
                 ['!='], ['原当前余额', '现当前余额'], '%f'],
        '当天出入金': [[QueryInit['当天出入金'], QueryEnd['当天出入金']],
                  ['!='], ['原当天出入金', '现当天出入金'], '%f'],
        '当日交易资金扎差': [[QueryEnd['当日交易资金扎差'], cjhb_reslut['成交金额'], fee, QueryInit['当日交易资金扎差'], 0.01],
                     ['+', '+', '-', '>'], ['现当日交易资金扎差', '成交金额', '费用', '原当日交易资金扎差'], '%f'],
        '资金资产': [[QueryInit['资金资产'], cjhb_reslut['成交金额'], fee, QueryEnd['资金资产'], 0.01],
                 ['-', '-', '-', '>'], ['原资金资产', '成交金额', '费用', '现资金资产'], '%f'],
        '证券代码': [[QueryInit['证券代码'], QueryEnd['证券代码']],
                 ['!='], ['原证券代码', '现证券代码'], '%s'],
        '市场': [[market_init, market_end],
               ['!='], ['原市场', '现市场'], '%s'],
        '拥股数量': [[QueryInit['拥股数量'], cjhb_reslut['成交数量'], QueryEnd['拥股数量'], 0],
                 ['-', '-', '>'], ['原拥股数量', '成交数量', '现拥股数量'], '%d'],
        '可用股份数': [[QueryInit['可用股份数'], wt_reqs['quantity'], QueryEnd['可用股份数'], 0],
                  ['-', '-', '>'], ['原可用股份数', '委托数量', '现可用股份数'], '%d'],
        '持仓成本': [[QueryInit['持仓成本'], QueryEnd['持仓成本']],
                 ['!='], ['原持仓成本', '现持仓成本'], '%f'],
        '浮动盈亏': [[QueryInit['浮动盈亏'], QueryEnd['浮动盈亏']],
                 ['!='], ['原浮动盈亏', '现浮动盈亏'], '%f'],
        '昨日持仓': [[QueryInit['昨日持仓'], QueryEnd['昨日持仓']],
                 ['!='], ['原昨日持仓', '现昨日持仓'], '%d'],
        '今日可申购赎回持仓': [[QueryInit['今日可申购赎回持仓'], QueryEnd['今日可申购赎回持仓']],
                      ['!='], ['原今日可申购赎回持仓', '现今日可申购赎回持仓'], '%d'],
        # #'持仓方向' TODO
        '可行权合约': [[QueryInit['可行权合约'], QueryEnd['可行权合约']],
                  ['!='], ['原可行权合约', '现可行权合约'], '%d'],
        '可锁定标的': [[QueryInit['可锁定标的'], QueryEnd['可锁定标的']],
                  ['!='], ['原可锁定标的', '现可锁定标的'], '%d'],
        '可行权标的': [[QueryInit['可行权标的'], QueryEnd['可行权标的']],
                  ['!='], ['原可行权标的', '现可行权标的'], '%d'],
        '已锁定标的': [[QueryInit['已锁定标的'], QueryEnd['已锁定标的']],
                  ['!='], ['原已锁定标的', '现已锁定标的'], '%d'],
        '可用已锁定标的': [[QueryInit['可用已锁定标的'], QueryEnd['可用已锁定标的']],
                    ['!='], ['原可用已锁定标的', '现可用已锁定标的'], '%d'],
    }

    check_fund_stk_cjhb(check_item)

#--卖平--全部成交--费用持仓检查----------------------
def CJHB_QC_S_CLOSE(QueryInit, QueryEnd, wt_reqs):
    logger.info('成交回报－卖－全部成交－费用持仓检查')

    fee = get_fee(cjhb_reslut['成交数量'], wt_reqs)

    market_type = Api.const.XTP_MARKET_TYPE
    market_init = 2 if QueryInit['市场'] == market_type['XTP_MKT_SZ_A'] else 1
    market_end = 2 if QueryEnd['市场'] == market_type['XTP_MKT_SZ_A'] else 1

    check_item = {
        '可用资金': [[QueryInit['可用资金'], cjhb_reslut['成交金额'], fee, QueryEnd['可用资金'], 0.01],
                    ['+', '-', '-', '>'], ['原可用资金', '成交金额', '费用', '现可用资金'], '%f'],
        '总资产': [[QueryInit['总资产'], cjhb_reslut['成交金额'], fee, QueryEnd['总资产'], 0.01],
                    ['+', '-', '-', '>'], ['原总资产', '成交金额', '费用', '现总资产'], '%f'],
        '证券资产': [[QueryInit['证券资产'], QueryEnd['证券资产']],
                    ['!='], ['原证券资产', '现证券资产'], '%f'],
        '预扣资金': [[QueryInit['预扣资金'], QueryEnd['预扣资金']],
                    ['!='], ['原预扣资金', '现预扣资金'], '%f'],
        '买入资金': [[QueryInit['买入资金'], QueryEnd['买入资金']],
                    ['!='], ['原买入资金', '现买入资金'], '%f'],
        '买入费用': [[QueryInit['买入费用'], QueryEnd['买入费用']],
                    ['!='], ['原买入费用', '现买入费用'], '%f'],
        '卖出资金': [[QueryEnd['卖出资金'], cjhb_reslut['成交金额'], QueryInit['卖出资金'], 0.01],
                    ['-', '-', '>'], ['现卖出资金', '成交金额', '原卖出资金'], '%f'],
        '卖出费用': [[QueryEnd['卖出费用'], fee, QueryInit['卖出费用'], 0.01],
                    ['-', '-', '>'], ['现卖出费用', '费用', '原卖出费用'], '%f'],
        '冻结保证金': [[QueryInit['冻结保证金'], QueryEnd['冻结保证金']],
                    ['!='], ['原冻结保证金', '现冻结保证金'], '%f'],
        '行权冻结资金': [[QueryInit['行权冻结资金'], QueryEnd['行权冻结资金']],
                    ['!='], ['原行权冻结资金', '现行权冻结资金'], '%f'],
        '行权费用': [[QueryInit['行权费用'], QueryEnd['行权费用']],
                    ['!='], ['原行权费用', '现行权费用'], '%f'],
        '垫付资金': [[QueryInit['垫付资金'], QueryEnd['垫付资金']],
                    ['!='], ['原垫付资金', '现垫付资金'], '%f'],
        '预垫付资金': [[QueryInit['预垫付资金'], QueryEnd['预垫付资金']],
                    ['!='], ['原预垫付资金', '现预垫付资金'], '%f'],
        '昨日余额': [[QueryInit['昨日余额'], QueryEnd['昨日余额']],
                    ['!='], ['原昨日余额', '现昨日余额'], '%f'],
        '当前余额': [[QueryInit['当前余额'], QueryEnd['当前余额']],
                    ['!='], ['原当前余额', '现当前余额'], '%f'],
        '当天出入金': [[QueryInit['当天出入金'], QueryEnd['当天出入金']],
                    ['!='], ['原当天出入金', '现当天出入金'], '%f'],
        '当日交易资金扎差': [[QueryEnd['当日交易资金扎差'], cjhb_reslut['成交金额'], fee, QueryInit['当日交易资金扎差'], 0.01],
                    ['-', '+', '-', '>'], ['现当日交易资金扎差', '成交金额', '费用', '原当日交易资金扎差'], '%f'],
        '资金资产': [[QueryInit['资金资产'], cjhb_reslut['成交金额'], fee, QueryEnd['资金资产'], 0.01],
                    ['+', '-', '-', '>'], ['原资金资产', '成交金额', '费用', '现资金资产'], '%f'],
        '证券代码': [[QueryInit['证券代码'], QueryEnd['证券代码']],
                    ['!='], ['原证券代码', '现证券代码'], '%s'],
        '市场': [[market_init, market_end],
                    ['!='], ['原市场', '现市场'], '%s'],
        '拥股数量': [[QueryInit['拥股数量'], cjhb_reslut['成交数量'], QueryEnd['拥股数量'], 0],
                    ['-', '-', '>'], ['原拥股数量', '成交数量', '现拥股数量'], '%d'],
        '可用股份数': [[QueryInit['可用股份数'], cjhb_reslut['成交数量'], QueryEnd['可用股份数'], 0],
                    ['-', '-', '>'], ['原可用股份数', '成交数量', '现可用股份数'], '%d'],
        '持仓为0-持仓成本': [[QueryInit['持仓成本'], QueryEnd['持仓成本'], QueryEnd['可用股份数'], 0],
                      ['!=', ' and ', '!='], ['原持仓成本', '现持仓成本', '可用股份数'], '%f'],
        '持仓不为0-持仓成本': [[QueryEnd['持仓成本'], 0, QueryEnd['可用股份数'], 0],
                       ['!=', ' and ', '=='], ['现持仓成本', '实际持仓成本', '可用股份数'], '%f'],
        '浮动盈亏': [[QueryInit['浮动盈亏'], QueryEnd['浮动盈亏']],
                    ['!='], ['原浮动盈亏', '现浮动盈亏'], '%f'],
        '昨日持仓': [[QueryInit['昨日持仓'], QueryEnd['昨日持仓']],
                    ['!='], ['原昨日持仓', '现昨日持仓'], '%d'],
        '今日可申购赎回持仓': [[QueryInit['今日可申购赎回持仓'], QueryEnd['今日可申购赎回持仓']],
                    ['!='], ['原今日可申购赎回持仓', '现今日可申购赎回持仓'], '%d'],
        # #'持仓方向' TODO
        '可行权合约': [[QueryInit['可行权合约'], QueryEnd['可行权合约']],
                    ['!='], ['原可行权合约', '现可行权合约'], '%d'],
        '可锁定标的': [[QueryInit['可锁定标的'], QueryEnd['可锁定标的']],
                    ['!='], ['原可锁定标的', '现可锁定标的'], '%d'],
        '可行权标的': [[QueryInit['可行权标的'], QueryEnd['可行权标的']],
                    ['!='], ['原可行权标的', '现可行权标的'], '%d'],
        '已锁定标的': [[QueryInit['已锁定标的'], QueryEnd['已锁定标的']],
                    ['!='], ['原已锁定标的', '现已锁定标的'], '%d'],
        '可用已锁定标的': [[QueryInit['可用已锁定标的'], QueryEnd['可用已锁定标的']],
                    ['!='], ['原可用已锁定标的', '现可用已锁定标的'], '%d'],
    }

    check_fund_stk_cjhb(check_item)

#--卖开--全部成交--费用持仓检查----------------------
def CJHB_QC_S_OPEN(QueryInit, QueryEnd, wt_reqs):
    logger.info('成交回报－卖开－全部成交－费用持仓检查')

    fee = get_fee(wt_reqs['quantity'], wt_reqs)

    # 获取合约单位和认购认沽类型
    rs = QueryTable('xtp_opt_cntrt_info_' + today, ['cntrt_mul_unit', 'call_or_put'],
                    {'cntrt_id': wt_reqs['ticker']}, 2)

    # 保证金计算
    if rs['call_or_put'] == 'C':
        margin = cal_margin_call(wt_reqs['ticker'], cjhb_reslut['成交数量'], QueryInit['昨日持仓'])
    else:
        margin = cal_margin_put(wt_reqs['ticker'], cjhb_reslut['成交数量'], QueryInit['昨日持仓'])

    #--计算期待持仓成本
    price_avg = (QueryInit['持仓成本'] * QueryInit['拥股数量'] * rs['cntrt_mul_unit'] - cjhb_reslut['成交金额'])/\
                ((QueryInit['拥股数量'] + cjhb_reslut['成交数量']) * rs['cntrt_mul_unit'])

    market_type = Api.const.XTP_MARKET_TYPE
    market_init = 2 if QueryInit['市场'] == market_type['XTP_MKT_SZ_A'] else 1
    market_end = 2 if QueryEnd['市场'] == market_type['XTP_MKT_SZ_A'] else 1

    check_item = {
        '可用资金': [[QueryEnd['可用资金'], cjhb_reslut['成交金额'], fee, margin, QueryInit['可用资金'], 0.01],
                    ['-', '+', '+', '-', '>'], ['现可用资金', '成交金额', '费用', '冻结保证金', '原可用资金'], '%f'],
        '总资产': [[QueryEnd['总资产'], cjhb_reslut['成交金额'], fee, QueryInit['总资产'],  0.01],
                    ['-', '+', '-', '>'], ['现总资产', '成交金额', '费用', '原总资产'], '%f'],
        '证券资产': [[QueryInit['证券资产'], QueryEnd['证券资产']],
                    ['!='], ['原证券资产', '现证券资产'], '%f'],
        '预扣资金': [[QueryInit['预扣资金'], QueryEnd['预扣资金']],
                    ['!='], ['原预扣资金', '现预扣资金'], '%f'],
        '买入资金': [[QueryInit['买入资金'], QueryEnd['买入资金']],
                    ['!='], ['原买入资金', '现买入资金'], '%f'],
        '买入费用': [[QueryInit['买入费用'], QueryEnd['买入费用']],
                    ['!='], ['原买入费用', '现买入费用'], '%f'],
        '卖出资金': [[QueryEnd['卖出资金'], cjhb_reslut['成交金额'], QueryInit['卖出资金'], 0.01],
                    ['-', '-', '>'], ['现卖出资金', '成交金额', '原卖出资金'], '%f'],
        '卖出费用': [[QueryEnd['卖出费用'], fee, QueryInit['卖出费用'], 0.01],
                    ['-', '-', '>'], ['现卖出费用', '原卖出费用'], '%f'],
        '冻结保证金': [[QueryEnd['冻结保证金'], margin, QueryInit['冻结保证金'], 0.01],
                    ['-', '-', '>'], ['现冻结保证金', '冻结保证金', '原冻结保证金'], '%f'],
        '行权冻结资金': [[QueryInit['行权冻结资金'], QueryEnd['行权冻结资金']],
                    ['!='], ['原行权冻结资金', '现行权冻结资金'], '%f'],
        '行权费用': [[QueryInit['行权费用'], QueryEnd['行权费用']],
                    ['!='], ['原行权费用', '现行权费用'], '%f'],
        '垫付资金': [[QueryInit['垫付资金'], QueryEnd['垫付资金']],
                    ['!='], ['原垫付资金', '现垫付资金'], '%f'],
        '预垫付资金': [[QueryInit['预垫付资金'], QueryEnd['预垫付资金']],
                    ['!='], ['原预垫付资金', '现预垫付资金'], '%f'],
        '昨日余额': [[QueryInit['昨日余额'], QueryEnd['昨日余额']],
                    ['!='], ['原昨日余额', '现昨日余额'], '%f'],
        '当前余额': [[QueryInit['当前余额'], QueryEnd['当前余额']],
                    ['!='], ['原当前余额', '现当前余额'], '%f'],
        '当天出入金': [[QueryInit['当天出入金'], QueryEnd['当天出入金']],
                    ['!='], ['原当天出入金', '现当天出入金'], '%f'],
        '当日交易资金扎差': [[QueryEnd['当日交易资金扎差'], fee, cjhb_reslut['成交金额'], QueryInit['当日交易资金扎差'], 0.01],
                    ['+', '-', '-', '>'], ['现当日交易资金扎差', '费用', '成交金额', '原当日交易资金扎差'], '%f'],
        '资金资产': [[QueryEnd['资金资产'], cjhb_reslut['成交金额'], fee, QueryInit['资金资产'], 0.01],
                    ['-', '+', '-', '>'], ['现资金资产', '成交金额', '费用', '原资金资产'], '%f'],
        '证券代码': [[QueryInit['证券代码'], QueryEnd['证券代码']],
                    ['!='], ['原证券代码', '现证券代码'], '%s'],
        '市场': [[market_init, market_end],
                    ['!='], ['原市场', '现市场'], '%s'],
        '拥股数量': [[QueryEnd['拥股数量'], cjhb_reslut['成交数量'], QueryInit['拥股数量'], 0],
                    ['-', '-', '>'], ['现拥股数量', '成交数量', '原拥股数量'], '%d'],
        '可用股份数': [[QueryEnd['可用股份数'], cjhb_reslut['成交数量'], QueryInit['可用股份数'], 0],
                    ['-', '-', '>'], ['现可用股份数', '成交数量', '原可用股份数'], '%d'],
        '持仓成本': [[abs(price_avg), abs(QueryEnd['持仓成本']), 0.0001],
                    ['-', '>'], ['期待持仓成本', '实际持仓成本'], '%f'],
        '浮动盈亏': [[QueryInit['浮动盈亏'], QueryEnd['浮动盈亏']],
                    ['!='], ['原浮动盈亏', '现浮动盈亏'], '%f'],
        '昨日持仓': [[QueryInit['昨日持仓'], QueryEnd['昨日持仓']],
                    ['!='], ['原昨日持仓', '现昨日持仓'], '%d'],
        '今日可申购赎回持仓': [[QueryInit['今日可申购赎回持仓'], QueryEnd['今日可申购赎回持仓']],
                    ['!='], ['原今日可申购赎回持仓', '现今日可申购赎回持仓'], '%d'],
        # #'持仓方向' TODO
        '可行权合约': [[QueryInit['可行权合约'], QueryEnd['可行权合约']],
                    ['!='], ['原可行权合约', '现可行权合约'], '%d'],
        '可锁定标的': [[QueryInit['可锁定标的'], QueryEnd['可锁定标的']],
                    ['!='], ['原可锁定标的', '现可锁定标的'], '%d'],
        '可行权标的': [[QueryInit['可行权标的'], QueryEnd['可行权标的']],
                    ['!='], ['原可行权标的', '现可行权标的'], '%d'],
        '已锁定标的': [[QueryInit['已锁定标的'], QueryEnd['已锁定标的']],
                    ['!='], ['原已锁定标的', '现已锁定标的'], '%d'],
        '可用已锁定标的': [[QueryInit['可用已锁定标的'], QueryEnd['可用已锁定标的']],
                    ['!='], ['原可用已锁定标的', '现可用已锁定标的'], '%d'],
    }

    check_fund_stk_cjhb(check_item)

#--卖开--部分成交--费用持仓检查－－－－－－－－－－
def CJHB_BC_S_OPEN(QueryInit, wt_reqs, QueryEnd):
    logger.info('成交回报－卖开－部成－费用持仓检查')

    # 获取合约单位
    rs = QueryTable('xtp_opt_cntrt_info_' + today, ['cntrt_mul_unit', 'call_or_put'],
                    {'cntrt_id': wt_reqs['ticker']}, 2)

    # 保证金计算
    if rs['call_or_put'] == 'C':
        margin = cal_margin_call(wt_reqs['ticker'], cjhb_reslut['成交数量'], QueryInit['昨日持仓'])
    else:
        margin = cal_margin_put(wt_reqs['ticker'], cjhb_reslut['成交数量'], QueryInit['昨日持仓'])

    #--计算期待持仓成本
    price_avg = (QueryInit['持仓成本'] * QueryInit['拥股数量'] * rs['cntrt_mul_unit'] - cjhb_reslut['成交金额'])/\
                ((QueryInit['拥股数量'] + cjhb_reslut['成交数量']) * rs['cntrt_mul_unit'])

    # ----计算费用
    fee = get_fee(cjhb_reslut['成交数量'], wt_reqs)

    market_type = Api.const.XTP_MARKET_TYPE
    market_init = 2 if QueryInit['市场'] == market_type['XTP_MKT_SZ_A'] else 1
    market_end = 2 if QueryEnd['市场'] == market_type['XTP_MKT_SZ_A'] else 1

    if wt_reqs['price_type'] == Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT']:
        wt_price = wt_reqs['price']
    else:
        wt_price = getDownPrice(wt_reqs['ticker'])

    # 预扣资金
    Prefreezing = margin + get_fee(wt_reqs['quantity'] - cjhb_reslut['成交数量'], wt_reqs) - \
                  wt_price * (wt_reqs['quantity'] - cjhb_reslut['成交数量']) * rs['cntrt_mul_unit']
    Prefreezing = Prefreezing if Prefreezing > 0 else 0

    check_item = {
        '可用资金': [[QueryInit['可用资金'], margin, Prefreezing, cjhb_reslut['成交金额'], fee, QueryEnd['可用资金'], 0.01],
                 ['-', '-', '+', '-', '-', '>'], ['原可用资金', '冻结保证金','预扣资金', '成交金额', '费用', '现可用资金'], '%f'],
        '总资产': [[QueryInit['总资产'], cjhb_reslut['成交金额'], fee, QueryEnd['总资产'], 0.01],
                ['+', '-', '-', '>'], ['原总资产', '成交金额', '费用', '现总资产'], '%f'],
        '证券资产': [[QueryInit['证券资产'], QueryEnd['证券资产']],
                 ['!='], ['原证券资产', '现证券资产'], '%f'],
        '预扣资金': [[QueryInit['预扣资金'], Prefreezing, QueryEnd['预扣资金'], 0.01],
                 ['+', '-', '>'], ['原预扣资金', '冻结资金', '现预扣资金'], '%f'],
        '买入资金': [[QueryInit['买入资金'], QueryEnd['买入资金']],
                 ['!='], ['原买入资金', '现买入资金'], '%f'],
        '买入费用': [[QueryInit['买入费用'], QueryEnd['买入费用']],
                 ['!='], ['原买入费用', '现买入费用'], '%f'],
        '卖出资金': [[QueryEnd['卖出资金'], cjhb_reslut['成交金额'], QueryInit['卖出资金'], 0.01],
                 ['-', '-', '>'], ['现卖出资金', '成交金额', '原卖出资金'], '%f'],
        '卖出费用': [[QueryEnd['卖出费用'], fee, QueryInit['卖出费用'], 0.01],
                 ['-', '-', '>'], ['现卖出费用', '费用', '原卖出费用'], '%f'],
        '冻结保证金': [[QueryInit['冻结保证金'], margin, QueryEnd['冻结保证金'], 0.01],
                  ['+', '-', '>'], ['原冻结保证金', '冻结保证金', '现冻结保证金'], '%f'],
        '行权冻结资金': [[QueryInit['行权冻结资金'], QueryEnd['行权冻结资金']],
                   ['!='], ['原行权冻结资金', '现行权冻结资金'], '%f'],
        '行权费用': [[QueryInit['行权费用'], QueryEnd['行权费用']],
                 ['!='], ['原行权费用', '现行权费用'], '%f'],
        '垫付资金': [[QueryInit['垫付资金'], QueryEnd['垫付资金']],
                 ['!='], ['原垫付资金', '现垫付资金'], '%f'],
        '预垫付资金': [[QueryInit['预垫付资金'], QueryEnd['预垫付资金']],
                  ['!='], ['原预垫付资金', '现预垫付资金'], '%f'],
        '昨日余额': [[QueryInit['昨日余额'], QueryEnd['昨日余额']],
                 ['!='], ['原昨日余额', '现昨日余额'], '%f'],
        '当前余额': [[QueryInit['当前余额'], QueryEnd['当前余额']],
                 ['!='], ['原当前余额', '现当前余额'], '%f'],
        '当天出入金': [[QueryInit['当天出入金'], QueryEnd['当天出入金']],
                  ['!='], ['原当天出入金', '现当天出入金'], '%f'],
        '当日交易资金扎差': [[QueryEnd['当日交易资金扎差'], cjhb_reslut['成交金额'], fee, QueryInit['当日交易资金扎差'], 0.01],
                     ['-', '+', '-', '>'], ['现当日交易资金扎差', '成交金额', '费用', '原当日交易资金扎差'], '%f'],
        '资金资产': [[QueryInit['资金资产'], cjhb_reslut['成交金额'], fee, QueryEnd['资金资产'], 0.01],
                 ['+', '-', '-', '>'], ['原资金资产', '成交金额', '费用', '现资金资产'], '%f'],
        '证券代码': [[QueryInit['证券代码'], QueryEnd['证券代码']],
                 ['!='], ['原证券代码', '现证券代码'], '%s'],
        '市场': [[market_init, market_end],
               ['!='], ['原市场', '现市场'], '%s'],
        '拥股数量': [[QueryInit['拥股数量'], cjhb_reslut['成交数量'], QueryEnd['拥股数量'], 0],
                 ['+', '-', '>'], ['原拥股数量', '成交数量', '现拥股数量'], '%d'],
        '可用股份数': [[QueryInit['可用股份数'], cjhb_reslut['成交数量'], QueryEnd['可用股份数'], 0],
                  ['+', '-', '>'], ['原可用股份数', '成交数量', '现可用股份数'], '%d'],
        '持仓成本': [[abs(price_avg), abs(QueryEnd['持仓成本']), 0.0001],
                 ['-', '>'], ['期待持仓成本', '实际持仓成本'], '%f'],
        '浮动盈亏': [[QueryInit['浮动盈亏'], QueryEnd['浮动盈亏']],
                 ['!='], ['原浮动盈亏', '现浮动盈亏'], '%f'],
        '昨日持仓': [[QueryInit['昨日持仓'], QueryEnd['昨日持仓']],
                 ['!='], ['原昨日持仓', '现昨日持仓'], '%d'],
        '今日可申购赎回持仓': [[QueryInit['今日可申购赎回持仓'], QueryEnd['今日可申购赎回持仓']],
                      ['!='], ['原今日可申购赎回持仓', '现今日可申购赎回持仓'], '%d'],
        # #'持仓方向' TODO
        '可行权合约': [[QueryInit['可行权合约'], QueryEnd['可行权合约']],
                  ['!='], ['原可行权合约', '现可行权合约'], '%d'],
        '可锁定标的': [[QueryInit['可锁定标的'], QueryEnd['可锁定标的']],
                  ['!='], ['原可锁定标的', '现可锁定标的'], '%d'],
        '可行权标的': [[QueryInit['可行权标的'], QueryEnd['可行权标的']],
                  ['!='], ['原可行权标的', '现可行权标的'], '%d'],
        '已锁定标的': [[QueryInit['已锁定标的'], QueryEnd['已锁定标的']],
                  ['!='], ['原已锁定标的', '现已锁定标的'], '%d'],
        '可用已锁定标的': [[QueryInit['可用已锁定标的'], QueryEnd['可用已锁定标的']],
                    ['!='], ['原可用已锁定标的', '现可用已锁定标的'], '%d'],
    }

    check_fund_stk_cjhb(check_item)

#--卖平--部分成交--费用持仓检查－－－－－－－－－－
def CJHB_BC_S_CLOSE(QueryInit, wt_reqs, QueryEnd, Prefreezing):
    logger.info('成交回报－卖平－部成－费用持仓检查')

    # ----计算费用
    fee = get_fee(cjhb_reslut['成交数量'], wt_reqs)

    market_type = Api.const.XTP_MARKET_TYPE
    market_init = 2 if QueryInit['市场'] == market_type['XTP_MKT_SZ_A'] else 1
    market_end = 2 if QueryEnd['市场'] == market_type['XTP_MKT_SZ_A'] else 1

    check_item = {
        '可用资金': [[QueryInit['可用资金'], cjhb_reslut['成交金额'], fee, Prefreezing, QueryEnd['可用资金'], 0.01],
                 ['+', '-', '-', '-', '>'], ['原可用资金', '成交金额', '费用', '预扣资金', '现可用资金'], '%f'],
        '总资产': [[QueryInit['总资产'], cjhb_reslut['成交金额'], fee, QueryEnd['总资产'], 0.01],
                ['+', '-', '-', '>'], ['原总资产', '成交金额', '费用', '现总资产'], '%f'],
        '证券资产': [[QueryInit['证券资产'], QueryEnd['证券资产']],
                 ['!='], ['原证券资产', '现证券资产'], '%f'],
        '预扣资金': [[QueryInit['预扣资金'], Prefreezing, QueryEnd['预扣资金'], 0.01],
                 ['+', '-', '>'], ['原预扣资金', '预扣资金', '现预扣资金'], '%f'],
        '买入资金': [[QueryInit['买入资金'], QueryEnd['买入资金']],
                 ['!='], ['原买入资金', '现买入资金'], '%f'],
        '买入费用': [[QueryInit['买入费用'], QueryEnd['买入费用']],
                 ['!='], ['原买入费用', '现买入费用'], '%f'],
        '卖出资金': [[QueryEnd['卖出资金'], cjhb_reslut['成交金额'], QueryInit['卖出资金'], 0.01],
                 ['-', '-', '>'], ['现卖出资金', '成交金额', '原卖出资金'], '%f'],
        '卖出费用': [[QueryEnd['卖出费用'], fee, QueryInit['卖出费用'], 0.01],
                 ['-', '-', '>'], ['现卖出费用', '费用', '原卖出费用'], '%f'],
        '冻结保证金': [[QueryInit['冻结保证金'], QueryEnd['冻结保证金']],
                  ['!='], ['原冻结保证金', '现冻结保证金'], '%f'],
        '行权冻结资金': [[QueryInit['行权冻结资金'], QueryEnd['行权冻结资金']],
                   ['!='], ['原行权冻结资金', '现行权冻结资金'], '%f'],
        '行权费用': [[QueryInit['行权费用'], QueryEnd['行权费用']],
                 ['!='], ['原行权费用', '现行权费用'], '%f'],
        '垫付资金': [[QueryInit['垫付资金'], QueryEnd['垫付资金']],
                 ['!='], ['原垫付资金', '现垫付资金'], '%f'],
        '预垫付资金': [[QueryInit['预垫付资金'], QueryEnd['预垫付资金']],
                  ['!='], ['原预垫付资金', '现预垫付资金'], '%f'],
        '昨日余额': [[QueryInit['昨日余额'], QueryEnd['昨日余额']],
                 ['!='], ['原昨日余额', '现昨日余额'], '%f'],
        '当前余额': [[QueryInit['当前余额'], QueryEnd['当前余额']],
                 ['!='], ['原当前余额', '现当前余额'], '%f'],
        '当天出入金': [[QueryInit['当天出入金'], QueryEnd['当天出入金']],
                  ['!='], ['原当天出入金', '现当天出入金'], '%f'],
        '当日交易资金扎差': [[QueryEnd['当日交易资金扎差'], cjhb_reslut['成交金额'], fee, QueryInit['当日交易资金扎差'], 0.01],
                     ['-', '+', '-', '>'], ['现当日交易资金扎差', '成交金额', '费用', '原当日交易资金扎差'], '%f'],
        '资金资产': [[QueryInit['资金资产'], cjhb_reslut['成交金额'], fee, QueryEnd['资金资产'], 0.01],
                 ['+', '-', '-', '>'], ['原资金资产', '成交金额', '费用', '现资金资产'], '%f'],
        '证券代码': [[QueryInit['证券代码'], QueryEnd['证券代码']],
                 ['!='], ['原证券代码', '现证券代码'], '%s'],
        '市场': [[market_init, market_end],
               ['!='], ['原市场', '现市场'], '%s'],
        '拥股数量': [[QueryInit['拥股数量'], cjhb_reslut['成交数量'], QueryEnd['拥股数量'], 0],
                 ['-', '-', '>'], ['原拥股数量', '成交数量', '现拥股数量'], '%d'],
        '可用股份数': [[QueryInit['可用股份数'], wt_reqs['quantity'], QueryEnd['可用股份数'], 0],
                  ['-', '-', '>'], ['原可用股份数', '委托数量', '现可用股份数'], '%d'],
        '持仓成本': [[QueryInit['持仓成本'], QueryEnd['持仓成本']],
                 ['!='], ['原持仓成本', '现持仓成本'], '%f'],
        '浮动盈亏': [[QueryInit['浮动盈亏'], QueryEnd['浮动盈亏']],
                 ['!='], ['原浮动盈亏', '现浮动盈亏'], '%f'],
        '昨日持仓': [[QueryInit['昨日持仓'], QueryEnd['昨日持仓']],
                 ['!='], ['原昨日持仓', '现昨日持仓'], '%d'],
        '今日可申购赎回持仓': [[QueryInit['今日可申购赎回持仓'], QueryEnd['今日可申购赎回持仓']],
                      ['!='], ['原今日可申购赎回持仓', '现今日可申购赎回持仓'], '%d'],
        # #'持仓方向' TODO
        '可行权合约': [[QueryInit['可行权合约'], QueryEnd['可行权合约']],
                  ['!='], ['原可行权合约', '现可行权合约'], '%d'],
        '可锁定标的': [[QueryInit['可锁定标的'], QueryEnd['可锁定标的']],
                  ['!='], ['原可锁定标的', '现可锁定标的'], '%d'],
        '可行权标的': [[QueryInit['可行权标的'], QueryEnd['可行权标的']],
                  ['!='], ['原可行权标的', '现可行权标的'], '%d'],
        '已锁定标的': [[QueryInit['已锁定标的'], QueryEnd['已锁定标的']],
                  ['!='], ['原已锁定标的', '现已锁定标的'], '%d'],
        '可用已锁定标的': [[QueryInit['可用已锁定标的'], QueryEnd['可用已锁定标的']],
                    ['!='], ['原可用已锁定标的', '现可用已锁定标的'], '%d'],
    }

    check_fund_stk_cjhb(check_item)

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

def check_order(xtp_id, hb_data, wt_reqs, Api):

    if xtp_id == hb_data['order_xtp_id'] \
        and wt_reqs['market'] == hb_data['market'] \
            and wt_reqs['ticker'] == hb_data['ticker'] \
            and wt_reqs['side'] == hb_data['side'] \
            and checkDataPrice(Api, wt_reqs, hb_data['price']):
        return True
    else:
        return False

def get_fee(trade_qty, wt_reqs):
    #----计算费用
    SIDE_TYPE = Api.const.XTP_SIDE_TYPE
    POSITION_EFFECT_TYPE = Api.const.XTP_POSITION_EFFECT_TYPE
    BUSINESS_TYPE = Api.const.XTP_BUSINESS_TYPE

    if wt_reqs['business_type'] == BUSINESS_TYPE['XTP_BUSINESS_TYPE_OPTION']:
        if wt_reqs['side'] == SIDE_TYPE['XTP_SIDE_BUY'] \
            and wt_reqs['position_effect'] == POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_OPEN']:
            fee_rate = fee_rate_option_buy_open
        elif wt_reqs['side'] == SIDE_TYPE['XTP_SIDE_BUY'] \
            and wt_reqs['position_effect'] == POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_CLOSE']:
            fee_rate = fee_rate_option_buy_close
        elif wt_reqs['side'] == SIDE_TYPE['XTP_SIDE_SELL'] \
            and wt_reqs['position_effect'] == POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_OPEN']:
            fee_rate = fee_rate_option_sell_open
        elif wt_reqs['side'] == SIDE_TYPE['XTP_SIDE_SELL'] \
            and wt_reqs['position_effect'] == POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_CLOSE']:
            fee_rate = fee_rate_option_sell_close
        else:
            logger.error('错误的下单类型，买卖方向： %s，开平标志： %s！' % (
                str(wt_reqs['side']), str(wt_reqs['position_effect'])
            ))
            return
    elif wt_reqs['business_type'] == BUSINESS_TYPE['XTP_BUSINESS_TYPE_OPTION']:
        fee_rate = fee_rate_option_execute
    else:
        logger.error('错误的下单类型，业务类型： %s！' % (str(wt_reqs['business_type'])))
        return

    fee = trade_qty * fee_rate
    fee = float(Decimal(Decimal(str(fee)).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)))
    return fee

def check_fund_stk_cjhb(check_item):
    '''
    校验成交回报资金和持仓情况
    :param check_item: 校验的数字项和符号项
    :return:
    '''
    global cjhb_reslut

    if type(check_item) != dict:
        logger.error('参数类型错误，应传入dict类型的参数！')
    else:
        # current_quantity = 0
        for k, v in check_item.items():
            exp = ''
            for index, ele in enumerate(v[0]):
                ele = Decimal(ele)
                # 获取计算表达式
                exp += str(ele)
                if index < len(v[0]) - 1:
                    exp += v[1][index]
            # 若是>比较，加上abs
            if v[1][-1] == '>':
                exp = 'abs(' + exp[0:exp.find('>')] + ')' + exp[exp.find('>'):]

            # 校验每个资金和持仓项
            if eval(exp):
                fund_item = v[0][0:len(v[2])]
                print_item_temp = [k]
                print_item_temp.extend(v[2])
                print_item_temp.extend(fund_item)
                print_item = tuple(print_item_temp)
                num_type = ((v[3] + ',') * len(v[2]))[0:-1]
                str_type = ('%s,' * len(v[2]))[0:-1]
                logger.error(('%s错误，' + str_type + '分别为' + num_type) % print_item)
                cjhb_reslut['成交回报检查状态'] = 'end'
                cjhb_reslut['测试结果'] = False

                err_info = {}
                for index, ele in enumerate(v[2]):
                    err_info[ele] = v[0][index]
                cjhb_reslut['测试错误原因'] = [k + '错误', err_info]
                return

        logger.info('成交回报_业务校验正确！')
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = True


