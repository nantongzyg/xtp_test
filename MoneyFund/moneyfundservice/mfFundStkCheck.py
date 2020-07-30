#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/service")
import ServiceConfig
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/MoneyFund/moneyfundmysql")
from mfgetUpOrDownPrice import *
from mfQueryAllotmentStkInfoDB import *
from decimal import *
sys.path.append("/home/yhl2/workspace/xtp_test/MoneyFund/moneyfundservice")
from mfCjhbDataCheck import getFee
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from QuerySecurityType import *
from GetSecurityType import getSecurityType


#注：部成和全成状态的校验写在了成交回报校验中
#注：初始未成交资金股份检查fundStkCheck_nomatch(Api,QueryInit,QueryEnd,wt_reqs)
#注：部撤资金股份检查fundStkCheck_partCancel(Api,QueryInit,QueryEnd,wt_reqs,data)
#注：'已撤'、'部撤已报'、'已报待撤'、'废单'、'撤废'资金股份检查fundStkCheck_other(QueryInit,QueryEnd)

#---定义费率，最低收费
fee_rate_buy_fixed = ServiceConfig.FEE_RATE_BUY_FIXED
fee_rate_sell_fixed = ServiceConfig.FEE_RATE_SELL_FIXED
fee_rate_buy_special = ServiceConfig.FEE_RATE_BUY_SPECIAL
fee_rate_sell_special = ServiceConfig.FEE_RATE_SELL_SPECIAL
fee_min_buy_special = ServiceConfig.FEE_MIN_BUY_SPECIAL
fee_min_sell_special =ServiceConfig.FEE_MIN_SELL_SPECIAL
fee_addition_buy_fixed = ServiceConfig.FEE_ADDITION_BUY_FIXED
fee_addition_sell_fixed = ServiceConfig.FEE_ADDITION_SELL_FIXED
fee_rate_buy = ServiceConfig.FEE_RATE_BUY
fee_rate_sell = ServiceConfig.FEE_RATE_SELL
fee_min = ServiceConfig.FEE_MIN

fee_etf_rate_buy_fixed=ServiceConfig.FEE_RATE_ETF_BUY_FIXED
fee_etf_rate_sell_fixed=ServiceConfig.FEE_RATE_ETF_SELL_FIXED
fee_etf_rate_buy_special = ServiceConfig.FEE_RATE_ETF_BUY_SPECIAL
fee_etf_rate_sell_special =ServiceConfig.FEE_RATE_ETF_SELL_SPECIAL
fee_etf_min_buy_special =ServiceConfig.FEE_MIN_ETF_BUY_SPECIAL
fee_etf_min_sell_special = ServiceConfig.FEE_MIN_ETF_SELL_SPECIAL
fee_etf_addition_buy_fixed = ServiceConfig.FEE_ADDITION_ETF_BUY_FIXED
fee_etf_addition_sell_fixed=ServiceConfig.FEE_ADDITION_ETF_SELL_FIXED

fee_rate_reverse_repo = ServiceConfig.FEE_RATE_REVERSE_REPO
fee_reverse_repo_min = ServiceConfig.FEE_REVERSE_REPO_MIN

#报单状态为'初始'、'未成交'，资金股份校验
def fundStkCheck_nomatch(Api,QueryInit,QueryEnd,wt_reqs,case_goal):
    logger.info('初始、未成交状态报单资金股份校验')
    fundStkCheck_reslut = {
        '检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
    }
    fee = fee_min
    Prefreezing=0

    if '是否是新股申购' not in case_goal:
        rs = nomatch_bs(Api, QueryInit, QueryEnd, wt_reqs)
        fundStkCheck_reslut['检查状态'] = rs['检查状态']
        fundStkCheck_reslut['测试结果'] = rs['测试结果']
        fundStkCheck_reslut['错误信息'] = rs['错误信息']
    else:
        rs = nomatch_B(QueryInit, QueryEnd, wt_reqs, Prefreezing, Api)
        fundStkCheck_reslut['检查状态'] = rs['检查状态']
        fundStkCheck_reslut['测试结果'] = rs['测试结果']
        fundStkCheck_reslut['错误信息'] = rs['错误信息']
    return fundStkCheck_reslut

def nomatch_bs(Api,QueryInit,QueryEnd,wt_reqs):
    global fee_rate_buy,fee_min
    # 获取涨停价
    upPrice = getUpPrice(wt_reqs['ticker'])
    if wt_reqs['business_type'] == Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_ALLOTMENT']:
        wt_reqs['price'] = QueryAllotmentStkPrice(wt_reqs['ticker'])
    # 如果是买
    if wt_reqs['side'] == Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY'] or \
        wt_reqs['business_type'] == Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_REPO'] or \
        wt_reqs['business_type'] == Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_ALLOTMENT']:
        # 限价
        if wt_reqs['price_type'] == Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT']:
            if wt_reqs['business_type'] == Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_REPO']:
                fee_rate_buy = fee_rate_reverse_repo
                fee_min = fee_reverse_repo_min
                amount = wt_reqs['quantity'] * 100
                fee = max(fee_min,amount * fee_rate_buy)
                fee = float(Decimal(Decimal(str(fee)).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)))
                Prefreezing = amount + fee
            elif wt_reqs['business_type'] == Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_ALLOTMENT']:
                Prefreezing = wt_reqs['quantity'] * wt_reqs['price']
                fee = 0
            else:
                #ETF预扣资金第3位小数非零进一位
                secuid=str(QuerySecuid(wt_reqs['ticker']))
                print 'wt_price = ',wt_reqs['price']
                if secuid in ('14','15','17','19','111') and wt_reqs['price']*1000%10 != 0:
                    wt_reqs['price'] = wt_reqs['price']+0.01-(wt_reqs['price']*1000%10/1000)
                print 'wt_price = ',wt_reqs['price']
                fee = getFee(wt_reqs, upPrice)
                amount = wt_reqs['quantity'] * wt_reqs['price']
                Prefreezing = amount + fee
        # 市价
        else:
            if wt_reqs['business_type'] == Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_REPO']:
                wt_reqs['price'] = ServiceConfig.Reverse_price
                fee_rate_buy = fee_rate_reverse_repo
                fee_min = fee_reverse_repo_min
                amount = wt_reqs['quantity'] * 100
                fee = max(fee_min,amount * fee_rate_buy)
                Prefreezing = amount + fee
            elif wt_reqs['business_type'] == Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_ALLOTMENT']:
                wt_reqs['price'] = QueryAllotmentStkPrice(wt_reqs['ticker'])
                Prefreezing = wt_reqs['quantity'] * wt_reqs['price']
                fee = 0
            else:
                wt_reqs['price'] = upPrice + 0.01
                amount = wt_reqs['quantity'] * wt_reqs['price']
                fee = getFee(wt_reqs, upPrice)
                Prefreezing = amount + fee

        logger.info('fee=' + str(fee))
        rs = nomatch_B(QueryInit, QueryEnd, wt_reqs, Prefreezing, Api)
        return rs

    # 如果是卖,不再预扣交易费用，收到成交回报时再扣除交易费用
    elif wt_reqs['side'] == Api.const.XTP_SIDE_TYPE['XTP_SIDE_SELL']:
        fee = 0
        logger.info('fee=' + str(fee))
        rs = nomatch_S(QueryInit, QueryEnd, wt_reqs, fee)
        return rs

#报单状态为'部撤'，资金股份校验
def fundStkCheck_partCancel(Api,QueryInit,QueryEnd,wt_reqs,data):
    logger.info('部撤状态报单资金股份校验')

    global fee_min,fee_rate_buy,fee_rate_buy_special,  fee_rate_sell_special, fee_min_buy_special, fee_min_sell_special,fee_rate_buy_fixed,fee_rate_sell_fixed,fee_addition_buy_fixed,fee_addition_sell_fixed
    secuid=str(QuerySecuid(wt_reqs['ticker']))
    if secuid in ('14','15','17','19','111') and wt_reqs['side']in (1,2):
        fee_rate_buy_fixed = fee_etf_rate_buy_fixed
        fee_rate_sell_fixed = fee_etf_rate_sell_fixed
        fee_rate_buy_special = fee_etf_rate_buy_special
        fee_rate_sell_special = fee_etf_rate_sell_special
        fee_min_buy_special = fee_etf_min_buy_special
        fee_min_sell_special =fee_etf_min_sell_special
        fee_addition_buy_fixed = fee_etf_addition_buy_fixed
        fee_addition_sell_fixed = fee_etf_addition_sell_fixed
    elif secuid in ('0') and wt_reqs['side']in (1,2):
        fee_rate_buy_fixed = ServiceConfig.FEE_RATE_BUY_FIXED
        fee_rate_sell_fixed = ServiceConfig.FEE_RATE_SELL_FIXED
        fee_rate_buy_special = ServiceConfig.FEE_RATE_BUY_SPECIAL
        fee_rate_sell_special = ServiceConfig.FEE_RATE_SELL_SPECIAL
        fee_min_buy_special = ServiceConfig.FEE_MIN_BUY_SPECIAL
        fee_min_sell_special =ServiceConfig.FEE_MIN_SELL_SPECIAL
        fee_addition_buy_fixed = ServiceConfig.FEE_ADDITION_BUY_FIXED
        fee_addition_sell_fixed = ServiceConfig.FEE_ADDITION_SELL_FIXED
        fee_rate_buy = ServiceConfig.FEE_RATE_BUY
        fee_rate_sell =ServiceConfig.FEE_RATE_SELL
        fee_min = ServiceConfig.FEE_MIN

    fundStkCheck_reslut = {
        '检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
    }
    #初始费用和持仓成本
    #global fee_min,fee_rate_buy
    fee = fee_min
    cccb=QueryInit['持仓成本']
    # 如果是买
    if wt_reqs['side'] == Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY'] or wt_reqs['business_type'] == Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_REPO']:
        # 持仓成本
        cccb = (QueryInit['持仓成本'] * QueryInit['拥股数量'] + data['trade_amount']) / (QueryInit['拥股数量'] + data['qty_traded'])
        #获取逆回购费率，持仓成本
        if wt_reqs['business_type'] == Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_REPO']:
            fee_rate_buy = fee_rate_reverse_repo
            fee_min = fee_reverse_repo_min
            cccb = QueryInit['持仓成本']
        #买入费用
        amount = data['trade_amount']
        fee_fixed = amount * fee_rate_buy_fixed + fee_addition_buy_fixed
        fee_special = max(fee_min_buy_special, amount * fee_rate_buy_special)
        fee_fixed = float(Decimal(Decimal(str(fee_fixed)).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)))
        fee_special = float(Decimal(Decimal(str(fee_special)).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)))
        fee = fee_fixed + fee_special
        
        logger.info('fee=' + str(fee))
        rs = partCancel_B(QueryInit, QueryEnd, cccb, fee,data)
        fundStkCheck_reslut['检查状态'] = rs['检查状态']
        fundStkCheck_reslut['测试结果'] = rs['测试结果']
        fundStkCheck_reslut['错误信息'] = rs['错误信息']
    # 如果是卖
    elif wt_reqs['side'] == Api.const.XTP_SIDE_TYPE['XTP_SIDE_SELL']:
        amount = data['trade_amount']
        fee_fixed = amount * fee_rate_sell_fixed + fee_addition_sell_fixed
        fee_special = max(fee_min_sell_special, amount * fee_rate_sell_special)
        fee_fixed = float(Decimal(Decimal(str(fee_fixed)).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)))
        fee_special = float(Decimal(Decimal(str(fee_special)).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)))
        fee = fee_fixed + fee_special
        
        logger.info('fee=' + str(fee))
        rs = partCancel_S(QueryInit, QueryEnd,fee,data)
        fundStkCheck_reslut['检查状态'] = rs['检查状态']
        fundStkCheck_reslut['测试结果'] = rs['测试结果']
        fundStkCheck_reslut['错误信息'] = rs['错误信息']

    return fundStkCheck_reslut

#报单状态为'已撤'、'部撤已报'、'已报待撤'、'撤废'，资金股份校验（资金股份前后不变）
def fundStkCheck_other(QueryInit,QueryEnd):
    logger.info('已撤、部撤已报、已报待撤、撤废状态报单资金股份校验')
    fundStkCheck_reslut = {
        '检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
    }
    # 判断股票代码和市场是否一致
    if QueryInit['股票代码'] != QueryEnd['股票代码'] or QueryInit['市场'] != QueryEnd['市场']:
        logger.error('QueryInit和QueryEnd的股票代码或市场不一致')
        fundStkCheck_reslut['检查状态'] = 'end'
        fundStkCheck_reslut['错误信息'] = 'QueryInit和QueryEnd的股票代码或市场不一致'
    # 判断可用资金
    elif abs(QueryInit['可用资金'] - QueryEnd['可用资金']) > 0.001:
        logger.info('可用资金：'+str(abs(QueryInit['可用资金'] - QueryEnd['可用资金'])))
        logger.error('可用资金预冻结不正确')
        fundStkCheck_reslut['检查状态'] = 'end'
        fundStkCheck_reslut['错误信息'] = '可用资金预冻结不正确'
    # 判断总资产
    elif abs(QueryInit['总资产'] - QueryEnd['总资产']) > 0.001:
        logger.error('总资产计算不正确')
        fundStkCheck_reslut['检查状态'] = 'end'
        fundStkCheck_reslut['错误信息'] = '总资产计算不正确'
    # 判断预扣资金
    elif abs(QueryInit['预扣资金'] - QueryEnd['预扣资金']) > 0.001:
        logger.error('预扣资金计算不正确')
        fundStkCheck_reslut['检查状态'] = 'end'
        fundStkCheck_reslut['错误信息'] = '预扣资金计算不正确'
    #判断买入资金下单前后是否一致
    elif abs(QueryInit['买入资金'] - QueryEnd['买入资金']) > 0.001:
        logger.error('买入资金计算不正确')
        fundStkCheck_reslut['检查状态'] = 'end'
        fundStkCheck_reslut['错误信息'] = '买入资金计算不正确'
    # 判断买入费用下单前后是否一致
    elif abs(QueryInit['买入费用'] - QueryEnd['买入费用']) > 0.001:
        logger.error('买入费用计算不正确')
        fundStkCheck_reslut['检查状态'] = 'end'
        fundStkCheck_reslut['错误信息'] = '买入费用计算不正确'
    # 判断卖出资金下单前后是否一致
    elif abs(QueryInit['卖出资金'] - QueryEnd['卖出资金']) > 0.001:
        logger.error('卖出资金计算不正确')
        fundStkCheck_reslut['检查状态'] = 'end'
        fundStkCheck_reslut['错误信息'] = '卖出资金计算不正确'
    # 判断卖出费用下单前后是否一致
    elif abs(QueryInit['卖出费用'] - QueryEnd['卖出费用']) > 0.001:
        logger.error('卖出费用计算不正确')
        fundStkCheck_reslut['检查状态'] = 'end'
        fundStkCheck_reslut['错误信息'] = '卖出费用计算不正确'
    # 判断拥股数量是否正确
    elif QueryInit['拥股数量'] != QueryEnd['拥股数量']:
        logger.error('拥股数量计算不正确')
        fundStkCheck_reslut['检查状态'] = 'end'
        fundStkCheck_reslut['错误信息'] = '拥股数量计算不正确'
    # 判断可用股份数是否正确
    elif QueryInit['可用股份数'] != QueryEnd['可用股份数']:
        logger.error('可用股份数计算不正确')
        fundStkCheck_reslut['检查状态'] = 'end'
        fundStkCheck_reslut['错误信息'] = '可用股份数计算不正确'
    # 判断卖出费用下单前后是否一致
    elif abs(QueryInit['持仓成本'] - QueryEnd['持仓成本']) > 0.001:
        logger.error('持仓成本计算不正确')
        fundStkCheck_reslut['检查状态'] = 'end'
        fundStkCheck_reslut['错误信息'] = '持仓成本计算不正确'
    # 判断卖出费用下单前后是否一致
    elif abs(QueryInit['浮动盈亏'] - QueryEnd['浮动盈亏']) > 0.001:
        logger.error('浮动盈亏计算不正确')
        fundStkCheck_reslut['检查状态'] = 'end'
        fundStkCheck_reslut['错误信息'] = '浮动盈亏计算不正确'
    else:
        fundStkCheck_reslut['检查状态'] = 'end'
        fundStkCheck_reslut['测试结果'] = True
        logger.info('资金股份验证正确')

    return fundStkCheck_reslut

def nomatch_B(QueryInit,QueryEnd,wt_reqs,Prefreezing,Api):
    Check_reslut = {
        '检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
    }
    #判断股票代码和市场是否一致
    if QueryInit['股票代码']!=QueryEnd['股票代码'] or QueryInit['市场']!=QueryEnd['市场']:
        logger.error('QueryInit和QueryEnd的股票代码或市场不一致')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = 'QueryInit和QueryEnd的股票代码或市场不一致'
    #判断可用资金
    elif abs(QueryInit['可用资金']-Prefreezing-QueryEnd['可用资金']) > 0.01:
        logger.error('可用资金预冻结不正确')
        Check_reslut['检查状态']='end'
        Check_reslut['错误信息'] = '可用资金预冻结不正确'
    # 判断总资产
    elif abs(QueryInit['总资产'] - QueryEnd['总资产']) > 0.01:
        logger.error('总资产计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '总资产计算不正确'
    # 判断预扣资金
    elif abs(QueryEnd['预扣资金'] - Prefreezing - QueryInit['预扣资金']) > 0.01:
        logger.error('预扣资金计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '预扣资金计算不正确'
    #判断买入资金下单前后是否一致
    elif abs(QueryInit['买入资金']-QueryEnd['买入资金']) > 0.001:
        logger.error('买入资金计算不正确')
        Check_reslut['检查状态']='end'
        Check_reslut['错误信息'] = '买入资金计算不正确'
    #判断买入费用下单前后是否一致
    elif abs(QueryInit['买入费用']-QueryEnd['买入费用']) > 0.001:
        logger.error('买入费用计算不正确')
        Check_reslut['检查状态']='end'
        Check_reslut['错误信息'] = '买入费用计算不正确'
    #判断卖出资金下单前后是否一致
    elif abs(QueryInit['卖出资金']-QueryEnd['卖出资金']) > 0.001:
        logger.error('卖出资金计算不正确')
        Check_reslut['检查状态']='end'
        Check_reslut['错误信息'] = '卖出资金计算不正确'
    #判断卖出费用下单前后是否一致
    elif abs(QueryInit['卖出费用']-QueryEnd['卖出费用']) > 0.001:
        logger.error('卖出费用计算不正确')
        Check_reslut['检查状态']='end'
        Check_reslut['错误信息'] = '卖出费用计算不正确'
    #判断拥股数量是否正确
    elif QueryInit['拥股数量']!=QueryEnd['拥股数量']:
        logger.error('拥股数量计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '拥股数量计算不正确'
   
    #判断可用股份数是否正确
    elif QueryInit['可用股份数']!=QueryEnd['可用股份数'] and wt_reqs['business_type'] != Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_ALLOTMENT']:
        logger.error('可用股份数计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '可用股份数计算不正确'
    elif QueryInit['可用股份数'] - wt_reqs['quantity'] != QueryEnd['可用股份数'] and wt_reqs['business_type'] == Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_ALLOTMENT']:
        logger.error('可用股份数计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '可用股份数计算不正确'
    # 判断卖出费用下单前后是否一致
    elif abs(QueryInit['持仓成本'] - QueryEnd['持仓成本']) > 0.001:
        logger.error('持仓成本计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '持仓成本计算不正确'
    # 判断卖出费用下单前后是否一致
    elif abs(QueryInit['浮动盈亏'] - QueryEnd['浮动盈亏']) > 0.001:
        logger.error('浮动盈亏计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '浮动盈亏计算不正确'
    else:
        Check_reslut['检查状态'] = 'end'
        Check_reslut['测试结果'] = True
        logger.info('资金股份验证正确')

    return Check_reslut

def nomatch_S(QueryInit, QueryEnd,wt_reqs, fee):
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
    elif abs(QueryInit['可用资金'] - fee - QueryEnd['可用资金']) > 0.01:
        logger.error('可用资金预冻结不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '可用资金预冻结不正确'
    # 判断总资产
    elif abs(QueryInit['总资产'] - QueryEnd['总资产']) > 0.01:
        logger.error('总资产计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '总资产计算不正确'
    # 判断预扣资金
    elif abs(QueryEnd['预扣资金'] - fee - QueryInit['预扣资金']) > 0.01:
        logger.error('预扣资金计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '预扣资金计算不正确'
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
    elif QueryInit['拥股数量'] != QueryEnd['拥股数量']:
        logger.error('拥股数量计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '拥股数量计算不正确'
    # 判断可用股份数是否正确
    elif QueryInit['可用股份数']- wt_reqs['quantity'] != QueryEnd['可用股份数']:
        logger.error('可用股份数计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '可用股份数计算不正确'
    # 判断卖出费用下单前后是否一致
    elif abs(QueryInit['持仓成本'] - QueryEnd['持仓成本']) > 0.001:
        logger.error('持仓成本计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '持仓成本计算不正确'
    # 判断卖出费用下单前后是否一致
    elif abs(QueryInit['浮动盈亏'] - QueryEnd['浮动盈亏']) > 0.001:
        logger.error('浮动盈亏计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '浮动盈亏计算不正确'
    else:
        Check_reslut['检查状态'] = 'end'
        Check_reslut['测试结果'] = True
        logger.info('资金股份验证正确')

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
    # 判断总资产
    elif abs(QueryInit['总资产'] - data['trade_amount'] - fee - QueryEnd['总资产']) > 0.01:
        logger.error('总资产计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '总资产计算不正确'
    # 判断预扣资金
    elif abs(QueryInit['预扣资金'] - QueryEnd['预扣资金']) > 0.01:
        logger.error('预扣资金计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '预扣资金计算不正确'
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
    elif QueryInit['拥股数量'] + data['qty_traded']!= QueryEnd['拥股数量']:
        logger.error('拥股数量计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '拥股数量计算不正确'
    # 判断可用股份数是否正确
    elif QueryInit['可用股份数'] + data['qty_traded']!= QueryEnd['可用股份数']:
        logger.error('可用股份数计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '可用股份数计算不正确'
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
    # 判断总资产
    elif abs(QueryInit['总资产'] + data['trade_amount'] - fee - QueryEnd['总资产']) > 0.01:
        logger.error('总资产计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '总资产计算不正确'
    # 判断预扣资金
    elif abs(QueryInit['预扣资金'] - QueryEnd['预扣资金']) > 0.01:
        logger.error('预扣资金计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '预扣资金计算不正确'
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
    elif QueryInit['可用股份数'] - data['qty_traded']!= QueryEnd['可用股份数']:
        logger.error('可用股份数计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '可用股份数计算不正确'
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
