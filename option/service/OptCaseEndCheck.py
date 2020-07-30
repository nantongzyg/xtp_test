#!/usr/bin/python
# -*- encoding: utf-8 -*-
from log import *
from OptGetCancelType import *

def caseEndCheck(Api,bdhb_rs, bdquery_rs, cdquery_rs, cjhb_rs, expectStatus,pricetype):
    logger.info('CaseEndCheck校验开始')
    #定义检查结果集
    result={
        '测试结果':False,
        '错误原因':'',
        '错误源':'',
    }
    # 期望状态：全成／部成，检查点包含：成交回报、报单查询、报单推送
    if expectStatus in ('全成','部成'):
        rs=checkDetail_1(bdquery_rs, bdhb_rs, cjhb_rs,expectStatus)
        result['测试结果'] = rs['测试结果']
        result['错误原因'] = rs['错误原因']
        result['错误源'] = rs['错误源']

    # 期望状态：／部撤／已撤／已报待撤／部撤已报／撤废，检查点包含：报单查询、撤单查询、报单推送
    elif expectStatus in ('部撤','已撤','已报待撤','部撤已报','撤废','内部撤单'):
        # if pricetype not in(Api.const.XTP_PRICE_TYPE['XTP_PRICE_BEST_OR_CANCEL'],Api.const.XTP_PRICE_TYPE['XTP_PRICE_BEST5_OR_CANCEL'],Api.const.XTP_PRICE_TYPE['XTP_PRICE_ALL_OR_CANCEL']) or expectStatus=='内部撤单':
        if getCancelType(Api,pricetype,expectStatus):
            rs = checkDetail_2(bdquery_rs, cdquery_rs, bdhb_rs, expectStatus)
            result['测试结果'] = rs['测试结果']
            result['错误原因'] = rs['错误原因']
            result['错误源'] = rs['错误源']
        else:
            rs = checkDetail_2_1(bdquery_rs, bdhb_rs)
            result['测试结果'] = rs['测试结果']
            result['错误原因'] = rs['错误原因']
            result['错误源'] = rs['错误源']


    # 期望状态:未成交／废单，检查点包含：报单查询、报单推送
    elif expectStatus in ('未成交','废单'):
        rs = checkDetail_3(bdquery_rs, bdhb_rs)
        result['测试结果'] = rs['测试结果']
        result['错误原因'] = rs['错误原因']
        result['错误源'] = rs['错误源']
    #期望状态:’初始‘,只有报单查询
    else:
        if bdquery_rs['测试结果']==False:
            result['测试结果'] = bdquery_rs['测试结果']
            result['错误原因'] = bdquery_rs['错误信息']
            result['错误源']='报单查询'
        else:
            result['测试结果']=True
    logger.info('CaseEndCheck校验结束')

    return result


def checkDetail_1(bdquery_rs,bdhb_rs,cjhb_rs,expectStatus):
    # 定义检查结果集
    result = {
        '测试结果': False,
        '错误原因': '',
        '错误源': '',
    }
    #检查各检查项是否正确
    if bdquery_rs['测试结果']==False:
        result['错误原因']=bdquery_rs['错误信息']
        result['错误源']='报单查询'
    elif bdhb_rs['测试结果']==False:
        result['错误原因'] = bdhb_rs['错误信息']
        result['错误源'] = '报单推送'
    elif cjhb_rs['测试结果']==False:
        result['错误原因'] = cjhb_rs['测试错误原因']
        result['错误源'] = '成交回报'
    #检查xtpID是否一致
    elif bdhb_rs['xtpID']!=cjhb_rs['xtp_id']:
        logger.error('报单推送的xtpID与成交回报的xtpID不一致,bdhb_rs的xtpID='+str(bdhb_rs['xtpID'])+'，cjhb_rs的xtp_id='+str(cjhb_rs['xtp_id']))
        result['错误原因'] = '报单推送的xtpID与成交回报的xtpID不一致'
        result['错误源'] = '报单推送或成交回报'
    elif bdquery_rs['xtpID']!=bdhb_rs['xtpID']:
        logger.error('报单查询的xtpID与报单推送的xtpID不一致,bdhb_rs的xtpID=' + str(bdhb_rs['xtpID']) + '，bdquery_rs的xtp_id=' + str(
            bdquery_rs['xtp_id']))
        result['错误原因'] = '报单查询的xtpID与报单推送的xtpID不一致'
        result['错误源'] = '报单查询或报单推送'

    else:
        if expectStatus == '全成':
            # 检查报单的成交金额是否与成交回报成交金额一致
            if abs(bdhb_rs['成交金额'] - cjhb_rs['成交金额'])>0.01:
                logger.error('报单推送的成交金额与成交回报的成交金额不一致,报单回报和成交回报的成交金额分别是'+str(bdhb_rs['成交金额'])+','+str(cjhb_rs['成交金额']))
                result['错误原因'] = '报单推送的成交金额与成交回报的成交金额不一致'
                result['错误源'] = '报单推送或成交回报'
            elif bdhb_rs['成交数量'] != cjhb_rs['成交数量']:
                logger.error(
                    '报单推送的成交数量与成交回报的成交数量不一致,报单回报和成交回报的成交数量分别是' + str(bdhb_rs['成交数量']) + ',' + str(cjhb_rs['成交数量']))
                result['错误原因'] = '报单推送的成交数量与成交回报的成交数量不一致'
                result['错误源'] = '报单推送或成交回报'
            elif bdhb_rs['成交金额'] != bdquery_rs['成交金额']:
                logger.error(
                    '报单推送的成交金额与报单查询的成交金额不一致,报单回报和报单查询的成交金额分别是' + str(bdhb_rs['成交金额']) + ',' + str(bdquery_rs['成交金额']))
                result['错误原因'] = '报单推送的成交金额与报单查询的成交金额不一致'
                result['错误源'] = '报单推送或报单查询'
            elif bdhb_rs['成交数量'] != bdquery_rs['成交数量']:
                logger.error(
                    '报单推送的成交数量与报单查询的成交数量不一致,报单回报和报单查询的成交数量分别是' + str(bdhb_rs['成交数量']) + ',' + str(bdquery_rs['成交数量']))
                result['错误原因'] = '报单推送的成交数量与报单查询的成交数量不一致'
                result['错误源'] = '报单推送或报单查询'
            elif bdhb_rs['委托价格'] != bdquery_rs['委托价格']:
                logger.error(
                    '报单推送的委托价格与报单查询的委托价格不一致,报单回报和报单查询的委托价格分别是' + str(bdhb_rs['委托价格']) + ',' + str(bdquery_rs['委托价格']))
                result['错误原因'] = '报单推送的委托价格与报单查询的委托价格不一致'
                result['错误源'] = '报单推送或报单查询'
            else:
                result['测试结果'] = True
        else:
            # 检查报单查询的成交金额是否与成交回报成交金额一致
            if abs(bdquery_rs['成交金额'] - cjhb_rs['成交金额'])>0.01:
                logger.error(
                    '报单查询的成交金额与成交回报的成交金额不一致,报单查询和成交回报的成交金额分别是' + str(bdquery_rs['成交金额']) + ',' + str(cjhb_rs['成交金额']))
                result['错误原因'] = '报单查询的成交金额与成交回报的成交金额不一致'
                result['错误源'] = '报单查询或成交回报'
            # 检查报单查询的成交数量是否与成交回报成交数量一致
            elif bdquery_rs['成交数量'] != cjhb_rs['成交数量']:
                logger.error(
                    '报单查询的成交数量与成交回报的成交数量不一致,报单查询和成交回报的成交数量分别是' + str(bdquery_rs['成交数量']) + ',' + str(cjhb_rs['成交数量']))
                result['错误原因'] = '报单查询的成交数量与成交回报的成交数量不一致'
                result['错误源'] = '报单查询或成交回报'
            else:
                result['测试结果'] = True

    return result

def checkDetail_2(bdquery_rs, cdquery_rs, bdhb_rs,expectStatus):
    # 定义检查结果集
    result = {
        '测试结果': False,
        '错误原因': '',
        '错误源': '',
    }
    # 检查各检查项是否正确
    if bdquery_rs['测试结果'] == False:
        result['错误原因'] = bdquery_rs['错误信息']
        result['错误源'] = '报单查询'
    elif bdhb_rs['测试结果'] == False:
        result['错误原因'] = bdhb_rs['错误信息']
        result['错误源'] = '报单推送'
    elif cdquery_rs['测试结果'] == False:
        result['错误原因'] = cdquery_rs['测试错误原因']
        result['错误源'] = '成交回报'
    # 检查xtpID是否一致
    elif bdquery_rs['xtpID'] != bdhb_rs['xtpID']:
        logger.error('报单查询的xtpID与报单推送的xtpID不一致,bdquery_rs的xtpID=' + str(bdquery_rs['xtpID']) + '，bdhb_rs的xtp_id=' + str(
            bdhb_rs['xtp_id']))
        result['错误原因'] = '报单查询的xtpID与报单推送的xtpID不一致'
        result['错误源'] = '报单查询或报单推送'
    else:
        if expectStatus in('部撤已报','已报待撤'):
            result['测试结果'] = True
        else:
            # 检查报单查询和报单推送成交金额／成交数量／剩余数量／委托时间是否一致
            if bdquery_rs['成交金额'] != bdhb_rs['成交金额']:
                logger.error(
                    '报单查询的成交金额与报单推送的成交金额不一致,报单查询和报单推送的成交金额分别是' + str(bdquery_rs['成交金额']) + ',' + str(bdhb_rs['成交金额']))
                result['错误原因'] = '报单查询的成交金额与报单推送的成交金额不一致'
                result['错误源'] = '报单查询或报单推送'
            elif bdquery_rs['成交数量'] != bdhb_rs['成交数量']:
                logger.error(
                    '报单查询的成交数量与报单推送的成交数量不一致,报单查询和报单推送的成交数量分别是' + str(bdquery_rs['成交数量']) + ',' + str(bdhb_rs['成交数量']))
                result['错误原因'] = '报单查询的成交数量与报单推送的成交数量不一致'
                result['错误源'] = '报单查询或报单推送'
            elif bdquery_rs['剩余数量'] != bdhb_rs['剩余数量']:
                logger.error(
                    '报单查询的剩余数量与报单推送的剩余数量不一致,报单查询和报单推送的剩余数量分别是' + str(bdquery_rs['剩余数量']) + ',' + str(bdhb_rs['剩余数量']))
                result['错误原因'] = '报单查询的剩余数量与报单推送的剩余数量不一致'
                result['错误源'] = '报单查询或报单推送'
            elif cdquery_rs['xtpID'] != bdhb_rs['cancel_xtpID']:
                logger.error(
                    '撤单报单查询的xtpID与报单推送的cancel_xtpID不一致,撤单查询和报单推送的的cancel_xtpID分别是' + str(cdquery_rs['xtpID']) + ',' + str(bdhb_rs['cancel_xtpID']))
                result['错误原因'] = '撤单报单查询的xtpID与报单推送的cancel_xtpID不一致'
                result['错误源'] = '撤单报单查询或报单推送'
            else:
                if expectStatus in('部撤','已撤','内部撤单'):
                    if cdquery_rs['成交数量'] != bdhb_rs['剩余数量']:
                        logger.error('撤单报单查询的成交数量与原报单的剩余数量不一致,撤单查询和报单查询的剩余数量分别为'+str(cdquery_rs['成交数量'])+','+str(bdhb_rs['剩余数量']))
                        result['错误原因'] = '撤单报单查询的成交数量与原报单的剩余数量不一致'
                        result['错误源'] = '撤单查询或报单推送'
                    else:
                        result['测试结果'] = True
                else:
                    result['测试结果'] = True

    return result


def checkDetail_2_1(bdquery_rs, bdhb_rs):
    # 定义检查结果集
    result = {
        '测试结果': False,
        '错误原因': '',
        '错误源': '',
    }
    # 检查各检查项是否正确
    if bdquery_rs['测试结果'] == False:
        result['错误原因'] = bdquery_rs['错误信息']
        result['错误源'] = '报单查询'
    elif bdhb_rs['测试结果'] == False:
        result['错误原因'] = bdhb_rs['错误信息']
        result['错误源'] = '报单推送'
    # 检查xtpID是否一致
    elif bdquery_rs['xtpID'] != bdhb_rs['xtpID']:
        logger.error('报单查询的xtpID与报单推送的xtpID不一致,报单查询和报单回报的xtpID分别是'+str(bdquery_rs['xtpID'])+','+str(bdhb_rs['xtpID']))
        result['错误原因'] = '报单查询的xtpID与报单推送的xtpID不一致'
        result['错误源'] = '报单查询或报单推送'
    # 检查报单查询的cancel_xtpID是否和报单推送的cancel_xtpID一致
    # elif bdquery_rs['cancel_xtpID'] != bdhb_rs['cancel_xtpID']:
    #     result['错误原因'] = '报单查询的cancel_xtpID与报单推送的cancel_xtpID不一致'
    #     result['错误源'] = '报单查询或报单推送'
    # 检查报单查询和报单推送成交金额／成交数量／剩余数量／委托时间是否一致
    elif bdquery_rs['成交金额'] != bdhb_rs['成交金额']:
        logger.error('报单查询的成交金额与报单推送的成交金额不一致,报单查询和报单推送的成交金额分别是'+str(bdquery_rs['成交金额'])+','+str(bdhb_rs['成交金额']))
        result['错误原因'] = '报单查询的成交金额与报单推送的成交金额不一致'
        result['错误源'] = '报单查询或报单推送'
    elif bdquery_rs['成交数量'] != bdhb_rs['成交数量']:
        logger.error('报单查询的成交数量与报单推送的成交数量不一致，报单查询和报单推送的成交数量分别是'+str(bdquery_rs['成交数量'])+','+str(bdhb_rs['成交数量']))
        result['错误原因'] = '报单查询的成交数量与报单推送的成交数量不一致'
        result['错误源'] = '报单查询或报单推送'
    elif bdquery_rs['剩余数量'] != bdhb_rs['剩余数量']:
        logger.error('报单查询的剩余数量与报单推送的剩余数量不一致，报单查询和报单推送的剩余数量分别是'+str(bdquery_rs['剩余数量'])+','+str(bdhb_rs['剩余数量']))
        result['错误原因'] = '报单查询的剩余数量与报单推送的剩余数量不一致'
        result['错误源'] = '报单查询或报单推送'
    elif bdquery_rs['委托时间'] != bdhb_rs['委托时间']:
        logger.error('报单查询的委托时间与报单推送的委托时间不一致，报单查询和报单推送的委托时分别是'+str(bdquery_rs['委托时间'])+','+str(bdhb_rs['委托时间']))
        result['错误原因'] = '报单查询的委托时间与报单推送的委托时间不一致'
        result['错误源'] = '报单查询或报单推送'
    # elif bdquery_rs['撤销时间'] != bdhb_rs['撤销时间']:
    #     result['错误原因'] = '报单查询的撤销时间与报单推送的撤销时间不一致'
    #     result['错误源'] = '报单查询或报单推送'
    else:
        result['测试结果'] = True

    return result


def checkDetail_3(bdquery_rs, bdhb_rs):
    # 定义检查结果集
    result = {
        '测试结果': False,
        '错误原因': '',
        '错误源': '',
    }
    # 检查各检查项是否正确
    if bdquery_rs['测试结果'] == False:
        result['错误原因'] = bdquery_rs['错误信息']
        result['错误源'] = '报单查询'
    elif bdhb_rs['测试结果'] == False:
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
    # 当前报单查询不显示Err_code和ErrMsg
    # elif bdquery_rs['Err_code'] != bdhb_rs['Err_code']:
    #     result['错误原因'] = '报单查询的Err_code与报单推送的Err_code不一致'
    #     result['错误源'] = '报单查询或报单推送'
    # elif bdquery_rs['ErrMsg'] != bdhb_rs['ErrMsg']:
    #     result['错误原因'] = '报单查询的ErrMsg与报单推送的ErrMsg不一致'
    #     result['错误源'] = '报单查询或报单推送'

    else:
        result['测试结果'] = True

    return result