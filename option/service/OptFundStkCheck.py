#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
import json
import time
import decimal
sys.path.append("/home/yhl2/workspace/xtp_test/service")
import ServiceConfig
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/option/mysql")
from OptGetUpOrDownPrice import *
from opt_database_manager import QueryTable
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtpapi import Api
from OptUtils import cal_margin_call
from OptUtils import cal_margin_put

reload(sys)
sys.setdefaultencoding('utf-8')

#注：部成和全成状态的校验写在了成交回报校验中
#注：初始未成交资金股份检查fundStkCheck_nomatch(Api,QueryInit,QueryEnd,wt_reqs)
#注：部撤资金股份检查fundStkCheck_partCancel(Api,QueryInit,QueryEnd,wt_reqs,data)
#注：'已撤'、'部撤已报'、'已报待撤'、'废单'、'撤废'资金股份检查fundStkCheck_other(QueryInit,QueryEnd)

#---定义费率，最低收费
fee_buy_open = ServiceConfig.FEE_RATE_OPTION_BUY_OPEN
fee_sell_close = ServiceConfig.FEE_RATE_OPTION_SELL_CLOSE
fee_sell_open = ServiceConfig.FEE_RATE_OPTION_SELL_OPEN
fee_buy_close = ServiceConfig.FEE_RATE_OPTION_BUY_CLOSE
fee_execute = ServiceConfig.FEE_RATE_OPTION_EXECUTE

today = time.strftime('%Y%m%d', time.localtime(time.time()))

#--持仓成本，保留小数位
avg_price_DecimalPlaces_option = ServiceConfig.AVG_PRICE_DECIMALPLACES_OPTION

#报单状态为'初始'、'未成交'，资金股份校验
def fundStkCheck_nomatch(Api,QueryInit,QueryEnd,wt_reqs,case_goal):
    logger.info('初始、未成交状态报单资金股份校验')
    fundStkCheck_reslut = {
        '检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
    }

    rs = nomatch_bs(Api, QueryInit, QueryEnd, wt_reqs)
    fundStkCheck_reslut['检查状态'] = rs['检查状态']
    fundStkCheck_reslut['测试结果'] = rs['测试结果']
    fundStkCheck_reslut['错误信息'] = rs['错误信息']
    return fundStkCheck_reslut

def nomatch_bs(Api,QueryInit,QueryEnd,wt_reqs):
    global fee_rate_buy,fee_min
    # 获取涨停价
    upPrice = getUpPrice(wt_reqs['ticker'])
    downPrice = getDownPrice(wt_reqs['ticker'])

    # 获取合约单位
    rs = QueryTable('xtp_opt_cntrt_info_' + today, ['cntrt_mul_unit', 'call_or_put', 'exercise_price'],
                    {'cntrt_id': wt_reqs['ticker']}, 2)

    # 行权
    if wt_reqs['business_type'] == Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_EXECUTE']:
        if rs['call_or_put'] == 'C':
            fee = wt_reqs['quantity'] * fee_execute
            Prefreezing = wt_reqs['quantity'] * (fee_execute + 
                rs['exercise_price'] / 10000.0 * rs['cntrt_mul_unit'])
        else:
            fee = fee_execute * wt_reqs['quantity']
            Prefreezing = fee
        momatch_rs = nomatch_exercise(QueryInit, QueryEnd, wt_reqs, Prefreezing, fee)
        return momatch_rs
    # 如果是买
    elif wt_reqs['side'] == Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY']:
        fee = fee_buy_open * wt_reqs['quantity']
        logger.info('fee=' + str(fee))
        if wt_reqs['price_type'] != Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT']:
            wt_reqs['price'] = upPrice

        if wt_reqs['position_effect'] == Api.const.XTP_POSITION_EFFECT_TYPE[
            'XTP_POSITION_EFFECT_OPEN']:
            Prefreezing = wt_reqs['quantity'] * wt_reqs['price'] * rs['cntrt_mul_unit'] + fee
            nomatch_rs = nomatch_b_open(QueryInit, QueryEnd, wt_reqs, Prefreezing, Api)
        else:
            # 计算保证金
            if rs['call_or_put'] == 'C':
                margin = cal_margin_call(wt_reqs['ticker'], wt_reqs['quantity'], QueryInit['昨日持仓'])
            else:
                margin = cal_margin_put(wt_reqs['ticker'], wt_reqs['quantity'], QueryInit['昨日持仓'])
            Prefreezing = wt_reqs['quantity'] * wt_reqs['price'] * rs['cntrt_mul_unit'] + fee - margin
            Prefreezing = Prefreezing if Prefreezing >= 0 else 0
            nomatch_rs = nomatch_b_close(QueryInit, QueryEnd, wt_reqs, Prefreezing, Api)
        return nomatch_rs
    # 如果是卖
    elif wt_reqs['side'] == Api.const.XTP_SIDE_TYPE['XTP_SIDE_SELL']:
        if wt_reqs['price_type'] == Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT']:
            wt_price = wt_reqs['price']
        else:
            wt_price = downPrice
        if wt_reqs['position_effect'] == Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_OPEN']:
            # 计算保证金
            if rs['call_or_put'] == 'C':
                margin = cal_margin_call(wt_reqs['ticker'], wt_reqs['quantity'], QueryInit['昨日持仓'])
            else:
                margin = cal_margin_put(wt_reqs['ticker'], wt_reqs['quantity'], QueryInit['昨日持仓'])

            trade_amount = wt_reqs['quantity'] * wt_price * rs['cntrt_mul_unit']
            Prefreezing = margin - trade_amount + fee_sell_open * wt_reqs['quantity']
            Prefreezing = Prefreezing if Prefreezing >= 0 else 0
            rs = nomatch_s_open(QueryInit, QueryEnd, wt_reqs, Prefreezing)
        else:
            Prefreezing = fee_sell_close * wt_reqs['quantity'] -  \
                          wt_reqs['quantity'] * wt_price * rs['cntrt_mul_unit']
            Prefreezing = Prefreezing if Prefreezing > 0 else 0
            rs = nomatch_s_close(QueryInit, QueryEnd, wt_reqs, Prefreezing)
        return rs

#报单状态为'部撤'，资金股份校验
def fundStkCheck_partCancel(Api,QueryInit, QueryEnd,wt_reqs,data):
    logger.info('部撤状态报单资金股份校验')
    fundStkCheck_reslut = {
        '检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
    }

    fee = fee_buy_open * data['qty_traded']

    # 如果是买
    if wt_reqs['side'] == Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY']:
        if wt_reqs['position_effect'] == Api.const.XTP_POSITION_EFFECT_TYPE[
            'XTP_POSITION_EFFECT_CLOSE']:
            rs = partCancel_b_close(QueryInit, QueryEnd, fee, data, wt_reqs)
        else:
            rs = partCancel_b_open(QueryInit, QueryEnd, fee, data, wt_reqs)
        fundStkCheck_reslut['检查状态'] = rs['检查状态']
        fundStkCheck_reslut['测试结果'] = rs['测试结果']
        fundStkCheck_reslut['错误信息'] = rs['错误信息']
    # 如果是卖
    elif wt_reqs['side'] == Api.const.XTP_SIDE_TYPE['XTP_SIDE_SELL']:
        logger.info('fee=' + str(fee))
        if wt_reqs['position_effect'] == Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_OPEN']:
            rs = partcancel_s_open(QueryInit, QueryEnd, fee, data, wt_reqs)
        else:
            rs = partCancel_S_CLOSE(QueryInit, QueryEnd, fee, data)
        fundStkCheck_reslut['检查状态'] = rs['检查状态']
        fundStkCheck_reslut['测试结果'] = rs['测试结果']
        fundStkCheck_reslut['错误信息'] = rs['错误信息']

    return fundStkCheck_reslut

#报单状态为'已撤'、'部撤已报'、'已报待撤'、'撤废'，资金股份校验（资金股份前后不变）
def fundStkCheck_other(QueryInit,QueryEnd):
    logger.info('已撤、部撤已报、已报待撤、撤废状态报单资金股份校验')
    market_type = Api.const.XTP_MARKET_TYPE
    market_init = 2 if QueryInit['市场'] == market_type['XTP_MKT_SZ_A'] else 1
    market_end = 2 if QueryEnd['市场'] == market_type['XTP_MKT_SZ_A'] else 1

    check_item = {
        '可用资金': [[QueryInit['可用资金'], QueryEnd['可用资金']],
                 ['!='], ['原可用资金', '现可用资金'], '%f'],
        '总资产': [[QueryInit['总资产'], QueryEnd['总资产']],
                ['!='], ['原总资产', '现总资产'], '%f'],
        '证券资产': [[QueryInit['证券资产'], QueryEnd['证券资产']],
                 ['!='], ['原证券资产', '现证券资产'], '%f'],
        '预扣资金': [[QueryInit['预扣资金'], QueryEnd['预扣资金']],
                 ['!='], ['原预扣资金', '现预扣资金'], '%f'],
        '买入资金': [[QueryInit['买入资金'], QueryEnd['买入资金']],
                 ['!='], ['原买入资金', '现买入资金'], '%f'],
        '买入费用': [[QueryInit['买入费用'], QueryEnd['买入费用']],
                 ['!='], ['原买入费用', '现买入费用'], '%f'],
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
        '当日交易资金扎差': [[QueryEnd['当日交易资金扎差'], QueryInit['当日交易资金扎差']],
                     ['!='], ['现当日交易资金扎差', '原当日交易资金扎差'], '%f'],
        '资金资产': [[QueryInit['资金资产'], QueryEnd['资金资产']],
                 ['!='], ['原资金资产', '现资金资产'], '%f'],
        '证券代码': [[QueryInit['证券代码'], QueryEnd['证券代码']],
                 ['!='], ['原证券代码', '现证券代码'], '%s'],
        '市场': [[market_init, market_end],
               ['!='], ['原市场', '现市场'], '%s'],
        '拥股数量': [[QueryInit['拥股数量'], QueryEnd['拥股数量']],
                 ['!='], ['原拥股数量', '现拥股数量'], '%d'],
        '可用股份数': [[QueryInit['可用股份数'], QueryEnd['可用股份数']],
                  ['!='], ['原可用股份数', '现可用股份数'], '%d'],
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

    rs = check_fund_stk_bdquery(check_item)
    return rs

# 未成交-认沽行权
def nomatch_exercise(QueryInit, QueryEnd, wt_reqs, Prefreezing, fee):
    market_type = Api.const.XTP_MARKET_TYPE
    market_init = 2 if QueryInit['市场'] == market_type['XTP_MKT_SZ_A'] else 1
    market_end = 2 if QueryEnd['市场'] == market_type['XTP_MKT_SZ_A'] else 1

    check_item = {
        '可用资金': [[QueryInit['可用资金'], Prefreezing, QueryEnd['可用资金'], 0.01],
                 ['-', '-', '>'], ['原可用资金', '冻结资金', '现可用资金'], '%f'],
        '总资产': [[QueryInit['总资产'], QueryEnd['总资产']],
                ['!='], ['原总资产', '现总资产'], '%f'],
        '证券资产': [[QueryInit['证券资产'], QueryEnd['证券资产']],
                 ['!='], ['原证券资产', '现证券资产'], '%f'],
        '预扣资金': [[QueryInit['预扣资金'], Prefreezing, QueryEnd['预扣资金'], 0.01],
                 ['+', '-', '>'], ['原预扣资金', '冻结资金', '现预扣资金'], '%f'],
        '买入资金': [[QueryInit['买入资金'], QueryEnd['买入资金']],
                 ['!='], ['原买入资金', '现买入资金'], '%f'],
        '买入费用': [[QueryInit['买入费用'], QueryEnd['买入费用']],
                 ['!='], ['原买入费用', '现买入费用'], '%f'],
        '卖出资金': [[QueryEnd['卖出资金'], QueryInit['卖出资金']],
                 ['!='], ['现卖出资金', '原卖出资金'], '%f'],
        '卖出费用': [[QueryEnd['卖出费用'], QueryInit['卖出费用']],
                 ['!='], ['现卖出费用', '原卖出费用'], '%f'],
        '冻结保证金': [[QueryInit['冻结保证金'], QueryEnd['冻结保证金']],
                  ['!='], ['原冻结保证金', '现冻结保证金'], '%f'],
        '行权冻结资金': [[QueryInit['行权冻结资金'], Prefreezing - fee, QueryEnd['行权冻结资金'], 0.01],
                   ['+', '-', '>'], ['原行权冻结资金', '行权冻结资金', '现行权冻结资金'], '%f'],
        '行权费用': [[QueryInit['行权费用'], fee, QueryEnd['行权费用'], 0.01],
                 ['+', '-', '>'], ['原行权费用', '行权费用', '现行权费用'], '%f'],
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
        '当日交易资金扎差': [[QueryEnd['当日交易资金扎差'], QueryInit['当日交易资金扎差']],
                     ['!='], ['现当日交易资金扎差', '原当日交易资金扎差'], '%f'],
        '资金资产': [[QueryInit['资金资产'], QueryEnd['资金资产']],
                 ['!='], ['原资金资产', '现资金资产'], '%f'],
        '证券代码': [[QueryInit['证券代码'], QueryEnd['证券代码']],
                 ['!='], ['原证券代码', '现证券代码'], '%s'],
        '市场': [[market_init, market_end],
               ['!='], ['原市场', '现市场'], '%s'],
        '拥股数量': [[QueryInit['拥股数量'], QueryEnd['拥股数量']],
                 ['!='], ['原拥股数量', '现拥股数量'], '%d'],
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
        '可行权合约': [[QueryInit['可行权合约'], wt_reqs['quantity'], QueryEnd['可行权合约'], 0],
                  ['-', '-', '>'], ['原可行权合约', '委托数量', '现可行权合约'], '%d'],
        '可锁定标的': [[QueryInit['可锁定标的'], QueryEnd['可锁定标的']],
                  ['!='], ['原可锁定标的', '现可锁定标的'], '%d'],
        '可行权标的': [[QueryInit['可行权标的'], QueryEnd['可行权标的']],
                  ['!='], ['原可行权标的', '现可行权标的'], '%d'],
        '已锁定标的': [[QueryInit['已锁定标的'], QueryEnd['已锁定标的']],
                  ['!='], ['原已锁定标的', '现已锁定标的'], '%d'],
        '可用已锁定标的': [[QueryInit['可用已锁定标的'], QueryEnd['可用已锁定标的']],
                    ['!='], ['原可用已锁定标的', '现可用已锁定标的'], '%d'],
    }

    rs = check_fund_stk_bdquery(check_item)
    return rs


# 未成交-买开
def nomatch_b_open(QueryInit,QueryEnd,wt_reqs,Prefreezing,Api):
    market_type = Api.const.XTP_MARKET_TYPE
    market_init = 2 if QueryInit['市场'] == market_type['XTP_MKT_SZ_A'] else 1
    market_end = 2 if QueryEnd['市场'] == market_type['XTP_MKT_SZ_A'] else 1

    check_item = {
        '可用资金': [[QueryInit['可用资金'], Prefreezing, QueryEnd['可用资金'], 0.01],
                 ['-', '-', '>'], ['原可用资金', '冻结资金', '现可用资金'], '%f'],
        '总资产': [[QueryInit['总资产'], QueryEnd['总资产']],
                ['!='], ['原总资产', '现总资产'], '%f'],
        '证券资产': [[QueryInit['证券资产'], QueryEnd['证券资产']],
                 ['!='], ['原证券资产', '现证券资产'], '%f'],
        '预扣资金': [[QueryInit['预扣资金'], Prefreezing, QueryEnd['预扣资金'], 0.01],
                 ['+', '-', '>'], ['原预扣资金', '冻结资金', '现预扣资金'], '%f'],
        '买入资金': [[QueryInit['买入资金'], QueryEnd['买入资金']],
                 ['!='], ['原买入资金', '现买入资金'], '%f'],
        '买入费用': [[QueryInit['买入费用'], QueryEnd['买入费用']],
                 ['!='], ['原买入费用', '现买入费用'], '%f'],
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
        '当日交易资金扎差': [[QueryEnd['当日交易资金扎差'], QueryInit['当日交易资金扎差']],
                     ['!='], ['现当日交易资金扎差', '原当日交易资金扎差'], '%f'],
        '资金资产': [[QueryInit['资金资产'], QueryEnd['资金资产']],
                 ['!='], ['原资金资产', '现资金资产'], '%f'],
        '证券代码': [[QueryInit['证券代码'], QueryEnd['证券代码']],
                 ['!='], ['原证券代码', '现证券代码'], '%s'],
        '市场': [[market_init, market_end],
               ['!='], ['原市场', '现市场'], '%s'],
        '拥股数量': [[QueryInit['拥股数量'], QueryEnd['拥股数量']],
                 ['!='], ['原拥股数量', '现拥股数量'], '%d'],
        '可用股份数': [[QueryInit['可用股份数'], QueryEnd['可用股份数']],
                  ['!='], ['原可用股份数', '现可用股份数'], '%d'],
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

    rs = check_fund_stk_bdquery(check_item)
    return rs

# 未成交-买平
def nomatch_b_close(QueryInit, QueryEnd, wt_reqs, Prefreezing, Api):
    market_type = Api.const.XTP_MARKET_TYPE
    market_init = 2 if QueryInit['市场'] == market_type['XTP_MKT_SZ_A'] else 1
    market_end = 2 if QueryEnd['市场'] == market_type['XTP_MKT_SZ_A'] else 1

    check_item = {
        '可用资金': [[QueryInit['可用资金'], Prefreezing, QueryEnd['可用资金'], 0.01],
                 ['-', '-', '>'], ['原可用资金', '冻结资金', '现可用资金'], '%f'],
        '总资产': [[QueryInit['总资产'], QueryEnd['总资产']],
                ['!='], ['原总资产', '现总资产'], '%f'],
        '证券资产': [[QueryInit['证券资产'], QueryEnd['证券资产']],
                 ['!='], ['原证券资产', '现证券资产'], '%f'],
        '预扣资金': [[QueryInit['预扣资金'], Prefreezing, QueryEnd['预扣资金'], 0.01],
                 ['+', '-', '>'], ['原预扣资金', '冻结资金', '现预扣资金'], '%f'],
        '买入资金': [[QueryInit['买入资金'], QueryEnd['买入资金']],
                 ['!='], ['原买入资金', '现买入资金'], '%f'],
        '买入费用': [[QueryInit['买入费用'], QueryEnd['买入费用']],
                 ['!='], ['原买入费用', '现买入费用'], '%f'],
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
        '当日交易资金扎差': [[QueryEnd['当日交易资金扎差'], QueryInit['当日交易资金扎差']],
                     ['!='], ['现当日交易资金扎差', '原当日交易资金扎差'], '%f'],
        '资金资产': [[QueryInit['资金资产'], QueryEnd['资金资产']],
                 ['!='], ['原资金资产', '现资金资产'], '%f'],
        '证券代码': [[QueryInit['证券代码'], QueryEnd['证券代码']],
                 ['!='], ['原证券代码', '现证券代码'], '%s'],
        '市场': [[market_init, market_end],
               ['!='], ['原市场', '现市场'], '%s'],
        '拥股数量': [[QueryInit['拥股数量'], QueryEnd['拥股数量']],
                 ['!='], ['原拥股数量', '现拥股数量'], '%d'],
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

    rs = check_fund_stk_bdquery(check_item)
    return rs

# 未成交-卖开
def nomatch_s_open(QueryInit, QueryEnd, wt_reqs, Prefreezing):
    market_type = Api.const.XTP_MARKET_TYPE
    market_init = 2 if QueryInit['市场'] == market_type['XTP_MKT_SZ_A'] else 1
    market_end = 2 if QueryEnd['市场'] == market_type['XTP_MKT_SZ_A'] else 1

    check_item = {
        '可用资金': [[QueryInit['可用资金'], Prefreezing, QueryEnd['可用资金'], 0.01],
                 ['-', '-', '>'], ['原可用资金', '冻结资金', '现可用资金'], '%f'],
        '总资产': [[QueryInit['总资产'], QueryEnd['总资产']],
                ['!='], ['原总资产', '现总资产'], '%f'],
        '证券资产': [[QueryInit['证券资产'], QueryEnd['证券资产']],
                 ['!='], ['原证券资产', '现证券资产'], '%f'],
        '预扣资金': [[QueryInit['预扣资金'], Prefreezing, QueryEnd['预扣资金'], 0.01],
                 ['+', '-', '>'], ['原预扣资金', '冻结资金', '现预扣资金'], '%f'],
        '买入资金': [[QueryInit['买入资金'], QueryEnd['买入资金']],
                 ['!='], ['原买入资金', '现买入资金'], '%f'],
        '买入费用': [[QueryInit['买入费用'], QueryEnd['买入费用']],
                 ['!='], ['原买入费用', '现买入费用'], '%f'],
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
        '当日交易资金扎差': [[QueryEnd['当日交易资金扎差'], QueryInit['当日交易资金扎差']],
                     ['!='], ['现当日交易资金扎差', '原当日交易资金扎差'], '%f'],
        '资金资产': [[QueryInit['资金资产'], QueryEnd['资金资产']],
                 ['!='], ['原资金资产', '现资金资产'], '%f'],
        '证券代码': [[QueryInit['证券代码'], QueryEnd['证券代码']],
                 ['!='], ['原证券代码', '现证券代码'], '%s'],
        '市场': [[market_init, market_end],
               ['!='], ['原市场', '现市场'], '%s'],
        '拥股数量': [[QueryInit['拥股数量'], QueryEnd['拥股数量']],
                 ['!='], ['原拥股数量', '现拥股数量'], '%d'],
        '可用股份数': [[QueryInit['可用股份数'], QueryEnd['可用股份数']],
                  ['!='], ['原可用股份数', '现可用股份数'], '%d'],
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

    rs = check_fund_stk_bdquery(check_item)
    return rs

# 未成交-卖平
def nomatch_s_close(QueryInit, QueryEnd, wt_reqs, Prefreezing):
    market_type = Api.const.XTP_MARKET_TYPE
    market_init = 2 if QueryInit['市场'] == market_type['XTP_MKT_SZ_A'] else 1
    market_end = 2 if QueryEnd['市场'] == market_type['XTP_MKT_SZ_A'] else 1

    check_item = {
        '可用资金': [[QueryInit['可用资金'], Prefreezing , QueryEnd['可用资金'], 0.01],
                 ['-', '-', '>'], ['原可用资金', '预扣资金', '现可用资金'], '%f'],
        '总资产': [[QueryInit['总资产'], QueryEnd['总资产']],
                ['!='], ['原总资产', '现总资产'], '%f'],
        '证券资产': [[QueryInit['证券资产'], QueryEnd['证券资产']],
                 ['!='], ['原证券资产', '现证券资产'], '%f'],
        '预扣资金': [[QueryInit['预扣资金'], Prefreezing, QueryEnd['预扣资金'], 0.01],
                 ['+', '-', '>'], ['原预扣资金', '预扣资金', '现预扣资金'], '%f'],
        '买入资金': [[QueryInit['买入资金'], QueryEnd['买入资金']],
                 ['!='], ['原买入资金', '现买入资金'], '%f'],
        '买入费用': [[QueryInit['买入费用'], QueryEnd['买入费用']],
                 ['!='], ['原买入费用', '现买入费用'], '%f'],
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
        '当日交易资金扎差': [[QueryEnd['当日交易资金扎差'], QueryInit['当日交易资金扎差']],
                     ['!='], ['现当日交易资金扎差', '原当日交易资金扎差'], '%f'],
        '资金资产': [[QueryInit['资金资产'], QueryEnd['资金资产']],
                 ['!='], ['原资金资产', '现资金资产'], '%f'],
        '证券代码': [[QueryInit['证券代码'], QueryEnd['证券代码']],
                 ['!='], ['原证券代码', '现证券代码'], '%s'],
        '市场': [[market_init, market_end],
               ['!='], ['原市场', '现市场'], '%s'],
        '拥股数量': [[QueryInit['拥股数量'], QueryEnd['拥股数量']],
                 ['!='], ['原拥股数量', '现拥股数量'], '%d'],
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

    rs = check_fund_stk_bdquery(check_item)
    return rs

# 部撤-买开
def partCancel_b_open(QueryInit, QueryEnd, fee, data, wt_reqs):
    market_type = Api.const.XTP_MARKET_TYPE
    market_init = 2 if QueryInit['市场'] == market_type['XTP_MKT_SZ_A'] else 1
    market_end = 2 if QueryEnd['市场'] == market_type['XTP_MKT_SZ_A'] else 1

    # 获取合约单位
    rs = QueryTable('xtp_opt_cntrt_info_' + today, ['cntrt_mul_unit', 'call_or_put'],
                    {'cntrt_id': wt_reqs['ticker']}, 2)

    # --计算期待持仓成本
    price_avg = ((QueryInit['持仓成本'] * QueryInit['拥股数量'] * rs['cntrt_mul_unit'] +
                  data['trade_amount']) + fee) / \
                ((QueryInit['拥股数量'] + data['qty_traded']) * rs['cntrt_mul_unit'])

    check_item = {
        '可用资金': [[QueryInit['可用资金'], data['trade_amount'], fee, QueryEnd['可用资金'], 0.01],
                 ['-', '-', '-', '>'], ['原可用资金', '成交金额', '费用', '现可用资金'], '%f'],
        '总资产': [[QueryInit['总资产'], data['trade_amount'], fee, QueryEnd['总资产'], 0.01],
                ['-', '-', '-', '>'], ['原总资产', '成交金额', '费用', '现总资产'], '%f'],
        '证券资产': [[QueryInit['证券资产'], QueryEnd['证券资产']],
                 ['!='], ['原证券资产', '现证券资产'], '%f'],
        '预扣资金': [[QueryInit['预扣资金'], QueryEnd['预扣资金']],
                 ['!='], ['原预扣资金', '现预扣资金'], '%f'],
        '买入资金': [[QueryInit['买入资金'], data['trade_amount'], QueryEnd['买入资金'], 0.01],
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
        '当日交易资金扎差': [[QueryEnd['当日交易资金扎差'], data['trade_amount'], fee, QueryInit['当日交易资金扎差'], 0.01],
                     ['+', '+', '-', '>'], ['现当日交易资金扎差', '成交金额', '费用', '原当日交易资金扎差'], '%f'],
        '资金资产': [[QueryInit['资金资产'], data['trade_amount'], fee, QueryEnd['资金资产'], 0.01],
                 ['-', '-', '-', '>'], ['原资金资产', '成交金额', '费用', '现资金资产'], '%f'],
        '证券代码': [[QueryInit['证券代码'], QueryEnd['证券代码']],
                 ['!='], ['原证券代码', '现证券代码'], '%s'],
        '市场': [[market_init, market_end],
               ['!='], ['原市场', '现市场'], '%s'],
        '拥股数量': [[QueryInit['拥股数量'], data['qty_traded'], QueryEnd['拥股数量'], 0],
                 ['+', '-', '>'], ['原拥股数量', '成交数量', '现拥股数量'], '%d'],
        '可用股份数': [[QueryInit['可用股份数'], data['qty_traded'], QueryEnd['可用股份数'], 0],
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

    rs = check_fund_stk_bdquery(check_item)
    return rs

# 部撤-买平
def partCancel_b_close(QueryInit, QueryEnd, fee, data, wt_reqs):
    # 获取合约单位
    rs = QueryTable('xtp_opt_cntrt_info_' + today, ['cntrt_mul_unit', 'call_or_put'],
                    {'cntrt_id': wt_reqs['ticker']}, 2)

    # 释放的保证金
    if rs['call_or_put'] == 'C':
        margin = cal_margin_call(wt_reqs['ticker'], data['qty_traded'], QueryInit['昨日持仓'])
    else:
        margin = cal_margin_put(wt_reqs['ticker'], data['qty_traded'], QueryInit['昨日持仓'])

    market_type = Api.const.XTP_MARKET_TYPE
    market_init = 2 if QueryInit['市场'] == market_type['XTP_MKT_SZ_A'] else 1
    market_end = 2 if QueryEnd['市场'] == market_type['XTP_MKT_SZ_A'] else 1

    check_item = {
        '可用资金': [[QueryInit['可用资金'], data['trade_amount'], fee, margin, QueryEnd['可用资金'], 0.01],
                 ['-', '-', '+', '-', '>'], ['原可用资金', '成交金额', '费用', '冻结保证金', '现可用资金'], '%f'],
        '总资产': [[QueryInit['总资产'], data['trade_amount'], fee, QueryEnd['总资产'], 0.01],
                ['-', '-', '-', '>'], ['原总资产', '成交金额', '费用', '现总资产'], '%f'],
        '证券资产': [[QueryInit['证券资产'], QueryEnd['证券资产']],
                 ['!='], ['原证券资产', '现证券资产'], '%f'],
        '预扣资金': [[QueryInit['预扣资金'], QueryEnd['预扣资金']],
                 ['!='], ['原预扣资金', '现预扣资金'], '%f'],
        '买入资金': [[QueryInit['买入资金'], data['trade_amount'], QueryEnd['买入资金'], 0.01],
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
        '当日交易资金扎差': [[QueryEnd['当日交易资金扎差'], data['trade_amount'], fee, QueryInit['当日交易资金扎差'], 0.01],
                     ['+', '+', '-', '>'], ['现当日交易资金扎差', '成交金额', '费用', '原当日交易资金扎差'], '%f'],
        '资金资产': [[QueryInit['资金资产'], data['trade_amount'], fee, QueryEnd['资金资产'], 0.01],
                 ['-', '-', '-', '>'], ['原资金资产', '成交金额', '费用', '现资金资产'], '%f'],
        '证券代码': [[QueryInit['证券代码'], QueryEnd['证券代码']],
                 ['!='], ['原证券代码', '现证券代码'], '%s'],
        '市场': [[market_init, market_end],
               ['!='], ['原市场', '现市场'], '%s'],
        '拥股数量': [[QueryInit['拥股数量'], data['qty_traded'], QueryEnd['拥股数量'], 0],
                 ['-', '-', '>'], ['原拥股数量', '成交数量', '现拥股数量'], '%d'],
        '可用股份数': [[QueryInit['可用股份数'], data['qty_traded'], QueryEnd['可用股份数'], 0],
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

    rs = check_fund_stk_bdquery(check_item)
    return rs

# 部撤-卖开
def partcancel_s_open(QueryInit, QueryEnd, fee, data, wt_reqs):
    market_type = Api.const.XTP_MARKET_TYPE
    market_init = 2 if QueryInit['市场'] == market_type['XTP_MKT_SZ_A'] else 1
    market_end = 2 if QueryEnd['市场'] == market_type['XTP_MKT_SZ_A'] else 1

    # 获取合约单位
    rs = QueryTable('xtp_opt_cntrt_info_' + today, ['cntrt_mul_unit', 'call_or_put'],
                    {'cntrt_id': wt_reqs['ticker']}, 2)

    #--计算期待持仓成本
    price_avg = (QueryInit['持仓成本'] * QueryInit['拥股数量'] * rs['cntrt_mul_unit'] - data['trade_amount'])/\
                ((QueryInit['拥股数量'] + data['qty_traded']) * rs['cntrt_mul_unit'])

    # 计算保证金
    if rs['call_or_put'] == 'C':
        margin = cal_margin_call(wt_reqs['ticker'], data['qty_traded'], QueryInit['昨日持仓'])
    else:
        margin = cal_margin_put(wt_reqs['ticker'], data['qty_traded'], QueryInit['昨日持仓'])

    check_item = {
        '可用资金': [[QueryInit['可用资金'], margin, data['trade_amount'], fee, QueryEnd['可用资金'], 0.01],
                 ['-', '+', '-', '-', '>'], ['原可用资金', '成交金额', '费用', '现可用资金'], '%f'],
        '总资产': [[QueryInit['总资产'], data['trade_amount'], fee, QueryEnd['总资产'], 0.01],
                ['+', '-', '-', '>'], ['原总资产', '成交金额', '费用', '现总资产'], '%f'],
        '证券资产': [[QueryInit['证券资产'], QueryEnd['证券资产']],
                 ['!='], ['原证券资产', '现证券资产'], '%f'],
        '预扣资金': [[QueryInit['预扣资金'], QueryEnd['预扣资金']],
                 ['!='], ['原预扣资金', '现预扣资金'], '%f'],
        '买入资金': [[QueryInit['买入资金'], QueryEnd['买入资金']],
                 ['!='], ['原买入资金', '现买入资金'], '%f'],
        '买入费用': [[QueryInit['买入费用'], QueryEnd['买入费用']],
                 ['!='], ['原买入费用', '现买入费用'], '%f'],
        '卖出资金': [[QueryEnd['卖出资金'], data['trade_amount'], QueryInit['卖出资金'], 0.01],
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
        '当日交易资金扎差': [[QueryEnd['当日交易资金扎差'], data['trade_amount'], fee, QueryInit['当日交易资金扎差'], 0.01],
                     ['-', '+', '-', '>'], ['现当日交易资金扎差', '成交金额', '费用', '原当日交易资金扎差'], '%f'],
        '资金资产': [[QueryInit['资金资产'], data['trade_amount'], fee, QueryEnd['资金资产'], 0.01],
                 ['+', '-', '-', '>'], ['原资金资产', '成交金额', '费用', '现资金资产'], '%f'],
        '证券代码': [[QueryInit['证券代码'], QueryEnd['证券代码']],
                 ['!='], ['原证券代码', '现证券代码'], '%s'],
        '市场': [[market_init, market_end],
               ['!='], ['原市场', '现市场'], '%s'],
        '拥股数量': [[QueryInit['拥股数量'], data['qty_traded'], QueryEnd['拥股数量'], 0],
                 ['+', '-', '>'], ['原拥股数量', '成交数量', '现拥股数量'], '%d'],
        '可用股份数': [[QueryInit['可用股份数'], data['qty_traded'], QueryEnd['可用股份数'], 0],
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

    rs = check_fund_stk_bdquery(check_item)
    return rs

# 部撤-卖平
def partCancel_S_CLOSE(QueryInit, QueryEnd, fee, data):
    market_type = Api.const.XTP_MARKET_TYPE
    market_init = 2 if QueryInit['市场'] == market_type['XTP_MKT_SZ_A'] else 1
    market_end = 2 if QueryEnd['市场'] == market_type['XTP_MKT_SZ_A'] else 1

    check_item = {
        '可用资金': [[QueryInit['可用资金'], data['trade_amount'], fee, QueryEnd['可用资金'], 0.01],
                 ['+', '-', '-', '>'], ['原可用资金', '成交金额', '费用', '现可用资金'], '%f'],
        '总资产': [[QueryInit['总资产'], data['trade_amount'], fee, QueryEnd['总资产'], 0.01],
                ['+', '-', '-', '>'], ['原总资产', '成交金额', '费用', '现总资产'], '%f'],
        '证券资产': [[QueryInit['证券资产'], QueryEnd['证券资产']],
                 ['!='], ['原证券资产', '现证券资产'], '%f'],
        '预扣资金': [[QueryInit['预扣资金'], QueryEnd['预扣资金']],
                 ['!='], ['原预扣资金', '现预扣资金'], '%f'],
        '买入资金': [[QueryInit['买入资金'], QueryEnd['买入资金']],
                 ['!='], ['原买入资金', '现买入资金'], '%f'],
        '买入费用': [[QueryInit['买入费用'], QueryEnd['买入费用']],
                 ['!='], ['原买入费用', '现买入费用'], '%f'],
        '卖出资金': [[QueryEnd['卖出资金'], data['trade_amount'], QueryInit['卖出资金'], 0.01],
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
        '当日交易资金扎差': [[QueryEnd['当日交易资金扎差'], data['trade_amount'], fee, QueryInit['当日交易资金扎差'], 0.01],
                     ['-', '+', '-', '>'], ['现当日交易资金扎差', '成交金额', '费用', '原当日交易资金扎差'], '%f'],
        '资金资产': [[QueryInit['资金资产'], data['trade_amount'], fee, QueryEnd['资金资产'], 0.01],
                 ['+', '-', '-', '>'], ['原资金资产', '成交金额', '费用', '现资金资产'], '%f'],
        '证券代码': [[QueryInit['证券代码'], QueryEnd['证券代码']],
                 ['!='], ['原证券代码', '现证券代码'], '%s'],
        '市场': [[market_init, market_end],
               ['!='], ['原市场', '现市场'], '%s'],
        '拥股数量': [[QueryInit['拥股数量'], data['qty_traded'], QueryEnd['拥股数量'], 0],
                 ['-', '-', '>'], ['原拥股数量', '成交数量', '现拥股数量'], '%d'],
        '可用股份数': [[QueryInit['可用股份数'], data['qty_traded'], QueryEnd['可用股份数'], 0],
                  ['-', '-', '>'], ['原可用股份数', '成交数量', '现可用股份数'], '%d'],
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

    rs = check_fund_stk_bdquery(check_item)
    return rs

def check_fund_stk_bdquery(check_item):
    '''
    校验报单查询资金和持仓情况
    :param check_item: 校验的数字项和符号项
    :return:
    '''
    Check_reslut = {
        '检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
    }

    if type(check_item) != dict:
        logger.error('参数类型错误，应传入dict类型的参数！')
    else:
        for k, v in check_item.items():
            exp = ''
            for index, ele in enumerate(v[0]):
                ele = decimal.Decimal(ele)
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
                Check_reslut['检查状态'] = 'end'
                Check_reslut['错误信息'] = k + '错误'
                return Check_reslut

        Check_reslut['检查状态'] = 'end'
        Check_reslut['测试结果'] = True
        logger.info('资金股份验证正确')
        return Check_reslut


