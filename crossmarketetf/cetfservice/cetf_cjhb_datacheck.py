#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
from decimal import Decimal
from decimal import ROUND_HALF_UP
sys.path.append("/home/yhl2/workspace/xtp_test")
from service.log import *
from crossmarketetf.cetfmysql.query_creation_redem_unit import *
from crossmarketetf.cetfmysql.query_cetf_components import *
from crossmarketetf.cetfservice.cetf_get_components_asset import *
from crossmarketetf.cetfmysql.query_cetf_substitute_cash import *
from crossmarketetf.cetfmysql.query_cetf_nav import query_cetf_nav
from crossmarketetf.cetfmysql.query_estimate_cash_component import *
from service import ServiceConfig
from crossmarketetf.cetfmysql.query_cetf_count import query_cetf_count

class cjhb_var(object):
    # ---定义费率，最低收费
    fee_rate_etf_creation = ServiceConfig.FEE_RATE_ETF_CREATION
    fee_rate_etf_redemption = ServiceConfig.FEE_RATE_ETF_REDEMPTION
    fee_etf_min = ServiceConfig.FEE_ETF_MIN
    # 过户费率
    fee_count_rate_etf_creation = ServiceConfig.FEE_COUNT_RATE_ETF_CREATION
    fee_count_rate_etf_redemption = ServiceConfig.FEE_COUNT_RATE_ETF_REDEMPTION

    # 定义etf资金回报对应的数量字段
    cetf_fund_quantity_min = ServiceConfig.ETF_FUND_QUANTITY_MIN
    cetf_fund_quantity_max = ServiceConfig.ETF_FUND_QUANTITY_MAX

    cetf_fund_amount = ServiceConfig.ETF_FUND_AMOUNT

    # --持仓成本，保留小数位
    avg_price_DecimalPlaces = ServiceConfig.AVG_PRICE_DECIMALPLACES

    # etf资金回报总成交金额，当成交金额大于1000元时，会返回两条资金成交回报
    trade_amount_ha_total = 0
    trade_amount_sa_total = 0
    trade_amount_total = 0





# 业务判断程序：申购或是赎回，etf只有全成有成交回报，不用传入期望状态参数
def cetf_cjhb_datacheck(Api, QueryInit, wt_reqs, xtp_id,QueryEnd, hb_data,
                        cash_substitute_amount, pre_close_prices,
                        component_stk_before, pyname):
    """
    成交回报数据校验
    :param Api:
    :param QueryInit:
    :param wt_reqs:
    :param xtp_id:
    :param QueryEnd:
    :param hb_data:
    :param cash_substitute_amount: 允许现金替代的成分股，计算出的被替换的总金额
    :param pre_close_prices: 成分股昨收价
    :param component_stk_before: 下单前成分股持仓
    :param pyname:
    :return:
    """
    # 定义返回结果集
    cjhb_reslut = {
        '成交回报检查状态': 'init',
        '测试结果': True,
        '测试错误原因': None,
        'xtp_id': hb_data['order_xtp_id'],
        '市场': hb_data['market'],
        '股票代码': hb_data['ticker'],
        '买卖方向': hb_data['side'],
        '成交价格': hb_data['price'],
        '成交数量': hb_data['quantity'],
        '成交金额': hb_data['trade_amount'],
        '成交类型': hb_data['trade_type'],
         }

    # 查询跨市场etf 一级市场代码，资金代码
    # 查询跨市场etf 所有成分股代码
    cetf_code1_code2 = query_cetf_code1code2(wt_reqs['ticker'])
    component_codes = query_cetf_components_code(cetf_code1_code2['etf_code1'])
    # 获取跨市场资金代码,如果是上海市场的etf,代码将最后一位换成5
    # if wt_reqs['market'] == Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A']:
    cetf_code3 = (wt_reqs['ticker'][:-1] + '5')
    # etf申赎份数
    creation_redemption_num = (wt_reqs['quantity'] /
                               query_creation_redem_unit(wt_reqs['ticker']))

    # --------------------------------------------------------------------------
    # 如果委托方向是etf申购，执行如下
    # 1.etf二级市场成交回报校验 2.成分股成交回报校验 3.一级市场成交回报校验
    # 4.同市场资金成交回报校验 5.跨市场资金成交回报校验
    # --------------------------------------------------------------------------
    if wt_reqs['side'] == Api.const.XTP_SIDE_TYPE['XTP_SIDE_PURCHASE']:
        # ---------校验1：etf二级市场成交回报校验---------
        if (wt_reqs['ticker'] == hb_data['ticker'] and
                    hb_data['trade_type'] == '0'):
            primary_secondary_market_check(xtp_id, hb_data, wt_reqs,cjhb_reslut)
        # ---------校验2：成分股成交回报校验---------
        elif (hb_data['ticker'] in component_codes and
              hb_data['trade_type'] == '0' and
              hb_data['market'] == wt_reqs['market']):
            # 查询单支成分股数量、现金替代标志
            component_rs = query_cetf_substitute(wt_reqs['ticker'],
                                              hb_data['ticker'])
            component_share = component_rs[0]  # 成分股数量
            substitute_flag = component_rs[1]  # 现金替代标志
            # 查询某个股票持仓信息
            component_stk_end = cetf_get_one_component_stk(Api,hb_data['ticker'])
            component_end = component_stk_end[hb_data['ticker']]
            component_init = dict(component_stk_before[hb_data['ticker']])
            # 申购所需成分股数量
            creation_quantity = component_share * creation_redemption_num
            # 如果该成分股必须禁止现金替代
            if substitute_flag == 0:
                if hb_data['quantity'] != creation_quantity:
                    logger.error('禁止现金替代成分股数量计算错误, 证券代码： ' +
                                 hb_data['ticker'] +
                                 ', 申购需要的成分股数量为： ' +
                                 str(creation_quantity) +
                                 ', 成交数量为： ' + str(hb_data['quantity']))
                    cjhb_reslut['成交回报检查状态'] = 'end'
                    cjhb_reslut['测试结果'] = False
                    cjhb_reslut['测试错误原因'] = (
                        '禁止现金替代成分股数量计算错误, 证券代码： ' +
                        hb_data['ticker'] + ', 申购需要的成分股数量为： ' +
                        str(creation_quantity) + ', 成交数量为： ' +
                        str(hb_data['quantity']))
            # 如果该成分股可以现金替代
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
                elif (component_init['今日可申购赎回持仓'] > creation_quantity and
                    hb_data['quantity'] != creation_quantity ):
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
            # 成分股现金替代标志非0和1
            else:
                error_info = ('成交回报推送错误，当前成分股为:' + hb_data['ticker']
                              + ',现金替代标志为：' + substitute_flag +
                              '，不应推送该成交回报')
                logger.error(error_info)
                cjhb_reslut['成交回报检查状态'] = 'end'
                cjhb_reslut['测试结果'] = False
                cjhb_reslut['测试错误原因'] = error_info
            # 当成交回报检查状态为end时，说明成交回报数据已经有问题，无需进一步检查了
            if cjhb_reslut['成交回报检查状态'] != 'end':
                # etf申购 - -全部成交 - -成分股持仓检查
                cetf_component_cjhb_qc_b(hb_data['ticker'],
                                        component_end,
                                        cjhb_reslut,
                                        component_init,
                                        creation_quantity,
                                        substitute_flag)
        # ---------校验3：一级市场成交回报校验---------
        elif (hb_data['ticker'] == cetf_code1_code2['etf_code1'] and
              hb_data['trade_type'] == '2'):
            primary_secondary_market_check(xtp_id, hb_data, wt_reqs,cjhb_reslut)

        # ---------校验4：同市场资金成交回报校验---------
        elif (hb_data['ticker'] == cetf_code1_code2['etf_code2'] and
              hb_data['trade_type'] == '1'):
            cjhb_var.trade_amount_ha_total += cjhb_reslut['成交金额']
            # 计算etf同市场资金代码成交总金额
            if wt_reqs['market'] == Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A']:
                makert = 1
            else:
                makert = 2
            etf_trade_amount = get_etf_trade_amount(1, wt_reqs['ticker'],
                                creation_redemption_num, makert,
                                component_stk_before)
            #沪A-etf同市场资金回报校验(沪市成分股现金替代)
            if wt_reqs['market'] == Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A']:
                cetf_fund_check_ha(xtp_id,hb_data,wt_reqs,etf_trade_amount,
                                   cjhb_reslut, cjhb_var.trade_amount_ha_total)
            else:
                # 深市跨市场ETF待补充
                TODO

            # 资金成交回报全部推送后，校验费用、持仓等------
            # 查询同市场成分股必须现金替代总金额
            cash_substitute_ha = query_creation_redemption_subcash(
                    cetf_code1_code2['etf_code1'])
            if cash_substitute_ha:
                cash_substitute_ha=cash_substitute_ha['creation_cash_substitute']
            else:
                cash_substitute_ha = 0

            # 查询跨市场成分股现金替代总金额
            cash_substitute_sa = query_crossmakert_sub_cash(
                    cetf_code1_code2['etf_code1'])
            if cash_substitute_sa:
                cash_substitute_sa=cash_substitute_sa['creation_cash_substitute']
            else:
                cash_substitute_sa = 0
            # 申购一份ETF时，同市场+跨市场的必须现金替代+退补现金替代 总金额
            cash_substitute = cash_substitute_ha + cash_substitute_sa
            #print u'申购一份ETF时，同市场+跨市场的必须现金替代+退补现金替代 总金额',cash_substitute ,cash_substitute_ha ,cash_substitute_sa

            # 查询ETF最小申购赎回数量
            creation_redemption_unit = query_creation_redem_unit(
                wt_reqs['ticker'])

            # 同市场+跨市场实际成交总金额，保留三位小数
            cjhb_var.trade_amount_total = round(float(
                (cjhb_var.trade_amount_ha_total+ cjhb_var.trade_amount_sa_total)),3)

            # 计算出应成交总金额,转换成float 并保留三位小数
            calc_trade_amount = round(float(cash_substitute * wt_reqs['quantity'] /
                                 creation_redemption_unit / 10000 +
                                      Decimal(cash_substitute_amount)),3)
            #print 'all_cash',calc_trade_amount

            # 资金成交回报全部推送

            if cjhb_var.trade_amount_total == calc_trade_amount:
                logger.info('成交回报检查：全部成交业务数据开始检查!')
                # etf申购-全部成交-etf费用和持仓检查
                cetf_cjhb_qc_b(QueryInit, QueryEnd, wt_reqs,
                               cjhb_var.trade_amount_total,
                               creation_redemption_num,
                               cjhb_reslut, pyname)
            # 资金成交回报未推送或未全部推送
            elif (cjhb_var.trade_amount_total <calc_trade_amount):
                logger.info('资金成交回报-等待资金成交回报全部推送')
            # 资金成交回报未推送错误
            else:
                logger.error('资金成交回报-资金回报推送出错，'
                             '实际成交的金额和应成交金额分别为' +
                             str(cjhb_var.trade_amount_total) + ',' +
                             str(calc_trade_amount))
                cjhb_reslut['成交回报检查状态'] = 'end'
                cjhb_reslut['测试结果'] = False
                cjhb_reslut['测试错误原因'] = ('资金成交回报-资金回报推送出错，'
                                         '实际成交的金额和应成交金额分别为' +
                                         str(
                                            cjhb_var.trade_amount_total) + ',' +
                                         str(calc_trade_amount))

        # ---------校验5：跨市场资金成交回报校验---------
        elif (hb_data['ticker'] == cetf_code3 and
              hb_data['trade_type'] == '3'):
            cjhb_var.trade_amount_sa_total += cjhb_reslut['成交金额']
            # 计算etf跨市场资金代码申购成交总金额
            cetf_trade_amount = (query_crossmakert_sub_cash(
                cetf_code1_code2['etf_code1'])['creation_cash_substitute']
                                               * creation_redemption_num)
            #沪A-etf资金回报校验(深市成分股现金替代)
            if wt_reqs['market'] == Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A']:
                cetf_fund_check_ha(xtp_id, hb_data, wt_reqs, cetf_trade_amount,
                                   cjhb_reslut,cjhb_var.trade_amount_sa_total)
            else:
                # 深市跨市场ETF待补充
                TODO

            # 资金成交回报全部推送后，校验费用、持仓等------
            # 查询同市场成分股必须现金替代总金额
            cash_substitute_ha = query_creation_redemption_subcash(
                    cetf_code1_code2['etf_code1'])
            if cash_substitute_ha:
                cash_substitute_ha=cash_substitute_ha['creation_cash_substitute']
            else:
                cash_substitute_ha = 0

            # 查询跨市场成分股现金替代总金额
            cash_substitute_sa = query_crossmakert_sub_cash(
                    cetf_code1_code2['etf_code1'])
            if cash_substitute_sa:
                cash_substitute_sa=cash_substitute_sa['creation_cash_substitute']
            else:
                cash_substitute_sa = 0
            # 申购一份ETF时，同市场+跨市场的必须现金替代+退补现金替代 总金额
            cash_substitute = cash_substitute_ha + cash_substitute_sa

            # 查询ETF最小申购赎回数量
            creation_redemption_unit = query_creation_redem_unit(
                wt_reqs['ticker'])

            # 同市场+跨市场实际成交总金额，保留三位小数
            cjhb_var.trade_amount_total = round(float(
                (cjhb_var.trade_amount_ha_total+ cjhb_var.trade_amount_sa_total)),3)

            # 计算出应成交总金额,转换成float 并保留三位小数
            calc_trade_amount = round(float(cash_substitute * wt_reqs['quantity'] /
                                 creation_redemption_unit / 10000 +
                                      Decimal(cash_substitute_amount)),3)

            # 资金成交回报全部推送
            if cjhb_var.trade_amount_total == calc_trade_amount:
                logger.info('成交回报检查：全部成交业务数据开始检查!')
                # etf申购-全部成交-etf费用和持仓检查
                cetf_cjhb_qc_b(QueryInit, QueryEnd, wt_reqs,
                               cjhb_var.trade_amount_total,
                               creation_redemption_num,
                               cjhb_reslut, pyname)
            # 资金成交回报未推送或未全部推送
            elif (cjhb_var.trade_amount_total <calc_trade_amount):
                logger.info('资金成交回报-等待资金成交回报全部推送')
            # 资金成交回报未推送错误
            else:
                logger.error('资金成交回报-资金回报推送出错，'
                             '实际成交的金额和应成交金额分别为' +
                             str(cjhb_var.trade_amount_total) + ',' +
                             str(calc_trade_amount))
                cjhb_reslut['成交回报检查状态'] = 'end'
                cjhb_reslut['测试结果'] = False
                cjhb_reslut['测试错误原因'] = ('资金成交回报-资金回报推送出错，'
                                         '实际成交的金额和应成交金额分别为' +
                                         str(
                                            cjhb_var.trade_amount_total) + ',' +
                                         str(calc_trade_amount))
        else:
            logger.error('成交回报返回未知代码： ' + hb_data['ticker'])
            cjhb_reslut['成交回报检查状态'] = 'end'
            cjhb_reslut['测试结果'] = False
            cjhb_reslut['测试错误原因'] = ('成交回报返回未知代码： '
                                     + hb_data['ticker'])

    # --如果委托方向是赎回，执行如下－－－－－－－－－－－－－－－－－－－－－－－－－－－
    elif wt_reqs['side'] == Api.const.XTP_SIDE_TYPE['XTP_SIDE_REDEMPTION']:
        # ---------校验1：etf二级市场成交回报校验，委托数据和成交数据比较---------
        if (wt_reqs['ticker'] == hb_data['ticker'] and
                    hb_data['trade_type'] == '0'):
            primary_secondary_market_check(xtp_id, hb_data, wt_reqs,cjhb_reslut)
        # ---------校验2：成分股成交回报校验---------
        elif (hb_data['ticker'] in component_codes and
              hb_data['trade_type'] == '0'):
            # 查询单支成分股数量、现金替代标志
            component_rs = query_cetf_substitute(wt_reqs['ticker'],
                                              hb_data['ticker'])
            component_share = component_rs[0]  # etf成分股数量
            substitute_flag = component_rs[1]  # 现金替代标志
            # 查询某个股票持仓信息
            component_stk_end = cetf_get_one_component_stk(Api,
                              hb_data['ticker'])
            component_end = component_stk_end[hb_data['ticker']]
            component_init = dict(component_stk_before[hb_data['ticker']])
            # 赎回ETF后应得到成分股的数量
            creation_quantity = component_share * creation_redemption_num
            # 如果该成分股为禁止现金替代或可以现金替代
            if substitute_flag in (0, 1):
                if hb_data['quantity'] != creation_quantity:
                    logger.error('禁止现金替代成分股数量计算错误, 证券代码： ' +
                                 hb_data['ticker'] +
                                 ', 申购需要的成分股数量为： ' +
                                 str(creation_quantity) +
                                 ', 成交数量为： ' + str(hb_data['quantity']))
                    cjhb_reslut['成交回报检查状态'] = 'end'
                    cjhb_reslut['测试结果'] = False
                    cjhb_reslut['测试错误原因'] = ('禁止现金替代成分股数量计算错误, '
                                 '证券代码： ' + hb_data['ticker'] +
                                 ', 申购需要的成分股数量为： ' +
                                 str(creation_quantity) +
                                 ', 成交数量为： ' + str(hb_data['quantity']))
            # 成分股现金替代标志非0和1
            else:
                error_info = ('成交回报推送错误，当前成分股为:' + hb_data['ticker']
                              + ',现金替代标志为：' + substitute_flag +
                              '，不应推送该成交回报')
                logger.error(error_info)
                cjhb_reslut['成交回报检查状态'] = 'end'
                cjhb_reslut['测试结果'] = False
                cjhb_reslut['测试错误原因'] = error_info
            if cjhb_reslut['成交回报检查状态'] != 'end':
                # etf赎回 - -全部成交 - -成分股持仓检查
                cetf_component_cjhb_qc_s(hb_data['ticker'], component_end,
                                cjhb_reslut, component_init,pre_close_prices)

        # ---------校验3：一级市场成交回报校验 - --------
        elif (hb_data['ticker'] == cetf_code1_code2['etf_code1'] and
              hb_data['trade_type'] == '2'):
            primary_secondary_market_check(xtp_id, hb_data, wt_reqs,cjhb_reslut)

        # ---------校验4：同市场资金成交回报校验---------
        elif (hb_data['ticker'] == cetf_code1_code2['etf_code2'] and
              hb_data['trade_type'] == '1'):
            cjhb_var.trade_amount_ha_total += cjhb_reslut['成交金额']
            cjhb_var.trade_amount_ha_total = round(float(
                cjhb_var.trade_amount_ha_total),3)
            #print ' cjhb_var.trade_amount_ha_total', cjhb_var.trade_amount_ha_total 
            # 计算etf同市场资金代码成交总金额
            if wt_reqs['market'] == Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A']:
                makert = 1
            else:
                makert = 2
            etf_trade_amount = get_etf_trade_amount(2, wt_reqs['ticker'],
                                creation_redemption_num, makert,
                                component_stk_before)
            # 沪A-etf同市场资金回报校验(沪市成分股现金替代)
            if wt_reqs['market'] == Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A']:
                cetf_fund_check_ha(xtp_id,hb_data,wt_reqs,etf_trade_amount,
                                   cjhb_reslut,cjhb_var.trade_amount_ha_total)
            else:
                # 深市跨市场ETF待补充
                TODO

            # 资金成交回报全部推送后，校验费用、持仓等------
            # 查询同市场成分股必须现金替代总金额
            cash_substitute_ha = query_creation_redemption_subcash(
                    cetf_code1_code2['etf_code1'])
            if cash_substitute_ha:
                cash_substitute_ha=cash_substitute_ha['redemption_cash_substitute']
            else:
                cash_substitute_ha = 0

            # 查询跨市场成分股现金替代总金额
            cash_substitute_sa = query_crossmakert_sub_cash(
                    cetf_code1_code2['etf_code1'])
            if cash_substitute_sa:
                cash_substitute_sa=cash_substitute_sa['redemption_cash_substitute']
            else:
                cash_substitute_sa = 0

            # 申购一份ETF时，同市场+跨市场的必须现金替代+退补现金替代 总金额
            cash_substitute = cash_substitute_ha + cash_substitute_sa

            # 查询ETF最小申购赎回数量
            creation_redemption_unit = query_creation_redem_unit(
                wt_reqs['ticker'])

            # 计算出同市场+跨市场成交总金额，保留三位小数
            cjhb_var.trade_amount_total = round(float(
                cjhb_var.trade_amount_ha_total +cjhb_var.trade_amount_sa_total),3)

            # 计算出应成交总金额，转换成float并保留三位小数
            calc_trade_amount = round(float(cash_substitute *
                wt_reqs['quantity'] / creation_redemption_unit /10000),3)
            #print 'calc_all',calc_trade_amount

            # 资金成交回报全部推送
            if cjhb_var.trade_amount_total == calc_trade_amount:
                logger.info('成交回报检查：全部成交业务数据开始检查!')
                # etf申购-全部成交-etf费用和持仓检查
                cetf_cjhb_qc_s(QueryInit, QueryEnd, wt_reqs,
                               cjhb_var.trade_amount_ha_total,
                               cjhb_var.trade_amount_total,
                               creation_redemption_num,
                               cjhb_reslut, pyname)
            # 资金成交回报未推送或未全部推送
            elif (cjhb_var.trade_amount_total <calc_trade_amount):
                logger.info('资金成交回报-等待资金成交回报全部推送')
            # 资金成交回报未推送错误
            else:
                logger.error('资金成交回报-资金回报推送出错，'
                             '实际成交的金额和应成交金额分别为' +
                             str(cjhb_var.trade_amount_total) + ',' +
                             str(calc_trade_amount))
                cjhb_reslut['成交回报检查状态'] = 'end'
                cjhb_reslut['测试结果'] = False
                cjhb_reslut['测试错误原因'] = ('资金成交回报-资金回报推送出错，'
                                         '实际成交的金额和应成交金额分别为' +
                                         str(cjhb_var.trade_amount_total) + ','
                                         + str(calc_trade_amount))

        # ---------校验5：跨市场资金成交回报校验---------
        elif (hb_data['ticker'] == cetf_code3 and
              hb_data['trade_type'] == '3'):
            cjhb_var.trade_amount_sa_total += cjhb_reslut['成交金额']
            # 计算etf跨市场资金代码赎回成交总金额
            cetf_trade_amount = (query_crossmakert_sub_cash(
                cetf_code1_code2['etf_code1'])['redemption_cash_substitute']
                                * creation_redemption_num)
            #沪A-etf跨市场资金回报校验（深市成分股现金）
            if wt_reqs['market'] == Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A']:
                cetf_fund_check_ha(xtp_id, hb_data, wt_reqs, cetf_trade_amount,
                                   cjhb_reslut,cjhb_var.trade_amount_sa_total)
            else:
                # 深市跨市场ETF待补充
                TODO

            # 资金成交回报全部推送后，校验费用、持仓等------
            # 查询同市场成分股必须现金替代总金额
            cash_substitute_ha = query_creation_redemption_subcash(
                cetf_code1_code2['etf_code1'])
            if cash_substitute_ha:
                cash_substitute_ha = cash_substitute_ha[
                    'redemption_cash_substitute']
            else:
                cash_substitute_ha = 0

            # 查询跨市场成分股现金替代总金额
            cash_substitute_sa = query_crossmakert_sub_cash(
                cetf_code1_code2['etf_code1'])
            if cash_substitute_sa:
                cash_substitute_sa = cash_substitute_sa[
                    'redemption_cash_substitute']
            else:
                cash_substitute_sa = 0

            # 申购一份ETF时，同市场+跨市场的必须现金替代+退补现金替代 总金额
            cash_substitute = cash_substitute_ha + cash_substitute_sa

            # 查询ETF最小申购赎回数量
            creation_redemption_unit = query_creation_redem_unit(
                wt_reqs['ticker'])

            # 计算出同市场+跨市场成交总金额，保留三位小数
            cjhb_var.trade_amount_total = round(float(
                cjhb_var.trade_amount_ha_total + cjhb_var.trade_amount_sa_total),
                3)

            # 计算出应成交总金额，转换成float并保留三位小数
            calc_trade_amount = round(float(cash_substitute *
                                            wt_reqs['quantity'] /
                                        creation_redemption_unit / 10000),3)

            # 资金成交回报全部推送
            if cjhb_var.trade_amount_total == calc_trade_amount:
                logger.info('成交回报检查：全部成交业务数据开始检查!')
                # etf申购-全部成交-etf费用和持仓检查
                cetf_cjhb_qc_s(QueryInit, QueryEnd, wt_reqs,
                               cjhb_var.trade_amount_ha_total,
                               cjhb_var.trade_amount_total,
                               creation_redemption_num,
                               cjhb_reslut, pyname)
            # 资金成交回报未推送或未全部推送
            elif (cjhb_var.trade_amount_total < calc_trade_amount):
                logger.info('资金成交回报-等待资金成交回报全部推送')
            # 资金成交回报未推送错误
            else:
                logger.error('资金成交回报-资金回报推送出错，'
                             '实际成交的金额和应成交金额分别为' +
                             str(cjhb_var.trade_amount_total) + ',' +
                             str(calc_trade_amount))
                cjhb_reslut['成交回报检查状态'] = 'end'
                cjhb_reslut['测试结果'] = False
                cjhb_reslut['测试错误原因'] = ('资金成交回报-资金回报推送出错，'
                                         '实际成交的金额和应成交金额分别为' +
                                         str(
                                             cjhb_var.trade_amount_total) + ','
                                         + str(calc_trade_amount))
        else:
            logger.error('成交回报返回未知代码： ' + hb_data['ticker'])
            cjhb_reslut['成交回报检查状态'] = 'end'
            cjhb_reslut['测试结果'] = False
            cjhb_reslut['测试错误原因'] = ('成交回报返回未知代码： '
                                     + hb_data['ticker'])

    return cjhb_reslut



def cetf_cjhb_qc_b(QueryInit, QueryEnd, wt_reqs,
                  trade_amount_total, creation_unit,
                   cjhb_reslut, py_name):
    """
    etf申购--全部成交--etf费用和持仓检查
    :param QueryInit:
    :param QueryEnd:
    :param wt_reqs:
    :param trade_amount_total: 实际成交总金额
    :param creation_unit: 申购份数
    :param py_name:
    :return:
    """
    logger.info('成交回报－申购－全部成交－费用持仓检查')
    #  ----计算费用----
    # nav是etf基金份额净值
    nav = query_cetf_nav(wt_reqs['ticker'])
    if py_name:
        fee_etf = ServiceConfig.fee_etf_creation_redemption[py_name]
        cjhb_var.fee_etf_min = float(fee_etf[ServiceConfig.fee_etf_min_str])
        cjhb_var.fee_rate_etf_creation = float(
            fee_etf[ServiceConfig.fee_rate_etf_creation_str])
    # 申购费用
    fee = wt_reqs['quantity'] * cjhb_var.fee_rate_etf_creation * nav / 10000
    if fee <= cjhb_var.fee_etf_min:
        fee = cjhb_var.fee_etf_min
    else:
        fee = float(Decimal(Decimal(str(fee)).quantize(Decimal('.01'),
                                                       rounding=ROUND_HALF_UP)))
    #原有费用加上过户费用
    count = query_cetf_count(wt_reqs['ticker'])
    fee_count = cjhb_var.fee_count_rate_etf_creation * count * creation_unit
    fee += float(fee_count)

    # ----获取预估现金差额----
    estimate_cash_origin = query_estimate_cash_component(wt_reqs['ticker'])
    estimate_cash = (estimate_cash_origin * creation_unit
        if estimate_cash_origin > 0 else 0)

    # ----判断可用资金是否正确-----
    if abs(QueryInit['可用资金'] - trade_amount_total -
                   estimate_cash - fee - QueryEnd['可用资金']) > 0.00001:
        logger.error('可用资金计算有错,原可用资金、成交金额、'
                     '预估现金差额总额、费用、现可用资金分别是' + str(
            QueryInit['可用资金']) + ',' + str(trade_amount_total) +
                     ',' + str(estimate_cash) + ',' + str(
            fee) + ',' + str(QueryEnd['可用资金']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['可用资金计算有错', {
            '原可用资金': QueryInit['可用资金'],
            '成交金额': trade_amount_total,
            '预估现金差额总额': estimate_cash,
            '费用': fee,
            '现可用资金': QueryEnd['可用资金']
        }]
    # ----判断总资产是否正确-----
    elif abs(QueryInit['总资产'] - trade_amount_total -
                     fee - QueryEnd['总资产']) > 0.00001:
        logger.error('总资产计算有错,原总资产、成交金额、费用、现总资产分别是' +
                     str(QueryInit['总资产']) + ',' + str(trade_amount_total)
                     + ',' + str(fee) + ',' + str(QueryEnd['总资产']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['总资产计算有错', {
            '原总资产': QueryInit['总资产'],
            '成交金额': trade_amount_total,
            '费用': fee,
            '现总资产': QueryEnd['总资产']
        }]
    # ----判断买入资金是否正确-----
    elif (QueryEnd['买入资金'] - trade_amount_total -
              QueryInit['买入资金']) > 0.00001:
        logger.error('买入资金计算有错,原买入资金、成交金额、现买入资金分别是' +
                     str(QueryInit['买入资金']) + ',' +
                     str(trade_amount_total) + ',' +
                     str(QueryEnd['买入资金']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['买入资金计算有错', {
            '原买入资金': QueryInit['买入资金'],
            '成交金额': trade_amount_total,
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
    elif QueryEnd['预扣资金'] - estimate_cash - QueryInit['预扣资金'] > 0.00001:
        logger.error('预扣资金计算有错,原预扣资金、预估现金差额总额、'
                     '申购份数、现预扣资金分别是' +
                     str(QueryInit['预扣资金']) + ',' +
                     str(estimate_cash) + ',' +
                     str(creation_unit) + ',' +
                     str(QueryEnd['预扣资金']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['预扣资金计算有错', {
            '原预扣资金': QueryInit['预扣资金'],
            '预估现金差额总额': estimate_cash,
            '申购份数': creation_unit,
            '现预扣资金': QueryEnd['预扣资金']
        }]
    # -----判断下单前后股票代码、市场是否一致-------
    elif (QueryEnd['股票代码'] != QueryInit['股票代码'] or
                    QueryEnd['市场'] != QueryInit['市场']):
        logger.error('下单前后查询的市场股票代码信息不一致,下单前查询的市场和股票代码是'
                     + str(QueryInit['市场']) +
                     ',' + str(QueryInit['股票代码']) +
                     ',下单后查询的市场和股票代码是' +
                     str(QueryEnd['市场']) +
                     ',' + str(QueryEnd['股票代码']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['下单前后查询的市场股票代码信息不一致', {
            '下单前查询的市场是': QueryInit['市场'],
            '下单前查询的股票代码是': QueryInit['股票代码'],
            '下单后查询的市场是': QueryEnd['市场'],
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
    elif QueryEnd['今日可申购赎回持仓'] != QueryInit['今日可申购赎回持仓']:
        logger.error('今日可申购赎回持仓不正确，原今日可申购赎回持仓，' +
                     '现今日可申购赎回持仓分别是' +
                     str(QueryInit['今日可申购赎回持仓']) +
                     ',' + str(QueryEnd['今日可申购赎回持仓']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['今日可申购赎回持仓不正确', {
            '原今日可申购赎回持仓': QueryInit['今日可申购赎回持仓'],
            '现今日可申购赎回持仓': QueryEnd['今日可申购赎回持仓']
        }]
    else:
        logger.info('申购_全成_成交回报_业务校验正确！')
        cjhb_reslut['成交回报检查状态'] = 'end'


def cetf_component_cjhb_qc_b(ticker, component_end, cjhb_reslut,
                            component_init, creation_quantity, substitute_flag):
    """*********************引用单市场的函数，未仔细校验**************************
    etf申购--全部成交--成分股持仓检查
    """
    logger.info('成交回报－申购－全部成交－成分股: ' + str(ticker) + '持仓检查')

    # -----判断下单前后股票代码、市场是否一致-------
    if component_init['证券代码'] != component_end['证券代码'] or \
        component_init['市场'] != component_end['市场']:
        logger.error('下单前后查询的市场证券代码信息不一致,下单前查询的市场和证券代码是'
                     + str(component_init['市场']) +
                     ',' + str(component_init['证券代码']) +
                     ',下单后查询的市场和证券代码是' +
                     str(component_end['市场']) +
                     ',' + str(component_end['证券代码']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['下单前后查询的市场证券代码信息不一致', {
            '下单前查询的市场是': component_init['市场'],
            '下单前查询的证券代码是': component_init['证券代码'],
            '下单后查询的市场是': component_end['市场'],
            '下单后查询的证券代码是': component_end['证券代码'],
        }]
    # -----判断总持仓是否正确
    elif (component_init['总持仓'] - component_end['总持仓'] -
              cjhb_reslut['成交数量'] > 0.00001):
        logger.error('总持仓不正确，原总持仓，成交数量，现总持仓分别是' +
                     str(component_init['总持仓']) +
                     ',' + str(cjhb_reslut['成交数量']) +
                     ',' + str(component_end['总持仓']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['总持仓不正确', {
            '原总持仓': component_init['总持仓'],
            '成交数量': cjhb_reslut['成交数量'],
            '现总持仓': component_end['总持仓'],
        }]
    # --判断可卖持仓成交量是否正确
    elif component_init['可卖持仓'] - component_end['可卖持仓'] \
            - cjhb_reslut['成交数量'] > 0.00001:
        logger.error('可卖持仓不正确，原可卖持仓，现可卖持仓，成交数量分别是' +
                     str(component_init['可卖持仓']) +
                     ',' + str(component_end['可卖持仓']) +
                     ',' + str(cjhb_reslut['成交数量']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['可卖持仓不正确', {
            '原可卖持仓': component_init['可卖持仓'],
            '现可卖持仓': component_end['可卖持仓'],
            '成交数量': cjhb_reslut['成交数量']
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
            '浮动盈亏不正确/，期待浮动盈亏和实际浮动盈亏分别是' +
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
            - cjhb_reslut['成交数量'] > 0.00001:
        logger.error('今日可申购赎回持仓不正确，原今日可申购赎回持仓，' +
                     '现今日可申购赎回持仓，成交数量分别是' +
                     str(component_init['今日可申购赎回持仓']) +
                     ',' + str(component_end['今日可申购赎回持仓']) +
                     ',' + str(cjhb_reslut['成交数量']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['今日可申购赎回持仓不正确', {
            '原今日可申购赎回持仓': component_init['今日可申购赎回持仓'],
            '现今日可申购赎回持仓': component_end['今日可申购赎回持仓'],
            '成交数量': cjhb_reslut['成交数量']
        }]
    else:
        logger.info('买_全成_成交回报_成分股校验正确！')
        cjhb_reslut['成交回报检查状态'] = 'end'



def cetf_component_cjhb_qc_s(ticker, component_end, cjhb_reslut,
                            component_init, pre_close_prices):
    """
    etf赎回--全部成交--成分股持仓检查
    :param ticker:
    :param component_end:
    :param cjhb_reslut:
    :param component_init:
    :param pre_close_prices:
    :return:
    """

    logger.info('成交回报－赎回－全部成交－成分股: ' + str(ticker) + '持仓检查')

    # 获取成分股昨收价
    pre_close_price = pre_close_prices[ticker]

    # --计算期待持仓成本应该是，深圳赎回时会返回全部现金替代的成分股回报，且成交数量为0
    price_avg = 0
    if cjhb_reslut['成交数量'] != 0:
        price_avg = ((component_init['持仓成本价'] * component_init['总持仓'] +
                     cjhb_reslut['成交数量'] * pre_close_price) /
                    (component_init['总持仓'] + cjhb_reslut['成交数量']))
    # 应得持仓成本价和实际持仓成本价误差
    price_avg_deviation = round(component_end['持仓成本价'] - price_avg,
                                cjhb_var.avg_price_DecimalPlaces)

    # -----判断下单前后股票代码、市场是否一致-------
    if component_init['证券代码'] != component_end['证券代码'] or \
                    component_init['市场'] != component_end['市场']:
        logger.error('下单前后查询的市场证券代码信息不一致,下单前查询的市场和证券代码是'
                     + str(component_init['市场']) +
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
              cjhb_reslut['成交数量'] > 0.00001):
        logger.error('总持仓不正确，原总持仓，成交数量，现总持仓分别是' +
                     str(component_init['总持仓']) +
                     ',' + str(cjhb_reslut['成交数量']) +
                     ',' + str(component_end['总持仓']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['总持仓不正确', {
            '原总持仓': component_init['总持仓'],
            '成交数量': cjhb_reslut['成交数量'],
            '现总持仓': component_end['总持仓'],
        }]
    # --判断可卖持仓成交量是否正确
    elif component_end['可卖持仓'] - component_init['可卖持仓'] \
            - cjhb_reslut['成交数量'] > 0.00001:
        logger.error('可卖持仓不正确，原可卖持仓，现可卖持仓，成交数量分别是' +
                     str(component_init['可卖持仓']) +
                     ',' + str(component_end['可卖持仓']) +
                     ',' + str(cjhb_reslut['成交数量']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['可卖持仓不正确', {
            '原可卖持仓': component_init['可卖持仓'],
            '现可卖持仓': component_end['可卖持仓'],
            '成交数量': cjhb_reslut['成交数量']
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
            - cjhb_reslut['成交数量'] > 0.00001:
        logger.error('今日可申购赎回持仓不正确，原今日可申购赎回持仓，' +
                     '现今日可申购赎回持仓，成交数量分别是' +
                     str(component_init['今日可申购赎回持仓']) +
                     ',' + str(component_end['今日可申购赎回持仓']) +
                     ',' + str(cjhb_reslut['成交数量']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['今日可申购赎回持仓不正确', {
            '原今日可申购赎回持仓': component_init['今日可申购赎回持仓'],
            '现今日可申购赎回持仓': component_end['今日可申购赎回持仓'],
            '成交数量': cjhb_reslut['成交数量']
        }]
    else:
        logger.info('买_全成_成交回报_成分股校验正确！')
        cjhb_reslut['成交回报检查状态'] = 'end'


def cetf_cjhb_qc_s(QueryInit, QueryEnd, wt_reqs,
                   trade_amount_ha, trade_amount_total,redemption_unit,
                   cjhb_reslut,py_name):
    """
    etf赎回--全部成交--费用持仓检查
    :param QueryInit:
    :param QueryEnd:
    :param wt_reqs:
    :param trade_amount_ha: 沪市成交总金额
    :param trade_amount_total: 沪市+深市的总成交总金额
    :param redemption_unit: 赎回份数
    :param cjhb_reslut:
    :param py_name:
    :return:
    """
    # 定义函数，校验赎回后etf可卖持仓
    def check_avliable_sell(QueryInit,QueryEnd,wt_reqs):
        """
        校验赎回后etf可卖持仓
        """
        # 计算出今天买入的etf数量
        etf_today_asset = QueryInit['今日可申购赎回持仓'] - QueryInit['昨日持仓']
        # 如果今天买入的etf数量大于等于赎回数量，赎回前后该etf可卖持仓不变
        if (etf_today_asset >= wt_reqs['quantity'] and
            QueryInit['可卖持仓'] != QueryEnd['可卖持仓']):
            return False
        # 如果今天买入的etf数量小于赎回数量，
        # 赎回后该etf可卖持仓 = 今日可申购赎回持仓 - 赎回数量
        elif (etf_today_asset<wt_reqs['quantity']<=QueryInit['今日可申购赎回持仓']
            and QueryInit['今日可申购赎回持仓'] - wt_reqs['quantity']
                !=QueryEnd['可卖持仓']):
            return False
        else:
            return True

    logger.info('成交回报－赎回－全部成交－费用持仓检查')
    # ----计算费用----
    # etf单位净值
    nav = query_cetf_nav(wt_reqs['ticker'])
    if py_name:
        fee_etf = ServiceConfig.fee_etf_creation_redemption[py_name]
        cjhb_var.fee_etf_min = float(fee_etf[ServiceConfig.fee_etf_min_str])
        cjhb_var.fee_rate_etf_redemption = float(
            fee_etf[ServiceConfig.fee_rate_etf_redemption_str])
    # 赎回费用
    fee = wt_reqs['quantity'] * cjhb_var.fee_rate_etf_redemption * nav / 10000
    if fee <= cjhb_var.fee_etf_min:
        fee = cjhb_var.fee_etf_min
    else:
        fee = float(Decimal(Decimal(str(fee)).quantize(Decimal('.01'),
                                                       rounding=ROUND_HALF_UP)))
    #原有费用加上过户费用
    count = query_cetf_count(wt_reqs['ticker'])
    fee_count = cjhb_var.fee_count_rate_etf_redemption * count * redemption_unit
    fee += float(fee_count)

    # ----获取预估现金差额----
    estimate_cash_origin = query_estimate_cash_component(wt_reqs['ticker'])
    estimate_cash = -(estimate_cash_origin * redemption_unit
                     if estimate_cash_origin < 0 else 0)

    # ----判断可用资金是否正确-----
    #if abs(QueryInit['可用资金'] + trade_amount_ha -
    if abs(QueryInit['可用资金'] + trade_amount_total -
                   estimate_cash - fee - QueryEnd['可用资金'])> 0.00001:
        #print 'keyongzijn ***********',QueryInit['可用资金'] ,trade_amount_total, estimate_cash,fee,QueryEnd['可用资金']
        logger.error('可用资金计算有错,原可用资金、沪市成交金额、'
                     '预估现金差额总额、费用、现可用资金分别是' +
                     str(QueryInit['可用资金']) +
                     ',' + str(trade_amount_total) +
                     ',' + str(estimate_cash) +
                     ',' + str(fee) + ',' + str(QueryEnd['可用资金']))
        a=QueryInit['可用资金'] + trade_amount_total -estimate_cash - fee - QueryEnd['可用资金']
        #print a,'aaa'
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['可用资金计算有错', {
            '原可用资金': QueryInit['可用资金'],
            #'沪市成交金额': trade_amount_ha,
            '沪市成交金额': trade_amount_total,
            '预估现金差额总额': estimate_cash,
            '费用': fee,
            '现可用资金': QueryEnd['可用资金']
        }]
    # ----判断总资产是否正确-----
    elif abs(QueryInit['总资产'] + trade_amount_total -
                 fee - QueryEnd['总资产'])> 0.00001:
        logger.error('总资产计算有错,原总资产、成交金额、费用、现总资产分别是' +
                     str(QueryInit['总资产']) + ',' + str(trade_amount_total) +
                     ',' + str(fee) + ',' + str(QueryEnd['总资产']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['总资产计算有错', {
            '原总资产': QueryInit['总资产'],
            '成交金额': trade_amount_total,
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
    #elif abs(QueryEnd['卖出资金'] - trade_amount_ha -
    elif abs(QueryEnd['卖出资金'] - trade_amount_total -
            QueryInit['卖出资金']) > 0.00001:
        logger.error('卖出资金计算有错,原卖出资金、沪市成交金额、现卖出资金分别是' +
                     str(QueryInit['卖出资金']) + ',' +
                     str(trade_amount_total) + ',' +
                     str(QueryEnd['卖出资金']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['卖出资金计算有错', {
            '原卖出资金': QueryInit['卖出资金'],
            '沪市成交金额': trade_amount_ha,
            '沪市成交金额': trade_amount_total,
            '现卖出资金': QueryEnd['卖出资金']
        }]
    # ----判断卖出费用是否正确-----
    elif abs(QueryEnd['卖出费用'] - fee - QueryInit['卖出费用']) > 0.00001 :
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
    elif (QueryEnd['预扣资金'] - estimate_cash -
            QueryInit['预扣资金']) > 0.00001 :
        logger.error('预扣资金计算有错,原预扣资金、预估现金差额总额、'
                     '赎回份数、现预扣资金分别是' +
                     str(QueryInit['预扣资金']) + ',' +
                     str(estimate_cash) + ',' +
                     str(redemption_unit) + ',' +
                     str(QueryEnd['预扣资金']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['预扣资金计算有错', {
            '原预扣资金': QueryInit['预扣资金'],
            '预估现金差额总额': estimate_cash,
            '赎回份数': redemption_unit,
            '现预扣资金': QueryEnd['预扣资金']
        }]
    # ---－判断总持仓是否正确
    elif abs(QueryInit['总持仓'] - QueryEnd['总持仓'] -
                     wt_reqs['quantity']) > 0.00001:
        logger.error('总持仓不正确，原总持仓，成交数量，现总持仓分别是' +
                     str(QueryInit['总持仓']) +
                     ',' + str(wt_reqs['quantity']) +
                     ',' + str(QueryEnd['总持仓']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['总持仓不正确', {
            '原总持仓': QueryInit['总持仓'],
            '成交数量': wt_reqs['quantity'],
            '现总持仓': QueryEnd['总持仓'],
        }]
    # --判断可卖持仓是否正确
    elif not check_avliable_sell(QueryInit,QueryEnd,wt_reqs):
        logger.error('可卖持仓不正确，原可卖持仓，现可卖持仓，成交数量分别是' +
                     str(QueryInit['可卖持仓']) +
                     ',' + str(QueryEnd['可卖持仓']) +
                     ',' + str(wt_reqs['quantity']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['可卖持仓不正确', {
            '原可卖持仓': QueryInit['可卖持仓'],
            '现可卖持仓': QueryEnd['可卖持仓'],
            '成交数量': wt_reqs['quantity']
        }]

    # -----判断下单前后股票代码、市场是否一致-------
    elif (QueryEnd['股票代码'] != QueryInit['股票代码'] or
             QueryEnd['市场'] != QueryInit['市场']):
        logger.error('下单前后查询的市场股票代码信息不一致,下单前查询的市场和股票代码是'
                     + str(QueryInit['市场']) +
                     ',' + str(QueryInit['股票代码']) +
                     ',下单后查询的市场和股票代码是' +
                     str(QueryEnd['市场']) +
                     ',' + str(QueryEnd['股票代码']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['下单前后查询的市场股票代码信息不一致', {
            '下单前查询的市场是': QueryInit['市场'],
            '下单前查询的股票代码是': QueryInit['股票代码'],
            '下单后查询的市场是': QueryEnd['市场'],
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
    elif abs(QueryInit['今日可申购赎回持仓'] - QueryEnd['今日可申购赎回持仓'] -
                     wt_reqs['quantity']) > 0.00001:
        logger.error('今日可申购赎回持仓不正确，原今日可申购赎回持仓，' +
                     '现今日可申购赎回持仓分别是' +
                     str(QueryInit['今日可申购赎回持仓']) +
                     ',' + str(QueryEnd['今日可申购赎回持仓']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['今日可申购赎回持仓不正确', {
            '原今日可申购赎回持仓': QueryInit['今日可申购赎回持仓'],
            '现今日可申购赎回持仓': QueryEnd['今日可申购赎回持仓']
        }]
    else:
        logger.info('赎回_全成_成交回报_业务校验正确！')
        cjhb_reslut['成交回报检查状态'] = 'end'


def primary_secondary_market_check(xtp_id, hb_data, wt_reqs, cjhb_reslut):
    """etf一级市场和二级市场回报校验"""

    # 设置标志来区别1级市场和2级市场,方面区分写日志--True：二级市场  False:一级市场
    if wt_reqs['ticker'] == hb_data['ticker']:
        flag = True
    else:
        flag = False

    # 判断委托和成交回报的xtpid，市场，买卖方向是否一致
    if (xtp_id == hb_data['order_xtp_id'] and
        wt_reqs['market'] == hb_data['market'] and
        wt_reqs['side'] == hb_data['side']) is False:
        if flag:
            logger.error('etf二级市场成交回报和委托信息不一致，如：xtpid,market,side')
            cjhb_reslut['测试错误原因'] = ('二级市场成交回报和委托信息不一致，' +
                                    '如：xtpid,market,side')
        else:
            logger.error('etf一级市场成交回报和委托信息不一致，如：xtpid,market,side')
            cjhb_reslut['测试错误原因'] = ('一级市场成交回报和委托信息不一致，' +
                                    '如：xtpid,market,side')
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False

    # 判断成交价格是否为0
    elif hb_data['price'] != 0:
        if flag:
            logger.error('etf二级市场成交回报-价格错误，应为0，实际为' +
                         str(hb_data['price']))
            cjhb_reslut['测试错误原因'] = ('etf二级市场成交回报-价格错误，应为0，'
                        + '实际为' + str(hb_data['price']))
        else:
            logger.error('etf一级市场成交回报-价格错误，应为0，实际为' +
                         str(hb_data['price']))
            cjhb_reslut['测试错误原因'] = ('etf一级市场成交回报-价格错误，应为0，'
                                     + '实际为' + str(hb_data['price']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False

    # 判断成交数量是否等于委托数量
    elif hb_data['quantity'] != wt_reqs['quantity']:
        if flag:
            logger.error('etf二级市场成交回报-委托数量和成交回报数量不一致,'
                         '委托数量和成交回报数量分别为' +
                         str(wt_reqs['quantity']) + ',' +
                         str(hb_data['quantity']))
            cjhb_reslut['测试错误原因'] = ('etf二级市场成交回报-委托数量和成交回报数量'
                                '不一致,委托数量和成交回报数量分别为' +
                                str(wt_reqs['quantity']) + ',' +
                                str(hb_data['quantity']))
        else:
            logger.error('etf一级市场成交回报-委托数量和成交回报数量不一致,'
                         '委托数量和成交回报数量分别为' +
                         str(wt_reqs['quantity']) + ',' +
                         str(hb_data['quantity']))
            cjhb_reslut['测试错误原因'] = ('etf一级市场成交回报-委托数量和成交回报数量'
                                '不一致,委托数量和成交回报数量分别为' +
                                str(wt_reqs['quantity']) + ',' +
                                str(hb_data['quantity']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False

    # 判断成交金额是否为0
    elif hb_data['trade_amount'] != 0:
        if flag:
            logger.error('etf二级市场成交回报-成交金额错误，应为0，实际为' +
                         str(hb_data['trade_amount']))
            cjhb_reslut['测试错误原因'] = ('etf二级市场成交回报-成交金额错误，应为0，'
                                     + '实际为' + str(hb_data['trade_amount']))
        else:
            logger.error('etf一级市场成交回报-成交金额错误，应为0，实际为' +
                         str(hb_data['trade_amount']))
            cjhb_reslut['测试错误原因'] = ('etf一级市场成交回报-成交金额错误，应为0，'
                                     + '实际为' + str(hb_data['trade_amount']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False

    else:
        if flag:
            logger.info('etf二级市场成交回报校验正确')
        else:
            logger.info('etf一级市场成交回报校验正确')
        cjhb_reslut['成交回报检查状态'] = 'end'


def cetf_fund_check_ha(xtp_id, hb_data, wt_reqs, etf_trade_amount,cjhb_reslut,
                       trade_amount_actual):
    """
    沪市的etf资金回报校验（同市场资金回报/跨市场资金回报）
    :param xtp_id:
    :param hb_data:
    :param wt_reqs:
    :param etf_trade_amount:
    :param cjhb_reslut:
    :param trade_amount_actual:当前实际总成交额（同市场和跨市场分开计算）
    :return:
    """
    # 判断委托和成交回报的xtpid，市场，买卖方向是否一致
    if (xtp_id == hb_data['order_xtp_id'] and
        wt_reqs['market'] == hb_data['market'] and
        wt_reqs['side'] == hb_data['side']) is False:
        logger.error('成交回报和委托信息不一致，如：xtpid,market,side')
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = '成交回报和委托信息不一致，' \
                                '如：xtpid,market,side'
    # 计算出的成交金额小于1000
    elif etf_trade_amount < cjhb_var.cetf_fund_amount:
        # 金额校验
        if abs(hb_data['trade_amount'] - etf_trade_amount) > 0.00001:
            logger.error('etf资金成交回报-实际成交金额和期望的成交金额不一致，'
                    '分别为%d,%d' % (hb_data['trade_amount'], etf_trade_amount))
            cjhb_reslut['成交回报检查状态'] = 'end'
            cjhb_reslut['测试结果'] = False
            cjhb_reslut['测试错误原因'] = ('etf资金成交回报-实际成交金额和期望的成' +
                                '交金额不一致，分别为' + str(hb_data[
                                'trade_amount']) + ',' + str(etf_trade_amount))
        else:
            logger.info('etf资金成交回报校验正确')
            cjhb_reslut['成交回报检查状态'] = 'end'
    # 计算出的成交金额大于1000
    elif etf_trade_amount >= cjhb_var.cetf_fund_amount:
        if trade_amount_actual < etf_trade_amount:
            logger.info("等待资金成交回报全部返回！")
            cjhb_reslut['成交回报检查状态'] = 'end'
        # 金额校验
        elif (trade_amount_actual >= etf_trade_amount and
            abs(etf_trade_amount - trade_amount_actual) >0.00001):
                logger.error('etf资金成交回报-实际成交金额和期望的成交金额' +
                            '不一致，分别为' + str(trade_amount_actual)
                             + ',' + str(etf_trade_amount))
                cjhb_reslut['成交回报检查状态'] = 'end'
                cjhb_reslut['测试结果'] = False
                cjhb_reslut['测试错误原因'] = ('etf资金成交回报-实际成交金额和期望的'
                    +'成交金额不一致，分别为' + str(trade_amount_actual)
                    + ',' + str(etf_trade_amount))
        else:
            cjhb_reslut['成交回报检查状态'] = 'end'
    # 未知结果
    else:
        TODO



def etf_fund_check_sa(xtp_id, hb_data, wt_reqs, etf_trade_amount):
    """
    深市的etf资金回报校验
    :param xtp_id:
    :param hb_data:
    :param wt_reqs:
    :param etf_trade_amount:
    :return:
    """

def get_etf_trade_amount(is_creation_redemption, ticker, unit,market_id,
                         component_stk_before):
    """
    计算etf申赎的同市场资金代码的成交金额
    :param is_creation_redemption: 申赎类型 - 1：申购，2：赎回
    :param ticker: etf交易代码
    :param unit: 申赎份数
    :param component_stk_before: 下单前成分股持仓
    :return: etf成交金额
    """
    etf_trade_amount = 0
    # 查询etf成分股申购所需数量、现金替代标识、申赎替代金额
    components_info = query_cetf_components_info(ticker,
                                               market_id)
    # 申购
    if is_creation_redemption == 1:
        for stk in components_info:
            # 允许现金替代
            if stk[1] == 1:
                if not component_stk_before:
                    etf_trade_amount += ((unit * stk[2] - 0) *
                        float(stk[4]) * (1 + float(stk[3]) / 100000))
                else:
                    if unit * stk[2] > component_stk_before[stk[0]][
                        '今日可申购赎回持仓']:
                        etf_trade_amount += ((unit * stk[2] -
                                             component_stk_before[stk[0]][
                                                 '今日可申购赎回持仓'])
                                * float(stk[4]) * (1 + float(stk[3]) / 100000))

            # 全部现金替代
            elif stk[1] == 2:
                etf_trade_amount += unit * float(stk[7]) / 10000
    # 赎回
    elif is_creation_redemption == 2:
        for stk in components_info:
            if stk[1] == 2:
                etf_trade_amount += unit * float(stk[7]) / 10000
    else:
        logger.error('错误的参数值，1表示申购，2表示赎回，实际参数值为' +
                     str(is_creation_redemption))
    return etf_trade_amount
