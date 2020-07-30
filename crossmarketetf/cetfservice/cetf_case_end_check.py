#!/usr/bin/python
# -*- encoding: utf-8 -*-
from service.log import *

def cetf_case_end_check(bdhb_rs, bdquery_rs, cdquery_rs, cjhb_rs,
                     expectStatus):
    """
    根据报单推送结果/报单查询结果/撤单查询结果/成交回报结果 等进行ETF用例执行结果检查
    :param Api:
    :param bdhb_rs: 报单推送结果
    :param bdquery_rs: 报单查询结果
    :param cdquery_rs: 撤单查询结果
    :param cjhb_rs: 成交回报结果
    :param expectStatus: 期望状态
    :param pricetype: 价格类型
    :return:
    """
    logger.info('CaseEndCheck校验开始')
    #定义检查结果集
    result={
        '测试结果':False,
        '错误原因':'',
        '错误源':'',
    }
    # 期望状态：全成，检查点包含：成交回报、报单查询、报单推送
    if expectStatus == '全成':
        rs=checkDetail_1(bdhb_rs, bdquery_rs, cjhb_rs)
        result['测试结果'] = rs['测试结果']
        result['错误原因'] = rs['错误原因']
        result['错误源'] = rs['错误源']
    # 期望状态：内部撤单，检查点包含：报单查询、撤单查询、报单推送
    elif expectStatus =='内部撤单':
        checkDetail_2(bdhb_rs,bdquery_rs, cdquery_rs)
        checkDetail_2_1(bdhb_rs,bdquery_rs)
        TODO

    # 期望状态:未成交／废单，检查点包含：报单查询、报单推送
    elif expectStatus == '废单':
        rs = checkDetail_3(bdhb_rs, bdquery_rs)
        result['测试结果'] = rs['测试结果']
        result['错误原因'] = rs['错误原因']
        result['错误源'] = rs['错误源']
    # 其他期望状态
    else:
        TODO
    logger.info('CaseEndCheck校验结束')

    return result


def checkDetail_1(bdhb_rs,bdquery_rs,cjhb_rs):
    """
    期望状态为全部成交时，结果检查函数
    :param bdhb_rs: 报单推送结果
    :param bdquery_rs: 报单查询结果
    :param cjhb_rs: 成交回报结果
    :param expectStatus: 期望状态
    :return:
    """
    # 定义检查结果集
    result = {
        '测试结果': False,
        '错误原因': '',
        '错误源': '',
    }
    #检查各检查项是否正确
    if bdhb_rs['测试结果'] == False:
        result['错误原因'] = bdhb_rs['错误信息']
        result['错误源'] = '报单推送'
    elif bdquery_rs['测试结果'] == False:
        result['错误原因']=bdquery_rs['错误信息']
        result['错误源']='报单查询'
    elif cjhb_rs['测试结果'] == False:
        result['错误原因'] = cjhb_rs['测试错误原因']
        result['错误源'] = '成交回报'
    #检查xtpID是否一致
    elif bdhb_rs['xtpID'] != cjhb_rs['xtp_id']:
        logger.error('报单推送的xtpID与成交回报的xtpID不一致,bdhb_rs的xtpID=' +
                     str(bdhb_rs['xtpID'])+'，cjhb_rs的xtp_id=' +
                     str(cjhb_rs['xtp_id']))
        result['错误原因'] = '报单推送的xtpID与成交回报的xtpID不一致'
        result['错误源'] = '报单推送或成交回报'
    elif bdquery_rs['xtpID'] != bdhb_rs['xtpID']:
        logger.error('报单查询的xtpID与报单推送的xtpID不一致,bdhb_rs的xtpID=' +
                     str(bdhb_rs['xtpID']) + '，bdquery_rs的xtp_id=' +
                     str(bdquery_rs['xtp_id']))
        result['错误原因'] = '报单查询的xtpID与报单推送的xtpID不一致'
        result['错误源'] = '报单查询或报单推送'
    else:
        result['测试结果'] = True

    return result

def checkDetail_2(bdhb_rs, bdquery_rs, cdquery_rs):
    """
    期望状态为内部撤单时，结果检查函数
    :param bdquery_rs:
    :param cdquery_rs:
    :param bdhb_rs:
    :return:
    """


def checkDetail_2_1(bdhb_rs, bdquery_rs):
    """
    期望状态为内部撤单时，结果检查函数
    :param bdquery_rs:
    :param bdhb_rs:
    :return:
    """



def checkDetail_3(bdhb_rs, bdquery_rs):
    """
    期望状态为废单时，结果检查函数
    :param bdhb_rs: 报单推送结果
    :param bdquery_rs: 报单查询结果
    :return:
    """
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
        logger.error('报单查询的xtpID与报单推送的xtpID不一致，'
                     '报单查询和报单推送的xtpID分别是'+str(bdquery_rs['xtpID'])
                     +','+str(bdhb_rs['xtpID']))
        result['错误原因'] = '报单查询的xtpID与报单推送的xtpID不一致'
        result['错误源'] = '报单查询或报单推送'
    elif bdquery_rs['成交数量'] != bdhb_rs['成交数量']:
        logger.error('报单查询的成交数量与报单推送的成交数量不一致,'
                     '报单查询和报单推送的成交数量分别是'+str(bdquery_rs['成交数量'])
                     +','+str(bdhb_rs['成交数量']))
        result['错误原因'] = '报单查询的成交数量与报单推送的成交数量不一致'
        result['错误源'] = '报单查询或报单推送'
    elif bdquery_rs['成交金额'] != bdhb_rs['成交金额']:
        logger.error('报单查询的成交金额与报单推送的成交金额不一致,'
                     '报单查询和报单推送的成交金额分别是'+str(bdquery_rs['成交金额'])
                     +','+str(bdhb_rs['成交金额']))
        result['错误原因'] = '报单查询的成交金额与报单推送的成交金额不一致'
        result['错误源'] = '报单查询或报单推送'

    else:
        result['测试结果'] = True

    return result
