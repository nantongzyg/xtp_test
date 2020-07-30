#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/service")
import ServiceConfig
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from getUpOrDownPrice import *
from QueryAllotmentStkInfoDB import *
from database_manager import QueryTable
from mysql_config import fund_creation


#报单状态为'未成交'，资金股份校验
def fundStkCheck_nomatch(Api,QueryInit,QueryEnd,wt_reqs,case_goal):
    logger.info('未成交状态报单资金股份校验')
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
    # 拆分合并
    if wt_reqs['side'] in (Api.const.XTP_SIDE_TYPE['XTP_SIDE_SPLIT'], Api.const.XTP_SIDE_TYPE['XTP_SIDE_MERGE']):
        rs = nomatch(QueryInit, QueryEnd, wt_reqs, Api)
    else:
        err_msg = '买卖方向错误，' + str(wt_reqs['side'])
        logger.error(err_msg)
        rs = {
        '检查状态': 'end',
        '测试结果': False,
        '错误信息': err_msg,
        }

    return rs

def nomatch(QueryInit,QueryEnd,wt_reqs,Api):
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
    elif abs(QueryInit['可用资金'] - QueryEnd['可用资金']) > 0.01:
        logger.error('可用资金预冻结不正确')
        Check_reslut['检查状态']='end'
        Check_reslut['错误信息'] = '可用资金预冻结不正确'
    # 判断总资产
    elif abs(QueryInit['总资产'] - QueryEnd['总资产']) > 0.01:
        logger.error('总资产计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '总资产计算不正确'
    # 判断预扣资金
    elif abs(QueryEnd['预扣资金'] - QueryInit['预扣资金']) > 0.01:
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
    elif QueryInit['可用股份数']!=QueryEnd['可用股份数']:
        logger.error('可用股份数计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '可用股份数计算不正确'
    # 判断持仓成本下单前后是否一致
    elif abs(QueryInit['持仓成本'] - QueryEnd['持仓成本']) > 0.001:
        logger.error('持仓成本计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '持仓成本计算不正确'
    # 判断浮动盈亏下单前后是否一致
    elif abs(QueryInit['浮动盈亏'] - QueryEnd['浮动盈亏']) > 0.001:
        logger.error('浮动盈亏计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '浮动盈亏计算不正确'
    #判断昨日持仓是否正确
    elif QueryInit['昨日持仓']!=QueryEnd['昨日持仓']:
        logger.error('昨日持仓计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '昨日持仓计算不正确'
    #判断今日可申购赎回持仓是否正确
    elif QueryInit['今日可申购赎回持仓'] != QueryEnd['今日可申购赎回持仓']:
        logger.error('今日可申购赎回持仓计算不正确')
        Check_reslut['检查状态'] = 'end'
        Check_reslut['错误信息'] = '今日可申购赎回持仓计算不正确'
    else:
        Check_reslut['检查状态'] = 'end'
        Check_reslut['测试结果'] = True
        logger.info('资金股份验证正确')

    return Check_reslut

#报单状态为'废单'资金股份校验（资金股份前后不变）
def fundStkCheck_other(QueryInit,QueryEnd):
    logger.info('已撤状态报单资金股份校验')
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