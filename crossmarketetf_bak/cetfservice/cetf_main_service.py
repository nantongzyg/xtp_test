#!/usr/bin/python
# -*- encoding: utf-8 -*-
# import time
import sys
sys.path.append('/home/yhl2/workspace/xtp_test')
# from service.log import *
# from service import ServiceConfig
from service import getTime
from cetf_bdts_datacheck import *
from cetf_cjhb_datacheck import *
from service.CancelOrderErrorDataCheck import cancelOrderErrorDataCheck
from cetf_bdquery_datacheck import cetf_bdquery_datacheck
from crossmarketetf.cetfmysql.query_cetf_components_code import *
from crossmarketetf.cetfservice.cetf_get_cash_subtitute_amount import *
from crossmarketetf.cetfmysql.query_preclose_price import *
from crossmarketetf.cetfmysql.query_creation_redem_unit import *
from crossmarketetf.cetfservice.cetf_case_end_check import *

class g_var(object):
    """定义全局变量"""

    # 报单查询请求id
    request_id = 0

    # etf申购允许现金替代成分股所需金额，已乘以ETF份数，非单份
    cash_substitute_amount = 0

    # etf成分股昨天价
    pre_close_prices = {}

    # 定义报单推送结果的全局变量bdts_rs，结果检查函数cetf_case_endcheck会用到
    bdts_rs = {}

    bdquery_rs = None
    cdquery_rs = None

    # 撤废前成分股持仓
    component_stk_info_reject = {}

    # 定义下单前资金持仓全局变量
    QueryInit = {
        '总资产': 0,
        '可用资金': 0,
        '证券资产': 0,
        '买入资金': 0,
        '买入费用': 0,
        '卖出资金': 0,
        '卖出费用': 0,
        '预扣资金': 0,
        '股票代码': None,
        '市场': None,
        '总持仓': 0,
        '可卖持仓': 0,
        '昨日持仓': 0,
        '今日可申购赎回持仓': 0,
        '持仓成本价': 0,
        '浮动盈亏': 0
        }

    # 定义下单后的资金持仓全局变量
    QueryEnd = {
        '总资产': 0,
        '可用资金': 0,
        '证券资产': 0,
        '买入资金': 0,
        '买入费用': 0,
        '卖出资金': 0,
        '卖出费用': 0,
        '预扣资金': 0,
        '股票代码': None,
        '市场': None,
        '总持仓': 0,
        '可卖持仓': 0,
        '昨日持仓': 0,
        '今日可申购赎回持仓': 0,
        '持仓成本价': 0,
        '浮动盈亏': 0
        }

    # 定义用例检查结果全局变量
    result = {
        '用例检查状态':'init',
        '用例测试结果': False,
        '用例错误原因': '',
        '用例错误源': '',
        '报单检查状态':'init',
        '报单测试结果': False,
        '报单错误原因': '',
        '撤单检查状态':'init',
        '撤单测试结果': False,
        '撤单错误原因': '',
    }


    cjhb_rs = {
        '成交回报检查状态': 'init',
        'xtp_id': None,
        '市场': None,
        '股票代码': None,
        '买卖方向': None,
        '成交价格': None,
        '成交数量': 0,
        '成交金额': 0.00,
        '成交类型': None,
        '测试结果': True,
        '测试错误原因': None,
    }

class g_func(object):
    """定义主函数将要使用的方法"""


    @staticmethod
    def set_query_init(Api, wt_reqs):
        """下单前查询的资金和持仓初始值"""
        # 初始资金查询及赋值------------------------------------------------------
        fundasset0 = Api.trade.QueryAssetSync()
        if fundasset0['data']['result'] == 0:
            g_var.QueryInit['可用资金'] = fundasset0['data']['buying_power']
            g_var.QueryInit['买入资金'] = fundasset0['data']['fund_buy_amount']
            g_var.QueryInit['买入费用'] = fundasset0['data']['fund_buy_fee']
            g_var.QueryInit['卖出资金'] = fundasset0['data']['fund_sell_amount']
            g_var.QueryInit['卖出费用'] = fundasset0['data']['fund_sell_fee']
            g_var.QueryInit['预扣资金'] = fundasset0['data']['withholding_amount']
            g_var.QueryInit['总资产'] = fundasset0['data']['total_asset']
            g_var.QueryInit['证券资产'] = fundasset0['data']['security_asset']
        else:
            logger.error('初始查询资金数据失败，请检查测试环境')

        # 初始持仓查询及赋值QueryInit---------------------------------------------
        stkcode = {'ticker': ''}
        # 接口定义 ticker:'' 表示查询所有持仓
        stkasset0 = Api.trade.QueryPositionSync(stkcode)
        if wt_reqs['ticker'] in stkasset0['data']:
            g_var.QueryInit['股票代码'] = (
                stkasset0['data'][wt_reqs['ticker']]['position']['ticker'])
            g_var.QueryInit['市场'] = (
                stkasset0['data'][wt_reqs['ticker']]['position']['market'])
            g_var.QueryInit['总持仓'] = (
                stkasset0['data'][wt_reqs['ticker']]['position']['total_qty'])
            g_var.QueryInit['可卖持仓'] = (
                stkasset0['data'][wt_reqs['ticker']]
                                       ['position']['sellable_qty'])
            g_var.QueryInit['昨日持仓'] = (
                stkasset0['data'][wt_reqs['ticker']]
                                       ['position']['yesterday_position'])
            g_var.QueryInit['今日可申购赎回持仓'] = (
                stkasset0['data'][wt_reqs['ticker']]
                                       ['position']['purchase_redeemable_qty'])
            g_var.QueryInit['持仓成本价'] = (
                stkasset0['data'][wt_reqs['ticker']]['position']['avg_price'])
            g_var.QueryInit['浮动盈亏'] = (
                stkasset0['data'][wt_reqs['ticker']]
                                       ['position']['unrealized_pnl'])
        else:
            g_var.QueryInit['股票代码'] = wt_reqs['ticker']
            g_var.QueryInit['市场'] = wt_reqs['market']
            g_var.QueryInit['总持仓'] = 0
            g_var.QueryInit['可卖持仓'] = 0
            g_var.QueryInit['昨日持仓'] = 0
            g_var.QueryInit['可卖出证券数'] = 0
            g_var.QueryInit['持仓成本'] = 0
            g_var.QueryInit['浮动盈亏'] = 0
        logger.info('初始资金持仓为:')
        dictLogging(g_var.QueryInit)

    @staticmethod
    def set_query_end(Api, wt_reqs):
        """业务操作后查询资金和持仓"""
        time.sleep(0.5)
        # 资金查询及赋值----------------------------------------------------------
        fundasset9 = Api.trade.QueryAssetSync()
        time.sleep(0.5)
        if fundasset9['data']['result'] == 0:
            g_var.QueryEnd['可用资金'] = fundasset9['data']['buying_power']
            g_var.QueryEnd['买入资金'] = fundasset9['data']['fund_buy_amount']
            g_var.QueryEnd['买入费用'] = fundasset9['data']['fund_buy_fee']
            g_var.QueryEnd['卖出资金'] = fundasset9['data']['fund_sell_amount']
            g_var.QueryEnd['卖出费用'] = fundasset9['data']['fund_sell_fee']
            g_var.QueryEnd['预扣资金'] = fundasset9['data']['withholding_amount']
            g_var.QueryEnd['总资产'] = fundasset9['data']['total_asset']
            g_var.QueryEnd['证券资产'] = fundasset9['data']['security_asset']
        else:
            logger.error("未收到成交回报资金查询：请检查测试环境")

        # 收到成交回报后查询持仓---------------------------------------------------
        stkcode = {'ticker': ''}
        stkasset9 = Api.trade.QueryPositionSync(stkcode)
        time.sleep(0.5)
        if wt_reqs['ticker'] in stkasset9['data']:
            g_var.QueryEnd['股票代码'] = (
                stkasset9['data'][wt_reqs['ticker']]['position']['ticker'])
            g_var.QueryEnd['市场'] = (
                stkasset9['data'][wt_reqs['ticker']]['position']['market'])
            g_var.QueryEnd['总持仓'] = (
                stkasset9['data'][wt_reqs['ticker']]['position']['total_qty'])
            g_var.QueryEnd['可卖持仓'] = (
                stkasset9['data'][wt_reqs['ticker']]['position']['sellable_qty'])
            g_var.QueryEnd['昨日持仓'] = (
                stkasset9['data'][wt_reqs['ticker']]['position']
                                                         ['yesterday_position'])
            g_var.QueryEnd['今日可申购赎回持仓'] = (
                stkasset9['data'][wt_reqs['ticker']]['position']
                                                    ['purchase_redeemable_qty'])
            g_var.QueryEnd['持仓成本价'] = (
                stkasset9['data'][wt_reqs['ticker']]['position']['avg_price'])
            g_var.QueryEnd['浮动盈亏'] = (
                stkasset9['data'][wt_reqs['ticker']]['position']
                                                             ['unrealized_pnl'])
        else:
            g_var.QueryEnd['股票代码'] = wt_reqs['ticker']
            g_var.QueryEnd['市场'] = wt_reqs['market']
            g_var.QueryEnd['总持仓'] = 0
            g_var.QueryEnd['可卖持仓'] = 0
            g_var.QueryEnd['昨日持仓'] = 0
            g_var.QueryEnd['可卖出证券数'] = 0
            g_var.QueryEnd['持仓成本'] = 0
            g_var.QueryEnd['浮动盈亏'] = 0
        logger.info('最终资金持仓为:')
        dictLogging(g_var.QueryEnd)

    @staticmethod
    def query_by_xtpid(Api, xtpid):
        """通过xtpID查询报单,此函数会出发回调函数on_queryorder"""
        rs_QueryOrder = Api.trade.QueryOrderByXTPID(xtpid, g_var.request_id)
        g_var.request_id += 1
        # --如果返回的是非０，说明调用报单查询方法失败
        if rs_QueryOrder != 0:
            logger.info('报单查询出错' + str(rs_QueryOrder))
        else:
            logger.info('正在进行报单查询，xtpID=' + str(xtpid))

    @staticmethod
    def get_time_pending(expectStatus):
        """根据期望状态返回超时时间"""
        # 默认
        time = ServiceConfig.TIMEPENDING['DEFAULT']
        # 各状态
        if expectStatus in ('全成', '未成交', '初始', '内部撤单', '废单'):
            time = ServiceConfig.TIMEPENDING['CREATION']
        return time

    @staticmethod
    def cetf_bdts_check(Api, case_goal,wt_reqs, data):
        """报单推送外层检查，根据报单推送的类型和期望状态进行撤单和赋值查询"""
        # 参数
        # status 报单检查是否结束：init/pending/end
        # flag 报单检查是否通过：True/False
        # remark 报单检查未通过原因
        # cancel_xtpID 撤单的xtpID
        bdCheck = {
            'status': 'init',
            'flag': False,
            'remark': '',
            'cancel_xtpID': 0,
        }

        # 当报单是‘未成交’时，报单已接受
        # 1.如果期望状态是全成，进行等待
        # 2.如果期望状态是其他，
        if data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE[
            'XTP_ORDER_STATUS_NOTRADEQUEUEING'] and data[
            'order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
            'XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
            if case_goal['期望状态']  == '全成':
                logger.info('当前报单推送状态为未成交，等待..')
                bdCheck['status'] = 'pending'
            else:
                TODO

        # 当报单是‘全部成交’时，报单已接受
        # 1.当期望'全成再撤单'时，
        # 2.如果期望状态是'全成',报单推送外层检查通过，进行报单查询业务处理
        # 3.如果期望状态不是'全成'、'全成再撤单'，则报单推送与期望不符
        elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE[
            'XTP_ORDER_STATUS_ALLTRADED'] and data[
            'order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
            'XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
            if case_goal['期望状态'] == '全成' and case_goal['是否是撤废'] == '是':
                # 查询撤废前成分股持仓
                g_var.component_stk_info_reject = cetf_get_all_component_stk(Api
                    , wt_reqs['ticker'])
                g_func.set_query_init(Api, wt_reqs)
                # 撤废
                bdCheck['cancel_xtpID'] = Api.trade.CancelOrder(
                    case_goal['xtp_ID'])
                bdCheck['status'] = 'pending'
            elif case_goal['期望状态'] == '全成':
                g_func.query_by_xtpid(Api, case_goal['xtp_ID'])
                bdCheck['status'] = 'end'
                bdCheck['flag'] = True
            else:
                bdCheck['status'] = 'end'
                bdCheck['flag'] = False

        # 当报单是'已撤'，报单已接受
        # 1.如果期望状态是 '内部撤单',
        # 2.如果其他状态是其他状态，则报单推送与期望不符
        elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE[
            'XTP_ORDER_STATUS_CANCELED'] and data['order_submit_status'
            ] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
                 'XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
            if case_goal['期望状态'] == '内部撤单':
                TODO
            else:
                bdCheck['status'] = 'end'
                bdCheck['flag'] = False

        # 当报单是'废单'，报单已拒绝
        # 1.如果期望状态 撤废，
        # 2.如果期望状态是'废单'，
        # 3.如果期望状态是其他状态，
        elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE[
            'XTP_ORDER_STATUS_REJECTED'] and data[
            'order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
            'XTP_ORDER_SUBMIT_STATUS_INSERT_REJECTED']:
            if case_goal['期望状态'] == '废单' and case_goal['是否是撤废'] == '是':
                # 查询撤废前成分股持仓
                g_var.component_stk_info_reject = cetf_get_all_component_stk(Api
                    , wt_reqs['ticker'])
                g_func.set_query_init(Api, wt_reqs)
                # 撤废
                bdCheck['cancel_xtpID'] = Api.trade.CancelOrder(
                    case_goal['xtp_ID'])
                bdCheck['status'] = 'pending'
            elif case_goal['期望状态'] == '废单':
                g_func.set_query_end(Api, wt_reqs)
                g_func.query_by_xtpid(Api, case_goal['xtp_ID'])
                bdCheck['status'] = 'end'
                bdCheck['flag'] = True
            else:
                TODO
        # 当报单是其他状态时，用例执行失败
        else:
            logger.error(
                '当前报单推送状态无法识别，' + str(data['order_status']) + ',' + str(
                    data['order_submit_status']))
            bdCheck['status'] = 'end'
            bdCheck['flag'] = False
            bdCheck['remark'] = '当前报单推送状态无法识别'

        return bdCheck

    @staticmethod
    def cetf_bdquery_check(Api, case_goal, wt_reqs, data):
        """报单查询检查，此检查为外层的检查，主要检查查询回来的报单的状态是什么，
        然后根据状态进行不同的操作"""
        bdQuecyCheck = {
            '检查状态': 'init',
            'flag': False,
            'cancel_xtpID': 0,
            'remark': '',
        }
        # 当报单查询结果是‘初始’报单已提交
        if data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE[
            'XTP_ORDER_STATUS_INIT'] and data[
            'order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
            'XTP_ORDER_SUBMIT_STATUS_INSERT_SUBMITTED']:
            if case_goal['期望状态'] == '内部撤单':
                TODO
            else:
                bdQuecyCheck['检查状态'] = 'end'
                bdQuecyCheck['flag'] = False
                bdQuecyCheck['remark'] = '期望状态与报单状态不匹配'

        # 当报单查询结果是‘未成交’，报单已接受
        elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE[
            'XTP_ORDER_STATUS_NOTRADEQUEUEING'] and data[
            'order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
            'XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
            # 当期望状态是‘未成交’时，赋值queryEnd，检查报单查询数据
            if (case_goal['期望状态'] == '未成交' and
                        case_goal['是否是撤废'] == '否'):
                g_func.set_query_end(Api, wt_reqs)
                bdQuecyCheck['检查状态'] = 'end'
                bdQuecyCheck['flag'] = True
            # 当期望状态是’撤废’时，进行撤单
            elif (case_goal['期望状态'] == '未成交' and
                            case_goal['是否是撤废'] == '是'):
                TODO
            # 当期望状态是‘全成’
            elif case_goal['期望状态'] in ('全成',):
                bdQuecyCheck['检查状态'] = 'pending'
                TODO
            else:
                bdQuecyCheck['检查状态'] = 'end'
                bdQuecyCheck['flag'] = False
                bdQuecyCheck['remark'] = '期望状态与报单状态不匹配'

        # 当报单查询结果是‘全成’，报单已接受
        elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE[
            'XTP_ORDER_STATUS_ALLTRADED'] and data[
            'order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
            'XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED']:
            # 当期望状态是‘全成’时，检查报单查询数据
            if case_goal['期望状态'] == '全成':
                bdQuecyCheck['检查状态'] = 'end'
                bdQuecyCheck['flag'] = True
            else:
                bdQuecyCheck['检查状态'] = 'end'
                bdQuecyCheck['flag'] = False
                bdQuecyCheck['remark'] = '期望状态与报单状态不匹配'

        # 当报单查询结果是‘已撤’
        elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE[
            'XTP_ORDER_STATUS_CANCELED']:
            bdQuecyCheck['检查状态'] = 'end'
            bdQuecyCheck['flag'] = False
            bdQuecyCheck['remark'] = '期望状态与报单状态不匹配'
            TODO

        # 当报单查询结果是‘废单’，报单已拒绝
        elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE[
            'XTP_ORDER_STATUS_REJECTED'] and data[
            'order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
            'XTP_ORDER_SUBMIT_STATUS_INSERT_REJECTED']:
            # 当期望状态是‘废单’，进行报单查询数据处理
            if case_goal['期望状态'] == '废单':
                g_func.set_query_end(Api, wt_reqs)
                bdQuecyCheck['检查状态'] = 'end'
                bdQuecyCheck['flag'] = True
            else:
                bdQuecyCheck['检查状态'] = 'end'
                bdQuecyCheck['flag'] = False
                bdQuecyCheck['remark'] = '期望状态与报单状态不匹配'


        # 当报单查询结果是‘撤单废单’,撤单已拒绝
        elif data['order_status'] == Api.const.XTP_ORDER_STATUS_TYPE[
            'XTP_ORDER_STATUS_REJECTED'] and data[
            'order_submit_status'] == Api.const.XTP_ORDER_SUBMIT_STATUS_TYPE[
            'XTP_ORDER_SUBMIT_STATUS_CANCEL_REJECTED']:
            # 当期望状态是‘撤废’，先进行赋值queryEnd,然后报单查询数据处理
            if case_goal['是否是撤废'] == '是':
                g_func.set_query_end(Api, wt_reqs)
                bdQuecyCheck['检查状态'] = 'end'
                bdQuecyCheck['flag'] = True
            else:
                bdQuecyCheck['检查状态'] = 'end'
                bdQuecyCheck['flag'] = False
                bdQuecyCheck['remark'] = '期望状态与报单状态不匹配'

        return bdQuecyCheck

    @staticmethod
    def cetf_parm_init(expectStatus):
        """初始化全局变量方法"""
        logger.info('ParmIni初始化全局变量开始..')

        g_var.QueryInit['可用资金'] = 0
        g_var.QueryInit['买入资金'] = 0
        g_var.QueryInit['买入费用'] = 0
        g_var.QueryInit['卖出资金'] = 0
        g_var.QueryInit['卖出费用'] = 0
        g_var.QueryInit['预扣资金'] = 0
        g_var.QueryInit['总资产'] = 0
        g_var.QueryInit['证券资产'] = 0
        g_var.QueryInit['股票代码'] = None
        g_var.QueryInit['市场'] = None
        g_var.QueryInit['总持仓'] = 0
        g_var.QueryInit['可卖持仓'] = 0
        g_var.QueryInit['昨日持仓'] = 0
        g_var.QueryInit['今日可申购赎回持仓'] = 0
        g_var.QueryInit['持仓成本价'] = 0.000
        g_var.QueryInit['浮动盈亏'] = 0.00

        g_var.QueryEnd['可用资金'] = 0
        g_var.QueryEnd['买入资金'] = 0
        g_var.QueryEnd['买入费用'] = 0
        g_var.QueryEnd['卖出资金'] = 0
        g_var.QueryEnd['卖出费用'] = 0
        g_var.QueryEnd['预扣资金'] = 0
        g_var.QueryEnd['总资产'] = 0
        g_var.QueryEnd['证券资产'] = 0
        g_var.QueryEnd['股票代码'] = None
        g_var.QueryEnd['市场'] = None
        g_var.QueryEnd['总持仓'] = 0
        g_var.QueryEnd['可卖持仓'] = 0
        g_var.QueryEnd['昨日持仓'] = 0
        g_var.QueryEnd['今日可申购赎回持仓'] = 0
        g_var.QueryEnd['持仓成本价'] = 0.000
        g_var.QueryEnd['浮动盈亏'] = 0.00

        g_var.result['用例检查状态'] = 'init'
        g_var.result['用例错误源'] = ''
        g_var.result['用例测试结果'] = False
        g_var.result['用例错误原因'] = ''
        g_var.result['报单检查状态'] = 'init'
        g_var.result['报单测试结果'] = False
        g_var.result['报单错误原因'] = ''
        g_var.result['撤单错误原因'] = ''

        if expectStatus in ('初始', '未成交', '全成', '废单'):
            g_var.result['撤单检查状态'] = 'end'  #此处变量有何用处，全成撤废，废单撤废不用再检查吗～～～～～～～～～～～～～～
            g_var.result['撤单测试结果'] = True
        else:
            g_var.result['撤单检查状态'] = 'init'
            g_var.result['撤单测试结果'] = False

        # 下单前初始化bd_time(各个状态的报单时间)为空,cetf_bdts_datacheck模块使用
        bdTimeInit()
        # 下单前初始化成交回报测试结果集
        # cjhbDataInit()
        logger.info('ParmIni初始化全局变量完成')


def cetf_service_test(Api, case_goal, wt_reqs, component_stk_before = None,
                      pyname = None):
    """
    下单及业务校验主函数
    :param Api:
    :param case_goal: 期望结果
    :param wt_reqs: 委托参数
    :param component_stk_before: 下单前ETF成分股持仓
    :param pyname: 用例名称，部分修改申购赎回费率的用例需传此参数
    :return:
    """

    def on_order(data, error):
        """定义回调函数：实时报单推送校验"""

        # 报单推送外层校验
        bdCheck = g_func.cetf_bdts_check(Api, case_goal, wt_reqs, data)
        logger.info('报单推送-报单状态/提交状态check结果:' + str(bdCheck['flag']) +
                    ',' + bdCheck['remark'])

        # 如果报单报单推送外层检查通过，进行报单推送内层检查，否则用例执行结束
        if (bdCheck['flag'] and bdCheck['status'] == 'end' and
                    case_goal['是否是撤废'] == '否'):
            g_var.bdts_rs = cetf_bdts_datacheck(Api, wt_reqs, case_goal, data, error,
                                        g_var.QueryInit, g_var.QueryEnd)
        elif not bdCheck['flag'] and bdCheck['status'] == 'end':
            g_var.bdts_rs = {
                '报单检查状态': 'end',
                '测试结果': False,
                '错误信息': bdCheck['remark'],
            }
            g_var.result['用例检查状态'] = 'end'
            g_var.result['用例测试结果'] = False
            g_var.result['用例错误原因'] = bdCheck['remark']
            g_var.result['用例错误源'] = '报单推送－状态检查'
        elif bdCheck['status']=='pending' and case_goal['是否是撤废']=='是':
            case_goal['cancel_xtpID']=bdCheck['cancel_xtpID']

    def on_queryorder(data,error,reqID,is_last):
        """定义回调函数：报单查询结果校验"""
        logger.info('报单查询回调开始，当前报单xtpID=' + str(data['order_xtp_id'])
                    + ',报单状态=' + str(data['order_status']) + ',提交状态=' +
                    str(data['order_submit_status']))

        # 进行报单查询外层检查
        bdQuecyCheck = g_func.cetf_bdquery_check(Api, case_goal, wt_reqs, data)
        logger.info('报单查询-报单状态/提交状态check结果:' +
                    str(bdQuecyCheck['flag']) + ',' +
                    str(bdQuecyCheck['检查状态']) + ',' + bdQuecyCheck['remark'])

        # 定义全局变量bdquery_rs(报单查询结果)，cdquery_rs（撤单查询结果）

        # 如果外层检查通过
        if bdQuecyCheck['flag'] and bdQuecyCheck['检查状态'] == 'end':
            if case_goal['是否是撤废'] == '是':
                component_stk_begin = g_var.component_stk_info_reject
            else:
                component_stk_begin = component_stk_before

            rs = cetf_bdquery_datacheck(Api, wt_reqs, case_goal, data, error,
                        g_var.QueryInit, g_var.QueryEnd, component_stk_begin,
                        g_var.cash_substitute_amount)
            if rs['报单类型'] == '报单':
                g_var.bdquery_rs = rs
                g_var.result['报单检查状态'] = rs['报单检查状态']
                g_var.result['报单测试结果'] = rs['测试结果']
                g_var.result['报单错误原因'] = rs['错误信息']
            elif rs['报单类型'] == '撤单':
                g_var.QueryEnd['股票代码'] = None
                g_var.cdquery_rs = rs
                g_var.result['撤单检查状态'] = rs['报单检查状态']
                g_var.result['撤单测试结果'] = rs['测试结果']
                g_var.result['撤单错误原因'] = rs['错误信息']
                if case_goal['是否是撤废']=='是':
                    if rs['测试结果']:
                        g_var.result['用例测试结果'] = True
                        g_var.result['用例检查状态'] = 'end'
            else:
                g_var.result['报单检查状态'] = 'end'
                g_var.result['报单测试结果'] = False
                g_var.result['报单错误原因'] = '报单类型无法识别'
                g_var.result['撤单检查状态'] = 'end'
                g_var.result['撤单测试结果'] = False
                g_var.result['撤单错误原因'] = '报单类型无法识别'
        elif bdQuecyCheck['检查状态'] == 'pending':
            # case_goal['cancel_xtpID'] = bdQuecyCheck['cancel_xtpID']
            logger.warning('报单查询等待...,xtpID='+str(data['order_xtp_id']))
            g_var.bdquery_rs = {'检查状态':'pending'}
            TODO
        elif bdQuecyCheck['检查状态'] == 'end' and bdQuecyCheck['flag'] == False:
            g_var.bdquery_rs = {
                '检查状态': 'end',
                '测试结果': False,
                '错误信息': bdQuecyCheck['remark']
            }
            g_var.result['报单检查状态'] = 'end'
            g_var.result['用例检查状态'] = 'end'
            g_var.result['用例测试结果'] = False
            g_var.result['用例错误原因'] = bdQuecyCheck['remark']
            g_var.result['用例错误源'] = '报单查询－状态检查'

    def on_trade(hb_data):
        """定义回调函数：成交回报数据校验"""
        logger.info('交易数据回报如下')
        dictLogging(hb_data)
        if case_goal['期望状态'] == '全成':
            g_func.set_query_end(Api, wt_reqs)
            # 收到成交回报后进行业务处理，返回值为为一个dict
            rs = cetf_cjhb_datacheck(
                                   Api,
                                   g_var.QueryInit,
                                   wt_reqs,
                                   case_goal['xtp_ID'],
                                   g_var.QueryEnd,
                                   hb_data,
                                   g_var.cash_substitute_amount,
                                   g_var.pre_close_prices,
                                   component_stk_before,
                                   pyname
                                   )
            # 只要有一笔成交回报有错误，就修改成交回报结果为False
            if rs['测试结果'] == False:
                g_var.cjhb_rs['成交回报检查状态'] = rs['成交回报检查状态']
                g_var.cjhb_rs['xtp_id'] = rs['xtp_id']
                g_var.cjhb_rs['市场'] = rs['市场']
                g_var.cjhb_rs['股票代码'] = rs['股票代码']
                g_var.cjhb_rs['买卖方向'] = rs['买卖方向']
                g_var.cjhb_rs['成交价格'] = rs['成交价格']
                g_var.cjhb_rs['成交数量'] = rs['成交数量']
                g_var.cjhb_rs['成交金额'] = rs['成交金额']
                g_var.cjhb_rs['成交类型'] = rs['成交类型']
                g_var.cjhb_rs['测试结果'] = rs['测试结果']
                g_var.cjhb_rs['测试错误原因'] = rs['测试错误原因']
            # 未发生错误的成交回报无需修改状态
            else:
                g_var.cjhb_rs['xtp_id'] = rs['xtp_id']

        # 其他状态不会收到成交回报，如果触发了成交回报但是期望状态为其他状态，说明用例失败
        else:
            logger.info('成交回报检查：收到成交回报，但用例期望状态非【全成】,'
                        '用例执行失败！')
            g_var.cjhb_rs = {
                '成交回报检查状态': 'end',
                '测试结果': False,
            }

    def on_cancelorder_error(cancel_info, error_info):
        """定义异步回调函数：撤废业务校验"""
        logger.info('当前为撤废异步回调函数..start')
        time.sleep(0.2)
        if case_goal['是否是撤废'] == '是':
            # 外层校验：校验撤废的原始xtpID是否为该用例的xtpID
            if cancel_info['order_xtp_id'] != case_goal['xtp_ID']:
                logger.error('错误，当前API返回撤废的原xtpID与当前用例的xtpID不一致，'
                             '当前API返回的xtpID和此用例的xtpID分别是' + str(
                    cancel_info['order_xtp_id']) + ',' + str(case_goal['xtp_ID']))
                g_var.result['用例检查状态'] = 'end'
                g_var.result['用例错误源'] = '撤单'
                g_var.result['用例测试结果'] = False
                g_var.result['用例错误原因'] = '当前API返回撤废的原xtpID与当前用例的xtpID不一致'
            # 外层校验：校验当前撤单xtpID是否为该用例的撤单xtpID
            elif cancel_info['order_cancel_xtp_id'] != case_goal['cancel_xtpID']:
                print cancel_info['order_cancel_xtp_id']
                print case_goal['cancel_xtpID']
                g_var.result['用例检查状态'] = 'end'
                g_var.result['用例错误源'] = '撤单'
                g_var.result['用例测试结果'] = False
                g_var.result['用例错误原因'] = '当前API返回撤废的xtpID与当前用例的撤废xtpID不一致'
            else:
                rs = cancelOrderErrorDataCheck(case_goal, error_info)

                if rs['检查状态'] == 'end' and rs['测试结果'] == True:
                    # 报单查询（撤废）
                    g_func.query_by_xtpid(Api, case_goal['cancel_xtpID'])
                else:
                    g_var.result['用例检查状态'] = 'end'
                    g_var.result['用例测试结果'] = False
                    g_var.result['用例错误原因'] = rs['错误原因']
                    g_var.result['用例错误源'] = rs['撤废']

        else:
            logger.error('错误，当前撤单为撤废与期望状态不符合，期望状态为' + case_goal['期望状态'])
            g_var.result['用例检查状态'] = 'end'
            g_var.result['用例错误源'] = '撤单'
            g_var.result['用例测试结果'] = False
            g_var.result['用例错误原因'] = '当前撤单为撤废与期望状态不符合'

    # 将定义后的回调函数设置成Api回调函数
    Api.trade.setTradeEventHandle(on_trade)
    Api.trade.setQueryOrderHandle(on_queryorder)
    Api.trade.setOrderEventHandle(on_order)
    Api.trade.setCancelOrderErrorHandle(on_cancelorder_error)

    # --------------------------------------------------------------------------
    # 当期望状态是'未成交','全成','废单','内部撤单'，在下单前查询初始资金、持仓
    # --------------------------------------------------------------------------
    if case_goal['期望状态'] in ('未成交', '全成', '废单','内部撤单'):
        g_func.set_query_init(Api, wt_reqs)

    # 如果期望状态是全成、未成交，获取允许现金替代金额、成分股昨收价
    if case_goal['期望状态'] in ('全成', '未成交'):
        g_var.pre_close_prices = query_compnents_preclose_price(
            wt_reqs['ticker'])
        etf_code1_code2 = query_cetf_code1code2(wt_reqs['ticker'])
        # 计算etf申购赎回委托份数
        creation_redemption_unit = (wt_reqs['quantity'] /
                                query_creation_redem_unit(wt_reqs['ticker']))
        if etf_code1_code2 != {}:
            # 计算允许现金替代金额, 已乘以下单ETF份数，非单份ETF
            g_var.cash_substitute_amount = cetf_get_cash_subtitute_amount(
                Api,
                wt_reqs['market'],
                etf_code1_code2['etf_code1'],
                creation_redemption_unit)

    # --------------------------------------------------------------------------
    # 准备下单，获取当前时间戳
    # 下单，并获取该笔订单xtpID
    # --------------------------------------------------------------------------
    insertOrderTime = getTime.getTimestampInt()
    case_goal['xtp_ID'] = Api.trade.InsertOrder(wt_reqs)
    logger.info('下单的xtpID=' + str(case_goal['xtp_ID']))

    # 不生成报单的用例（数量小于0），xtpID为0
    if case_goal['xtp_ID']==0:
        if case_goal['期望状态']=='废单':
            msg=Api.trade.GetApiLastError()
            dictLogging(msg)
            if case_goal['errorID'] == msg['error_id']:
                logger.info('废单校验正确！')
                g_var.result['用例检查状态'] = 'end'
                g_var.result['用例测试结果'] = True

            else:
                logger.error('期望的errorID和实际errorID不一致，'+'期望errorID＝'
                             + str(case_goal['errorID'])+'，实际errorID＝'
                             + str(msg['error_id']))
                g_var.result['用例检查状态'] = 'end'
                g_var.result['用例测试结果'] = False
                g_var.result['用例错误原因'] = '期望的errorID和实际errorID不一致'
        else:
            logger.error('下单的xtpID为0')
            g_var.result['用例检查状态'] = 'end'
            g_var.result['用例测试结果'] = False
            g_var.result['用例错误原因'] = '下单的xtpID为0'

    # --------------------------------------------------------------------------
    # 当报单检查状态非‘end’时，等待0.5秒再次检查状态,直到报单检查结束
    # --------------------------------------------------------------------------
    # 获取超时时间
    t = g_func.get_time_pending(case_goal['期望状态'])


    while getTime.getTimestampInt() <= insertOrderTime + t:
        if g_var.result['用例检查状态'] == 'end':
            break
        else:
            time.sleep(0.5)
            if (g_var.result['报单检查状态'] == 'end'
                    and g_var.result['撤单检查状态'] == 'end'):
                rs = cetf_case_end_check(g_var.bdts_rs, g_var.bdquery_rs,
                                      g_var.cdquery_rs, g_var.cjhb_rs,
                                    case_goal['期望状态'])
                g_var.result['用例检查状态'] = 'end'
                g_var.result['用例测试结果'] = rs['测试结果']
                g_var.result['用例错误原因'] = rs['错误原因']
                g_var.result['用例错误源'] = rs['错误源']

    # 超出设置的“超时”时间后
    if g_var.result['用例检查状态'] == 'init':
        g_var.result['用例测试结果'] = False
        g_var.result['用例错误原因'] = '用例超时'

    return g_var.result


