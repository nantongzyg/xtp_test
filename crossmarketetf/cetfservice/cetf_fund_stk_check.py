#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
sys.path.append('/home/yhl2/workspace/xtp_test')
from service.log import *
from crossmarketetf.cetfservice.cetf_get_components_asset import *


def fund_stk_check_other(QueryInit,QueryEnd,component_stk_info,Api):
    """
    报单状态为'全成撤废','废单撤废',etf和其成分股资金股份校验（资金股份前后不变）
    :param QueryInit: 
    :param QueryEnd: 
    :param component_stk_info: 
    :param Api: 
    :return: 
    """
    logger.info('撤废状态报单资金股份校验')
    reslut = {
        '检查状态': 'init',
        '测试结果': False,
        '错误信息': '',
    }
    # ---------ETF----------
    # 判断股票代码和市场是否一致
    if QueryInit['股票代码'] != QueryEnd['股票代码'] or QueryInit['市场'] != QueryEnd['市场']:
        logger.error('ETF的QueryInit和QueryEnd的股票代码或市场不一致')
        reslut['检查状态'] = 'end'
        reslut['错误信息'] = 'ETF的QueryInit和QueryEnd的股票代码或市场不一致'
    # 判断可用资金
    elif abs(QueryInit['可用资金'] - QueryEnd['可用资金']) > 0.001:
        logger.info('可用资金：'+str(abs(QueryInit['可用资金'] - QueryEnd['可用资金'])))
        logger.error('ETF可用资金预冻结不正确')
        reslut['检查状态'] = 'end'
        reslut['错误信息'] = 'ETF可用资金预冻结不正确'
    # 判断买入资金下单前后是否一致
    elif abs(QueryInit['买入资金'] - QueryEnd['买入资金']) > 0.001:
        logger.error('ETF买入资金计算不正确')
        reslut['检查状态'] = 'end'
        reslut['错误信息'] = 'ETF买入资金计算不正确'
    # 判断买入费用下单前后是否一致
    elif abs(QueryInit['买入费用'] - QueryEnd['买入费用']) > 0.001:
        logger.error('ETF买入费用计算不正确')
        reslut['检查状态'] = 'end'
        reslut['错误信息'] = 'ETF买入费用计算不正确'
    # 判断卖出资金下单前后是否一致
    elif abs(QueryInit['卖出资金'] - QueryEnd['卖出资金']) > 0.001:
        logger.error('ETF卖出资金计算不正确')
        reslut['检查状态'] = 'end'
        reslut['错误信息'] = 'ETF卖出资金计算不正确'
    # 判断卖出费用下单前后是否一致
    elif abs(QueryInit['卖出费用'] - QueryEnd['卖出费用']) > 0.001:
        logger.error('ETF卖出费用计算不正确')
        reslut['检查状态'] = 'end'
        reslut['错误信息'] = 'ETF卖出费用计算不正确'
    # 判断拥股数量是否正确
    elif QueryInit['预扣资金'] != QueryEnd['预扣资金']:
        logger.error('ETF预扣资金计算不正确')
        reslut['检查状态'] = 'end'
        reslut['错误信息'] = 'ETF预扣资金计算不正确'
    # 判断可用股份数是否正确
    elif QueryInit['总资产'] != QueryEnd['总资产']:
        logger.error('ETF总资产计算不正确')
        reslut['检查状态'] = 'end'
        reslut['错误信息'] = 'ETF总资产计算不正确'
    # 判断可用股份数是否正确
    elif QueryInit['总持仓'] != QueryEnd['总持仓']:
        logger.error('ETF总持仓计算不正确')
        reslut['检查状态'] = 'end'
        reslut['错误信息'] = 'ETF总持仓计算不正确'
    # 判断可用股份数是否正确
    elif QueryInit['可卖持仓'] != QueryEnd['可卖持仓']:
        logger.error('ETF可卖持仓计算不正确')
        reslut['检查状态'] = 'end'
        reslut['错误信息'] = 'ETF可卖持仓计算不正确'
    # 判断可用股份数是否正确
    elif QueryInit['昨日持仓'] != QueryEnd['昨日持仓']:
        logger.error('ETF昨日持仓计算不正确')
        reslut['检查状态'] = 'end'
        reslut['错误信息'] = 'ETF昨日持仓计算不正确'
        # 判断可用股份数是否正确
    elif QueryInit['今日可申购赎回持仓'] != QueryEnd['今日可申购赎回持仓']:
        logger.error('ETF今日可申购赎回持仓计算不正确')
        reslut['检查状态'] = 'end'
        reslut['错误信息'] = 'ETF今日可申购赎回持仓计算不正确'
    # 判断卖出费用下单前后是否一致
    elif abs(QueryInit['持仓成本价'] - QueryEnd['持仓成本价']) > 0.001:
        logger.error('ETF持仓成本价计算不正确')
        reslut['检查状态'] = 'end'
        reslut['错误信息'] = 'ETF持仓成本价计算不正确'
    # 判断卖出费用下单前后是否一致
    elif abs(QueryInit['浮动盈亏'] - QueryEnd['浮动盈亏']) > 0.001:
        logger.error('ETF浮动盈亏计算不正确')
        reslut['检查状态'] = 'end'
        reslut['错误信息'] = 'ETF浮动盈亏计算不正确'
    else:
        reslut['检查状态'] = 'end'
        reslut['测试结果'] = True
        logger.info('ETF资金股份验证正确')
    # --------成分股---------
    if isinstance(component_stk_info, dict):
        stk_info =  component_stk_info
    else:
        stk_info = ()
        if component_stk_info:
            stk_info = component_stk_info[0]

    if stk_info != ():
        for code in stk_info:
            reslut = {
                '检查状态': 'init',
                '测试结果': False,
                '错误信息': '',
            }
            component_stk_info_one = cetf_get_one_component_stk(Api,code)
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
                reslut['检查状态'] = 'end'
                reslut['错误信息'] = '申购前后成分股的股票代码或市场不一致'
            # 判断可用股份数是否正确
            elif StkInit['总持仓'] != StkEnd['总持仓']:
                logger.error('成分股' + code + '总持仓计算不正确'
                             '申赎前后总持仓分别为： ' +
                             str(StkInit['总持仓']) + ', ' + str(StkEnd['总持仓']))
                reslut['检查状态'] = 'end'
                reslut['错误信息'] = '成分股总持仓计算不正确'
            # 判断可用股份数是否正确
            elif StkInit['可卖持仓'] != StkEnd['可卖持仓']:
                logger.error('成分股' + code + '可卖持仓计算不正确'
                             '申赎前后可卖持仓分别为： ' +
                             str(StkInit['可卖持仓']) + ', '
                             + str(StkEnd['可卖持仓']))
                reslut['检查状态'] = 'end'
                reslut['错误信息'] = '成分股可卖持仓计算不正确'
            # 判断可用股份数是否正确
            elif StkInit['昨日持仓'] != StkEnd['昨日持仓']:
                logger.error('成分股' + code + '昨日持仓计算不正确'
                             '申赎前后昨日持仓分别为： ' +
                             str(StkInit['昨日持仓']) + ', '
                             + str(StkEnd['昨日持仓']))
                reslut['检查状态'] = 'end'
                reslut['错误信息'] = '成分股昨日持仓计算不正确'
                # 判断可用股份数是否正确
            elif StkInit['今日可申购赎回持仓'] != StkEnd['今日可申购赎回持仓']:
                logger.error('成分股' + code + '今日可申购赎回持仓计算不正确'
                             '申赎前后今日可申购赎回持仓分别为： ' +
                             str(StkInit['今日可申购赎回持仓']) + ', '
                             + str(StkEnd['今日可申购赎回持仓']))
                reslut['检查状态'] = 'end'
                reslut['错误信息'] = '成分股今日可申购赎回持仓计算不正确'
            # 判断卖出费用下单前后是否一致
            elif abs(StkInit['持仓成本价'] - StkEnd['持仓成本价']) > 0.001:
                logger.error('成分股' + code + '持仓成本价计算不正确'
                             '申赎前后持仓成本价分别为： ' +
                             str(StkInit['持仓成本价']) + ', '
                             + str(StkEnd['持仓成本价']))
                reslut['检查状态'] = 'end'
                reslut['错误信息'] = '成分股持仓成本价计算不正确'
            # 判断卖出费用下单前后是否一致
            elif abs(StkInit['浮动盈亏'] - StkEnd['浮动盈亏']) > 0.001:
                logger.error('成分股' + code + '浮动盈亏计算不正确'
                             '申赎前后浮动盈亏分别为： ' +
                             str(StkInit['浮动盈亏']) + ', '
                             + str(StkEnd['浮动盈亏']))
                reslut['检查状态'] = 'end'
                reslut['错误信息'] = '成分股浮动盈亏计算不正确'
            else:
                reslut['检查状态'] = 'end'
                reslut['测试结果'] = True
                logger.info('成分股' + code + '资金股份验证正确')

            if reslut['测试结果'] is False:
                return reslut

    return reslut
