#!/usr/bin/python
# -*- encoding: utf-8 -*-
aaa={
    'branch_pbu': '016701',
    'trade_amount': 2271.0,
    'exec_id': '0000741632297920',
    'trade_type': '0',
    'order_client_id': 0,
    'order_exch_id': '000000BFDEADBF4F',
    'price': 22.71,
    'report_index': 195,
    'local_order_id': 122485588643361,
    'trade_time': 20160816161748778,
    'order_xtp_id': 122485588643361,
    'ticker': '000002',
    'side': api.vnxtptrade.XTP_SIDE_TYPE.XTP_SIDE_BUY,
    'market': api.vnxtptrade.XTP_MARKET_TYPE.XTP_MKT_SZ_A,
    'quantity': 100}
Traceback (most recent call last):





# １．先部分成交
# 委托数据回报 {'cancel_time': 0, 'update_time': 0, 'order_cancel_xtp_id': 0, 'order_client_id': 0, 'trade_amount': 0.0, 'price_type': api.vnxtptrade.XTP_PRICE_TYPE.XTP_PRICE_LIMIT, 'order_type': '\x00', 'price': 22.74, 'qty_traded': 0, 'qty_left': 200, 'order_local_id': 'C41roag5', 'side': api.vnxtptrade.XTP_SIDE_TYPE.XTP_SIDE_BUY, 'order_submit_status': api.vnxtptrade.XTP_ORDER_SUBMIT_STATUS_TYPE.XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED, 'insert_time': 20160816163053652, 'order_xtp_id': 122485588683361, 'order_status': api.vnxtptrade.XTP_ORDER_STATUS_TYPE.XTP_ORDER_STATUS_NOTRADEQUEUEING, 'ticker': '000002', 'order_cancel_client_id': 0, 'market': api.vnxtptrade.XTP_MARKET_TYPE.XTP_MKT_SZ_A, 'quantity': 200}
# 委托error回报 {'error_id': 0, 'error_msg': ''}
#
# ２．再全部成交
# 委托数据回报 {'cancel_time': 0, 'update_time': 0, 'order_cancel_xtp_id': 0, 'order_client_id': 0, 'trade_amount': 4548.0, 'price_type': api.vnxtptrade.XTP_PRICE_TYPE.XTP_PRICE_LIMIT, 'order_type': '\x00', 'price': 22.74, 'qty_traded': 200, 'qty_left': 0, 'order_local_id': 'C41roag5', 'side': api.vnxtptrade.XTP_SIDE_TYPE.XTP_SIDE_BUY, 'order_submit_status': api.vnxtptrade.XTP_ORDER_SUBMIT_STATUS_TYPE.XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED, 'insert_time': 20160816163053652, 'order_xtp_id': 122485588683361, 'order_status': api.vnxtptrade.XTP_ORDER_STATUS_TYPE.XTP_ORDER_STATUS_ALLTRADED, 'ticker': '000002', 'order_cancel_client_id': 0, 'market': api.vnxtptrade.XTP_MARKET_TYPE.XTP_MKT_SZ_A, 'quantity': 200}
# 委托error回报 {'error_id': 0, 'error_msg': ''}


# ２．再全部成交
aa={'cancel_time': 0,
 'update_time': 0,
 'order_cancel_xtp_id': 0,
 'order_client_id': 0,
 'trade_amount': 4548.0,
 'price_type': api.vnxtptrade.XTP_PRICE_TYPE.XTP_PRICE_LIMIT,
 'order_type': '\x00',
 'price': 22.74,
 'qty_traded': 200,
 'qty_left': 0,
 'order_local_id': 'C41roag5',
 'side': api.vnxtptrade.XTP_SIDE_TYPE.XTP_SIDE_BUY,
 'order_submit_status': api.vnxtptrade.XTP_ORDER_SUBMIT_STATUS_TYPE.XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED,
 'insert_time': 20160816163053652, 'order_xtp_id': 122485588683361,
 'order_status': api.vnxtptrade.XTP_ORDER_STATUS_TYPE.XTP_ORDER_STATUS_ALLTRADED,
 'ticker': '000002',
 'order_cancel_client_id': 0,
 'market': api.vnxtptrade.XTP_MARKET_TYPE.XTP_MKT_SZ_A,
 'quantity': 200}



# 委托error回报 {'error_id': 0, 'error_msg': ''}































