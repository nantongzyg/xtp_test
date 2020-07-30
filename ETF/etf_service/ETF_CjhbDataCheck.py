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
from QueryEtfinfoDB import QueryCreationRedemptionCash
from QueryCreationRedemUnitDB import QueryCreationRedemUnitDB
import QueryEtfQty
from QueryEtfQty import stkQty
from QueryEstimateCashComponent import QueryEstimateCashComponent
from QueryPreclosePriceDB import QueryCompnentsPreclosePriceDB
from QueryEtfcountDB import QueryEtfcountDB
sys.path.append("/home/yhl2/workspace/xtp_test/ETF/etf_service")
from ETF_Get_Cash_Subtitute_Amount import etf_get_cash_subtitute_amount
from ETF_GetComponentShare import etf_get_one_component_stk
from ETF_GetComponentShare import etf_get_all_component_stk



#---定义费率，最低收费
fee_rate_etf_creation = ServiceConfig.FEE_RATE_ETF_CREATION
fee_rate_etf_redemption = ServiceConfig.FEE_RATE_ETF_REDEMPTION
fee_etf_min = ServiceConfig.FEE_ETF_MIN
#过户费率
fee_count_rate_etf_creation = ServiceConfig.FEE_COUNT_RATE_ETF_CREATION
fee_count_rate_etf_redemption = ServiceConfig.FEE_COUNT_RATE_ETF_REDEMPTION

# 定义etf资金回报对应的数量字段
etf_fund_quantity_min = ServiceConfig.ETF_FUND_QUANTITY_MIN
etf_fund_quantity_max = ServiceConfig.ETF_FUND_QUANTITY_MAX

etf_fund_amount = ServiceConfig.ETF_FUND_AMOUNT

#--持仓成本，保留小数位
avg_price_DecimalPlaces = ServiceConfig.AVG_PRICE_DECIMALPLACES

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
# etf资金回报总成交金额，当成交金额大于1000元时，会返回两条资金成交回报
etf_trade_amount_total = 0
# 成交回报顺序
trade_seq = 0
# 定义4个list，分别存放二级市场、成分股、资金、一级市场的trade_seq
secondary_market_count_index = []
component_count_index = []
fund_count_index = []
primary_market_count_index = []

# etf申购成交回报中的总成交金额
trade_amount_total = 0

#---业务判断程序：买或是卖，及全成或是部成
def etf_cjhbDataCheck(expectStatus, Api, QueryInit, wt_reqs, xtp_id,
                      QueryEnd, hb_data, cash_substitute_amount, *args):
    global trade_seq, primary_market_count_index, etf_trade_amount_total, \
        component_count_index, fund_count_index, secondary_market_count_index

    py_name = ''
    if len(args[0]) > 1:
        py_name = args[0][1]
    trade_seq += 1
    # -----如果委托方向是etf申购，执行如下－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
    etf_code1_code2 = QueryEtfCode1Code2DB(wt_reqs['ticker'])
    component_codes = QueryEtfComponentsCodeDB(etf_code1_code2['etf_code1'])
    cjhb_reslut['xtp_id'] = hb_data['order_xtp_id']
    cjhb_reslut['市场'] = hb_data['market']
    cjhb_reslut['股票代码'] = hb_data['ticker']
    cjhb_reslut['买卖方向'] = hb_data['side']
    cjhb_reslut['成交价格'] = hb_data['price']
    cjhb_reslut['成交类型'] = hb_data['trade_type']
    cjhb_reslut['成交数量'] = hb_data['quantity']
    cjhb_reslut['成交金额'] = hb_data['trade_amount']
    # 成交回报顺序校验
    # trade_seq_check(hb_data,
    #                 trade_seq,
    #                 primary_market_count_index,
    #                 component_count_index,
    #                 fund_count_index,
    #                 secondary_market_count_index)

    creation_redemption_num = wt_reqs['quantity'] / stkQty['最小申赎单位']  # etf申赎份数

    if wt_reqs['side'] == Api.const.XTP_SIDE_TYPE['XTP_SIDE_PURCHASE']:
        # # 二级市场成交回报校验
        if (wt_reqs['ticker'] == hb_data['ticker'] and
            hb_data['trade_type'] == '0'):
            primary_secondary_market_check(xtp_id, hb_data, wt_reqs)
        # 成分股成交回报校验
        elif (hb_data['ticker'] in component_codes and
              hb_data['trade_type'] == '0'):
            component_rs = QueryEtfSubstitute(wt_reqs['ticker'],
                                              hb_data['ticker'])
            component_share = component_rs[0]  # etf成分股数量
            substitute_flag = component_rs[1]  # 现金替代标志
            component_stk_end = etf_get_one_component_stk(hb_data['ticker'])  # 查询某个股票持仓信息
            component_end = component_stk_end[hb_data['ticker']]
            component_init = args[0][0][hb_data['ticker']]
            creation_quantity = component_share * creation_redemption_num  # 申购所需成分股数量

            if substitute_flag == 0:
                if hb_data['quantity'] != creation_quantity:
                    logger.error('禁止现金替代成分股数量计算错误, 证券代码： ' +
                                 hb_data['ticker'] +
                                 ', 申购需要的成分股数量为： ' +
                                 str(creation_quantity) +
                                 ', 成交数量为： ' + str(hb_data['quantity']))
                    cjhb_reslut['成交回报检查状态'] = 'end'
                    cjhb_reslut['测试结果'] = False
                    cjhb_reslut['测试错误原因'] = ('禁止现金替代成分股数量计算错误, 证券代码： ' +
                                 hb_data['ticker'] +
                                 ', 申购需要的成分股数量为： ' +
                                 str(creation_quantity) +
                                 ', 成交数量为： ' + str(hb_data['quantity']))
            elif substitute_flag == 1:
                if (component_init['今日可申购赎回持仓'] <= creation_quantity and
                            hb_data['quantity'] != component_init['今日可申购赎回持仓']):
                    error_info = ('允许现金替代成分股数量计算错误, 证券代码： ' +
                                  hb_data['ticker'] +
                                  ', 原今日可申购赎回持仓数量为： ' +
                                  str(component_init['今日可申购赎回持仓']) +
                                  ', 申购需要的成分股数量为： ' +
                                  str(creation_quantity) +
                                  ', 成交数量为： ' + str(hb_data['quantity']))
                    logger.error(error_info)
                    cjhb_reslut['成交回报检查状态'] = 'end'
                    cjhb_reslut['测试结果'] = False
                    cjhb_reslut['测试错误原因'] = error_info
                    # return cjhb_reslut

            # 查询成分股昨收价
            ETF_COMPONENT_CJHB_QC_B(hb_data['ticker'],
                                    component_end,
                                    cjhb_reslut['成交数量'],
                                    component_init,
                                    creation_quantity,
                                    substitute_flag)
        # 一级市场成交回报校验
        elif (hb_data['ticker'] == etf_code1_code2['etf_code1'] and
              hb_data['trade_type'] == '2'):

            primary_secondary_market_check(xtp_id, hb_data, wt_reqs)
        # 资金成交回报校验
        elif (hb_data['ticker'] == etf_code1_code2['etf_code2'] and
              hb_data['trade_type'] == '1'):

            etf_trade_amount_total = etf_trade_amount_total + cjhb_reslut['成交金额']
            cash_substitute = QueryCreationRedemptionCash(etf_code1_code2['etf_code1']) # etf一级市场代码
            creation_redemption_unit = QueryCreationRedemUnitDB(wt_reqs['ticker'])
            etf_trade_amount = get_etf_trade_amount(1,
                                                    wt_reqs['ticker'],
                                                    creation_redemption_num, wt_reqs['market'],args)  # etf成交金额
            if wt_reqs['market'] == Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A']:
                etf_fund_check_ha(xtp_id, hb_data, wt_reqs, etf_trade_amount)
            else:
                etf_fund_check_sa(xtp_id, hb_data, wt_reqs, etf_trade_amount)

            # 资金成交回报全部推送
            if (etf_trade_amount_total ==
                cash_substitute['creation_cash_substitute'] *
                wt_reqs['quantity'] / creation_redemption_unit / 10000 +
                Decimal(cash_substitute_amount)):
                logger.info('成交回报检查：全部成交业务数据开始检查!')
                ETF_CJHB_QC_B(QueryInit, QueryEnd, wt_reqs,
                              etf_trade_amount_total, creation_redemption_num,
                              py_name)
            # 资金成交回报未推送或未全部推送
            elif (etf_trade_amount_total <
                cash_substitute['creation_cash_substitute'] *
                wt_reqs['quantity'] / creation_redemption_unit / 10000 +
                Decimal(cash_substitute_amount)):
                logger.info('资金成交回报-等待资金成交回报全部推送')
            # 资金成交回报未推送错误
            else:
                logger.error('资金成交回报-资金回报推送出错，'
                             '实际成交的金额和应成交金额分别为' +
                             str(etf_trade_amount_total) + ',' +
                             str(cash_substitute['creation_cash_substitute'] *
                                 wt_reqs['quantity'] /
                                 creation_redemption_unit / 10000 +
                                 Decimal(cash_substitute_amount)))
                cjhb_reslut['成交回报检查状态'] = 'end'
                cjhb_reslut['测试结果'] = False
                cjhb_reslut['测试错误原因'] = ('资金成交回报-资金回报推送出错，'
                             '实际成交的金额和应成交金额分别为' +
                             str(etf_trade_amount_total) + ',' +
                             str(cash_substitute['creation_cash_substitute'] *
                                 wt_reqs['quantity'] /
                                 creation_redemption_unit / 10000 +
                                 Decimal(cash_substitute_amount)))

        else:
            logger.error('成交回报返回未知代码： ' + hb_data['ticker'])
            cjhb_reslut['成交回报检查状态'] = 'end'
            cjhb_reslut['测试结果'] = False
            cjhb_reslut['测试错误原因'] = ('成交回报返回未知代码： ' + hb_data['ticker'])

    # --如果委托方向是赎回，执行如下－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
    elif wt_reqs['side'] == Api.const.XTP_SIDE_TYPE['XTP_SIDE_REDEMPTION']:
        # --etf二级市场校验,委托数据和成交数据比较
        if (wt_reqs['ticker'] == hb_data['ticker'] and
            hb_data['trade_type'] == '0'):
            # 二级市场成交回报校验
            primary_secondary_market_check(xtp_id, hb_data, wt_reqs)
        # 成分股校验
        elif (hb_data['ticker'] in component_codes and
              hb_data['trade_type'] == '0'):
            component_rs = QueryEtfSubstitute(wt_reqs['ticker'],
                                              hb_data['ticker'])
            component_share = component_rs[0]  # etf成分股数量
            substitute_flag = component_rs[1]  # 现金替代标志
            component_stk_end = etf_get_one_component_stk(
                              hb_data['ticker'])  # 查询某个股票持仓信息
            component_end = component_stk_end[hb_data['ticker']]
            component_init = args[0][0][hb_data['ticker']]
            creation_quantity = component_share * creation_redemption_num  # 申购所需成分股数量

            if substitute_flag in (0, 1):
                if hb_data['quantity'] != creation_quantity:
                    logger.error('禁止现金替代成分股数量计算错误, 证券代码： ' +
                                 hb_data['ticker'] +
                                 ', 申购需要的成分股数量为： ' +
                                 str(creation_quantity) +
                                 ', 成交数量为： ' + str(hb_data['quantity']))
                    cjhb_reslut['成交回报检查状态'] = 'end'
                    cjhb_reslut['测试结果'] = False
                    cjhb_reslut['测试错误原因'] = ('禁止现金替代成分股数量计算错误, 证券代码： ' +
                                 hb_data['ticker'] +
                                 ', 申购需要的成分股数量为： ' +
                                 str(creation_quantity) +
                                 ', 成交数量为： ' + str(hb_data['quantity']))
            # 查询成分股昨收价
            pre_close_prices = args[1]
            ETF_COMPONENT_CJHB_QC_S(hb_data['ticker'],
                                    component_end,
                                    cjhb_reslut['成交数量'],
                                    component_init,
                                    pre_close_prices)

        # 一级市场回报校验
        elif (hb_data['ticker'] == etf_code1_code2['etf_code1'] and
              hb_data['trade_type'] == '2'):
            primary_secondary_market_check(xtp_id, hb_data, wt_reqs)
        # 资金回报校验
        elif (hb_data['ticker'] == etf_code1_code2['etf_code2'] and
                      hb_data['trade_type'] == '1'):
            etf_trade_amount_total = etf_trade_amount_total + cjhb_reslut[
                '成交金额']
            cash_substitute = QueryCreationRedemptionCash(
                etf_code1_code2['etf_code1'])  # etf一级市场代码
            creation_redemption_unit = QueryCreationRedemUnitDB(
                wt_reqs['ticker'])
            etf_trade_amount = get_etf_trade_amount(2,
                                                    wt_reqs['ticker'],
                                                    creation_redemption_num, wt_reqs['market'],args)  # etf成交金额
            if wt_reqs['market'] == Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A']:
                etf_fund_check_ha(xtp_id, hb_data, wt_reqs, etf_trade_amount)
            else:
                etf_fund_check_sa(xtp_id, hb_data, wt_reqs, etf_trade_amount)
            # 资金成交回报全部推送
            if (etf_trade_amount_total ==
                                    cash_substitute['redemption_cash_substitute'] *
                                    wt_reqs['quantity'] / creation_redemption_unit / 10000):
                logger.info('成交回报检查：全部成交业务数据开始检查!')
                ETF_CJHB_QC_S(QueryInit, QueryEnd, wt_reqs,
                              etf_trade_amount_total,
                              creation_redemption_num,
                              py_name)
            # 资金成交回报未推送或未全部推送
            elif (etf_trade_amount_total <
                                      cash_substitute['creation_cash_substitute'] *
                                      wt_reqs['quantity'] / creation_redemption_unit / 10000):
                logger.info('资金成交回报-等待资金成交回报全部推送')
            # 资金成交回报未推送错误
            else:
                logger.error('资金成交回报-资金回报推送出错，'
                             '实际成交的金额和应成交金额分别为' +
                             str(etf_trade_amount_total) + ',' +
                             str(cash_substitute[
                                     'creation_cash_substitute'] *
                                 wt_reqs['quantity'] /
                                 creation_redemption_unit / 10000 +
                                 Decimal(cash_substitute_amount)))
                cjhb_reslut['成交回报检查状态'] = 'end'
                cjhb_reslut['测试结果'] = False
                cjhb_reslut['测试错误原因'] = ('资金成交回报-资金回报推送出错，'
                                         '实际成交的金额和应成交金额分别为' +
                                         str(etf_trade_amount_total) + ',' +
                                         str(cash_substitute[
                                                 'creation_cash_substitute'] *
                                             wt_reqs['quantity'] /
                                             creation_redemption_unit / 10000 +
                                             Decimal(cash_substitute_amount)))
        else:
            logger.error('成交回报返回未知代码： ' + hb_data['ticker'] + ', ' +hb_data['trade_type'])
            cjhb_reslut['成交回报检查状态'] = 'end'
            cjhb_reslut['测试结果'] = False
            cjhb_reslut['测试错误原因'] = ('成交回报返回未知代码： ' + hb_data['ticker'])

    return cjhb_reslut


# -----------------------------------------------------------------------------------------------------------------------
#--etf申购--全部成交--etf费用和持仓检查－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
def ETF_CJHB_QC_B(QueryInit, QueryEnd, wt_reqs,
                  etf_trade_amount_total, creation_redemption_num, *py_name):
    global fee_etf_min, fee_rate_etf_creation, fee_count_rate_etf_creation
    logger.info('成交回报－买－全部成交－费用持仓检查')
    #  ----计算费用----
    nav = QueryEtfNavDB(wt_reqs['ticker'])  # etf基金份额净值
    if py_name[0] != '':
        fee_etf = ServiceConfig.fee_etf_creation_redemption[py_name[0]]
        fee_etf_min = float(fee_etf[ServiceConfig.fee_etf_min_str])
        fee_rate_etf_creation = float(fee_etf[ServiceConfig.fee_rate_etf_creation_str])

    fee = wt_reqs['quantity'] * fee_rate_etf_creation * nav / 10000  # 申赎费用

    if  fee <= fee_etf_min:
        fee = fee_etf_min
    else:
        fee = float(Decimal(Decimal(str(fee)).quantize(Decimal('.01'),
                    rounding=ROUND_HALF_UP)))
    #原有费用加上过户费用
    count = QueryEtfcountDB(wt_reqs['ticker'])
    fee_count = fee_count_rate_etf_creation * count * creation_redemption_num
    fee += float(fee_count)

    #  ----获取预估现金差额----
    estimate_cash_component = QueryEstimateCashComponent(wt_reqs['ticker'])
    estimate_cash_component_origin = estimate_cash_component
    estimate_cash_component = estimate_cash_component * creation_redemption_num\
                                if estimate_cash_component > 0 else 0

    # --计算期待持仓成本应该是
    price_avg = (QueryInit['持仓成本价'] * QueryInit['总持仓'] +
                 cjhb_reslut['成交金额']) / \
                (QueryInit['总持仓'] + cjhb_reslut['成交数量'])
    price_avg = round(price_avg, avg_price_DecimalPlaces)

    # ----判断可用资金是否正确-----
    if abs(QueryInit['可用资金'] - etf_trade_amount_total -
            estimate_cash_component - fee - QueryEnd['可用资金']) > 0.00001:
        logger.error('可用资金计算有错,原可用资金、成交金额、'
                     '预估现金差额、费用、现可用资金分别是' + str(
                    QueryInit['可用资金']) + ',' + str(etf_trade_amount_total)+
                    ',' + str(estimate_cash_component_origin)+ ',' + str(
                    fee) + ',' + str(QueryEnd['可用资金']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['可用资金计算有错', {
            '原可用资金': QueryInit['可用资金'],
            '成交金额': cjhb_reslut['成交金额'],
            '费用': fee,
            '现可用资金': QueryEnd['可用资金']
        }]
    # ----判断总资产是否正确-----
    elif abs(QueryInit['总资产'] - etf_trade_amount_total -
            fee - QueryEnd['总资产']) > 0.00001:
        logger.error('总资产计算有错,原总资产、成交金额、费用、现总资产分别是' +
                    str(QueryInit['总资产']) + ',' + str(etf_trade_amount_total) +
                    ',' + str(fee) + ',' + str(QueryEnd['总资产']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['总资产计算有错', {
            '原总资产': QueryInit['总资产'],
            '成交金额': cjhb_reslut['成交金额'],
            '费用': fee,
            '现总资产': QueryEnd['总资产']
        }]
    # ----判断买入资金是否正确-----
    elif QueryEnd['买入资金'] - etf_trade_amount_total - \
            QueryInit['买入资金'] > 0.00001:
        logger.error('买入资金计算有错,原买入资金、成交金额、现买入资金分别是' +
                     str(QueryInit['买入资金']) + ',' +
                     str(etf_trade_amount_total) + ',' +
                     str(QueryEnd['买入资金']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['买入资金计算有错', {
            '原买入资金': QueryInit['买入资金'],
            '成交金额': cjhb_reslut['成交金额'],
            '现买入资金': QueryEnd['买入资金']
        }]
    # ----判断买入费用是否正确-----
    elif QueryEnd['买入费用'] - fee - QueryInit['买入费用'] > 0.00001:
        logger.error('买入费用计算有错,原买入费用、费用、现买入费用分别是' +
                     str(QueryInit['买入费用']) + ',' +
                     str(fee) + ',' +
                     str(QueryEnd['买入费用']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['买入费用计算有错', {
            '原买入费用': QueryInit['买入费用'],
            '费用': fee,
            '现买入费用': QueryEnd['买入费用']
        }]
    # ----判断卖出资金是否正确-----
    elif QueryEnd['卖出资金'] != QueryInit['卖出资金']:
        logger.error('卖出资金计算有错,原卖出资金、现卖出资金分别是' +
                     str(QueryInit['卖出资金']) + ',' +
                     str(QueryEnd['卖出资金']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['卖出资金计算有错', {
            '原卖出资金': QueryInit['卖出资金'],
            '现卖出资金': QueryEnd['卖出资金']
        }]
    # ----判断卖出费用是否正确-----
    elif QueryEnd['卖出费用'] != QueryInit['卖出费用']:
        logger.error('卖出费用计算有错,原卖出费用、现卖出费用分别是' +
                     str(QueryInit['卖出费用']) + ',' +
                     str(QueryEnd['卖出费用']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['卖出费用计算有错', {
            '原卖出费用': QueryInit['卖出费用'],
            '现卖出费用': QueryEnd['卖出费用']
        }]
    # ----判断预扣资金是否正确-----
    elif QueryEnd['预扣资金'] - estimate_cash_component - \
            QueryInit['预扣资金'] > 0.00001:
        logger.error('预扣资金计算有错,原预扣资金、预估现金差额、'
                     '赎回份数、现预扣资金分别是' +
                     str(QueryInit['预扣资金']) + ',' +
                     str(estimate_cash_component_origin) + ',' +
                     str(creation_redemption_num) + ',' +
                     str(QueryEnd['预扣资金']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['预扣资金计算有错', {
            '原预扣资金': QueryInit['预扣资金'],
            '预估现金差额': estimate_cash_component_origin,
            '赎回份数': creation_redemption_num,
            '现预扣资金': QueryEnd['预扣资金']
        }]
    # -----判断下单前后股票代码、市场是否一致-------
    elif QueryEnd['股票代码'] != QueryInit['股票代码'] or QueryEnd['市场'] !=QueryInit['市场']:
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

# --etf申购--全部成交--成分股持仓检查－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
def ETF_COMPONENT_CJHB_QC_B(ticker, component_end, trade_amount,
                            component_init, creation_quantity, substitute_flag):
    logger.info('成交回报－申购－全部成交－成分股: ' + str(ticker) + '持仓检查')

    # -----判断下单前后股票代码、市场是否一致-------
    if component_init['证券代码'] != component_end['证券代码'] or \
        component_init['市场'] != component_end['市场']:
        logger.error('下单前后查询的市场证券代码信息不一致,下单前查询的市场和证券代码是' +
                     str(component_init['市场']) +
                     ',' + str(component_init['证券代码']) +
                     ',下单后查询的市场和证券代码是' +
                     str(component_end['市场']) +
                     ',' + str(component_end['证券代码']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['下单前后查询的市场证券代码信息不一致', {
            '下单前查询的市场是': component_init['市场'],
            '下单前查询的证券代码是': component_end['证券代码'],
            '下单后查询的市场是': component_init['市场'],
            '下单后查询的证券代码是': component_end['证券代码'],
        }]
    # -----判断总持仓是否正确
    elif (component_init['总持仓'] - component_end['总持仓'] -
          trade_amount > 0.00001):
        logger.error('总持仓不正确，原总持仓，成交数量，现总持仓分别是' +
                     str(component_init['总持仓']) +
                     ',' + str(trade_amount) +
                     ',' + str(component_end['总持仓']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['总持仓不正确', {
            '原总持仓': component_init['总持仓'],
            '成交数量': trade_amount,
            '现总持仓': component_end['总持仓'],
        }]
    # --判断可卖持仓成交量是否正确
    elif component_init['可卖持仓'] - component_end['可卖持仓'] \
            - trade_amount > 0.00001:
        logger.error('可卖持仓不正确，原可卖持仓，现可卖持仓，成交数量分别是' +
                     str(component_init['可卖持仓']) +
                     ',' + str(component_end['可卖持仓']) +
                     ',' + str(trade_amount))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['可卖持仓不正确', {
            '原可卖持仓': component_init['可卖持仓'],
            '现可卖持仓': component_end['可卖持仓'],
            '成交数量': trade_amount
        }]
    # --判断全部和允许现金替代成分股的可卖持仓，今日可申购赎回持仓<=申购所需成分股数量
    elif (component_init['今日可申购赎回持仓'] <= creation_quantity and
          component_end['可卖持仓'] > 0) and substitute_flag in (0, 1):
        logger.error('证券代码' + ticker + '，可卖持仓不正确，原今日可申购赎回持仓，'
                     '申购所需成分股数量，现可卖持仓分别为' +
                     str(component_init['今日可申购赎回持仓']) +
                     ',' + str(creation_quantity) +
                     ',' + str(component_end['可卖持仓']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['可卖持仓不正确', {
            '原今日可申购赎回持仓': component_init['今日可申购赎回持仓'],
            '申购所需成分股数量': creation_quantity,
            '现可卖持仓分别为': component_end['可卖持仓']
        }]
    # --判断全部和允许现金替代成分股的可卖持仓，
    # 今日可申购赎回持仓>申购所需成分股数量>T日买入持仓
    elif (component_init['总持仓'] - component_init['可卖持仓'] <
              creation_quantity <
              component_init['今日可申购赎回持仓'] and
          component_init['今日可申购赎回持仓'] - creation_quantity !=
              component_end['可卖持仓']) and substitute_flag in (0, 1):
        logger.error('证券代码' + ticker + '，可卖持仓不正确，'
                     '原总持仓，原可卖持仓，申购所需成分股数量'
                     '原今日可申购赎回持仓，现可卖持仓分别为' +
                     str(component_init['总持仓']) +
                     ',' + str(component_init['可卖持仓']) +
                     ',' + str(creation_quantity) +
                     ',' + str(component_init['今日可申购赎回持仓']) +
                     ',' + str(component_end['可卖持仓']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['可卖持仓不正确', {
            '原总持仓': component_init['总持仓'],
            '原可卖持仓': component_init['可卖持仓'],
            '原今日可申购赎回持仓': component_init['今日可申购赎回持仓'],
            '申购所需成分股数量': creation_quantity,
            '现可卖持仓分别为': component_end['可卖持仓']
    }]
    # --判断全部和允许现金替代成分股的可卖持仓，申购所需成分股数量<T日买入持仓
    elif (component_init['总持仓'] - component_init['可卖持仓'] >
              creation_quantity and
          component_init['可卖持仓'] != component_end['可卖持仓'])  and \
          substitute_flag in (0, 1):
        logger.error('可卖持仓不正确，原总持仓，原可卖持仓，申购所需成分股数量'
                     '现可卖持仓分别为' +
                     str(component_init['总持仓']) +
                     ',' + str(component_init['可卖持仓']) +
                     ',' + str(creation_quantity) +
                     ',' + str(component_end['可卖持仓']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['可卖持仓不正确', {
            '原总持仓': component_init['总持仓'],
            '原可卖持仓': component_init['可卖持仓'],
            '申购所需成分股数量': creation_quantity,
            '现可卖持仓分别为': component_end['可卖持仓']
        }]
    # --判断持仓成本价是否正确
    elif abs(component_init['持仓成本价'] - component_end['持仓成本价']) > 0.001 \
            and component_end['总持仓'] > 0:
        logger.error(
            '持仓成本价不正确，期待持仓成本价和实际持仓成本价分别是' +
            str(component_init['持仓成本价']) +
            ',' + str(component_end['持仓成本价']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['持仓成本价不正确', {
            '期待持仓成本价': component_init['持仓成本价'],
            '实际持仓成本价': component_end['持仓成本价']
        }]
    elif component_end['持仓成本价'] != 0 and component_end['总持仓'] == 0:
        logger.error(
            '持仓成本价不正确，期待持仓成本价和实际持仓成本价分别是' +
            str(component_init['持仓成本价']) +
            ',' + str(component_end['持仓成本价']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['持仓成本价不正确', {
            '期待持仓成本价': component_init['持仓成本价'],
            '实际持仓成本价': component_end['持仓成本价']
        }]

    # --判断浮动盈亏是否正确
    elif abs(component_init['浮动盈亏'] - component_end['浮动盈亏']) > 0.001:
        logger.error(
            '浮动盈亏不正确，期待浮动盈亏和实际浮动盈亏分别是' +
            str(component_init['浮动盈亏']) +
            ',' + str(component_end['浮动盈亏']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['浮动盈亏不正确', {
            '期待浮动盈亏': component_init['浮动盈亏'],
            '实际浮动盈亏': component_end['浮动盈亏']
        }]
    # --判断昨日持仓是否正确
    elif component_init['昨日持仓'] != component_end['昨日持仓']:
        logger.error('昨日持仓不正确，原昨日持仓，现昨日持仓分别是' +
                     str(component_init['昨日持仓']) +
                     ',' + str(component_end['昨日持仓']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['昨日持仓不正确', {
            '原昨日持仓': component_init['昨日持仓'],
            '现昨日持仓': component_end['昨日持仓']
        }]
    # --判断可赎回证券数是否正确
    elif component_init['今日可申购赎回持仓'] - component_end['今日可申购赎回持仓']\
            - trade_amount > 0.00001:
        logger.error('今日可申购赎回持仓不正确，原今日可申购赎回持仓，' +
                     '现今日可申购赎回持仓，成交数量分别是' +
                     str(component_init['今日可申购赎回持仓']) +
                     ',' + str(component_end['今日可申购赎回持仓']) +
                     ',' + str(trade_amount))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['今日可申购赎回持仓不正确', {
            '原今日可申购赎回持仓': component_init['今日可申购赎回持仓'],
            '现今日可申购赎回持仓': component_end['今日可申购赎回持仓'],
            '成交数量': trade_amount
        }]
    else:
        logger.info('买_全成_成交回报_成分股校验正确！')
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = True

# --etf赎回--全部成交--成分股持仓检查－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
def ETF_COMPONENT_CJHB_QC_S(ticker, component_end, trade_amount,
                            component_init, pre_close_prices):
    logger.info('成交回报－赎回－全部成交－成分股: ' + str(ticker) + '持仓检查')

    # 获取成分股昨收价
    pre_close_price = pre_close_prices[ticker]

    # --计算期待持仓成本应该是，深圳赎回时会返回全部现金替代的成分股回报，且成交数量为0
    price_avg = 0
    if cjhb_reslut['成交数量'] != 0:
        price_avg = (component_init['持仓成本价'] * component_init['总持仓'] +
                     trade_amount * pre_close_price) / \
                    (component_init['总持仓'] + cjhb_reslut['成交数量'])
    price_avg_deviation = round(component_end['持仓成本价'] - price_avg,
                          avg_price_DecimalPlaces)   # 应得持仓成本价和实际持仓成本价误差

    # -----判断下单前后股票代码、市场是否一致-------
    if component_init['证券代码'] != component_end['证券代码'] or \
                    component_init['市场'] != component_end['市场']:
        logger.error('下单前后查询的市场证券代码信息不一致,下单前查询的市场和证券代码是' +
                     str(component_init['市场']) +
                     ',' + str(component_init['证券代码']) +
                     ',下单后查询的市场和证券代码是' +
                     str(component_end['市场']) +
                     ',' + str(component_end['证券代码']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['下单前后查询的市场证券代码信息不一致', {
            '下单前查询的市场是': component_init['市场'],
            '下单前查询的证券代码是': component_end['证券代码'],
            '下单后查询的市场是': component_init['市场'],
            '下单后查询的证券代码是': component_end['证券代码'],
        }]
    # -----判断总持仓是否正确
    elif (component_end['总持仓'] - component_init['总持仓'] -
              trade_amount > 0.00001):
        logger.error('总持仓不正确，原总持仓，成交数量，现总持仓分别是' +
                     str(component_init['总持仓']) +
                     ',' + str(trade_amount) +
                     ',' + str(component_end['总持仓']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['总持仓不正确', {
            '原总持仓': component_init['总持仓'],
            '成交数量': trade_amount,
            '现总持仓': component_end['总持仓'],
        }]
    # --判断可卖持仓成交量是否正确
    elif component_end['可卖持仓'] - component_init['可卖持仓'] \
            - trade_amount > 0.00001:
        logger.error('可卖持仓不正确，原可卖持仓，现可卖持仓，成交数量分别是' +
                     str(component_init['可卖持仓']) +
                     ',' + str(component_end['可卖持仓']) +
                     ',' + str(trade_amount))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['可卖持仓不正确', {
            '原可卖持仓': component_init['可卖持仓'],
            '现可卖持仓': component_end['可卖持仓'],
            '成交数量': trade_amount
        }]
    # --判断持仓成本价是否正确
    elif price_avg_deviation > 0.001 and cjhb_reslut['成交数量'] != 0:
        logger.error(
            '成分股' + ticker + '持仓成本价不正确，'
            '期待持仓成本价和实际持仓成本价分别是' + str(price_avg) +
            ',' + str(component_end['持仓成本价']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['持仓成本价不正确', {
            '期待持仓成本价': component_init['持仓成本价'],
            '实际持仓成本价': component_end['持仓成本价']
        }]

    # --判断浮动盈亏是否正确
    elif abs(component_init['浮动盈亏'] - component_end['浮动盈亏']) > 0.001:
        logger.error(
            '浮动盈亏不正确，期待浮动盈亏和实际浮动盈亏分别是' +
            str(component_init['浮动盈亏']) +
            ',' + str(component_end['浮动盈亏']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['浮动盈亏不正确', {
            '期待浮动盈亏': component_init['浮动盈亏'],
            '实际浮动盈亏': component_end['浮动盈亏']
        }]
    # --判断昨日持仓是否正确
    elif component_init['昨日持仓'] != component_end['昨日持仓']:
        logger.error('昨日持仓不正确，原昨日持仓，现昨日持仓分别是' +
                     str(component_init['昨日持仓']) +
                     ',' + str(component_end['昨日持仓']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['昨日持仓不正确', {
            '原昨日持仓': component_init['昨日持仓'],
            '现昨日持仓': component_end['昨日持仓']
        }]
    # --判断可赎回证券数是否正确
    elif component_init['今日可申购赎回持仓'] - component_end['今日可申购赎回持仓'] \
            - trade_amount > 0.00001:
        logger.error('今日可申购赎回持仓不正确，原今日可申购赎回持仓，' +
                     '现今日可申购赎回持仓，成交数量分别是' +
                     str(component_init['今日可申购赎回持仓']) +
                     ',' + str(component_end['今日可申购赎回持仓']) +
                     ',' + str(trade_amount))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['今日可申购赎回持仓不正确', {
            '原今日可申购赎回持仓': component_init['今日可申购赎回持仓'],
            '现今日可申购赎回持仓': component_end['今日可申购赎回持仓'],
            '成交数量': trade_amount
        }]
    else:
        logger.info('买_全成_成交回报_成分股校验正确！')
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = True

# --------------------------------------------------------------------------
#--etf赎回--全部成交--费用持仓检查---------------------------------------------
def ETF_CJHB_QC_S(QueryInit, QueryEnd, wt_reqs,
                  etf_trade_amount_total, creation_redemption_num, *py_name):
    '''
    :param QueryInit: 初始资金和持仓
    :param QueryEnd: 当前资金和持仓
    :param wt_reqs: 委托参数
    :param check_status: 校验状态 - 1:校验资金 2：校验持仓
    :return: None
    '''
    global fee_etf_min, fee_rate_etf_redemption , fee_count_rate_etf_redemption
    logger.info('成交回报－卖－全部成交－费用持仓检查')
    # ----计算费用----
    nav = QueryEtfNavDB(wt_reqs['ticker'])  # etf最小申赎单位净值
    if py_name[0] != '':
        fee_etf = ServiceConfig.fee_etf_creation_redemption[py_name[0]]
        fee_etf_min = float(fee_etf[ServiceConfig.fee_etf_min_str])
        fee_rate_etf_redemption = float(fee_etf[ServiceConfig.fee_rate_etf_redemption_str])

    fee = wt_reqs['quantity'] * fee_rate_etf_creation * nav / 10000  # 申赎费用
    if fee <= fee_etf_min:
        fee = fee_etf_min
    else:
        fee = float(Decimal(Decimal(str(fee)).quantize(Decimal('.01'),
                                                       rounding=ROUND_HALF_UP)))
    #原有费用加上过户费用 
    count = QueryEtfcountDB(wt_reqs['ticker'])
    fee_count = fee_count_rate_etf_redemption * count * creation_redemption_num
    fee += float(fee_count)

    # ----获取预估现金差额----
    estimate_cash_component = QueryEstimateCashComponent(wt_reqs['ticker'])
    estimate_cash_component_origin = estimate_cash_component
    estimate_cash_component = -(estimate_cash_component * creation_redemption_num
                               if estimate_cash_component < 0 else 0)

    # 成交数量计算
    if wt_reqs['market'] == Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A']:
        trade_amount = wt_reqs['quantity']
    else:
        trade_amount = cjhb_reslut['成交数量']

    # ----判断可用资金是否正确-----
    if abs(QueryInit['可用资金'] + etf_trade_amount_total -
               estimate_cash_component - fee - QueryEnd['可用资金'])> 0.00001:
        logger.error('可用资金计算有错,原可用资金、成交金额、'
                     '预估现金差额、费用、现可用资金分别是' +
                     str(QueryInit['可用资金']) +
                     ',' + str(etf_trade_amount_total) +
                     ',' + str(estimate_cash_component) +
                     ',' + str(fee) + ',' + str(QueryEnd['可用资金']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['可用资金计算有错', {
            '原可用资金': QueryInit['可用资金'],
            '成交金额': cjhb_reslut['成交金额'],
            '费用': fee,
            '现可用资金': QueryEnd['可用资金']
        }]
    # ----判断总资产是否正确-----
    elif abs(QueryInit['总资产'] + etf_trade_amount_total -
                 fee - QueryEnd['总资产'])> 0.00001:
        logger.error('总资产计算有错,原总资产、成交金额、费用、现总资产分别是' +
                     str(QueryInit['总资产']) + ',' + str(etf_trade_amount_total) +
                     ',' + str(fee) + ',' + str(QueryEnd['总资产']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['总资产计算有错', {
            '原总资产': QueryInit['总资产'],
            '成交金额': cjhb_reslut['成交金额'],
            '费用': fee,
            '现总资产': QueryEnd['总资产']
        }]
    # ----判断买入资金是否正确-----
    elif QueryInit['买入资金'] != QueryEnd['买入资金']:
        logger.error('买入资金计算有错,原买入资金、现买入资金分别是' +
                     str(QueryInit['买入资金']) + ',' +
                     str(QueryEnd['买入资金']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['买入资金计算有错', {
            '原买入资金': QueryInit['买入资金'],
            '现买入资金': QueryEnd['买入资金']
        }]
    # ----判断买入费用是否正确-----
    elif QueryInit['买入费用'] != QueryEnd['买入费用']:
        logger.error('买入费用计算有错,原买入费用、现买入费用分别是' +
                     str(QueryInit['买入费用']) + ',' +
                     str(QueryEnd['买入费用']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['买入费用计算有错', {
            '原买入费用': QueryInit['买入费用'],
            '现买入费用': QueryEnd['买入费用']
        }]
    # ----判断卖出资金是否正确-----
    elif QueryEnd['卖出资金'] - etf_trade_amount_total - \
            QueryInit['卖出资金'] > 0.00001:
        logger.error('卖出资金计算有错,原卖出资金、成交金额、现卖出资金分别是' +
                     str(QueryInit['卖出资金']) + ',' +
                     str(etf_trade_amount_total) + ',' +
                     str(QueryEnd['卖出资金']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['卖出资金计算有错', {
            '原卖出资金': QueryInit['卖出资金'],
            '成交金额': cjhb_reslut['成交金额'],
            '现卖出资金': QueryEnd['卖出资金']
        }]
    # ----判断卖出费用是否正确-----
    elif QueryEnd['卖出费用'] - fee - QueryInit['卖出费用'] > 0.00001 :
        logger.error('卖出费用计算有错,原卖出费用、费用、现卖出费用分别是' +
                     str(QueryInit['卖出费用']) + ',' +
                     str(fee) + ',' +
                     str(QueryEnd['卖出费用']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['卖出费用计算有错', {
            '原卖出费用': QueryInit['卖出费用'],
            '费用': fee,
            '现卖出费用': QueryEnd['卖出费用']
        }]
    # ----判断预扣资金是否正确-----
    elif QueryEnd['预扣资金'] - estimate_cash_component - \
            QueryInit['预扣资金'] > 0.00001 :
        logger.error('预扣资金计算有错,原预扣资金、预估现金差额、'
                     '赎回份数、现预扣资金分别是' +
                     str(QueryInit['预扣资金']) + ',' +
                     str(estimate_cash_component_origin) + ',' +
                     str(creation_redemption_num) + ',' +
                     str(QueryEnd['预扣资金']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['预扣资金计算有错', {
            '原预扣资金': QueryInit['预扣资金'],
            '预估现金差额': estimate_cash_component_origin,
            '赎回份数': creation_redemption_num,
            '现预扣资金': QueryEnd['预扣资金']
        }]
    # ---－判断总持仓是否正确
    elif abs(QueryInit['总持仓'] - QueryEnd['总持仓'] -
                     trade_amount) > 0.00001:
        logger.error('总持仓不正确，原总持仓，成交数量，现总持仓分别是' +
                     str(QueryInit['总持仓']) +
                     ',' + str(trade_amount) +
                     ',' + str(QueryEnd['总持仓']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['总持仓不正确', {
            '原总持仓': QueryInit['总持仓'],
            '成交数量': cjhb_reslut['成交数量'],
            '现总持仓': QueryEnd['总持仓'],
        }]
    # --判断可卖持仓是否正确
    elif QueryInit['可卖持仓'] - QueryEnd['可卖持仓'] - \
            trade_amount> 0.00001:
        logger.error('可卖持仓不正确，原可卖持仓，现可卖持仓，成交数量分别是' +
                     str(QueryInit['可卖持仓']) +
                     ',' + str(QueryEnd['可卖持仓']) +
                     ',' + str(trade_amount))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['可卖持仓不正确', {
            '原可卖持仓': QueryInit['可卖持仓'],
            '现可卖持仓': QueryEnd['可卖持仓'],
            '成交数量': cjhb_reslut['成交数量']
        }]
    # -----判断下单前后股票代码、市场是否一致-------
    elif QueryEnd['股票代码'] != QueryInit['股票代码'] or \
             QueryEnd['市场'] != QueryInit['市场']:
        logger.error('下单前后查询的市场股票代码信息不一致,下单前查询的市场和股票代码是' +
                     str(QueryInit['市场']) +
                     ',' + str(QueryInit['股票代码']) +
                     ',下单后查询的市场和股票代码是' +
                     str(QueryEnd['市场']) +
                     ',' + str(QueryEnd['股票代码']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['下单前后查询的市场股票代码信息不一致', {
            '下单前查询的市场是': QueryInit['市场'],
            '下单前查询的股票代码是': QueryEnd['股票代码'],
            '下单后查询的市场是': QueryInit['市场'],
            '下单后查询的股票代码是': QueryEnd['股票代码'],
        }]
    # --判断昨日持仓是否正确
    elif QueryEnd['昨日持仓'] != QueryInit['昨日持仓']:
        logger.error('昨日持仓不正确，原昨日持仓，现昨日持仓分别是' +
                     str(QueryInit['昨日持仓']) +
                     ',' + str(QueryEnd['昨日持仓']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['昨日持仓不正确', {
            '原昨日持仓': QueryInit['昨日持仓'],
            '现昨日持仓': QueryEnd['昨日持仓']
        }]
    # --判断可赎回证券数是否正确
    elif QueryInit['今日可申购赎回持仓'] - QueryEnd['今日可申购赎回持仓'] - \
            trade_amount > 0.00001:
        logger.error('今日可申购赎回持仓不正确，原今日可申购赎回持仓，现今日可申购赎回持仓分别是' +
                     str(QueryInit['今日可申购赎回持仓']) +
                     ',' + str(QueryEnd['今日可申购赎回持仓']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['今日可申购赎回持仓不正确', {
            '原今日可申购赎回持仓': QueryInit['今日可申购赎回持仓'],
            '现今日可申购赎回持仓': QueryEnd['今日可申购赎回持仓']
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

# 成交回报顺序校验
def trade_seq_check(
        hb_data, trade_seq, primary_market_count_index,
        component_count_index, fund_count_index, secondary_market_count_index):
    # 存放二级市场、成分股、资金、一级市场的trade_seq
    if hb_data['trade_type'] == '0' and trade_seq == 1:
        secondary_market_count_index.append(trade_seq)
    if hb_data['trade_type'] == '0' and trade_seq > 1:
        component_count_index.append(trade_seq)
    elif hb_data['trade_type'] == '1':
        fund_count_index.append(trade_seq)
    elif hb_data['trade_type'] == '2':
        primary_market_count_index.append(trade_seq)
        # ---------校验成交回报推送顺序---------
        # 无成分股成交回报和无资金回报时校验
        if component_count_index == [] and fund_count_index == []:
            if (min(primary_market_count_index) -
                    min(secondary_market_count_index) != 1):
                logger.error('成交回报推送顺序错误!')
        # 有成分股成交回报和有资金回报时校验
        elif component_count_index != [] and fund_count_index != []:
            if (min(component_count_index) -
                    min(secondary_market_count_index) != 1 or
                            min(fund_count_index) -
                            max(component_count_index) != 1 or
                            min(primary_market_count_index) -
                            max(fund_count_index) != 1):
                logger.error('成交回报推送顺序错误!')
        # 无成分股成交回报和有资金回报时校验
        elif component_count_index == [] and fund_count_index != []:
            if (min(fund_count_index) -
                    max(secondary_market_count_index) != 1 or
                            min(primary_market_count_index) -
                            max(fund_count_index) != 1):
                logger.error('成交回报推送顺序错误!')
        # 有成分股成交回报和无资金回报时校验
        elif component_count_index != [] and fund_count_index == []:
            if (min(component_count_index) -
                    max(secondary_market_count_index) != 1 or
                            min(primary_market_count_index) -
                            max(component_count_index) != 1):
                logger.error('成交回报推送顺序错误!')
    else:
        logger.info('成交回报错误，未知的成交类型：' + hb_data['trade_type'])
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = True

# etf一级市场和二级市场回报校验
def primary_secondary_market_check(xtp_id, hb_data, wt_reqs):
    # 判断委托和成交回报的xtpid，市场，买卖方向是否一致
    if (xtp_id == hb_data['order_xtp_id'] and
        wt_reqs['market'] == hb_data['market'] and
        wt_reqs['side'] == hb_data['side']) is False:
        logger.error('etf成交回报和委托信息不一致，如：xtpid,market,side')
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = '成交回报和委托信息不一致，' \
                                '如：xtpid,market,side'
    elif hb_data['price'] != 0:
        logger.error('etf二级市场成交回报-价格错误，应为0，实际为' +
                     str(hb_data['price']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ('etf二级市场成交回报-价格错误，应为0，实际为' +
                                     str(hb_data['price']))
    elif hb_data['quantity'] != wt_reqs['quantity']:
        logger.error('etf二级市场成交回报-委托数量和成交回报数量不一致,'
                     '委托数量和成交回报数量分别为' +
                     str(wt_reqs['quantity']) + ',' +
                     str(hb_data['quantity']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ('etf二级市场成交回报-委托数量和成交回报数量不一致,'
                                     '委托数量和成交回报数量分别为' +
                                     str(wt_reqs['quantity']) + ',' +
                                     str(hb_data['quantity']))
    elif hb_data['trade_amount'] != 0:
        logger.error('etf二级市场成交回报-成交金额错误，应为0，实际为' +
                     str(hb_data['trade_amount']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ('etf二级市场成交回报-成交金额错误，应为0，实际为' +
                                     str(hb_data['trade_amount']))
    else:
        logger.info('etf二级市场成交回报校验正确')
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = True

# 沪A-etf资金回报校验
def etf_fund_check_ha(xtp_id, hb_data, wt_reqs, etf_trade_amount):
    global trade_amount_total
    # 判断委托和成交回报的xtpid，市场，买卖方向是否一致
    if (xtp_id == hb_data['order_xtp_id'] and
        wt_reqs['market'] == hb_data['market'] and
        wt_reqs['side'] == hb_data['side']) is False:
        logger.error('etf成交回报和委托信息不一致，如：xtpid,market,side')
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = '成交回报和委托信息不一致，' \
                                '如：xtpid,market,side'
    # 回报金额小于1000
    elif etf_trade_amount < etf_fund_amount:
        # 金额校验
        if abs(hb_data['trade_amount'] - etf_trade_amount) > 0.00001:
            logger.error('etf资金成交回报-实际成交金额和期望的成交金额不一致，'
                         '分别为%d,%d' % (hb_data['trade_amount'], etf_trade_amount))
            cjhb_reslut['成交回报检查状态'] = 'end'
            cjhb_reslut['测试结果'] = False
            cjhb_reslut['测试错误原因'] = ('etf资金成交回报-实际成交金额和期望的成交金额不一致，'
                                         '分别为' + str(hb_data['trade_amount']) + ',' +
                                         str(etf_trade_amount))
        # 价格校验
        # elif abs(hb_data['price'] -
        #          hb_data['trade_amount'] / etf_fund_quantity_min) > 0.00001:
        #     logger.error('etf资金成交回报-实际成交价格和期望的成交价格不一致，'
        #                  '分别为' + str(hb_data['price']) + ',' +
        #                  str(hb_data['trade_amount'] / etf_fund_quantity_min))
        #     cjhb_reslut['成交回报检查状态'] = 'end'
        #     cjhb_reslut['测试结果'] = False
        #     cjhb_reslut['测试错误原因'] = ('etf资金成交回报-实际成交价格和期望的成交价格不一致，'
        #                  '分别为' + str(hb_data['price']) + ',' +
        #                  str(hb_data['trade_amount'] / etf_fund_quantity_min))
        # 数量校验
        # elif hb_data['quantity'] != etf_fund_quantity_min:
        #     logger.error('etf资金成交回报-实际成交数量和期望的成交数量不一致，'
        #                  '分别为' + str(hb_data['quantity']) + ',' +
        #                  str(etf_fund_quantity_min))
        #     cjhb_reslut['成交回报检查状态'] = 'end'
        #     cjhb_reslut['测试结果'] = False
        #     cjhb_reslut['测试错误原因'] = ('etf资金成交回报-实际成交数量和期望的成交数量不一致，'
        #                  '分别为' + str(hb_data['quantity']) + ',' +
        #                  str(etf_fund_quantity_min))
    # 回报金额大于1000
    elif etf_trade_amount >= etf_fund_amount:
        trade_amount_total += hb_data['trade_amount']
        if trade_amount_total < etf_trade_amount:
            logger.info("等待资金成交回报全部返回！")
        else:
            # 金额校验
            if abs(etf_trade_amount - trade_amount_total) > 0.00001:
                logger.error('etf资金成交回报-实际成交金额和期望的成交金额不一致，'
                             '分别为' + str(trade_amount_total) + ',' +
                             str(etf_trade_amount))
                cjhb_reslut['成交回报检查状态'] = 'end'
                cjhb_reslut['测试结果'] = False
                cjhb_reslut['测试错误原因'] = ('etf资金成交回报-实际成交金额和期望的成交金额不一致，'
                                         '分别为' + str(trade_amount_total) + ',' +
                                         str(etf_trade_amount))
        # 价格校验
        # elif abs(hb_data['price'] -
        #          hb_data['trade_amount'] / etf_fund_quantity_max) > 0.00001:
        #     logger.error('etf资金成交回报-实际成交价格和期望的成交价格不一致，'
        #                  '分别为' + str(hb_data['price']) + ',' +
        #                  str(hb_data['trade_amount'] / etf_fund_quantity_max))
        #     cjhb_reslut['成交回报检查状态'] = 'end'
        #     cjhb_reslut['测试结果'] = False
        #     cjhb_reslut['测试错误原因'] = ('etf资金成交回报-实际成交价格和期望的成交价格不一致，'
        #                              '分别为' + str(hb_data['price']) + ',' +
        #                              str(hb_data['trade_amount'] / etf_fund_quantity_max))
        # 数量校验
        # elif hb_data['quantity'] != etf_fund_quantity_max:
        #     logger.error('etf资金成交回报-实际成交数量和期望的成交数量不一致，'
        #                  '分别为' + str(hb_data['quantity']) + ',' +
        #                  str(etf_fund_quantity_max))
        #     cjhb_reslut['成交回报检查状态'] = 'end'
        #     cjhb_reslut['测试结果'] = False
        #     cjhb_reslut['测试错误原因'] = ('etf资金成交回报-实际成交数量和期望的成交数量不一致，'
        #                              '分别为' + str(hb_data['quantity']) + ',' +
        #                              str(etf_fund_quantity_max))
    else:
        logger.info('etf二级市场资金成交回报校验正确')
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = True

# 深A-etf资金回报校验
def etf_fund_check_sa(xtp_id, hb_data, wt_reqs, etf_trade_amount):
    # 判断委托和成交回报的xtpid，市场，买卖方向是否一致
    if (xtp_id == hb_data['order_xtp_id'] and
                wt_reqs['market'] == hb_data['market'] and
                wt_reqs['side'] == hb_data['side']) is False:
        logger.error('etf成交回报和委托信息不一致，如：xtpid,market,side')
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = '成交回报和委托信息不一致，' \
                                '如：xtpid,market,side'
    # 金额校验
    elif abs(hb_data['trade_amount'] - etf_trade_amount) > 0.00001:
        logger.error('etf资金成交回报-实际成交金额和期望的成交金额不一致，'
                     '分别为' + str(hb_data['trade_amount']) + ',' +
                     str(etf_trade_amount))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ('etf资金成交回报-实际成交金额和返回的成交金额不一致，'
                                 '分别为' + str(hb_data['trade_amount']) + ',' +
                                 str(etf_trade_amount))
    # 价格校验
    elif hb_data['price'] != 0:
        logger.error('etf资金成交回报-实际成交价格和期望的成交价格不一致，'
                     '分别为' + str(hb_data['price']) + ', 0')
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ('etf资金成交回报-实际成交价格和期望的成交价格不一致，'
                     '分别为' + str(hb_data['price']) + ', 0')
    # 数量校验
    elif hb_data['quantity'] != wt_reqs['quantity']:
        logger.error('etf资金成交回报-实际成交数量和期望的成交数量不一致，'
                     '分别为' + str(hb_data['quantity']) + ',' +
                     str(wt_reqs['quantity']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ('etf资金成交回报-实际成交数量和期望的成交数量不一致，'
                                 '分别为' + str(hb_data['quantity']) + ',' +
                                 str(wt_reqs['quantity']))
    else:
        logger.info('etf二级市场资金成交回报校验正确')
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = True

# 计算etf申赎的成交金额
def get_etf_trade_amount(is_creation_redemption, ticker, unit,market_id,component_stk_before):
    '''
    :param is_creation_redemption: 申赎类型 - 1：申购，2：赎回
    :param ticker: etf交易代码
    :param unit: 申赎份数
    :return: etf成交金额
    '''
    etf_trade_amount = 0
    components_stk = etf_get_all_component_stk(ticker) # 查询etf所有成分股的总持仓
    components_info = QueryEtfComponentsInfoDB(ticker,market_id) # 查询etf成分股申购所需数量、现金替代标识、申赎替代金额
    if is_creation_redemption == 1:
        for stk in components_info:
            # 允许现金替代
            if stk[1] == 1:
                if component_stk_before is None:
                    etf_trade_amount += (unit * stk[2] - 0) \
                                     * round(float(stk[4]) * (1 + float(stk[3])/100000),2)
                else:
                    if unit*stk[2] > component_stk_before[0][0][stk[0]]['今日可申购赎回持仓']:
                        etf_trade_amount += (unit * stk[2] -
                                            component_stk_before[0][0][stk[0]]['今日可申购赎回持仓']) \
                                            * round(float(stk[4]) * (1 + float(stk[3])/100000),2)

            # 全部现金替代
            elif stk[1] == 2:
                etf_trade_amount += unit * float(stk[7]) / 10000
    elif is_creation_redemption == 2:
        for stk in components_info:
            if stk[1] == 2:
                etf_trade_amount += unit * float(stk[7]) / 10000
    else:
        logger.error('错误的参数值，1表示申购，2表示赎回，实际参数值为' + str(is_creation_redemption))
    return etf_trade_amount
