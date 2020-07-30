#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
from decimal import Decimal
from decimal import ROUND_HALF_UP
from decimal import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
import ServiceConfig
from log import *
sys.path.append("/home/yhl2/workspace/xtp_test/MoneyFund/moneyfundmysql")
from mfgetUpOrDownPrice import *
from mfdatabase_manager import QueryTable
sys.path.append("/home/yhl2/workspace/xtp_test/MoneyFund/moneyfundservice")
from mfCheckDataPrice import *
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from mysql_config import out_rights_issue_params

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
fee_rate_sell =ServiceConfig.FEE_RATE_SELL
fee_min = ServiceConfig.FEE_MIN
#定义逆回购费率
fee_rate_reverse_repo = ServiceConfig.FEE_RATE_REVERSE_REPO
fee_reverse_repo_min = ServiceConfig.FEE_REVERSE_REPO_MIN
#--持仓成本，保留小数位
avg_price_DecimalPlaces=ServiceConfig.AVG_PRICE_DECIMALPLACES

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
    '测试结果':0,
    '测试错误原因':None,
}

#---业务判断程序：买或是卖，及全成或是部成
def cjhbDataCheck(expectStatus, Api, QueryInit, wt_reqs,
                  xtp_id, QueryEnd, hb_data, etf_sell_flag = 0):
    '''

    :param expectStatus: 期望状态
    :param Api: Api实例
    :param QueryInit: 初始资金持仓情况
    :param wt_reqs: 委托参数
    :param xtp_id: 下单编号
    :param QueryEnd: 当前资金持仓情况
    :param hb_data: 成交回报数据
    :param etf_sell_flag: 用来判断卖出etf前是否作了etf申购，如果是则为1，否则默认为0
    :return: cjhb_reslut
    '''
    #根据证券代码获取涨停和跌停价
    upPrice = getUpPrice(wt_reqs['ticker'])
    downPrice = getDownPrice(wt_reqs['ticker'])
    #-----如果委托方向是普通买，执行如下－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
    if (wt_reqs['side'] == Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY'] or \
            wt_reqs['business_type'] == Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_REPO']) and \
            wt_reqs['business_type'] != Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_ALLOTMENT']:
        # 逆回购不判断买卖方向
        if wt_reqs['business_type'] == Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_REPO']:
            side_type = True
        else:
            side_type = (wt_reqs['side'] == hb_data['side'])
        # 获取逆回购成交价格
        if wt_reqs['business_type'] == Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_REPO']:
            hb_data['price'] = ServiceConfig.Reverse_price
        #--委托数据和成交数据比较
        if xtp_id == hb_data['order_xtp_id'] and wt_reqs['market'] == hb_data['market'] and wt_reqs['ticker'] == \
                hb_data['ticker'] and side_type and checkDataPrice(Api,wt_reqs,hb_data['price']):
            if  abs(hb_data['trade_amount'] - round(hb_data['price'] * hb_data['quantity'],2)) < 0.01:
                cjhb_reslut['xtp_id'] = hb_data['order_xtp_id']
                cjhb_reslut['市场'] = hb_data['market']
                cjhb_reslut['股票代码'] = hb_data['ticker']
                cjhb_reslut['买卖方向'] = hb_data['side']
                cjhb_reslut['成交价格'] = hb_data['price']
                cjhb_reslut['成交类型'] = hb_data['trade_type']
                cjhb_reslut['成交数量'] += hb_data['quantity']
                cjhb_reslut['成交金额'] += hb_data['trade_amount']

                # 部分成交－－－－－－－－－－－－－
                if cjhb_reslut['成交数量'] < wt_reqs['quantity']:
                    if expectStatus == '部成':
                        logger.info('成交回报检查：部分成交业务数据开始检查')
                        CJHB_BC_B(QueryInit, wt_reqs, QueryEnd, upPrice)
                    elif expectStatus == '全成':
                        logger.info('成交回报检查：当前成交回报累计成交数量为部分成交，请等待全部成交！')
                        cjhb_reslut['成交回报检查状态']='pending'

                # 全部成交－－－－－－－－－－－－－
                elif cjhb_reslut['成交数量'] == wt_reqs['quantity']:
                    if expectStatus == '全成':
                        logger.info('成交回报检查：全部成交业务数据开始检查')
                        CJHB_QC_B(QueryInit, QueryEnd, wt_reqs, upPrice)
                    elif expectStatus == '部成':
                        logger.error('成交回报检查：错误,期待状态为部成，但成交回报数量累计已经全部成交！')
                        cjhb_reslut['成交回报检查状态'] = 'end'
                        cjhb_reslut['测试结果'] = False
                        cjhb_reslut['测试错误原因'] = '期待状态为部成，但成交回报数量累计已经全部成交！'

                # 错误：成交数量>委托数量
                elif cjhb_reslut['成交数量'] > wt_reqs['quantity']:
                    logger.error('成交回报错误，总成交数量大于委托数量')
                    cjhb_reslut['成交回报检查状态'] = 'end'
                    cjhb_reslut['测试结果'] = False
                    cjhb_reslut['测试错误原因'] = '成交回报错误，总成交数量大于委托数量'

            else:
                logger.error('成交回报有问题：价格×数量不等于成交金额'+str(hb_data['price']* hb_data['quantity'])+','+str(hb_data['trade_amount']))
                cjhb_reslut['成交回报检查状态'] = 'end'
                cjhb_reslut['测试结果'] = False
                cjhb_reslut['测试错误原因'] = '成交回报有问题：价格×数量不等于成交金额'
        else:
            logger.error('成交回报和委托信息不一致，如：xtpid,market,ticker,side,price')
            cjhb_reslut['成交回报检查状态'] = 'end'
            cjhb_reslut['测试结果'] = False
            cjhb_reslut['测试错误原因'] = '成交回报和委托信息不一致，如：xtpid,market,ticker,side,price'

    #--如果委托方向是卖，执行如下－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
    elif (wt_reqs['side'] == Api.const.XTP_SIDE_TYPE['XTP_SIDE_SELL'] and \
        wt_reqs['business_type'] != Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_REPO']) or \
        wt_reqs['business_type'] == Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_ALLOTMENT']:
        # --委托数据和成交数据比较
        if xtp_id == hb_data['order_xtp_id'] and wt_reqs['market'] == hb_data['market'] and wt_reqs['ticker'] == hb_data['ticker'] and wt_reqs['side'] == hb_data['side'] and checkDataPrice(Api,wt_reqs,hb_data['price']):

            if abs(hb_data['trade_amount']-hb_data['price'] * hb_data['quantity']) < 0.01:
                cjhb_reslut['xtp_id'] = hb_data['order_xtp_id']
                cjhb_reslut['市场'] = hb_data['market']
                cjhb_reslut['股票代码'] = hb_data['ticker']
                cjhb_reslut['买卖方向'] = hb_data['side']
                cjhb_reslut['成交价格'] = hb_data['price']
                cjhb_reslut['成交类型'] = hb_data['trade_type']
                cjhb_reslut['成交数量'] += hb_data['quantity']
                cjhb_reslut['成交金额'] += hb_data['trade_amount']

                # 部分成交－－－－－－－－－－－－－
                if cjhb_reslut['成交数量'] < wt_reqs['quantity']:
                    if expectStatus == '部成':
                        logger.info('成交回报检查：部分成交业务数据开始检查')
                        CJHB_BC_S(QueryInit, wt_reqs, QueryEnd, upPrice, etf_sell_flag)
                    elif expectStatus == '全成':
                        logger.info('成交回报检查：当前成交回报累计成交数量为部分成交，请等待全部成交！')
                        cjhb_reslut['成交回报检查状态'] = 'pending'

                # 全部成交－－－－－－－－－－－－－
                elif cjhb_reslut['成交数量'] == wt_reqs['quantity']:
                    if expectStatus == '全成':
                        logger.info('成交回报检查：全部成交业务数据开始检查')
                        if wt_reqs['business_type'] == Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_ALLOTMENT']:
                            CJHB_QC_ALLOT(QueryInit, QueryEnd, wt_reqs)
                        else:
                            CJHB_QC_S(QueryInit, QueryEnd, wt_reqs, upPrice, etf_sell_flag)
                    elif expectStatus == '部成':
                        logger.error('成交回报检查：错误,期待状态为部成，但成交回报数量累计已经全部成交！')
                        cjhb_reslut['成交回报检查状态'] = 'end'
                        cjhb_reslut['测试结果'] = False
                        cjhb_reslut['测试错误原因'] = '期待状态为部成，但成交回报数量累计已经全部成交！'

                # 错误：成交数量>委托数量
                elif cjhb_reslut['成交数量'] > wt_reqs['quantity']:
                    logger.error('成交回报错误，总成交数量大于委托数量')
                    cjhb_reslut['成交回报检查状态'] = 'end'
                    cjhb_reslut['测试结果'] = False
                    cjhb_reslut['测试错误原因'] = '成交回报错误，总成交数量大于委托数量'

            else:
                logger.error('成交回报有问题：价格×数量不等于成交金额'+str(hb_data['price'])+','+str(hb_data['quantity'])+','+str(hb_data['trade_amount']))
                cjhb_reslut['成交回报检查状态'] = 'end'
                cjhb_reslut['测试结果'] = False
                cjhb_reslut['测试错误原因'] = '成交回报有问题：价格×数量不等于成交金额'
        else:
            logger.error('成交回报和委托信息不一致，如：xtpid,market,ticker,side,price')
            cjhb_reslut['成交回报检查状态'] = 'end'
            cjhb_reslut['测试结果'] = False
            cjhb_reslut['测试错误原因'] = '成交回报和委托信息不一致，如：xtpid,market,ticker,side,price'

    return cjhb_reslut

# -----------------------------------------------------------------------------------------------------------------------
#--配股--全部成交--费用持仓检查－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
def CJHB_QC_ALLOT(QueryInit,QueryEnd,wt_reqs):
    logger.info('成交回报－配股－全部成交－费用持仓检查')

    # 查询配股发行价格
    issue_price = QueryTable(out_rights_issue_params,
                             ['issue_price'],
                             {'ticker': wt_reqs['ticker']},
                             2)['issue_price']/10000
    # ----判断可用资金是否正确
    if abs(QueryEnd['可用资金'] + cjhb_reslut['成交金额']  - QueryInit['可用资金']) > 0.01:
        logger.error(
            '可用资金计算有错,原可用资金、成交金额、费用、现可用资金分别是' + str(QueryInit['可用资金']) + ',' + str(cjhb_reslut['成交金额']) + ',' + str(QueryEnd['可用资金']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['可用资金计算有错', {
            '原可用资金': QueryInit['可用资金'],
            '成交金额': cjhb_reslut['成交金额'],
            '现可用资金': QueryEnd['可用资金']
        }]
    # ----判断总资产是否正确
    if abs(QueryEnd['总资产'] + cjhb_reslut['成交金额'] - QueryInit['总资产']) > 0.01:
        logger.error(
            '总资产计算有错,原总资产、成交金额、费用、现总资产分别是' + str(QueryInit['总资产']) + ',' + str(cjhb_reslut['成交金额']) + ',' + str(QueryEnd['总资产']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['总资产计算有错', {
            '原总资产': QueryInit['总资产'],
            '成交金额': cjhb_reslut['成交金额'],
            '现总资产': QueryEnd['总资产']
        }]
    # ----判断总资产是否正确
    if abs(QueryInit['预扣资金'] - QueryEnd['预扣资金']) > 0.01:
        logger.error(
            '预扣资金计算有错,原预扣资金、现预扣资金分别是' + str(QueryInit['预扣资金']) + ',' + str(QueryEnd['预扣资金']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['预扣资金计算有错', {
            '原预扣资金': QueryInit['预扣资金'],
            '现预扣资金': QueryEnd['预扣资金']
        }]
    # ----判断买入资金是否正确
    elif abs(QueryEnd['买入资金'] - cjhb_reslut['成交金额'] - QueryInit['买入资金']) > 0.01:
        logger.error('买入资金计算有误，原买入资金、现买入资金分别是' + str(QueryInit['买入资金']) + ',' + str(QueryEnd['买入资金']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['买入资金计算有误', {
            '原买入资金': QueryInit['买入资金'],
            '现买入资金': QueryEnd['买入资金'],
        }]
    # ----判断买入费用是否正确
    elif abs(QueryEnd['买入费用'] - QueryInit['买入费用']) > 0.01:
        logger.error('买入费用计算有误，原买入费用、费用、现买入费用分别是' + str(QueryInit['买入费用']) + ',' + str(QueryEnd['买入费用']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['买入资金计算有误', {
            '原买入费用': QueryInit['买入费用'],
            '现买入费用': QueryEnd['买入费用'],
        }]
    # ----判断卖出资金是否正确
    elif abs(QueryEnd['卖出资金'] - QueryInit['卖出资金']) > 0.01:
        logger.error('卖出资金有误，原卖出资金、成交金额、现卖出资金分别是' + str(QueryInit['卖出资金']) + ',' + str(cjhb_reslut['成交金额']) + ',' + str(
            QueryEnd['卖出资金']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['卖出资金有误', {
            '原卖出资金': QueryInit['卖出资金'],
            '成交金额': cjhb_reslut['成交金额'],
            '现卖出资金': QueryEnd['卖出资金'],
        }]
    # -----判断卖出费用是否正确
    elif QueryEnd['卖出费用'] - QueryInit['卖出费用'] > 0.01:
        logger.error('卖出费用有误，原卖出费用、费用、现卖出费用分别是' + str(QueryInit['卖出费用']) + ',' + str(QueryEnd['卖出费用']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['卖出费用有误', {
            '原卖出费用': QueryInit['卖出费用'],
            '现卖出费用': QueryEnd['卖出费用'],
        }]
    # -----判断下单前后股票代码、市场是否一致-------
    elif QueryEnd['股票代码'] != QueryInit['股票代码'] or QueryEnd['市场'] != QueryInit['市场']:
        logger.error('下单前后查询的市场股票代码信息不一致',
                     '下单前查询的市场和股票代码是' + str(QueryInit['市场']) + ',' + str(QueryInit['股票代码']) + ',下单后查询的市场和股票代码是' + str(
                         QueryEnd['市场']) + ',' + str(QueryEnd['股票代码']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['下单前后查询的市场股票代码信息不一致', {
            '下单前查询的市场是': QueryInit['市场'],
            '下单前查询的股票代码是': QueryEnd['股票代码'],
            '下单后查询的市场是': QueryInit['市场'],
            '下单后查询的股票代码是': QueryEnd['股票代码'],
        }]
    # ---－判断拥股数量是否正确
    elif abs(QueryEnd['拥股数量'] - QueryInit['拥股数量'] - cjhb_reslut['成交数量']) > 0.00001:
        logger.error(
            '拥股数量不正确，原拥股数量，成交数量，现拥股数量分别是' + str(QueryInit['拥股数量']) + ',' + str(cjhb_reslut['成交数量']) + ',' + str(
                QueryEnd['拥股数量']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['拥股数量不正确', {
            '原拥股数量': QueryInit['拥股数量'],
            '成交数量': cjhb_reslut['成交数量'],
            '现拥股数量': QueryEnd['拥股数量'],
        }]
    # --判断可用股份数是否正确
    elif abs(QueryInit['可用股份数'] - cjhb_reslut['成交数量'] - QueryEnd['可用股份数']) > 0.00001:
        logger.error(
            '可用股份数不正确，原可用股份数、成交数量、现可用股份数分别是' + str(QueryInit['可用股份数']) + ',' + str(cjhb_reslut['成交数量']) + ',' + str(
                QueryEnd['可用股份数']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['可用股份数不正确', {
            '原可用股份数': QueryInit['可用股份数'],
            '成交数量': cjhb_reslut['成交数量'],
            '现可用股份数': QueryEnd['可用股份数']
        }]

    # --判断持仓成本是否正确
    elif abs(QueryEnd['持仓成本'] - issue_price) > 0.001:
        logger.error('持仓成本不正确，期待持仓成本和实际持仓成本分别是' + str(issue_price) + ',' + str(QueryEnd['持仓成本']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['持仓成本不正确', {
            '期待持仓成本': issue_price,
            '实际持仓成本': QueryEnd['持仓成本']
        }]
    else:
        logger.info('卖_全成_成交回报_业务校验正确！')
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = True

#--买--全部成交--费用持仓检查－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
def CJHB_QC_B(QueryInit,QueryEnd,wt_reqs,upPrice):
    logger.info('成交回报－买－全部成交－费用持仓检查')
    #----计算费用
    if wt_reqs['business_type'] == Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_REPO']:
        fee_rate = fee_rate_reverse_repo
        fee_min = fee_reverse_repo_min
        price_avg = QueryInit['持仓成本']
    elif wt_reqs['business_type'] == Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_ALLOTMENT']:
        fee = 0
    else:
        fee = getFee(wt_reqs,upPrice)

    #--计算期待持仓成本应该是
    price_avg = (QueryInit['持仓成本']*QueryInit['拥股数量'] + cjhb_reslut['成交金额'])/(QueryInit['拥股数量']+cjhb_reslut['成交数量'])
    price_avg =round(price_avg,avg_price_DecimalPlaces)

    #----判断可用资金是否正确
    if abs(QueryInit['可用资金'] - cjhb_reslut['成交金额'] - fee - QueryEnd['可用资金']) > 0.00001:
        logger.error('可用资金计算有错,原可用资金、成交金额、费用、现可用资金分别是'+str(QueryInit['可用资金'])+','+str(cjhb_reslut['成交金额'])+','+str(fee)+','+str(QueryEnd['可用资金']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['可用资金计算有错',{
            '原可用资金':QueryInit['可用资金'],
            '成交金额':cjhb_reslut['成交金额'],
            '费用':fee,
            '现可用资金':QueryEnd['可用资金']
        }]
    # ----判断总资产是否正确
    if abs(QueryInit['总资产'] - cjhb_reslut['成交金额'] - fee - QueryEnd['总资产']) > 0.00001:
        logger.error(
            '总资产计算有错,原总资产、成交金额、费用、现总资产分别是' + str(QueryInit['总资产']) + ',' + str(cjhb_reslut['成交金额']) + ',' + str(
                fee) + ',' + str(QueryEnd['总资产']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['总资产计算有错', {
            '原总资产': QueryInit['总资产'],
            '成交金额': cjhb_reslut['成交金额'],
            '费用': fee,
            '现总资产': QueryEnd['总资产']
        }]
    # ----判断预扣资金是否正确
    if abs(QueryInit['预扣资金'] - QueryEnd['预扣资金']) > 0.00001:
        logger.error(
            '预扣资金计算有错,原预扣资金、现预扣资金分别是' + str(QueryInit['预扣资金']) + ',' + str(QueryEnd['预扣资金']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['预扣资金计算有错', {
            '原预扣资金': QueryInit['预扣资金'],
            '现预扣资金': QueryEnd['预扣资金']
        }]
    #----判断买入资金是否正确
    elif abs(QueryEnd['买入资金'] - QueryInit['买入资金'] - cjhb_reslut['成交金额']) > 0.00001:
        logger.error('买入资金计算有误，原买入资金、成交金额、现买入资金分别是'+str(QueryInit['买入资金'])+','+str(cjhb_reslut['成交金额'])+','+str(QueryEnd['买入资金']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['买入资金计算有误', {
        '原买入资金': QueryInit['买入资金'],
        '成交金额': cjhb_reslut['成交金额'],
        '现买入资金': QueryEnd['买入资金'],
        }]
    # ----判断买入费用是否正确
    elif abs(QueryEnd['买入费用'] - QueryInit['买入费用'] - fee) > 0.00001 :
        logger.error('买入费用计算有误，原买入费用、费用、现买入费用分别是'+str(QueryInit['买入费用'])+','+str(fee)+','+str(QueryEnd['买入费用']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['买入资金计算有误', {
            '原买入费用': QueryInit['买入费用'],
            '费用': cjhb_reslut['买入费用'],
            '现买入费用': QueryEnd['买入费用'],
        }]
    # ----判断卖出资金是否正确
    elif QueryEnd['卖出资金'] != QueryInit['卖出资金'] :
        logger.error('卖出资金有误，原卖出资金、现卖出资金分别是'+str(QueryInit['卖出资金'])+','+str(QueryEnd['卖出资金']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['卖出资金有误', {
            '原卖出资金': QueryInit['卖出资金'],
            '现卖出资金': QueryEnd['卖出资金'],
        }]
    #-----判断卖出费用是否正确
    elif QueryEnd['卖出费用'] != QueryInit['卖出费用'] :
        logger.error('卖出费用有误，原卖出费用、现卖出费用分别是'+str(QueryInit['卖出费用'])+','+str(QueryEnd['卖出费用']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['卖出费用有误', {
            '原卖出费用': QueryInit['卖出费用'],
            '现卖出费用': QueryEnd['卖出费用'],
        }]
    #-----判断下单前后股票代码、市场是否一致-------
    elif QueryEnd['股票代码'] !=QueryInit['股票代码'] or QueryEnd['市场'] !=QueryInit['市场']:
        logger.error('下单前后查询的市场股票代码信息不一致','下单前查询的市场和股票代码是'+str(QueryInit['市场'])+','+str(QueryInit['股票代码'])+',下单后查询的市场和股票代码是'+str(QueryEnd['市场'])+','+str(QueryEnd['股票代码']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['下单前后查询的市场股票代码信息不一致', {
            '下单前查询的市场是': QueryInit['市场'],
            '下单前查询的股票代码是': QueryEnd['股票代码'],
            '下单后查询的市场是': QueryInit['市场'],
            '下单后查询的股票代码是': QueryEnd['股票代码'],
        }]
    #---－判断拥股数量是否正确
    elif abs(QueryEnd['拥股数量'] - QueryInit['拥股数量'] - cjhb_reslut['成交数量']) > 0.00001:
        logger.error('拥股数量不正确，原拥股数量，成交数量，现拥股数量分别是'+str(QueryInit['拥股数量'])+','+str(cjhb_reslut['成交数量'])+','+str(QueryEnd['拥股数量']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['拥股数量不正确', {
            '原拥股数量': QueryInit['拥股数量'],
            '成交数量': cjhb_reslut['成交数量'],
            '现拥股数量': QueryEnd['拥股数量'],
        }]
    #--判断可用股份数是否正确
    elif abs(QueryEnd['可用股份数'] - cjhb_reslut['成交数量'] - QueryInit['可用股份数']) > 0.00001:
        logger.error('可用股份数不正确，原可用股份数，现可用股份数，成交数量分别是'+str(QueryInit['可用股份数'])+','+str(QueryEnd['可用股份数'])+','+str(cjhb_reslut['成交数量']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['可用股份数不正确', {
            '原可用股份数': QueryInit['可用股份数'],
            '现可用股份数':  QueryEnd['可用股份数']
        }]

    # #--判断持仓成本是否正确
    # elif abs(round(price_avg - QueryEnd['持仓成本'],4)) > 0.001 :
    #     logger.error('持仓成本不正确，期待持仓成本-实际持仓成本分别是'+str(abs(round(price_avg - QueryEnd['持仓成本'],4))))
    #     logger.error('持仓成本不正确，期待持仓成本和实际持仓成本分别是'+str(price_avg)+','+str(QueryEnd['持仓成本']))
    #     cjhb_reslut['成交回报检查状态'] = 'end'
    #     cjhb_reslut['测试结果'] = False
    #     cjhb_reslut['测试错误原因'] = ['可用股份数不正确', {
    #         '期待持仓成本': price_avg,
    #         '实际持仓成本': QueryEnd['持仓成本']
    #     }]
    else:
        logger.info('买_全成_成交回报_业务校验正确！')
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = True


#-----------------------------------------------------------------------------------------------------------------------
#--买--部分成交--费用持仓检查－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
def CJHB_BC_B(QueryInit,wt_reqs,QueryEnd,upPrice):
    logger.info('成交回报－买－部分成交－费用持仓检查')
    #----计算费用
    fee = 0
    upPrice = getUpPrice(wt_reqs['ticker'])
    if wt_reqs['business_type'] == Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_REPO']:
        fee_rate = fee_rate_reverse_repo
        fee_min = fee_reverse_repo_min
        price_avg = QueryInit['持仓成本']
    elif wt_reqs['business_type'] == Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_ALLOTMENT']:
        fee = 0
    else:
        fee = getFee(wt_reqs,upPrice)
    # 委托价格
    if wt_reqs['price_type'] == Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT']:
        wt_price = wt_reqs['price']
    else:
        wt_price = upPrice + 0.01

    #--计算期待持仓成本应该是
    price_avg= (QueryInit['持仓成本']*QueryInit['拥股数量']+cjhb_reslut['成交金额'])/(QueryInit['拥股数量']+cjhb_reslut['成交数量'])
    price_avg=round(price_avg,avg_price_DecimalPlaces)

    #--待成交数量为
    nomatch_qty = wt_reqs['quantity']- cjhb_reslut['成交数量']
    
    #----判断可用资金是否正确
    if abs(QueryInit['可用资金'] - cjhb_reslut['成交金额'] - fee - nomatch_qty * wt_price - QueryEnd['可用资金']) > 0.00001:
        logger.error(u'可用资金计算有错,原可用资金、成交金额、待成交数量、委托价格、费用、现可用资金分别是'+str(QueryInit['可用资金'])+','+str(cjhb_reslut['成交金额'])+','+str(nomatch_qty)+','+str(wt_reqs['price'])+','+str(fee)+','+str(QueryEnd['可用资金']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['可用资金计算有错',{
            '原可用资金':QueryInit['可用资金'],
            '成交金额':cjhb_reslut['成交金额'],
            '待成交数量':nomatch_qty,
            '委托价格':wt_price,
            '费用':fee,
            '现可用资金':QueryEnd['可用资金']
        }]
    # ----判断总资产是否正确
    elif abs(QueryInit['总资产'] - cjhb_reslut['成交金额'] - QueryEnd['总资产']) > 0.00001:
        logger.error('总资产计算有错,原总资产、成交金额、现总资产分别是' + str(QueryInit['总资产']) + ',' + str(
            cjhb_reslut['成交金额']) + str(QueryEnd['总资产']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['总资产计算有错', {
            '原总资产': QueryInit['总资产'],
            '成交金额': cjhb_reslut['成交金额'],
            '现总资产': QueryEnd['总资产']
        }]
    # ----判断预扣资金是否正确
    elif abs(QueryEnd['预扣资金'] - fee - nomatch_qty*wt_price - QueryInit['预扣资金']) > 0.00001:
        logger.error('预扣资金计算有错,原预扣资金、待成交数量、委托价格、费用、现预扣资金分别是' + str(QueryInit['预扣资金'])
            + ',' + str(nomatch_qty) + ',' + str(wt_reqs['price']) + ',' + str(fee) + ',' + str(QueryEnd['预扣资金']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['预扣资金计算有错', {
            '原预扣资金': QueryInit['预扣资金'],
            '待成交数量': nomatch_qty,
            '委托价格': wt_price,
            '费用': fee,
            '现预扣资金': QueryEnd['预扣资金']
        }]
    #----判断买入资金是否正确
    elif abs(QueryEnd['买入资金'] - QueryInit['买入资金'] - cjhb_reslut['成交金额']) > 0.00001:
        logger.error('买入资金计算有误，原买入资金、成交金额、现买入资金分别是'+str(QueryInit['买入资金'])+','+str(cjhb_reslut['成交金额'])+','+str(QueryEnd['买入资金']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['买入资金计算有误', {
        '原买入资金': QueryInit['买入资金'],
        '成交金额': cjhb_reslut['成交金额'],
        '现买入资金': QueryEnd['买入资金'],
        }]
    # ----判断买入费用是否正确
    elif abs(QueryEnd['买入费用'] - QueryInit['买入费用'] ) > 0.00001 :
        logger.error('买入费用计算有误，原买入费用、费用、现买入费用分别是'+str(QueryInit['买入费用'])+','+str(fee)+','+str(QueryEnd['买入费用']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['买入资金计算有误', {
            '原买入费用': QueryInit['买入费用'],
            '费用': cjhb_reslut['买入费用'],
            '现买入费用': QueryEnd['买入费用'],
        }]
    # ----判断卖出资金是否正确
    elif QueryEnd['卖出资金'] != QueryInit['卖出资金'] :
        logger.error('卖出资金有误，原卖出资金、现卖出资金分别是'+str(QueryInit['卖出资金'])+','+str(QueryEnd['卖出资金']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['卖出资金有误', {
            '原卖出资金': QueryInit['卖出资金'],
            '现卖出资金': QueryEnd['卖出资金'],
        }]
    #-----判断卖出费用是否正确
    elif QueryEnd['卖出费用'] != QueryInit['卖出费用'] :
        logger.error('卖出费用有误，原卖出费用、现卖出费用分别是'+str(QueryInit['卖出费用'])+','+str(QueryEnd['卖出费用']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['卖出费用有误', {
            '原卖出费用': QueryInit['卖出费用'],
            '现卖出费用': QueryEnd['卖出费用'],
        }]
    #-----判断下单前后股票代码、市场是否一致-------
    elif QueryEnd['股票代码'] !=QueryInit['股票代码'] or QueryEnd['市场'] !=QueryInit['市场']:
        logger.error('下单前后查询的市场股票代码信息不一致',
                     '下单前查询的市场和股票代码是' + str(QueryInit['市场']) + ',' + str(QueryInit['股票代码']) + ',下单后查询的市场和股票代码是' + str(
                         QueryEnd['市场']) + ',' + str(QueryEnd['股票代码']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['下单前后查询的市场股票代码信息不一致', {
            '下单前查询的市场是': QueryInit['市场'],
            '下单前查询的股票代码是': QueryEnd['股票代码'],
            '下单后查询的市场是': QueryInit['市场'],
            '下单后查询的股票代码是': QueryEnd['股票代码'],
        }]
    #---－判断拥股数量是否正确
    elif abs(QueryEnd['拥股数量'] - QueryInit['拥股数量'] - cjhb_reslut['成交数量']) > 0.00001:
        logger.error(
            '拥股数量不正确，原拥股数量，成交数量，现拥股数量分别是' + str(QueryInit['拥股数量']) + ',' + str(cjhb_reslut['成交数量']) + ',' + str(
                QueryEnd['拥股数量']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['拥股数量不正确', {
            '原拥股数量': QueryInit['拥股数量'],
            '成交数量': cjhb_reslut['成交数量'],
            '现拥股数量': QueryEnd['拥股数量'],
        }]
   #--判断可用股份数是否正确
    elif abs(QueryEnd['可用股份数'] - QueryInit['可用股份数'] - cjhb_reslut['成交数量']) > 0.00001 :
        logger.error(
            '可用股份数不正确，原可用股份数，成交数量，现可用股份数分别是' + str(QueryInit['可用股份数']) + ',' + str(cjhb_reslut['成交数量']) + ',' + str(
                QueryEnd['可用股份数']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['可用股份数不正确', {
            '原可用股份数': QueryInit['可用股份数'],
            '现可用股份数': QueryEnd['可用股份数']
        }]

    #--判断持仓成本是否正确
    elif abs(round(price_avg - QueryEnd['持仓成本'],4)) > 0.001 :
        logger.error('持仓成本不正确，期待持仓成本和实际持仓成本分别是' + str(price_avg) + ',' + str(QueryEnd['持仓成本']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['持仓成本不正确', {
            '期待持仓成本': price_avg,
            '实际持仓成本': QueryEnd['持仓成本']
        }]
    else:
        logger.info('买_部成_成交回报_业务校验正确！')
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = True


# -----------------------------------------------------------------------------------------------------------------------
#--卖--全部成交--费用持仓检查-----------------------------------------------------------------------------------------------
def CJHB_QC_S(QueryInit,QueryEnd,wt_reqs,etf_sell_flag,upPrice):
    logger.info('成交回报－卖－全部成交－费用持仓检查')
    # ----计算费用
    fee = 0
    if wt_reqs['business_type'] == Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_REPO']:
        wt_price = ServiceConfig.Reverse_price
        fee_rate = fee_rate_reverse_repo
        price_avg = QueryInit['持仓成本']
        fee = max(fee_min,fee_rate_reverse_repo * cjhb_reslut['成交金额'])
    elif wt_reqs['business_type'] == Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_ALLOTMENT']:
        fee = 0
    else:
        fee = getFee(wt_reqs, upPrice, )

    # ----判断可用资金是否正确
    if abs(QueryInit['可用资金'] + cjhb_reslut['成交金额'] - fee - QueryEnd['可用资金']) > 0.01:
        logger.error('可用资金计算有错,原可用资金、成交金额、费用、现可用资金分别是'+str(QueryInit['可用资金'])+','+str(cjhb_reslut['成交金额'])+','+str(fee)+','+str(QueryEnd['可用资金']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['可用资金计算有错', {
            '原可用资金': QueryInit['可用资金'],
            '成交金额': cjhb_reslut['成交金额'],
            '费用': fee,
            '现可用资金': QueryEnd['可用资金']
        }]
    # ----判断总资产是否正确
    if abs(QueryInit['总资产'] + cjhb_reslut['成交金额'] - fee - QueryEnd['总资产']) > 0.01:
        logger.error(
            '总资产计算有错,原总资产、成交金额、费用、现总资产分别是' + str(QueryInit['总资产']) + ',' + str(cjhb_reslut['成交金额']) + ',' + str(
                fee) + ',' + str(QueryEnd['总资产']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['总资产计算有错', {
            '原总资产': QueryInit['总资产'],
            '成交金额': cjhb_reslut['成交金额'],
            '费用': fee,
            '现总资产': QueryEnd['总资产']
        }]
    # ----判断总资产是否正确
    if abs(QueryInit['预扣资金'] - QueryEnd['预扣资金']) > 0.01:
        logger.error(
            '预扣资金计算有错,原预扣资金、现预扣资金分别是' + str(QueryInit['预扣资金']) + ',' + str(QueryEnd['预扣资金']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['预扣资金计算有错', {
            '原预扣资金': QueryInit['预扣资金'],
            '现预扣资金': QueryEnd['预扣资金']
        }]
    # ----判断买入资金是否正确
    elif abs(QueryEnd['买入资金'] - QueryInit['买入资金'] ) > 0.01:
        logger.error('买入资金计算有误，原买入资金、现买入资金分别是'+str(QueryInit['买入资金'])+','+str(QueryEnd['买入资金']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['买入资金计算有误', {
            '原买入资金': QueryInit['买入资金'],
            '现买入资金': QueryEnd['买入资金'],
        }]
    # ----判断买入费用是否正确
    elif abs(QueryEnd['买入费用'] - QueryInit['买入费用'] ) > 0.01:
        logger.error('买入费用计算有误，原买入费用、费用、现买入费用分别是'+str(QueryInit['买入费用'])+','+str(QueryEnd['买入费用']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['买入资金计算有误', {
            '原买入费用': QueryInit['买入费用'],
            '现买入费用': QueryEnd['买入费用'],
        }]
    # ----判断卖出资金是否正确
    elif abs(QueryEnd['卖出资金'] - cjhb_reslut['成交金额'] - QueryInit['卖出资金']) > 0.01:
        logger.error('卖出资金有误，原卖出资金、成交金额、现卖出资金分别是'+str(QueryInit['卖出资金'])+','+str(cjhb_reslut['成交金额'])+','+str(QueryEnd['卖出资金']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['卖出资金有误', {
            '原卖出资金': QueryInit['卖出资金'],
            '成交金额':cjhb_reslut['成交金额'],
            '现卖出资金': QueryEnd['卖出资金'],
        }]
    # -----判断卖出费用是否正确
    elif QueryEnd['卖出费用'] - fee - QueryInit['卖出费用'] > 0.01:
        logger.error('卖出费用有误，原卖出费用、费用、现卖出费用分别是'+str(QueryInit['卖出费用'])+','+str(fee)+','+str(QueryEnd['卖出费用']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['卖出费用有误', {
            '原卖出费用': QueryInit['卖出费用'],
            '费用':fee,
            '现卖出费用': QueryEnd['卖出费用'],
        }]
    # -----判断下单前后股票代码、市场是否一致-------
    elif QueryEnd['股票代码'] != QueryInit['股票代码'] or QueryEnd['市场'] != QueryInit['市场']:
        logger.error('下单前后查询的市场股票代码信息不一致',
                     '下单前查询的市场和股票代码是' + str(QueryInit['市场']) + ',' + str(QueryInit['股票代码']) + ',下单后查询的市场和股票代码是' + str(
                         QueryEnd['市场']) + ',' + str(QueryEnd['股票代码']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['下单前后查询的市场股票代码信息不一致', {
            '下单前查询的市场是': QueryInit['市场'],
            '下单前查询的股票代码是': QueryEnd['股票代码'],
            '下单后查询的市场是': QueryInit['市场'],
            '下单后查询的股票代码是': QueryEnd['股票代码'],
        }]
    # ---－判断拥股数量是否正确
    elif abs(QueryEnd['拥股数量'] - QueryInit['拥股数量'] + cjhb_reslut['成交数量']) > 0.00001:
        logger.error(
            '拥股数量不正确，原拥股数量，成交数量，现拥股数量分别是' + str(QueryInit['拥股数量']) + ',' + str(cjhb_reslut['成交数量']) + ',' + str(
                QueryEnd['拥股数量']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['拥股数量不正确', {
            '原拥股数量': QueryInit['拥股数量'],
            '成交数量': cjhb_reslut['成交数量'],
            '现拥股数量': QueryEnd['拥股数量'],
        }]
    # --判断可用股份数是否正确
    elif abs(QueryEnd['可用股份数'] + cjhb_reslut['成交数量']- QueryInit['可用股份数']) > 0.00001:
        logger.error('可用股份数不正确，原可用股份数、成交数量、现可用股份数分别是'+str(QueryInit['可用股份数'])+','+str(cjhb_reslut['成交数量'])+','+str(QueryEnd['可用股份数']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['可用股份数不正确', {
            '原可用股份数': QueryInit['可用股份数'],
            '成交数量': cjhb_reslut['成交数量'],
            '现可用股份数': QueryEnd['可用股份数']
        }]
    # 卖出ETF时判断是否优先使用T日申购得到的ETF，成交量 <= T日申购得到的ETF时
    elif etf_sell_flag == 1:
        if (QueryInit['可用股份数'] - QueryInit['昨日持仓'] >= cjhb_reslut['成交数量'] and
            QueryInit['今日可申购赎回持仓'] != QueryEnd['今日可申购赎回持仓']):
            logger.error('今日可申购赎回持仓不正确，T日申购所得ETF股份数、'
                     '成交股份数、原今日可申购赎回持仓、'
                     '现今日可申购赎回持仓分别是' +
                     str(QueryInit['可用股份数'] - QueryInit['昨日持仓']) + ',' +
                     str(cjhb_reslut['成交数量']) + ',' +
                     str(QueryInit['今日可申购赎回持仓']) + ',' +
                     str(QueryEnd['今日可申购赎回持仓']))
            cjhb_reslut['成交回报检查状态'] = 'end'
            cjhb_reslut['测试结果'] = False
            cjhb_reslut['测试错误原因'] = ['今日可申购赎回持仓不正确', {
            'T日申购所得ETF股份数': QueryInit['可用股份数'] - QueryInit['昨日持仓'],
            '成交数量': cjhb_reslut['成交数量'],
            '原今日可申购赎回持仓': QueryInit['今日可申购赎回持仓'],
            '现今日可申购赎回持仓': QueryEnd['今日可申购赎回持仓']
            }]
        # 卖出ETF时判断是否优先使用T日申购得到的ETF，T日可卖出量 > 成交量 > T日申购得到的ETF时
        elif (QueryInit['可用股份数'] - QueryInit['昨日持仓']
                  < cjhb_reslut['成交数量']
                  < QueryInit['可用股份数']  and
              QueryInit['今日可申购赎回持仓'] - cjhb_reslut['成交数量']
                  + QueryInit['可用股份数'] - QueryInit['昨日持仓']  # 计算应得的今日可申购赎回持仓
                  != QueryEnd['今日可申购赎回持仓']):
            logger.error('今日可申购赎回持仓不正确，T日申购所得ETF股份数、'
                         '成交股份数、原可用股份数、应得今日可申购赎回持仓、'
                         '现今日可申购赎回持仓分别是' +
                         str(QueryInit['可用股份数'] - QueryInit['昨日持仓']) + ',' +
                         str(cjhb_reslut['成交数量']) + ',' +
                         str(QueryInit['可用股份数']) + ',' +
                         str(QueryInit['今日可申购赎回持仓'] - cjhb_reslut['成交数量'] +
                             QueryInit['可用股份数'] - QueryInit['昨日持仓']) + ',' +
                         str(QueryEnd['今日可申购赎回持仓']))
            cjhb_reslut['成交回报检查状态'] = 'end'
            cjhb_reslut['测试结果'] = False
            cjhb_reslut['测试错误原因'] = ['今日可申购赎回持仓不正确', {
                'T日申购所得ETF股份数': QueryInit['可用股份数'] - QueryInit['昨日持仓'],
                '成交数量': cjhb_reslut['成交数量'],
                '原可用股份数': QueryInit['可用股份数'],
                '应得今日可申购赎回持仓': (QueryInit['今日可申购赎回持仓'] -
                                       cjhb_reslut['成交数量'] +
                                       QueryInit['可用股份数'] -
                                       QueryInit['昨日持仓']),
                '现今日可申购赎回持仓': QueryEnd['今日可申购赎回持仓']
            }]
    # --判断持仓成本是否正确
    elif abs(QueryInit['持仓成本']-QueryEnd['持仓成本'])> 0.001 and QueryEnd['拥股数量'] > 0 :
        logger.error('持仓成本不正确，期待持仓成本和实际持仓成本分别是' + str(QueryInit['持仓成本']) + ',' + str(QueryEnd['持仓成本']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['持仓成本不正确', {
            '期待持仓成本': QueryInit['持仓成本'],
            '实际持仓成本': QueryEnd['持仓成本']
        }]
    elif QueryEnd['持仓成本'] != 0 and QueryEnd['拥股数量'] == 0:
        logger.error('持仓成本不正确，期待持仓成本和实际持仓成本分别是' + str(QueryInit['持仓成本']) + ',' + str(QueryEnd['持仓成本']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['持仓成本不正确', {
            '期待持仓成本': QueryInit['持仓成本'],
            '实际持仓成本': QueryEnd['持仓成本']
        }]
    else:
        logger.info('卖_全成_成交回报_业务校验正确！')
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = True



# -----------------------------------------------------------------------------------------------------------------------
#--卖--部分成交--费用持仓检查－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
def CJHB_BC_S(QueryInit,wt_reqs,QueryEnd,upPrice,etf_sell_flag):
    logger.info('成交回报－卖－部成－费用持仓检查')
    # ----计算费用
    fee = 0
    if wt_reqs['business_type'] == Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_REPO']:
        wt_price = ServiceConfig.Reverse_price
        fee_rate = fee_rate_reverse_repo
        price_avg = QueryInit['持仓成本']
    else:
        fee = getFee(wt_reqs, upPrice)

    # --待成交数量为
    nomatch_qty = wt_reqs['quantity'] - cjhb_reslut['成交数量']

    # ----判断可用资金是否正确
    if abs(QueryInit['可用资金'] + cjhb_reslut['成交金额'] - fee - QueryEnd['可用资金']) > 0.00001:
        logger.error(
            '可用资金计算有错,原可用资金、成交金额、费用、现可用资金分别是' + str(QueryInit['可用资金']) + ',' + str(cjhb_reslut['成交金额']) + ',' + str(
                fee) + ',' + str(QueryEnd['可用资金']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['可用资金计算有错', {
            '原可用资金': QueryInit['可用资金'],
            '成交金额': cjhb_reslut['成交金额'],
            '费用': fee,
            '现可用资金': QueryEnd['可用资金']
        }]
    # ----判断总资产是否正确
    elif abs(QueryInit['总资产'] + cjhb_reslut['成交金额'] - fee - QueryEnd['总资产']) > 0.00001:
        logger.error('总资产计算有错,原总资产、成交金额、现总资产分别是' + str(QueryInit['总资产']) + ',' + str(
            cjhb_reslut['成交金额']) + str(QueryEnd['总资产']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['总资产计算有错', {
            '原总资产': QueryInit['总资产'],
            '成交金额': cjhb_reslut['成交金额'],
            '现总资产': QueryEnd['总资产']
        }]
    # ----判断预扣资金是否正确
    if abs(QueryEnd['预扣资金'] - QueryInit['预扣资金']) > 0.00001:
        logger.error(
            '预扣资金计算有错,原预扣资金、费用、现预扣资金分别是' + str(QueryInit['预扣资金']) + ',' + str(
                fee) + ',' + str(QueryEnd['预扣资金']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['预扣资金计算有错', {
            '原预扣资金': QueryInit['预扣资金'],
            '成交金额': cjhb_reslut['成交金额'],
            '费用': fee,
            '现预扣资金': QueryEnd['预扣资金']
        }]
    # ----判断买入资金是否正确
    elif abs(QueryEnd['买入资金'] - QueryInit['买入资金']) > 0.00001:
        logger.error('买入资金计算有误，原买入资金、现买入资金分别是' + str(QueryInit['买入资金']) + ',' + str(QueryEnd['买入资金']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['买入资金计算有误', {
            '原买入资金': QueryInit['买入资金'],
            '现买入资金': QueryEnd['买入资金'],
        }]
    # ----判断买入费用是否正确
    elif abs(QueryEnd['买入费用'] - QueryInit['买入费用']) > 0.00001:
        logger.error('买入费用计算有误，原买入费用、费用、现买入费用分别是' + str(QueryInit['买入费用']) + ',' + str(QueryEnd['买入费用']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['买入资金计算有误', {
            '原买入费用': QueryInit['买入费用'],
            '现买入费用': QueryEnd['买入费用'],
        }]
    # ----判断卖出资金是否正确
    elif abs(QueryEnd['卖出资金'] - cjhb_reslut['成交金额'] - QueryInit['卖出资金']) > 0.00001:
        logger.error('卖出资金有误，原卖出资金、成交金额、现卖出资金分别是' + str(QueryInit['卖出资金']) + ',' + str(cjhb_reslut['成交金额']) + ',' + str(
            QueryEnd['卖出资金']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['卖出资金有误', {
            '原卖出资金': QueryInit['卖出资金'],
            '成交金额': cjhb_reslut['成交金额'],
            '现卖出资金': QueryEnd['卖出资金'],
        }]
    # -----判断卖出费用是否正确
    elif QueryEnd['卖出费用'] - fee - QueryInit['卖出费用'] > 0.00001:
        logger.error('卖出费用有误，原卖出费用、现卖出费用分别是'+QueryInit['卖出费用']+','+str( QueryEnd['卖出费用']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['卖出费用有误', {
            '原卖出费用': QueryInit['卖出费用'],
            '现卖出费用': QueryEnd['卖出费用'],
        }]
    # -----判断下单前后股票代码、市场是否一致-------
    elif QueryEnd['股票代码'] != QueryInit['股票代码'] or QueryEnd['市场'] != QueryInit['市场']:
        logger.error('下单前后查询的市场股票代码信息不一致',
                     '下单前查询的市场和股票代码是' + str(QueryInit['市场']) + ',' + str(QueryInit['股票代码']) + ',下单后查询的市场和股票代码是' + str(
                         QueryEnd['市场']) + ',' + str(QueryEnd['股票代码']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['下单前后查询的市场股票代码信息不一致', {
            '下单前查询的市场是': QueryInit['市场'],
            '下单前查询的股票代码是': QueryEnd['股票代码'],
            '下单后查询的市场是': QueryInit['市场'],
            '下单后查询的股票代码是': QueryEnd['股票代码'],
        }]
    # ---－判断拥股数量是否正确
    elif abs(QueryInit['拥股数量']-QueryEnd['拥股数量'] - cjhb_reslut['成交数量']) > 0.00001:
        logger.error('拥股数量不正确，原拥股数量，成交数量，现拥股数量分别是'+str(QueryInit['拥股数量'])+','+str(cjhb_reslut['成交数量'])+','+str(QueryEnd['拥股数量']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['拥股数量不正确', {
            '原拥股数量': QueryInit['拥股数量'],
            '成交数量': cjhb_reslut['成交数量'],
            '现拥股数量': QueryEnd['拥股数量'],
        }]
    # --判断可用股份数是否正确
    elif abs(QueryInit['可用股份数'] - QueryEnd['可用股份数'] - cjhb_reslut['成交数量'] - nomatch_qty) > 0.00001:
        logger.error('可用股份数计算不正确，原可用股份数，成交数量、待成交数量、现可用股份数分别是'+str(QueryInit['可用股份数'])+','+str(cjhb_reslut['成交数量'])+','+str(nomatch_qty)+','+str(QueryEnd['可用股份数']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['可用股份数计算不正确', {
            '原可用股份数': QueryInit['可用股份数'],
            '成交数量': cjhb_reslut['成交数量'],
            '未成交数量':nomatch_qty,
            '现可用股份数': QueryEnd['可用股份数']
        }]
    elif etf_sell_flag == 1:
        # 卖出ETF时判断是否优先使用T日申购得到的ETF，成交量 <= T日申购得到的ETF时
        if (QueryInit['可用股份数'] - QueryInit['昨日持仓'] >= cjhb_reslut['成交数量'] and
              QueryInit['今日可申购赎回持仓'] != QueryEnd['今日可申购赎回持仓']):
            logger.error('今日可申购赎回持仓不正确，T日申购所得ETF股份数、'
                         '成交股份数、原今日可申购赎回持仓、'
                         '现今日可申购赎回持仓分别是' +
                         str(QueryInit['可用股份数'] - QueryInit['昨日持仓']) + ',' +
                         str(cjhb_reslut['成交数量']) + ',' +
                         str(QueryInit['今日可申购赎回持仓']) + ',' +
                         str(QueryEnd['今日可申购赎回持仓']))
            cjhb_reslut['成交回报检查状态'] = 'end'
            cjhb_reslut['测试结果'] = False
            cjhb_reslut['测试错误原因'] = ['今日可申购赎回持仓不正确', {
                'T日申购所得ETF股份数': QueryInit['可用股份数'] - QueryInit['昨日持仓'],
                '成交数量': cjhb_reslut['成交数量'],
                '原今日可申购赎回持仓': QueryInit['今日可申购赎回持仓'],
                '现今日可申购赎回持仓': QueryEnd['今日可申购赎回持仓']
            }]
        # 卖出ETF时判断是否优先使用T日申购得到的ETF，T日可卖出量 > 成交量 > T日申购得到的ETF时
        elif (QueryInit['可用股份数'] - QueryInit['昨日持仓']
                  < cjhb_reslut['成交数量']
                  < QueryInit['可用股份数'] and
              QueryInit['今日可申购赎回持仓'] - cjhb_reslut['成交数量']
                  + QueryInit['可用股份数'] - QueryInit['昨日持仓']  # 计算应得的今日可申购赎回持仓
                  != QueryEnd['今日可申购赎回持仓']):
            logger.error('今日可申购赎回持仓不正确，T日申购所得ETF股份数、'
                         '成交股份数、原可用股份数、应得今日可申购赎回持仓、'
                         '现今日可申购赎回持仓分别是' +
                         str(QueryInit['可用股份数'] - QueryInit['昨日持仓']) + ',' +
                         str(cjhb_reslut['成交数量']) + ',' +
                         str(QueryInit['可用股份数']) + ',' +
                         str(QueryInit['今日可申购赎回持仓'] - cjhb_reslut['成交数量'] +
                             QueryInit['可用股份数'] - QueryInit['昨日持仓']) + ',' +
                         str(QueryEnd['今日可申购赎回持仓']))
            cjhb_reslut['成交回报检查状态'] = 'end'
            cjhb_reslut['测试结果'] = False
            cjhb_reslut['测试错误原因'] = ['今日可申购赎回持仓不正确', {
                'T日申购所得ETF股份数': QueryInit['可用股份数'] - QueryInit['昨日持仓'],
                '成交数量': cjhb_reslut['成交数量'],
                '原可用股份数': QueryInit['可用股份数'],
                '应得今日可申购赎回持仓': (QueryInit['今日可申购赎回持仓'] -
                                cjhb_reslut['成交数量'] +
                                QueryInit['可用股份数'] -
                                QueryInit['昨日持仓']),
                '现今日可申购赎回持仓': QueryEnd['今日可申购赎回持仓']
            }]
    # --判断持仓成本是否正确
    elif abs(QueryInit['持仓成本']-QueryEnd['持仓成本']) > 0.001 :
        logger.error('持仓成本不正确，期待持仓成本和实际持仓成本分别是' + str(QueryInit['持仓成本']) + ',' + str(QueryEnd['持仓成本']))
        cjhb_reslut['成交回报检查状态'] = 'end'
        cjhb_reslut['测试结果'] = False
        cjhb_reslut['测试错误原因'] = ['持仓成本不正确', {
            '期待持仓成本': QueryInit['持仓成本'],
            '实际持仓成本': QueryEnd['持仓成本']
        }]
    else:
        logger.info('卖_部成_成交回报_业务校验正确！')
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

# 费用计算公式
def getFee(wt_reqs, upPrice):
    global  cjhb_reslut, fee_rate_buy_special,  fee_rate_sell_special, fee_min_buy_special, fee_min_sell_special
    upPrice = getUpPrice(wt_reqs['ticker'])
    if wt_reqs['side'] == Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY']:
        # 期望状态是部成或订单确认，预扣资金里有费用；其他状态则没有
        if wt_reqs['order_client_id'] in (1,3):
            # 如果委托类型为限价的，那么计算费用的价格＝委托的价格；如果为市价的，计算费用的价格＝涨停价
            if wt_reqs['price_type'] == Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT']:
                wt_price = wt_reqs['price']
            else:
                wt_price = upPrice + 0.01
            amount = wt_reqs['price'] * wt_reqs['quantity']
            fee_fixed = amount * fee_rate_buy_fixed + fee_addition_buy_fixed
            fee_special = max(fee_min_buy_special, amount * fee_rate_buy_special)
        else:
            fee_fixed = cjhb_reslut['成交金额'] * fee_rate_buy_fixed + fee_addition_buy_fixed
            fee_special = max(fee_min_buy_special, cjhb_reslut['成交金额'] * fee_rate_buy_special)
    # 如果是卖，卖出委托不再预扣交易费用，收到成交回报时再扣除交易费用 
    elif wt_reqs['side'] == Api.const.XTP_SIDE_TYPE['XTP_SIDE_SELL']:
        fee_fixed = cjhb_reslut['成交金额'] * fee_rate_sell_fixed+ fee_addition_sell_fixed
        fee_special = max(fee_min_sell_special, cjhb_reslut['成交金额'] * fee_rate_sell_special)
    else:
        logger.error("买卖方向错误")

    fee_fixed = float(Decimal(Decimal(str(fee_fixed)).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)))
    fee_special = float(Decimal(Decimal(str(fee_special)).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)))
    fee = fee_fixed + fee_special
    return fee
