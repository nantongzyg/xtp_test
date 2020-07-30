#!/usr/bin/python
# -*- encoding: utf-8 -*-
from log import *

def caseEndCheck(Api,bdhb_rs, bdquery_rs, cdquery_rs, cjhb_rs, expectStatus,pricetype):
    logger.info('CaseEndCheck校验开始')
    #定义检查结果集
    result = {
        '测试结果':False,
        '错误原因':'',
        '错误源':'',
    }
    # 期望状态：撤废，检查点包含：报单查询、撤单查询、报单推送
    # 期望状态:未成交／废单，检查点包含：报单查询、报单推送
    if expectStatus in ('未成交','废单'):
        rs = checkDetail(bdquery_rs, bdhb_rs)
        result['测试结果'] = rs['测试结果']
        result['错误原因'] = rs['错误原因']
        result['错误源'] = rs['错误源']
    #期望状态:’初始‘,只有报单查询
    else:
        if bdquery_rs['测试结果'] is False:
            result['测试结果'] = bdquery_rs['测试结果']
            result['错误原因'] = bdquery_rs['错误信息']
            result['错误源'] = '报单查询'
        else:
            result['测试结果'] = True
    logger.info('CaseEndCheck校验结束')

    return result

def checkDetail(bdquery_rs, bdhb_rs):
    # 定义检查结果集
    result = {
        '测试结果': False,
        '错误原因': '',
        '错误源': '',
    }
    # 检查各检查项是否正确
    if bdquery_rs['测试结果'] is False:
        result['错误原因'] = bdquery_rs['错误信息']
        result['错误源'] = '报单查询'
    elif bdhb_rs['测试结果'] is False:
        result['错误原因'] = bdhb_rs['错误信息']
        result['错误源'] = '报单推送'
    elif bdquery_rs['xtpID'] != bdhb_rs['xtpID']:
        logger.error('报单查询的xtpID与报单推送的xtpID不一致，报单查询和报单推送的xtpID分别是'+str(bdquery_rs['xtpID'])+','+str(bdhb_rs['xtpID']))
        result['错误原因'] = '报单查询的xtpID与报单推送的xtpID不一致'
        result['错误源'] = '报单查询或报单推送'
    elif bdquery_rs['成交数量'] != bdhb_rs['成交数量']:
        logger.error('报单查询的成交数量与报单推送的成交数量不一致,报单查询和报单推送的成交数量分别是'+str(bdquery_rs['成交数量'])+','+str(bdhb_rs['成交数量']))
        result['错误原因'] = '报单查询的成交数量与报单推送的成交数量不一致'
        result['错误源'] = '报单查询或报单推送'
    elif bdquery_rs['剩余数量'] != bdhb_rs['剩余数量']:
        logger.error('报单查询的剩余数量与报单推送的剩余数量不一致,报单查询和报单推送的剩余数量分别是'+str(bdquery_rs['剩余数量'])+','+str(bdhb_rs['剩余数量']))
        result['错误原因'] = '报单查询的剩余数量与报单推送的剩余数量不一致'
        result['错误源'] = '报单查询或报单推送'
    elif bdquery_rs['成交金额'] != bdhb_rs['成交金额']:
        logger.error('报单查询的成交金额与报单推送的成交金额不一致,报单查询和报单推送的成交金额分别是'+str(bdquery_rs['成交金额'])+','+str(bdhb_rs['成交金额']))
        result['错误原因'] = '报单查询的成交金额与报单推送的成交金额不一致'
        result['错误源'] = '报单查询或报单推送'
    else:
        result['测试结果'] = True

    return result