#!/usr/bin/python
# -*- encoding: utf-8 -*-


import sys
sys.path.append("/home/yhl2/workspace/xtp_test")
import time
from service.log import *

# 定义存储 订单的实时报单信息/报单查询信息/成交回报信息 的字典
order_info = {}
# 定义存储 重启环境后收到的订单信息的字典
restart_info = {}

def service_insertorder(Api,wt_reqs,config):
    """
    下单业务处理逻辑，
    下单后，将每笔订单的实时报单信息/报单查询信息/成交回报信息 根据username 和 xtpid
    存储在 order_info中
    :param Api:
    :param wt_reqs:
    :param config:用户配置信息
    :return:
    """

    # 获取用户名
    username = config['user']

    # 报单查询业务回调
    def on_QueryOrder(data,error,reqID,is_last):
        logger.info( '下单后报单查询业务回调开始')
        global order_info
        if error['error_id'] != 0 or error['error_msg'] != '':
            logger.error('报单查询出错,当前订单查询error_id：' + str(
                error['error_id']) + ',error_msg:'+ error['error_msg'])
        else:
            xtpid = data['order_xtp_id']
            # 增加pop('price')的代码都因为上海市价单重启OMS后价格会变成1.0，故暂不校验价格
            data.pop('price')
            # 将报单查询结果存放在order_info中
            # 此结果存放在order_info的结构是 {username:{xtpid:{'query_rs':查询结果}}}
            order_info[username][xtpid]['query_rs'] = str(data)


    # 报单回报业务回调
    def on_order(data, error):
        logger.info('下单后实时报单业务回调开始')
        global order_info
        if error['error_id'] != 0 or error['error_msg'] != '':
            logger.error('实时报单出错,当前订单error_id：' + str(
                error['error_id']) + ',error_msg:'+ error['error_msg'])
        else:
            xtpid = data['order_xtp_id']
            data.pop('price')
            # 如果data['qty_left']为0，说明从此条回报是全部成交的消息
            if data['qty_left'] == 0:
                # 此结果存放在order_info的结构是
                # {username:{xtpid:{'onorder_rs':{'order_report'：回报消息}}}}
                order_info[username][xtpid]['onorder_rs'][
                    'order_report'] = str(data)
            # 如果data['qty_left']不为0，说明从此条回报是订单确认的消息(未成交或部成)
            else:
                # 此结果存放在order_info的结构是
                # {username:{xtpid:{'onorder_rs':{'order_pending'：回报消息}}}}
                order_info[username][xtpid]['onorder_rs'][
                    'order_pending'] = str(data)



    # 成交回报业务回调
    def on_trade(hb_data):
        logger.info('下单后成交回报业务回调开始')
        global order_info
        xtpid = hb_data['local_order_id']
        # 成交回报可能会有多条，每条消息根据report_index来区分
        # 如果是ETF申赎，每条成交回报根据 股票代码+成交类型
        cjhb_index = hb_data['report_index']
        etf_index = str(hb_data['trade_type']) + str(hb_data['ticker'])
        # 此结果存放在order_info的结构是
        # {username:{xtpid:{'trade_rs':{'cjhb_index'：成交回报消息}}}}
        if wt_reqs['business_type'] == Api.const.XTP_BUSINESS_TYPE[
                    'XTP_BUSINESS_TYPE_ETF']:
            order_info[username][xtpid]['trade_rs'][etf_index] = str(hb_data)
        else:
            order_info[username][xtpid]['trade_rs'][cjhb_index] = str(hb_data)


    Api.trade.setOrderEventHandle(on_order)
    Api.trade.setQueryOrderHandle(on_QueryOrder)
    Api.trade.setTradeEventHandle(on_trade)

    # -------------------------------------------------------------------------
    # 下单----------------------------------------------------------------------
    global order_info
    xtp_ID = Api.trade.InsertOrder(wt_reqs)
    # 定义当前用户存储订单的字典
    if not order_info.has_key(username):
        order_info[username] = {}
    # 下单后根据xtpid 在order_info变量中定义该笔订单的 信息结构
    order_info[username][xtp_ID] = {
        'query_rs': None,
        'trade_rs': {},
        'onorder_rs': {}}

    # 如果xtp_ID = 0，下单失败，获取错误信息
    if xtp_ID == 0:
        msg = Api.trade.GetApiLastError()
        logger.error('xtp_ID为0，下单失败,errmsg为：')
        dictLogging(msg)
    else:
        # 如果订单期望部成或者全成，等待成交回报和报单推送
        if wt_reqs['order_client_id'] in (2,3):
            # 下单成功后,如果该笔订单的成交回报或实时报单回报为空，
            # 则继续等待实时报单和成交回报的推送
            while not order_info[username][xtp_ID]['trade_rs']:
                # 如果成交模式为部成，价格条件为深圳全成或撤销，不会有成交回报
                if wt_reqs['order_client_id'] == 3 and (wt_reqs['price_type'] ==
                    Api.const.XTP_PRICE_TYPE['XTP_PRICE_ALL_OR_CANCEL']):
                    break
                time.sleep(0.1)
            while not order_info[username][xtp_ID]['onorder_rs']:
                time.sleep(0.1)
            # 如果业务类型为ETF申赎，成交回报较多，多等待两秒
            if wt_reqs['business_type'] == Api.const.XTP_BUSINESS_TYPE[
                    'XTP_BUSINESS_TYPE_ETF']:
                time.sleep(2)
        # 如果订单期望未成交，则仅等待报单推送
        else:
            while not order_info[username][xtp_ID]['onorder_rs']:
                time.sleep(0.1)

        # 如果为期权交易，推送较慢，多等一下再进行报单查询
        if wt_reqs['business_type'] == Api.const.XTP_BUSINESS_TYPE[
            'XTP_BUSINESS_TYPE_OPTION']:
            time.sleep(1)
        # 实时报单和成交回报的推送后，进行报单查询
        Api.trade.QueryOrderByXTPID(xtp_ID, 1)
        # 如果没有获取到查询结果，持续等待
        while not order_info[username][xtp_ID]['query_rs']:
            time.sleep(0.1)

def service_cancleorder(Api,wt_reqs,config):
    """
    下单业务处理逻辑，
    下单后，将每笔订单的实时报单信息/报单查询信息/成交回报信息 根据username 和 xtpid
    存储在 order_info中
    :param Api:
    :param wt_reqs:
    :param config:用户配置信息
    :return:
    """
    # 获取用户名
    username = config['user']
    # 报单查询业务回调
    def on_QueryOrder(data,error,reqID,is_last):
        logger.info( '下单后报单查询业务回调开始')
        global order_info
        if error['error_id'] != 0 or error['error_msg'] != '':
            logger.error('报单查询出错,当前订单查询error_id：' + str(
                error['error_id']) + ',error_msg:'+ error['error_msg'])
        else:
            xtpid = data['order_xtp_id']
            data.pop('price')
            # 将报单查询结果存放在order_info中
            # 此结果存放在order_info的结构是 {username:{xtpid:{'query_rs':查询结果}}}
            order_info[username][xtpid]['query_rs'] = str(data)


    # 报单回报业务回调
    def on_order(data, error):
        logger.info('下单后实时报单业务回调开始')
        global order_info
        if error['error_id'] != 0 or error['error_msg'] != '':
            logger.error('实时报单出错,当前订单error_id：' + str(
                error['error_id']) + ',error_msg:'+ error['error_msg'])
        else:
            xtpid = data['order_xtp_id']
            data.pop('price')
            # 如果data['order_cancel_xtp_id']不为0，说明从此条回报是撤单信息
            if data['order_cancel_xtp_id'] != 0:
                # 此结果存放在order_info的结构是
                # {username:{xtpid:{'onorder_rs':{'order_cancle'：回报消息}}}}
                order_info[username][xtpid]['onorder_rs'][
                    'order_cancle'] = str(data)
            # 如果data['order_cancel_xtp_id']为0，说明从此条回报是订单确认信息
            else:
                # 此结果存放在order_info的结构是
                # {username:{xtpid:{'onorder_rs':{'order_pending'：回报消息}}}}
                order_info[username][xtpid]['onorder_rs'][
                    'order_pending'] = str(data)



    # 成交回报业务回调
    def on_trade(hb_data):
        logger.info('下单后成交回报业务回调开始')
        global order_info
        xtpid = hb_data['local_order_id']
        # 成交回报可能会有多条，每条消息根据report_index来区分
        cjhb_index = hb_data['report_index']
        # 此结果存放在order_info的结构是
        # {username:{xtpid:{'trade_rs':{'cjhb_index'：成交回报消息}}}}
        order_info[username][xtpid]['trade_rs'][cjhb_index] = str(hb_data)


    Api.trade.setOrderEventHandle(on_order)
    Api.trade.setQueryOrderHandle(on_QueryOrder)
    Api.trade.setTradeEventHandle(on_trade)

    # -------------------------------------------------------------------------
    # 下单----------------------------------------------------------------------
    global order_info
    xtp_ID = Api.trade.InsertOrder(wt_reqs)

    # 定义当前用户存储订单的字典
    if not order_info.has_key(username):
        order_info[username] = {}
    # 下单后根据xtpid 在order_info变量中定义该笔订单的 信息结构
    order_info[username][xtp_ID] = {
        'query_rs': None,
        'trade_rs': {},
        'onorder_rs': {}}

    # 如果xtp_ID = 0，下单失败，获取错误信息
    if xtp_ID == 0:
        msg = Api.trade.GetApiLastError()
        logger.error('xtp_ID为0，下单失败,errmsg为：')
        dictLogging(msg)
    else:
        # 如果订单期望部成或者全成，等待成交回报和报单推送
        if wt_reqs['order_client_id'] ==3:
            # 下单成功后,如果该笔订单的成交回报或实时报单回报为空，
            # 则继续等待实时报单和成交回报的推送
            while ((not order_info[username][xtp_ID]['trade_rs']) or
                    (not order_info[username][xtp_ID]['onorder_rs'])):
                time.sleep(0.1)
        # 如果订单期望未成交，则仅等待报单推送
        else:
            while not order_info[username][xtp_ID]['onorder_rs']:
                time.sleep(0.1)
                logger.info( u'等待实时报单')

        # 撤单
        logger.info(u'开始撤单')
        Api.trade.CancelOrder(xtp_ID)
        time.sleep(0.5)
        # 如果为期权交易，撤单较慢，多等一下再进行报单查询
        if wt_reqs['business_type'] == Api.const.XTP_BUSINESS_TYPE[
                    'XTP_BUSINESS_TYPE_OPTION']:
            time.sleep(1)
        # 实时报单和成交回报的推送后，进行报单查询
        logger.info(u'开始查询订单')
        Api.trade.QueryOrderByXTPID(xtp_ID, 1)
        # 如果没有获取到查询结果，持续等待
        while not order_info[username][xtp_ID]['query_rs']:
            time.sleep(0.1)
            logger.info(u'等待订单查询')


def service_restart(Api,config):
    """
    重启环境后，接受订单信息的推送的业务逻辑处理
    将OMS推送的每笔订单的实时报单信息/报单查询信息/成交回报信息 根据username 和 xtpid
    存储在 restart_info中
    :param Api:
    :param config:用户配置信息
    :return:
    """

    # 获取用户名
    username = config['user']
    # 报单查询业务回调
    def on_QueryOrder(data,error,reqID,is_last):
        logger.info( '重启环境后报单查询业务回调开始')
        global restart_info
        if error['error_id'] != 0 or error['error_msg'] != '':
            logger.error('重启环境后报单查询出错,当前订单查询error_id：' + str(
                error['error_id']) + ',error_msg:'+ error['error_msg'])
        else:
            xtpid = data['order_xtp_id']
            data.pop('price')
            restart_info[username][xtpid]['query_rs'] = str(data)


    # 报单回报业务回调
    def on_order(data, error):
        logger.info('重启环境后实时报单业务回调开始')
        global restart_info
        if error['error_id'] != 0 or error['error_msg'] != '':
            logger.error('重启环境后实时报单出错,当前订单error_id：' + str(
                error['error_id']) + ',error_msg:'+ error['error_msg'])
        else:
            xtpid = data['order_xtp_id']
            data.pop('price')
            # 如果restart_info中还没有此订单信息，则定义该xtpid存储结构
            if not restart_info[username].has_key(xtpid):
                restart_info[username][xtpid] = {
                    'query_rs': None,
                    'trade_rs': {},
                    'onorder_rs': {}}
            if data['qty_left'] == 0:
                restart_info[username][xtpid]['onorder_rs'][
                    'order_report'] = str(data)
            elif data['order_cancel_xtp_id'] != 0:
                restart_info[username][xtpid]['onorder_rs'][
                    'order_cancle'] = str(data)
            else:
                restart_info[username][xtpid]['onorder_rs'][
                    'order_pending'] = str(data)



    # 成交回报业务回调
    def on_trade(hb_data):
        logger.info('重启环境后成交回报业务回调开始')
        global restart_info
        xtpid = hb_data['local_order_id']
        cjhb_index = hb_data['report_index']
        etf_index = str(hb_data['trade_type']) + str(hb_data['ticker'])
        # 如果restart_info中还没有此订单信息，则定义该xtpid存储结构
        if not restart_info[username].has_key(xtpid):
            restart_info[username][xtpid] = {
                'query_rs': None,
                'trade_rs': {},
                'onorder_rs': {}}
        if hb_data['business_type'] == Api.const.XTP_BUSINESS_TYPE[
                    'XTP_BUSINESS_TYPE_ETF']:
            restart_info[username][xtpid]['trade_rs'][etf_index] = str(hb_data)
        else:
            restart_info[username][xtpid]['trade_rs'][cjhb_index] = str(hb_data)

    Api.trade.setOrderEventHandle(on_order)
    Api.trade.setQueryOrderHandle(on_QueryOrder)
    Api.trade.setTradeEventHandle(on_trade)

    global restart_info
    # 定义当前用户存储订单的字典
    if not restart_info.has_key(username):
        restart_info[username] = {}
    # 账号登出
    Api.trade.Logout()
    time.sleep(0.5)
    # 使用该设置，在API登入时接收到OMS推送的实时报单和成交回报信息
    Api.trade.SubscribePublicTopic(
        {'resume_type': Api.const.XTP_TE_RESUME_TYPE['XTP_TERT_RESTART']})
    Api.trade.Login(config)
    time.sleep(1)
    # -------------------------------------------------------------------------
    # 下单----------------------------------------------------------------------
    time.sleep(2)
    # 对OMS推送的每一笔订单进行查询，获取订单查询信息
    for xtpid in restart_info[username]:
        Api.trade.QueryOrderByXTPID(xtpid, 1)
        time.sleep(0.5)




def query_capital_stock(Api,orders,config,ticker):
    """
    查询资金和总持仓
    :param Api:
    :param orders: 保存订单信息的字典，可传入order_info 或者restart_info
    :param config:用户配置信息
    :param ticker: 要查询持仓的股票
    :return:
    """
    # 获取用户名
    username = config['user']
    fund = Api.trade.QueryAssetSync()
    # 每次查询request_id的值会变动，故在结果信息里将其剔除，方便结果信息比对
    fund['data'].pop('request_id')
    # 将查询到的资金信息保存在order_info 或者restart_info中
    orders[username]['fund'] = str(fund)

    # 查询当前账号所有持仓信息
    stkcode = {
        'ticker': ticker
    }
    stock = Api.trade.QueryPositionSync(stkcode)
    stock['data'].pop('request_id')
    # 将查询到的持仓信息保存在order_info 或者restart_info中
    orders[username]['stock'] = str(stock)


def check_result(order_info, restart_info):
    """
    检查重启前后订单信息是否一直
    :param order_info: 重启环境前的所有用户订单信息
    :param restart_info: 重启环境后所有用户订单信息
    :return:
    """

    # 定义校验结果
    result = {
        '结果': True,
    }

    before_users = order_info.keys()
    after_users = restart_info.keys()
    if before_users != after_users:
        logger.error('''错误，重启前后的用户数目不一致，重启前下单的用户有：%s,
                    重启后用户为：%s''' % (before_users,after_users))
        result['结果'] = False

    else:
        for user in order_info:
            for info in order_info[user]:
                if order_info[user][info] != restart_info[user][info]:
                    if info == 'fund':
                        logger.error('''错误，重启前后当前用户的资金信息不一致''')
                        logger.info('''当前用户为：%s,
                        重启前资金信息为：%s,重启后资金信息为：%s'''
                        % (user,str(order_info[user][info]),
                           str(restart_info[user][info])))
                    elif info == 'stock':
                        logger.error('''错误，重启前后当前用户的持仓信息不一致''')
                        logger.info('''当前用户为：%s,
                                    重启前持仓信息为：%s,重启后持仓信息为：%s'''
                                     % (user, str(order_info[user][info]),
                                        str(restart_info[user][info])))
                    else:
                        logger.error('''错误，重启前后当前用户的订单信息不一致''')
                        logger.info('''当前用户为：%s,当前xtpid为：%s,
                        重启前订单信息为：%s,重启后订单信息为：%s'''
                        % (user,info,str(order_info[user][info]),
                           str(restart_info[user][info])))
                    result['结果'] = False
    return result

def insert_order(Api,wt_reqs, user):
    """
    批量下单,支持两融
    :param Api:
    :param wt_reqs:
    :param user:
    :return:
    """
    price_type_sh = [Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT'],
                     Api.const.XTP_PRICE_TYPE['XTP_PRICE_BEST5_OR_CANCEL'],
                     Api.const.XTP_PRICE_TYPE['XTP_PRICE_BEST5_OR_LIMIT']]
    price_type_sz = [Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT'],
                     Api.const.XTP_PRICE_TYPE['XTP_PRICE_BEST_OR_CANCEL'],
                     Api.const.XTP_PRICE_TYPE['XTP_PRICE_BEST5_OR_CANCEL'],
                     Api.const.XTP_PRICE_TYPE['XTP_PRICE_ALL_OR_CANCEL'],
                     Api.const.XTP_PRICE_TYPE['XTP_PRICE_FORWARD_BEST'],
                     Api.const.XTP_PRICE_TYPE['XTP_PRICE_REVERSE_BEST_LIMIT']]
    # 上海
    if wt_reqs['market'] == Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A']:
        # 遍历每一种成交模式，分别下单
        for client_id in range(1,4):
            wt_reqs['order_client_id'] = client_id
            if client_id in (1,3):
                # 遍历每一种价格类型
                for price_type in price_type_sh:
                    wt_reqs['price_type'] = price_type
                    if wt_reqs['price_type'] == Api.const.XTP_PRICE_TYPE[
                            'XTP_PRICE_BEST5_OR_CANCEL']:
                        service_insertorder(Api, wt_reqs, user)
                    else:
                        service_insertorder(Api, wt_reqs, user)
                        service_cancleorder(Api, wt_reqs, user)
            elif client_id == 2:
                for price_type in price_type_sh:
                    wt_reqs['price_type'] = price_type
                    service_insertorder(Api, wt_reqs, user)
            else:
                logger.error('错误，当前order_client_id非1,2,3，无法识别')
    # 深圳
    else:
        for client_id in range(1,4):
            wt_reqs['order_client_id'] = client_id
            if client_id in (1,3):
                # 配股缴款没有部成状态，如果成交模式部成则不下单
                if (client_id == 3 and wt_reqs['business_type'
                ] == Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_ALLOTMENT']):
                    break
                # 遍历每一种价格类型
                for price_type in price_type_sz:
                    wt_reqs['price_type'] = price_type
                    if wt_reqs['price_type'] in ( Api.const.XTP_PRICE_TYPE[
                            'XTP_PRICE_LIMIT'],Api.const.XTP_PRICE_TYPE[
                            'XTP_PRICE_FORWARD_BEST'],Api.const.XTP_PRICE_TYPE[
                            'XTP_PRICE_REVERSE_BEST_LIMIT']):
                        service_insertorder(Api, wt_reqs, user)
                        service_cancleorder(Api, wt_reqs, user)
                    else:
                        service_insertorder(Api, wt_reqs, user)
            elif client_id == 2:
                # 遍历每一种价格类型
                for price_type in price_type_sz:
                    wt_reqs['price_type'] = price_type
                    service_insertorder(Api, wt_reqs, user)
            else:
                logger.error('错误，当前order_client_id非1,2,3，无法识别')

def insert_order_option(Api,wt_reqs, user):
    """
    期权批量下单
    :param Api:
    :param wt_reqs:
    :param user:
    :return:
    """
    price_type_sh = [Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT'],
                     Api.const.XTP_PRICE_TYPE['XTP_PRICE_REVERSE_BEST_LIMIT'],
                     Api.const.XTP_PRICE_TYPE['XTP_PRICE_BEST_OR_CANCEL'],
                     Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT_OR_CANCEL'],
                     Api.const.XTP_PRICE_TYPE['XTP_PRICE_ALL_OR_CANCEL']
                     ]
    side_type = [Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY'],
                Api.const.XTP_SIDE_TYPE['XTP_SIDE_SELL']]

    for side in side_type:
        wt_reqs['side'] = side
        # 遍历每一种成交模式，分别下单
        for client_id in range(1,4):
            wt_reqs['order_client_id'] = client_id
            if client_id == 1:
                wt_reqs['price_type'] = price_type_sh[0]
                service_insertorder(Api, wt_reqs, user)
                service_cancleorder(Api, wt_reqs, user)
            elif client_id == 2:
                # 遍历每一种价格类型
                for price_type in price_type_sh:
                    wt_reqs['price_type'] = price_type
                    service_insertorder(Api, wt_reqs, user)
            elif client_id == 3:
                # 遍历每一种价格类型
                for price_type in price_type_sh[:3]:
                    wt_reqs['price_type'] = price_type
                    if wt_reqs['price_type'] == Api.const.XTP_PRICE_TYPE[
                            'XTP_PRICE_BEST_OR_CANCEL']:
                        service_insertorder(Api, wt_reqs, user)
                    else:
                        service_insertorder(Api, wt_reqs, user)
                        service_cancleorder(Api, wt_reqs, user)
            else:
                logger.error('错误，当前order_client_id非1,2,3，无法识别')


def save_orderinfo(file1,file2,info1,info2):
    with open(file1,'w') as f1,open(file2,'w') as f2:
        f1.write(info1)
        f2.write(info2)

