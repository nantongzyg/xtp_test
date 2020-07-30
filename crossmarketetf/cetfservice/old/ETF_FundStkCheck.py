#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
from decimal import Decimal
from decimal import ROUND_HALF_UP
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from getUpOrDownPrice import *
sys.path.append("/home/yhl2/workspace/xtp_test/ETF/etf_mysql")
from QueryEtfComponentsCodeDB import *
from QueryEtfComponentsDB import QueryEtfComponentShare
from QueryEtfNavDB import *
from QueryEtfQty import stkQty
from QueryEstimateCashComponent import QueryEstimateCashComponent
from QueryPreclosePriceDB import QueryPreclosePriceDB
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from ServiceConfig import *
from ETF_GetComponentShare import etf_get_one_component_stk

#注：部成和全成状态的校验写在了成交回报校验中
#注：初始未成交资金股份检查fundStkCheck_nomatch(Api,QueryInit,QueryEnd,wt_reqs)
#注：部撤资金股份检查fundStkCheck_partCancel(Api,QueryInit,QueryEnd,wt_reqs,data)
#注：'已撤'、'部撤已报'、'已报待撤'、'废单'、'撤废'资金股份检查fundStkCheck_other(QueryInit,QueryEnd)

#---定义费率，最低收费
fee_rate_buy = ServiceConfig.FEE_RATE_ETF_CREATION
fee_rate_sell = ServiceConfig.FEE_RATE_ETF_REDEMPTION
fee_min = ServiceConfig.FEE_ETF_MIN

#--持仓成本，保留小数位
avg_price_DecimalPlaces = ServiceConfig.AVG_PRICE_DECIMALPLACES

#报单状态为'未成交'，资金股份校验
def fundStkCheck_nomatch(Api, QueryInit, QueryEnd,
                         wt_reqs, trade_fund, pyname_source):
    logger.info('未成交状态报单资金股份校验')
    fundStkCheck_reslut = {
        '检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
    }
    # etf基金份额净值
    nav = QueryEtfNavDB(wt_reqs['ticker'])

    py_name = pyname_source[1]
    global fee_rate_buy, fee_rate_sell, fee_min
    if py_name != '':
        fee_etf = ServiceConfig.fee_etf_creation_redemption[py_name]
        fee_min = float(fee_etf[ServiceConfig.fee_etf_min_str])
        fee_rate_buy = float(fee_etf[ServiceConfig.fee_rate_etf_creation_str])
        fee_rate_sell = float(fee_etf[ServiceConfig.fee_rate_etf_redemption_str])

    # etf申赎份数
    creation_redemption_num = wt_reqs['quantity'] / stkQty['最小申赎单位']

    if wt_reqs['side'] == Api.const.XTP_SIDE_TYPE['XTP_SIDE_PURCHASE']:
        #  ----获取预估现金差额----
        estimate_cash_component = QueryEstimateCashComponent(wt_reqs['ticker'])
        estimate_cash_component = estimate_cash_component * creation_redemption_num \
            if estimate_cash_component > 0 else 0

        # 费用计算
        fee = wt_reqs['quantity'] * fee_rate_buy * nav / 10000
        if fee <= fee_min:
            fee = fee_min
        else:
            fee = float(Decimal(Decimal(str(fee)).quantize(Decimal('.01'),
                                                           rounding=ROUND_HALF_UP)))

        total_amount = trade_fund + fee + estimate_cash_component
        # 资金信息
        fund_dict = {
            'total_amount': total_amount,  # 可用资金变化金额
            'trade_fund': trade_fund,  # 买入资金
            'fee': fee,  # 买入费用
            'estimate_cash_component': estimate_cash_component,  # 冻结资金(预估现金差额)
        }
        logger.info('fee=' + str(fund_dict['fee']))
        rs = nomatch_B(QueryInit, QueryEnd, wt_reqs, fund_dict)
        fundStkCheck_reslut['检查状态'] = rs['检查状态']
        fundStkCheck_reslut['测试结果'] = rs['测试结果']
        fundStkCheck_reslut['错误信息'] = rs['错误信息']

    #如果是赎回  当交易费用＋预估现金差额－必须替代资金>0时，委托买入资金＝交易费用＋预估现金差额－必须替代资金。否则，委托买入资金＝交易费用
    elif wt_reqs['side'] == Api.const.XTP_SIDE_TYPE['XTP_SIDE_REDEMPTION']:
        # ----获取预估现金差额----
        estimate_cash_component = QueryEstimateCashComponent(wt_reqs['ticker'])
        estimate_cash_component = -(estimate_cash_component * creation_redemption_num
                                    if estimate_cash_component < 0 else 0)

        # 费用计算
        fee = wt_reqs['quantity'] * fee_rate_buy * nav / 10000
        if fee <= fee_min:
            fee = fee_min
        else:
            fee = float(Decimal(Decimal(str(fee)).quantize(Decimal('.01'),
                                                           rounding=ROUND_HALF_UP)))

        total_amount = fee + estimate_cash_component - trade_fund
        # 资金信息
        fund_dict = {
            'total_amount': total_amount,  # 可用资金变化金额
            'trade_fund': trade_fund,  # 卖出资金
            'fee': fee,  # 买入费用
            'estimate_cash_component': estimate_cash_component,  # 冻结资金(预估现金差额)
        }
        logger.info('fee=' + str(fund_dict['fee']))
        rs = nomatch_S(QueryInit, QueryEnd, wt_reqs, fund_dict)
        fundStkCheck_reslut['检查状态'] = rs['检查状态']
        fundStkCheck_reslut['测试结果'] = rs['测试结果']
        fundStkCheck_reslut['错误信息'] = rs['错误信息']

    return fundStkCheck_reslut

#报单状态为'初始'，资金股份校验
def fundStkCheck_init(Api, QueryInit, QueryEnd, wt_reqs, trade_fund, component_stk_info):
    logger.info('初始状态报单资金股份校验')
    fundStkCheck_reslut = {
        '检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
    }
    # etf基金份额净值
    nav = QueryEtfNavDB(wt_reqs['ticker'])

    # etf申赎份数
    creation_redemption_num = wt_reqs['quantity'] / stkQty['最小申赎单位']

    if wt_reqs['side'] == Api.const.XTP_SIDE_TYPE['XTP_SIDE_PURCHASE']:
        #  ----获取预估现金差额----
        estimate_cash_component = QueryEstimateCashComponent(wt_reqs['ticker'])
        estimate_cash_component = estimate_cash_component * creation_redemption_num \
            if estimate_cash_component > 0 else 0

        # 费用计算
        fee = wt_reqs['quantity'] * fee_rate_buy * nav / 10000
        if fee <= fee_min:
            fee = fee_min
        else:
            fee = float(Decimal(Decimal(str(fee)).quantize(Decimal('.01'),
                                                           rounding=ROUND_HALF_UP)))

        # 资金信息
        fund_dict = {
            'trade_fund': trade_fund,  # 买入资金
            'fee': fee,  # 买入费用
            'estimate_cash_component': estimate_cash_component,  # 冻结资金(预估现金差额)
        }
        rs = init_B(QueryInit, QueryEnd, wt_reqs, fund_dict, component_stk_info[0])

    #如果是赎回  当交易费用＋预估现金差额－必须替代资金>0时，委托买入资金＝交易费用＋预估现金差额－必须替代资金。否则，委托买入资金＝交易费用
    elif wt_reqs['side'] == Api.const.XTP_SIDE_TYPE['XTP_SIDE_REDEMPTION']:
        # ----获取预估现金差额----
        estimate_cash_component = QueryEstimateCashComponent(wt_reqs['ticker'])
        estimate_cash_component = -(estimate_cash_component * creation_redemption_num
                                    if estimate_cash_component < 0 else 0)

        # 费用计算
        fee = wt_reqs['quantity'] * fee_rate_sell * nav / 10000
        if fee <= fee_min:
            fee = fee_min
        else:
            fee = float(Decimal(Decimal(str(fee)).quantize(Decimal('.01'),
                                                           rounding=ROUND_HALF_UP)))

        # 资金信息
        fund_dict = {
            'fee': fee,
            'estimate_cash_component': estimate_cash_component,  # 冻结资金(预估现金差额)
        }
        rs = init_S(QueryInit, QueryEnd, wt_reqs, fund_dict)

    fundStkCheck_reslut['检查状态'] = rs['检查状态']
    fundStkCheck_reslut['测试结果'] = rs['测试结果']
    fundStkCheck_reslut['错误信息'] = rs['错误信息']
    return fundStkCheck_reslut

#报单状态为'部撤'，资金股份校验
def fundStkCheck_partCancel(Api,QueryInit,QueryEnd,wt_reqs,data):
    logger.info('部撤状态报单资金股份校验')
    fundStkCheck_reslut = {
        '检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
    }
    #初始费用和持仓成本
    fee = fee_min
    cccb=QueryInit['持仓成本']
    # 如果是买
    if wt_reqs['side'] == Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY']:
        #买入费用
        if data['trade_amount'] * fee_rate_buy >= fee_min:
            fee = data['trade_amount'] * fee_rate_buy
        else:
            fee = fee_min
        logger.info('fee=' + str(fee))
        #持仓成本
        cccb=(QueryInit['持仓成本']*QueryInit['拥股数量']+data['trade_amount'])/(QueryInit['拥股数量']+data['qty_traded'])
        rs = partCancel_B(QueryInit, QueryEnd, cccb, fee,data)
        fundStkCheck_reslut['检查状态'] = rs['检查状态']
        fundStkCheck_reslut['测试结果'] = rs['测试结果']
        fundStkCheck_reslut['错误信息'] = rs['错误信息']
    # 如果是卖
    elif wt_reqs['side'] == Api.const.XTP_SIDE_TYPE['XTP_SIDE_SELL']:
        if  data['trade_amount'] * fee_rate_sell >= fee_min:
            fee =  data['trade_amount'] * fee_rate_sell
        else:
            fee = fee_min
        logger.info('fee=' + str(fee))
        rs = partCancel_S(QueryInit, QueryEnd,fee,data)
        fundStkCheck_reslut['检查状态'] = rs['检查状态']
        fundStkCheck_reslut['测试结果'] = rs['测试结果']
        fundStkCheck_reslut['错误信息'] = rs['错误信息']

    return fundStkCheck_reslut

#报单状态为'全成撤废','废单撤废',etf和其成分股资金股份校验（资金股份前后不变）
def fundStkCheck_other(QueryInit,QueryEnd,component_stk_info):
    logger.info('撤废状态报单资金股份校验')
    fundStkCheck_reslut = {
        '检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
    }
    # ---------ETF----------
    # 判断股票代码和市场是否一致
    if QueryInit['股票代码'] != QueryEnd['股票代码'] or QueryInit['市场'] != QueryEnd['市场']:
        logger.error('ETF的QueryInit和QueryEnd的股票代码或市场不一致')
        fundStkCheck_reslut['检查状态'] = 'end'
        fundStkCheck_reslut['错误信息'] = 'ETF的QueryInit和QueryEnd的股票代码或市场不一致'
    # 判断可用资金
    elif abs(QueryInit['可用资金'] - QueryEnd['可用资金']) > 0.001:
        logger.info('可用资金：'+str(abs(QueryInit['可用资金'] - QueryEnd['可用资金'])))
        logger.error('ETF可用资金预冻结不正确')
        fundStkCheck_reslut['检查状态'] = 'end'
        fundStkCheck_reslut['错误信息'] = 'ETF可用资金预冻结不正确'
    # 判断买入资金下单前后是否一致
    elif abs(QueryInit['买入资金'] - QueryEnd['买入资金']) > 0.001:
        logger.error('ETF买入资金计算不正确')
        fundStkCheck_reslut['检查状态'] = 'end'
        fundStkCheck_reslut['错误信息'] = 'ETF买入资金计算不正确'
    # 判断买入费用下单前后是否一致
    elif abs(QueryInit['买入费用'] - QueryEnd['买入费用']) > 0.001:
        logger.error('ETF买入费用计算不正确')
        fundStkCheck_reslut['检查状态'] = 'end'
        fundStkCheck_reslut['错误信息'] = 'ETF买入费用计算不正确'
    # 判断卖出资金下单前后是否一致
    elif abs(QueryInit['卖出资金'] - QueryEnd['卖出资金']) > 0.001:
        logger.error('ETF卖出资金计算不正确')
        fundStkCheck_reslut['检查状态'] = 'end'
        fundStkCheck_reslut['错误信息'] = 'ETF卖出资金计算不正确'
    # 判断卖出费用下单前后是否一致
    elif abs(QueryInit['卖出费用'] - QueryEnd['卖出费用']) > 0.001:
        logger.error('ETF卖出费用计算不正确')
        fundStkCheck_reslut['检查状态'] = 'end'
        fundStkCheck_reslut['错误信息'] = 'ETF卖出费用计算不正确'
    # 判断拥股数量是否正确
    elif QueryInit['预扣资金'] != QueryEnd['预扣资金']:
        logger.error('ETF预扣资金计算不正确')
        fundStkCheck_reslut['检查状态'] = 'end'
        fundStkCheck_reslut['错误信息'] = 'ETF预扣资金计算不正确'
    # 判断可用股份数是否正确
    elif QueryInit['总资产'] != QueryEnd['总资产']:
        logger.error('ETF总资产计算不正确')
        fundStkCheck_reslut['检查状态'] = 'end'
        fundStkCheck_reslut['错误信息'] = 'ETF总资产计算不正确'
    # 判断可用股份数是否正确
    elif QueryInit['总持仓'] != QueryEnd['总持仓']:
        logger.error('ETF总持仓计算不正确')
        fundStkCheck_reslut['检查状态'] = 'end'
        fundStkCheck_reslut['错误信息'] = 'ETF总持仓计算不正确'
    # 判断可用股份数是否正确
    elif QueryInit['可卖持仓'] != QueryEnd['可卖持仓']:
        logger.error('ETF可卖持仓计算不正确')
        fundStkCheck_reslut['检查状态'] = 'end'
        fundStkCheck_reslut['错误信息'] = 'ETF可卖持仓计算不正确'
    # 判断可用股份数是否正确
    elif QueryInit['昨日持仓'] != QueryEnd['昨日持仓']:
        logger.error('ETF昨日持仓计算不正确')
        fundStkCheck_reslut['检查状态'] = 'end'
        fundStkCheck_reslut['错误信息'] = 'ETF昨日持仓计算不正确'
        # 判断可用股份数是否正确
    elif QueryInit['今日可申购赎回持仓'] != QueryEnd['今日可申购赎回持仓']:
        logger.error('ETF今日可申购赎回持仓计算不正确')
        fundStkCheck_reslut['检查状态'] = 'end'
        fundStkCheck_reslut['错误信息'] = 'ETF今日可申购赎回持仓计算不正确'
    # 判断卖出费用下单前后是否一致
    elif abs(QueryInit['持仓成本价'] - QueryEnd['持仓成本价']) > 0.001:
        logger.error('ETF持仓成本价计算不正确')
        fundStkCheck_reslut['检查状态'] = 'end'
        fundStkCheck_reslut['错误信息'] = 'ETF持仓成本价计算不正确'
    # 判断卖出费用下单前后是否一致
    elif abs(QueryInit['浮动盈亏'] - QueryEnd['浮动盈亏']) > 0.001:
        logger.error('ETF浮动盈亏计算不正确')
        fundStkCheck_reslut['检查状态'] = 'end'
        fundStkCheck_reslut['错误信息'] = 'ETF浮动盈亏计算不正确'
    else:
        fundStkCheck_reslut['检查状态'] = 'end'
        fundStkCheck_reslut['测试结果'] = True
        logger.info('ETF资金股份验证正确')

    # --------成分股---------
    if isinstance(component_stk_info, dict):
        stk_info =  component_stk_info
    else:
        stk_info = ()
        if component_stk_info != ():
            stk_info = component_stk_info[0]

    if stk_info != ():
        for code in stk_info:
            fundStkCheck_reslut = {
                '检查状态': 'init',
                '测试结果': False,
                '错误信息': '',
            }
            component_stk_info_one = etf_get_one_component_stk(code)
            StkInit = stk_info[code]
            StkEnd = component_stk_info_one[code]
            # 判断股票代码和市场是否一致
            if StkInit['证券代码'] != StkEnd['证券代码'] or \
                StkInit['市场'] != StkEnd['市场']:
                logger.error('成分股' + code + 'StkInit和StkEnd的股票代码或市场不一致'
                             '申赎前股票代码或市场分别为： ' +
                             StkInit['ticker'] + ', ' + StkInit['market'] +
                             '申赎后股票代码或市场分别为： ' +
                             StkEnd['ticker'] + ', ' + StkEnd['market'])
                fundStkCheck_reslut['检查状态'] = 'end'
                fundStkCheck_reslut['错误信息'] = '申购前后成分股的股票代码或市场不一致'
            # 判断可用股份数是否正确
            elif StkInit['总持仓'] != StkEnd['总持仓']:
                logger.error('成分股' + code + '总持仓计算不正确'
                             '申赎前后总持仓分别为： ' +
                             str(StkInit['总持仓']) + ', ' + str(StkEnd['总持仓']))
                fundStkCheck_reslut['检查状态'] = 'end'
                fundStkCheck_reslut['错误信息'] = '成分股总持仓计算不正确'
            # 判断可用股份数是否正确
            elif StkInit['可卖持仓'] != StkEnd['可卖持仓']:
                logger.error('成分股' + code + '可卖持仓计算不正确'
                             '申赎前后可卖持仓分别为： ' +
                             str(StkInit['可卖持仓']) + ', '
                             + str(StkEnd['可卖持仓']))
                fundStkCheck_reslut['检查状态'] = 'end'
                fundStkCheck_reslut['错误信息'] = '成分股可卖持仓计算不正确'
            # 判断可用股份数是否正确
            elif StkInit['昨日持仓'] != StkEnd['昨日持仓']:
                logger.error('成分股' + code + '昨日持仓计算不正确'
                             '申赎前后昨日持仓分别为： ' +
                             str(StkInit['昨日持仓']) + ', '
                             + str(StkEnd['昨日持仓']))
                fundStkCheck_reslut['检查状态'] = 'end'
                fundStkCheck_reslut['错误信息'] = '成分股昨日持仓计算不正确'
                # 判断可用股份数是否正确
            elif StkInit['今日可申购赎回持仓'] != StkEnd['今日可申购赎回持仓']:
                logger.error('成分股' + code + '今日可申购赎回持仓计算不正确'
                             '申赎前后今日可申购赎回持仓分别为： ' +
                             str(StkInit['今日可申购赎回持仓']) + ', '
                             + str(StkEnd['今日可申购赎回持仓']))
                fundStkCheck_reslut['检查状态'] = 'end'
                fundStkCheck_reslut['错误信息'] = '成分股今日可申购赎回持仓计算不正确'
            # 判断卖出费用下单前后是否一致
            elif abs(StkInit['持仓成本价'] - StkEnd['持仓成本价']) > 0.001:
                logger.error('成分股' + code + '持仓成本价计算不正确'
                             '申赎前后持仓成本价分别为： ' +
                             str(StkInit['持仓成本价']) + ', '
                             + str(StkEnd['持仓成本价']))
                fundStkCheck_reslut['检查状态'] = 'end'
                fundStkCheck_reslut['错误信息'] = '成分股持仓成本价计算不正确'
            # 判断卖出费用下单前后是否一致
            elif abs(StkInit['浮动盈亏'] - StkEnd['浮动盈亏']) > 0.001:
                logger.error('成分股' + code + '浮动盈亏计算不正确'
                             '申赎前后浮动盈亏分别为： ' +
                             str(StkInit['浮动盈亏']) + ', '
                             + str(StkEnd['浮动盈亏']))
                fundStkCheck_reslut['检查状态'] = 'end'
                fundStkCheck_reslut['错误信息'] = '成分股浮动盈亏计算不正确'
            else:
                fundStkCheck_reslut['检查状态'] = 'end'
                fundStkCheck_reslut['测试结果'] = True
                logger.info('成分股' + code + '资金股份验证正确')

            if fundStkCheck_reslut['测试结果'] is False:
                return fundStkCheck_reslut

    return fundStkCheck_reslut


def nomatch_B(QueryInit,QueryEnd,wt_reqs,fund_dict):
    Check_reslut = {
        '检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
    }

    # 获取成分股昨收价
    pre_close_price = float(QueryPreclosePriceDB(wt_reqs['ticker']))

    # --计算期待持仓成本应该是，深圳赎回时会返回全部现金替代的成分股回报，且成交数量为0
    price_avg = (QueryInit['持仓成本价'] * QueryInit['总持仓'] +
                 wt_reqs['quantity'] * pre_close_price) / \
                (QueryInit['总持仓'] + wt_reqs['quantity'])

    #判断股票代码和市场是否一致
    if (QueryInit['股票代码'] != QueryEnd['股票代码'] or
        QueryInit['市场'] != QueryEnd['市场']):
        logger.error('QueryInit和QueryEnd的股票代码或市场不一致')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = 'QueryInit和QueryEnd的股票代码或市场不一致'
    # 判断总资产
    elif abs(QueryInit['总资产']
             - fund_dict['trade_fund']
             - fund_dict['fee']
             - QueryEnd['总资产']) > 0.01:
        logger.error('总资产预冻结不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '总资产预冻结不正确'
    #判断可用资金
    elif abs(QueryInit['可用资金']
             - fund_dict['total_amount']
             - QueryEnd['可用资金']) > 0.01:
        logger.error('可用资金预冻结不正确')
        Check_reslut['检查状态']='end'
        Check_reslut['错误信息'] = '可用资金预冻结不正确'
    #判断买入资金
    elif abs(QueryEnd['买入资金']
             - fund_dict['trade_fund']
             - QueryInit['买入资金']) > 0.001:
        logger.error('买入资金计算不正确')
        Check_reslut['检查状态']='end'
        Check_reslut['错误信息'] = '买入资金计算不正确'
    #判断买入费用
    elif abs(QueryEnd['买入费用']
             - fund_dict['fee']
             - QueryInit['买入费用']) > 0.001:
        logger.error('买入费用计算不正确')
        Check_reslut['检查状态']='end'
        Check_reslut['错误信息'] = '买入费用计算不正确'
    #判断卖出资金下单前后是否一致
    elif abs(QueryInit['卖出资金'] - QueryEnd['卖出资金']) > 0.001:
        logger.error('卖出资金计算不正确')
        Check_reslut['检查状态']='end'
        Check_reslut['错误信息'] = '卖出资金计算不正确'
    # 判断卖出费用下单前后是否一致
    elif abs(QueryInit['卖出费用'] - QueryEnd['卖出费用']) > 0.001:
        logger.error('卖出费用计算不正确')
        Check_reslut['检查状态']='end'
        Check_reslut['错误信息'] = '卖出费用计算不正确'
    # 判断预扣资金
    elif abs(QueryEnd['预扣资金']
             - fund_dict['estimate_cash_component']
             - QueryInit['预扣资金']) > 0.001:
        logger.error('预扣资金计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '预扣资金计算不正确'
    #判断总持仓是否正确
    elif QueryEnd['总持仓'] - wt_reqs['quantity'] - QueryInit['总持仓'] > 0:
        logger.error('总持仓计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '总持仓计算不正确'
    #判断可卖持仓是否正确
    elif QueryEnd['可卖持仓'] - wt_reqs['quantity'] - QueryInit['可卖持仓'] > 0:
        logger.error('可卖持仓计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '可卖持仓计算不正确'
    # 判断昨日持仓是否正确
    elif QueryEnd['昨日持仓'] != QueryInit['昨日持仓']:
        logger.error('昨日持仓计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '昨日持仓计算不正确'
    # 判断今日可申购赎回持仓是否正确
    elif QueryEnd['今日可申购赎回持仓'] != QueryInit['今日可申购赎回持仓']:
        logger.error('今日可申购赎回持仓计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '今日可申购赎回持仓计算不正确'
    # 判断持仓成本
    elif abs(price_avg - QueryEnd['持仓成本价']) > 0.001:
        logger.error('持仓成本计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '持仓成本价计算不正确'
    # 判断浮动盈亏
    elif abs(QueryInit['浮动盈亏'] - QueryEnd['浮动盈亏']) > 0.001:
        logger.error('浮动盈亏计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '浮动盈亏计算不正确'
    else:
        Check_reslut['检查状态'] = 'end'
        Check_reslut['测试结果'] = True
        logger.info('资金股份验证正确')

    return Check_reslut

def init_B(QueryInit,QueryEnd,wt_reqs,fund_dict,component_stk_info):
    Check_reslut = {
        '检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
    }
    # 申购份数
    creation_redemption_num = wt_reqs['quantity'] / stkQty['最小申赎单位']

    #判断股票代码和市场是否一致
    if (QueryInit['股票代码'] != QueryEnd['股票代码'] or
        QueryInit['市场'] != QueryEnd['市场']):
        logger.error('QueryInit和QueryEnd的股票代码或市场不一致')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = 'QueryInit和QueryEnd的股票代码或市场不一致'
    # 判断总资产
    elif abs(QueryInit['总资产'] - QueryEnd['总资产']) > 0.01:
        logger.error('总资产预冻结不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '总资产预冻结不正确'
    #判断可用资金
    elif abs(QueryInit['可用资金']
             - fund_dict['estimate_cash_component']
             - fund_dict['trade_fund']
             - fund_dict['fee']
             - QueryEnd['可用资金']) > 0.01:
        logger.error('可用资金预冻结不正确')
        Check_reslut['检查状态']='end'
        Check_reslut['错误信息'] = '可用资金预冻结不正确'
    #判断买入资金
    elif abs(QueryEnd['买入资金'] - QueryInit['买入资金']) > 0.001:
        logger.error('买入资金计算不正确')
        Check_reslut['检查状态']='end'
        Check_reslut['错误信息'] = '买入资金计算不正确'
    #判断买入费用
    elif abs(QueryEnd['买入费用'] - QueryInit['买入费用']) > 0.001:
        logger.error('买入费用计算不正确')
        Check_reslut['检查状态']='end'
        Check_reslut['错误信息'] = '买入费用计算不正确'
    #判断卖出资金下单前后是否一致
    elif abs(QueryInit['卖出资金'] - QueryEnd['卖出资金']) > 0.001:
        logger.error('卖出资金计算不正确')
        Check_reslut['检查状态']='end'
        Check_reslut['错误信息'] = '卖出资金计算不正确'
    #判断卖出费用下单前后是否一致
    elif abs(QueryInit['卖出费用'] - QueryEnd['卖出费用']) > 0.001:
        logger.error('卖出费用计算不正确')
        Check_reslut['检查状态']='end'
        Check_reslut['错误信息'] = '卖出费用计算不正确'
    # 判断预扣资金
    elif abs(QueryEnd['预扣资金']
             - fund_dict['estimate_cash_component']
             - fund_dict['trade_fund']
             - fund_dict['fee']
             - QueryInit['预扣资金']) > 0.001:
        logger.error('预扣资金计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '预扣资金计算不正确'
    #判断总持仓是否正确
    elif QueryEnd['总持仓'] - QueryInit['总持仓'] > 0:
        logger.error('总持仓计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '总持仓计算不正确'
    #判断可卖持仓是否正确
    elif QueryEnd['可卖持仓'] - QueryInit['可卖持仓'] > 0:
        logger.error('可卖持仓计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '可卖持仓计算不正确'
    # 判断昨日持仓是否正确
    elif QueryEnd['昨日持仓'] != QueryInit['昨日持仓']:
        logger.error('昨日持仓计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '昨日持仓计算不正确'
    # 判断今日可申购赎回持仓是否正确
    elif QueryEnd['今日可申购赎回持仓'] != QueryInit['今日可申购赎回持仓']:
        logger.error('今日可申购赎回持仓计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '今日可申购赎回持仓计算不正确'
    # 判断持仓成本
    elif abs(QueryInit['持仓成本价'] - QueryEnd['持仓成本价']) > 0.001:
        logger.error('持仓成本计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '持仓成本价计算不正确'
    # 判断浮动盈亏
    elif abs(QueryInit['浮动盈亏'] - QueryEnd['浮动盈亏']) > 0.001:
        logger.error('浮动盈亏计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '浮动盈亏计算不正确'
    else:
        Check_reslut['检查状态'] = 'end'
        Check_reslut['测试结果'] = True
        logger.info('资金股份验证正确')

    # 成分股持仓校验
    component_b(wt_reqs['ticker'], component_stk_info, creation_redemption_num)

    return Check_reslut

def nomatch_S(QueryInit, QueryEnd,wt_reqs, fund_dict):
    Check_reslut = {
        '检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
    }
    # 判断股票代码和市场是否一致
    if QueryInit['股票代码'] != QueryEnd['股票代码'] or QueryInit['市场'] != QueryEnd['市场']:
        logger.error('QueryInit和QueryEnd的股票代码或市场不一致')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = 'QueryInit和QueryEnd的股票代码或市场不一致'
    # 判断总资产
    elif abs(QueryInit['总资产']
                - fund_dict['trade_fund']
                - fund_dict['fee']
                - QueryEnd['总资产']) > 0.01:
        logger.error('总资产预冻结不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '总资产预冻结不正确'
    # 判断可用资金
    elif abs(QueryInit['可用资金']
             - fund_dict['total_amount']
             - QueryEnd['可用资金']) > 0.01:
        logger.error('可用资金预冻结不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '可用资金预冻结不正确'
    # 判断买入资金下单前后是否一致
    elif abs(QueryInit['买入资金'] - QueryEnd['买入资金']) > 0.001:
        logger.error('买入资金计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '买入资金计算不正确'
    # 判断买入费用下单前后是否一致
    elif abs(QueryInit['买入费用'] - QueryEnd['买入费用']) > 0.001:
        logger.error('买入费用计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '买入费用计算不正确'
    # 判断卖出资金下单前后是否一致
    elif abs(QueryEnd['卖出资金']
            - fund_dict['trade_fund']
            - QueryInit['卖出资金']) > 0.001:
        logger.error('卖出资金计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '卖出资金计算不正确'
    # 判断卖出费用下单前后是否一致
    elif abs(QueryEnd['卖出费用']
            - fund_dict['fee']
            - QueryInit['卖出费用']) > 0.001:
        logger.error('卖出费用计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '卖出费用计算不正确'
    # 判断预扣资金
    elif abs(QueryEnd['预扣资金']
             - fund_dict['estimate_cash_component']
             - fund_dict['trade_fund']
             - fund_dict['fee']
             - QueryInit['预扣资金']) > 0.001:
        logger.error('预扣资金计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '预扣资金计算不正确'
        # 判断总持仓是否正确
    elif QueryInit['总持仓'] - wt_reqs['quantity'] - QueryEnd['总持仓'] > 0:
        logger.error('总持仓计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '总持仓计算不正确'
        # 判断可卖持仓是否正确
    elif QueryInit['可卖持仓'] - wt_reqs['quantity'] - QueryEnd['可卖持仓'] > 0:
        logger.error('可卖持仓计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '可卖持仓计算不正确'
        # 判断昨日持仓是否正确
    elif QueryEnd['昨日持仓'] != QueryInit['昨日持仓']:
        logger.error('昨日持仓计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '昨日持仓计算不正确'
        # 判断今日可申购赎回持仓是否正确
    elif QueryInit['今日可申购赎回持仓']\
            - wt_reqs['quantity']\
            - QueryEnd['今日可申购赎回持仓'] > 0:
        logger.error('今日可申购赎回持仓计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '今日可申购赎回持仓计算不正确'
        # 判断持仓成本
    elif abs(QueryInit['持仓成本价'] - QueryEnd['持仓成本价']) \
            and QueryEnd['总持仓'] != 0> 0.001:
        logger.error('持仓成本计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '持仓成本价计算不正确'
    elif QueryEnd['持仓成本价'] != 0 and QueryEnd['总持仓'] == 0:
        logger.error('持仓成本计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '持仓成本价计算不正确'
        # 判断浮动盈亏
    elif abs(QueryInit['浮动盈亏'] - QueryEnd['浮动盈亏']) > 0.001:
        logger.error('浮动盈亏计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '浮动盈亏计算不正确'
    else:
        Check_reslut['检查状态'] = 'end'
        Check_reslut['测试结果'] = True
        logger.info('资金股份验证正确')

    return Check_reslut

def init_S(QueryInit, QueryEnd,wt_reqs, fund_dict):
    Check_reslut = {
        '检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
    }
    # 判断股票代码和市场是否一致
    if QueryInit['股票代码'] != QueryEnd['股票代码'] or QueryInit['市场'] != QueryEnd['市场']:
        logger.error('QueryInit和QueryEnd的股票代码或市场不一致')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = 'QueryInit和QueryEnd的股票代码或市场不一致'
        # 判断总资产
    elif abs(QueryInit['总资产'] - QueryEnd['总资产']) > 0.01:
        logger.error('总资产预冻结不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '总资产预冻结不正确'
    # 判断可用资金
    elif abs(QueryInit['可用资金']
             - fund_dict['estimate_cash_component']
             - fund_dict['fee']
             - QueryEnd['可用资金']) > 0.01:
        logger.error('可用资金预冻结不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '可用资金预冻结不正确'
    # 判断买入资金下单前后是否一致
    elif abs(QueryInit['买入资金'] - QueryEnd['买入资金']) > 0.001:
        logger.error('买入资金计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '买入资金计算不正确'
    # 判断买入费用下单前后是否一致
    elif abs(QueryInit['买入费用'] - QueryEnd['买入费用']) > 0.001:
        logger.error('买入费用计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '买入费用计算不正确'
    # 判断卖出资金下单前后是否一致
    elif abs(QueryEnd['卖出资金'] - QueryInit['卖出资金']) > 0.001:
        logger.error('卖出资金计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '卖出资金计算不正确'
    # 判断卖出费用下单前后是否一致
    elif abs(QueryEnd['卖出费用'] - QueryInit['卖出费用']) > 0.001:
        logger.error('卖出费用计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '卖出费用计算不正确'
    # 判断预扣资金
    elif abs(QueryEnd['预扣资金']
             - fund_dict['estimate_cash_component']
             - fund_dict['fee']
             - QueryInit['预扣资金']) > 0.001:
        logger.error('预扣资金计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '预扣资金计算不正确'
        # 判断总持仓是否正确
    elif QueryInit['总持仓'] - wt_reqs['quantity'] - QueryEnd['总持仓'] > 0:
        logger.error('总持仓计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '总持仓计算不正确'
        # 判断可卖持仓是否正确
    elif QueryInit['可卖持仓'] - wt_reqs['quantity'] - QueryEnd['可卖持仓'] > 0:
        logger.error('可卖持仓计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '可卖持仓计算不正确'
        # 判断昨日持仓是否正确
    elif QueryEnd['昨日持仓'] != QueryInit['昨日持仓']:
        logger.error('昨日持仓计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '昨日持仓计算不正确'
        # 判断今日可申购赎回持仓是否正确
    elif QueryInit['今日可申购赎回持仓']\
            - wt_reqs['quantity']\
            - QueryEnd['今日可申购赎回持仓'] > 0:
        logger.error('今日可申购赎回持仓计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '今日可申购赎回持仓计算不正确'
        # 判断持仓成本
    elif abs(QueryInit['持仓成本价'] - QueryEnd['持仓成本价']) \
            and QueryEnd['总持仓'] != 0> 0.001:
        logger.error('持仓成本计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '持仓成本价计算不正确'
    elif QueryEnd['持仓成本价'] != 0 and QueryEnd['总持仓'] == 0:
        logger.error('持仓成本计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '持仓成本价计算不正确'
        # 判断浮动盈亏
    elif abs(QueryInit['浮动盈亏'] - QueryEnd['浮动盈亏']) > 0.001:
        logger.error('浮动盈亏计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '浮动盈亏计算不正确'
    else:
        Check_reslut['检查状态'] = 'end'
        Check_reslut['测试结果'] = True
        logger.info('资金股份验证正确')

    return Check_reslut

def component_b(ticker, component_stk_info, creation_redemption_num):
    compoenent_shares = QueryEtfComponentShare(ticker)  # 申购每份etf所需的成分股数
    for code in component_stk_info[0].keys():
        Check_reslut = {
            '检查状态': 'init',
            '测试结果': False,
            '错误信息': '',
        }
        component_stk_info_one = etf_get_one_component_stk(code)  # 查询某个股票持仓信息
        StkInit = component_stk_info[0][code]
        StkEnd = component_stk_info_one[code]

        stock_amount_freezing = compoenent_shares[code] * creation_redemption_num
        if StkInit['证券代码'] != StkEnd['证券代码'] or \
                        StkInit['市场'] != StkEnd['市场']:
            logger.error('申赎前后证券代码或市场不一致')
            Check_reslut['检查状态'] = 'end'
            Check_reslut['错误信息'] = '申赎前后证券代码或市场不一致'
        elif StkInit['总持仓']\
                - stock_amount_freezing\
                - StkEnd['总持仓'] > 0:
            logger.error('总持仓计算不正确')
            Check_reslut['检查状态'] = 'end'
            Check_reslut['错误信息'] = '总持仓计算不正确'
        elif StkInit['可卖持仓'] \
                - stock_amount_freezing \
                - StkEnd['可卖持仓'] > 0:
            logger.error('可卖持仓计算不正确')
            Check_reslut['检查状态'] = 'end'
            Check_reslut['错误信息'] = '可卖持仓计算不正确'
        elif StkInit['昨日持仓'] != StkEnd['昨日持仓']:
            logger.error('昨日持仓计算不正确')
            Check_reslut['检查状态'] = 'end'
            Check_reslut['错误信息'] = '昨日持仓计算不正确'
        elif StkInit['今日可申购赎回持仓'] \
                - stock_amount_freezing \
                - StkEnd['今日可申购赎回持仓']:
            logger.error('今日可申购赎回持仓计算不正确')
            Check_reslut['检查状态'] = 'end'
            Check_reslut['错误信息'] = '今日可申购赎回持仓计算不正确'
        elif abs(StkInit['持仓成本价'] - StkEnd['持仓成本价']) > 0.001:
            logger.error('持仓成本价计算不正确')
            Check_reslut['检查状态'] = 'end'
            Check_reslut['错误信息'] = '持仓成本价计算不正确'
        elif abs(StkInit['浮动盈亏'] - StkEnd['浮动盈亏']) > 0.001:
            logger.error('浮动盈亏计算不正确')
            Check_reslut['检查状态'] = 'end'
            Check_reslut['错误信息'] = '浮动盈亏计算不正确'
        else:
            Check_reslut['检查状态'] = 'end'
            Check_reslut['测试结果'] = True
            logger.info('成分股持仓验证正确')

        if Check_reslut['测试结果'] is False:
            return Check_reslut

    return Check_reslut

def partCancel_B(QueryInit, QueryEnd, cccb, fee,data):
    Check_reslut = {
        '检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
    }
    # 判断股票代码和市场是否一致
    if QueryInit['股票代码'] != QueryEnd['股票代码'] or QueryInit['市场'] != QueryEnd['市场']:
        logger.error('QueryInit和QueryEnd的股票代码或市场不一致')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = 'QueryInit和QueryEnd的股票代码或市场不一致'
    # 判断可用资金
    elif abs(QueryInit['可用资金'] - data['trade_amount'] - fee - QueryEnd['可用资金']) > 0.01:
        logger.error('可用资金计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '可用资金计算不正确'
    # 判断买入资金是否正确
    elif abs(QueryInit['买入资金'] + data['trade_amount']- QueryEnd['买入资金']) > 0.01:
        logger.error('买入资金计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '买入资金计算不正确'
    # 判断买入费用是否正确
    elif abs(QueryInit['买入费用'] + fee-QueryEnd['买入费用']) > 0.01:
        logger.error('买入费用计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '买入费用计算不正确'
    # 判断卖出资金下单前后是否一致
    elif abs(QueryInit['卖出资金'] - QueryEnd['卖出资金']) > 0.001:
        logger.error('卖出资金计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '卖出资金计算不正确'
    # 判断卖出费用下单前后是否一致
    elif abs(QueryInit['卖出费用'] - QueryEnd['卖出费用']) > 0.001:
        logger.error('卖出费用计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '卖出费用计算不正确'
    # 判断拥股数量是否正确
    elif QueryInit['拥股数量'] +data['qty_traded']!= QueryEnd['拥股数量']:
        logger.error('拥股数量计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '拥股数量计算不正确'
    # 判断可用股份数是否正确
    elif QueryInit['可卖出证券数'] != QueryEnd['可卖出证券数']:
        logger.error('可卖出证券数计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '可卖出证券数计算不正确'
    # 判断卖出费用下单前后是否一致
    elif abs(QueryEnd['持仓成本'] - cccb) > 0.001:
        logger.error('持仓成本计算不正确')
        Check_reslut['检查状态'] = 'end'
        logger.info(str(QueryInit['持仓成本'])+','+str(QueryEnd['持仓成本'])+','+str(cccb))
        Check_reslut['错误信息'] = '持仓成本计算不正确'
    # 判断卖出费用下单前后是否一致,浮动盈亏暂不考虑
    # elif abs(QueryInit['浮动盈亏'] - QueryEnd['浮动盈亏']) > 0.001:
    #     print '浮动盈亏计算不正确'
    #     Check_reslut['检查状态'] = 'end'
    #     Check_reslut['错误信息'] = '浮动盈亏计算不正确'
    else:
        Check_reslut['检查状态'] = 'end'
        Check_reslut['测试结果'] = True
        logger.info('资金股份验证正确')

    return Check_reslut

def partCancel_S(QueryInit, QueryEnd,fee,data):
    Check_reslut = {
        '检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
    }
    # 判断股票代码和市场是否一致
    if QueryInit['股票代码'] != QueryEnd['股票代码'] or QueryInit['市场'] != QueryEnd['市场']:
        logger.error('QueryInit和QueryEnd的股票代码或市场不一致')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = 'QueryInit和QueryEnd的股票代码或市场不一致'
    # 判断可用资金
    elif abs(QueryInit['可用资金'] + data['trade_amount'] - fee - QueryEnd['可用资金']) > 0.01:
        logger.error('可用资金计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '可用资金计算不正确'
    # 判断买入资金下单前后是否一致
    elif abs(QueryInit['买入资金'] - QueryEnd['买入资金']) > 0.001:
        logger.error('买入资金计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '买入资金计算不正确'
    # 判断买入费用下单前后是否一致
    elif abs(QueryInit['买入费用'] - QueryEnd['买入费用']) > 0.001:
        logger.error('买入费用计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '买入费用计算不正确'
    # 判断卖出资金是否正确
    elif abs(QueryInit['卖出资金'] + data['trade_amount'] - QueryEnd['卖出资金']) > 0.01:
        logger.error('卖出资金计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '卖出资金计算不正确'
    # 判断卖出费用下是否正确
    elif abs(QueryInit['卖出费用'] + fee - QueryEnd['卖出费用']) > 0.01:
        logger.error('卖出费用计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '卖出费用计算不正确'
    # 判断拥股数量是否正确
    elif QueryInit['拥股数量'] - data['qty_traded'] != QueryEnd['拥股数量']:
        logger.error('拥股数量计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '拥股数量计算不正确'
    # 判断可用股份数是否正确
    elif QueryInit['可卖出证券数'] - data['qty_traded']!= QueryEnd['可卖出证券数']:
        logger.error('可卖出证券数计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '可卖出证券数计算不正确'
    # 判断卖出费用下单前后是否一致
    elif abs(QueryInit['持仓成本'] - QueryEnd['持仓成本']) > 0.001:
        logger.error('持仓成本计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '持仓成本计算不正确'
    # 判断卖出费用下单前后是否一致,浮动盈亏暂不考虑
    # elif abs(QueryInit['浮动盈亏'] - QueryEnd['浮动盈亏']) > 0.001:
    #     print '浮动盈亏计算不正确'
    #     Check_reslut['检查状态'] = 'end'
    #     Check_reslut['错误信息'] = '浮动盈亏计算不正确'
    else:
        Check_reslut['检查状态'] = 'end'
        Check_reslut['测试结果'] = True
        logger.info('资金股份验证正确')

    return Check_reslut
