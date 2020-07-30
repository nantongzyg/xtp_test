#!/usr/bin/python
# -*- encoding: utf-8 -*-
import datetime
import logging
import os
import MySQLdb
from os.path import join 
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
from decimal import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from mysql_config import connectMysql

reload(sys)
sys.setdefaultencoding('utf-8')

def hq_index(data, client_id):
    stock_code = data['ticker']
    
    if str(data['ticker'])[0:3] == '000' and data['exchange_id'] == Api.const.XTP_EXCHANGE_TYPE['XTP_EXCHANGE_SH']:
        stock_code = 'SH' + stock_code
        save_md_to_files(data,  stock_code, client_id)
    elif str(data['ticker'])[0:3] == '399' and data['exchange_id'] == Api.const.XTP_EXCHANGE_TYPE['XTP_EXCHANGE_SZ']:
        stock_code = 'SZ' + stock_code
        save_md_to_files(data, stock_code, client_id)
    else:
        pass

 # 行情10档买卖盘和买一卖一委托队列字段 
def snap_level_spot(data, client_id):
    save_level_path = 'SNAP_LEVEL_SPOT'
    stock_code = data['ticker']

    if data['exchange_id'] == Api.const.XTP_EXCHANGE_TYPE['XTP_EXCHANGE_SH']:
        if str(data['ticker'])[0:3] != '000':
            stock_code = 'SH' + stock_code
    else:
        if str(data['ticker'])[0:3] != '399':
            stock_code = 'SZ' + stock_code
    foo = []
    len_bid1_qty = len(data['bid1_qty_list'])
    len_ask1_qty = len(data['ask1_qty_list'])
    bid1_qty_rs = ''
    ask1_qty_rs = ''
    if len_bid1_qty >= 1:
        for bid in data['bid1_qty_list']:
            bid1_qty_rs = bid1_qty_rs + str(bid) + '|'
        bid1_qty_rs = bid1_qty_rs[:-1] + '\t'
    else:
        bid1_qty_rs = ''

    if len_ask1_qty >= 1:
        for a in data['ask1_qty_list']:
            ask1_qty_rs = ask1_qty_rs + str(a) + '|'
        ask1_qty_rs = ask1_qty_rs[:-1] + '\t'
    else:
        ask1_qty_rs = ''


    with open(join(str(client_id), save_level_path, stock_code), 'a') as wf:
        wf.write('%s%s%d%s%f'
                '%s%d%s%f%s'
                  '%d%s%f%s%d'
                  '%s%f%s%d%s'
                  '%f%s%d%s'
                  '%f%s%d%s'
                  '%f%s%d%s'
                  '%f%s%d%s'
                  '%f%s%d%s'
                  '%f%s%d%s'
                  '%f%s%d%s'
                  '%f%s%d%s'
                  '%f%s%d%s'
                  '%f%s%d%s'
                  '%f%s%d%s'
                  '%f%s%d%s'
                  '%f%s%d%s'
                  '%f%s%d%s'
                  '%f%s%d%s'
                  '%f%s%d%s'
                  '%d%s%d%s%s'
                  '%d%s%d%s%s' %
                 (stock_code, '\t', data['data_time'], '\t', Decimal(data['ask10']).quantize(Decimal('0.000000')),
                   '\t', data['ask_qty10'], '\t', Decimal(data['ask9']).quantize(Decimal('0.000000')), '\t',
                   data['ask_qty9'], '\t', Decimal(data['ask8']).quantize(Decimal('0.000000')), '\t', data['ask_qty8'],
                   '\t', Decimal(data['ask7']).quantize(Decimal('0.000000')), '\t', data['ask_qty7'], '\t',
                   Decimal(data['ask6']).quantize(Decimal('0.000000')), '\t', data['ask_qty6'], '\t',
                   Decimal(data['ask5']).quantize(Decimal('0.000000')), '\t', data['ask_qty5'], '\t',
                   Decimal(data['ask4']).quantize(Decimal('0.000000')), '\t', data['ask_qty4'], '\t',
                   Decimal(data['ask3']).quantize(Decimal('0.000000')), '\t', data['ask_qty3'], '\t',
                   Decimal(data['ask2']).quantize(Decimal('0.000000')), '\t', data['ask_qty2'], '\t',
                   Decimal(data['ask1']).quantize(Decimal('0.000000')), '\t', data['ask_qty1'], '\t',
                   Decimal(data['bid1']).quantize(Decimal('0.000000')), '\t', data['bid_qty1'], '\t',
                   Decimal(data['bid2']).quantize(Decimal('0.000000')), '\t', data['bid_qty2'], '\t',
                   Decimal(data['bid3']).quantize(Decimal('0.000000')), '\t', data['bid_qty3'], '\t',
                   Decimal(data['bid4']).quantize(Decimal('0.000000')), '\t', data['bid_qty4'], '\t',
                   Decimal(data['bid5']).quantize(Decimal('0.000000')), '\t', data['bid_qty5'], '\t',
                   Decimal(data['bid6']).quantize(Decimal('0.000000')), '\t', data['bid_qty6'], '\t',
                   Decimal(data['bid7']).quantize(Decimal('0.000000')), '\t', data['bid_qty7'], '\t',
                   Decimal(data['bid8']).quantize(Decimal('0.000000')), '\t', data['bid_qty8'], '\t',
                   Decimal(data['bid9']).quantize(Decimal('0.000000')), '\t', data['bid_qty9'], '\t',
                   Decimal(data['bid10']).quantize(Decimal('0.000000')), '\t', data['bid_qty10'], '\t',
                   data['max_bid1_count'], '\t', data['bid1_count'], '\t', bid1_qty_rs,
                  data['max_ask1_count'], '\t', data['ask1_count'], '\t', ask1_qty_rs))
        wf.write('\n')

def snap_level_spot_one(data, client_id):
    save_level_path = 'SNAP_LEVEL_SPOT_ONE'
    stock_code = data['ticker']

    if data['exchange_id'] == Api.const.XTP_EXCHANGE_TYPE['XTP_EXCHANGE_SH']:
        stock_code = 'SH' + stock_code
    else:
        stock_code = 'SZ' + stock_code
    foo = []
    len_bid1_qty = len(data['bid1_qty_list'])
    len_ask1_qty = len(data['ask1_qty_list'])
    bid1_qty_rs = ''
    ask1_qty_rs = ''
    if len_bid1_qty >= 1:
        for bid in data['bid1_qty_list']:
            bid1_qty_rs = bid1_qty_rs + str(bid) + '|'
        bid1_qty_rs = bid1_qty_rs[:-1]
    else:
        bid1_qty_rs = ''

    if len_ask1_qty >= 1:
        for a in data['ask1_qty_list']:
            ask1_qty_rs = ask1_qty_rs + str(a) + '|'
        ask1_qty_rs = ask1_qty_rs[:-1]
    else:
        ask1_qty_rs = ''
    with open(join(save_level_path, stock_code), 'a') as wf:
        wf.write(stock_code + '\t' + str(data['data_time']) + '\t' + str(Decimal(data['ask10']).quantize(Decimal('0.000000'))) + '\t' + str(data['ask_qty10'])
            +'\t'+ str(Decimal(data['ask9']).quantize(Decimal('0.000000')))+'\t'+str(data['ask_qty9'])+'\t'+str(Decimal(data['ask8']).quantize(Decimal('0.000000')))+'\t'+str(data['ask_qty8'])
            +'\t' + str(Decimal(data['ask7']).quantize(Decimal('0.000000'))) + '\t' + str(data['ask_qty7']) +'\t'+str(Decimal(data['ask6']).quantize(Decimal('0.000000')))
			+'\t'+str(data['ask_qty6'])+'\t'+str(Decimal(data['ask5']).quantize(Decimal('0.000000')))+'\t'+str(data['ask_qty5'])
            +'\t' + str(Decimal(data['ask4']).quantize(Decimal('0.000000'))) + '\t' + str(data['ask_qty4']) + '\t' + str(Decimal(data['ask3']).quantize(Decimal('0.000000')))
			+'\t' +str(data['ask_qty3']) + '\t' + str(Decimal(data['ask2']).quantize(Decimal('0.000000'))) + '\t' + str(data['ask_qty2'])
            +'\t' + str(Decimal(data['ask1']).quantize(Decimal('0.000000'))) + '\t' + str(data['ask_qty1'])
            +'\t' + str(Decimal(data['bid1']).quantize(Decimal('0.000000'))) + '\t' +str(data['bid_qty1'])
			+'\t' + str(Decimal(data['bid2']).quantize(Decimal('0.000000'))) + '\t' + str(data['bid_qty2'])
            +'\t' + str(Decimal(data['bid3']).quantize(Decimal('0.000000'))) + '\t' + str(data['bid_qty3'])
			+'\t' + str(Decimal(data['bid4']).quantize(Decimal('0.000000'))) + '\t' +str(data['bid_qty4'])
			+'\t' + str(Decimal(data['bid5']).quantize(Decimal('0.000000'))) + '\t' + str(data['bid_qty5'])
            +'\t' + str(Decimal(data['bid6']).quantize(Decimal('0.000000'))) + '\t' + str(data['bid_qty6'])
			+'\t' + str(Decimal(data['bid7']).quantize(Decimal('0.000000'))) + '\t' +str(data['bid_qty7'])
			+'\t' + str(Decimal(data['bid8']).quantize(Decimal('0.000000'))) + '\t' + str(data['bid_qty8'])
            +'\t' + str(Decimal(data['bid9']).quantize(Decimal('0.000000'))) + '\t' + str(data['bid_qty9'])
			+'\t' + str(Decimal(data['bid10']).quantize(Decimal('0.000000'))) + '\t' + str(data['bid_qty10'])
            +'\t' + str(data['max_bid1_count']) + '\t' + str(data['bid1_count']) + '\t' + bid1_qty_rs
            +'\t' + str(data['max_ask1_count']) + '\t' + str(data['ask1_count']) + '\t' + ask1_qty_rs + '\t')
        wf.write('\n')

#行情基本字段
def hq_snap_spot(data, client_id):
    save_snap_path = 'HQ_SNAP_SPOT'
    stock_code = data['ticker']

    if data['exchange_id'] == Api.const.XTP_EXCHANGE_TYPE['XTP_EXCHANGE_SH']:
        if str(data['ticker'])[0:3] != '000':
            stock_code='SH' + stock_code
    else:
        if str(data['ticker'])[0:3] != '399':
            stock_code = 'SZ' + stock_code
    with open(join(str(client_id), save_snap_path, stock_code), 'a') as wf:
        wf.write(
                '%s%s%d%s%f%s'
                '%f%s%f%s'
                '%f%s%f%s'
                '%f%s%d%s%d%s'
                '%f%s%s%s' % (stock_code, '\t', data['data_time'], '\t', Decimal(data['pre_close_price']).quantize(Decimal('0.000000')), '\t',
                           Decimal(data['open_price']).quantize(Decimal('0.000000')), '\t', Decimal(data['high_price']).quantize(Decimal('0.000000')), '\t',
                           Decimal(data['low_price']).quantize(Decimal('0.000000')), '\t', Decimal(data['last_price']).quantize(Decimal('0.000000')), '\t',
                           Decimal(data['close_price']).quantize(Decimal('0.000000')), '\t', data['trades_count'], '\t', data['qty'], '\t',
                           Decimal(data['turnover']).quantize(Decimal('0.000000')), '\t', data['ticker_status'][0:2], '\t'))
        wf.write('\n')

#判断股票类型以及市场
def save_md_to_files(data, stock_code, client_id):
    filepath = 'HQ_INDEX'
    with open(join(str(client_id), filepath, stock_code), 'a') as wf:
        wf.write(
                '%s%s%d%s%f%s'
                '%f%s%f%s'
                '%f%s%f%s'
                '%d%s%d%s%f%s'
                '%s%s' % (stock_code, '\t', data['data_time'], '\t', Decimal(data['pre_close_price']).quantize(Decimal('0.000000')), '\t',
                       Decimal(data['open_price']).quantize(Decimal('0.000000')), '\t', Decimal(data['high_price']).quantize(Decimal('0.000000')), '\t',
                       Decimal(data['low_price']).quantize(Decimal('0.000000')), '\t', Decimal(data['last_price']).quantize(Decimal('0.000000')), '\t',
                       data['trades_count'], '\t', data['qty'], '\t', Decimal(data['turnover']).quantize(Decimal('0.000000')), '\t',
                       data['ticker_status'][0:2], '\t'))
        wf.write('\n')

#订单薄
def save_ob(data, client_id):
    save_ob_path = 'HQ_OB'
    stock_code = data['ticker']

    if data['exchange_id'] == Api.const.XTP_EXCHANGE_TYPE['XTP_EXCHANGE_SH']:
        if str(data['ticker'])[0:3] != '000':
            stock_code = 'SH' + stock_code
    else:
        if str(data['ticker'])[0:3] != '399':
            stock_code = 'SZ' + stock_code
    foo = []

    with open(join(str(client_id), save_ob_path, stock_code), 'a') as wf:
        wf.write(
                '%s%s%d%s%f%s%d%s'
                '%f%s%d%s'
                '%f%s%d%s'
                '%f%s%d%s'
                '%f%s%d%s'
                '%f%s%d%s'
                '%f%s%d%s'
                '%f%s%d%s'
                '%f%s%d%s'
                '%f%s%d%s'
                '%f%s%d%s'
                '%f%s%d%s'
                '%f%s%d%s'
                '%f%s%d%s'
                '%f%s%d%s'
                '%f%s%d%s'
                '%f%s%d%s'
                '%f%s%d%s'
                '%f%s%d%s'
                '%f%s%d%s'
                '%f%s%d%s'
                '%f%s%d%s' % (stock_code, '\t', data['data_time'], '\t', Decimal(data['last_price']).quantize(Decimal('0.000000')), '\t', data['qty'], '\t',
                  Decimal(data['turnover']).quantize(Decimal('0.000000')), '\t', data['trades_count'], '\t',
                  Decimal(data['ask10']).quantize(Decimal('0.000000')), '\t', data['ask_qty10'], '\t',
                  Decimal(data['ask9']).quantize(Decimal('0.000000')), '\t', data['ask_qty9'], '\t',
                  Decimal(data['ask8']).quantize(Decimal('0.000000')), '\t', data['ask_qty8'], '\t',
                  Decimal(data['ask7']).quantize(Decimal('0.000000')), '\t', data['ask_qty7'], '\t',
                  Decimal(data['ask6']).quantize(Decimal('0.000000')), '\t', data['ask_qty6'], '\t',
                  Decimal(data['ask5']).quantize(Decimal('0.000000')), '\t', data['ask_qty5'], '\t',
                  Decimal(data['ask4']).quantize(Decimal('0.000000')), '\t', data['ask_qty4'], '\t',
                  Decimal(data['ask3']).quantize(Decimal('0.000000')), '\t', data['ask_qty3'], '\t',
                  Decimal(data['ask2']).quantize(Decimal('0.000000')), '\t', data['ask_qty2'], '\t',
                  Decimal(data['ask1']).quantize(Decimal('0.000000')), '\t', data['ask_qty1'], '\t',
                  Decimal(data['bid1']).quantize(Decimal('0.000000')), '\t', data['bid_qty1'], '\t',
                  Decimal(data['bid2']).quantize(Decimal('0.000000')), '\t', data['bid_qty2'], '\t',
                  Decimal(data['bid3']).quantize(Decimal('0.000000')), '\t', data['bid_qty3'], '\t',
                  Decimal(data['bid4']).quantize(Decimal('0.000000')), '\t', data['bid_qty4'], '\t',
                  Decimal(data['bid5']).quantize(Decimal('0.000000')), '\t', data['bid_qty5'], '\t',
                  Decimal(data['bid6']).quantize(Decimal('0.000000')), '\t', data['bid_qty6'], '\t',
                  Decimal(data['bid7']).quantize(Decimal('0.000000')), '\t', data['bid_qty7'], '\t',
                  Decimal(data['bid8']).quantize(Decimal('0.000000')), '\t', data['bid_qty8'], '\t',
                  Decimal(data['bid9']).quantize(Decimal('0.000000')), '\t', data['bid_qty9'], '\t',
                  Decimal(data['bid10']).quantize(Decimal('0.000000')), '\t', data['bid_qty10'], '\t'))
        wf.write('\n')

#逐笔委托
def save_tick_by_tick(data, client_id):
    stock_code = data['ticker']

    if data['exchange_id'] == Api.const.XTP_EXCHANGE_TYPE['XTP_EXCHANGE_SH']:
        if str(data['ticker'])[0:3] != '000':
            stock_code = 'SH' + stock_code
    else:
        if str(data['ticker'])[0:3] != '399':
            stock_code = 'SZ' + stock_code

    if data['type'] == Api.const.XTP_TBT_TYPE['XTP_TBT_ENTRUST']:
        save_order_path = 'HQ_ORDER_SPOT'
        with open(join(str(client_id), save_order_path, stock_code), 'a') as wf:
            wf.write(
                    '%s%s%d%s%d%s%d%s'
                    '%f%s%d%s'
                    '%d%s%s%s%s%s' % (stock_code, '\t', data['data_time'], '\t', data['channel_no'], '\t', data['seq'], '\t',
                   Decimal(data['price']).quantize(Decimal('0.000000')), '\t', data['qty'], '\t',
                   data['data_time'], '\t', data['side'], '\t', data['ord_type'], '\t'))
            wf.write('\n')
    else:
        save_trade_path = 'HQ_TRADE_SPOT'
        with open(join(str(client_id), save_trade_path, stock_code), 'a') as wf:
            wf.write(
                    '%s%s%d%s%d%s%d%s'
                    '%d%s%d%s%f%s'
                    '%d%s%s%s%d%s' % (stock_code, '\t', data['data_time'], '\t', data['channel_no'], '\t', data['seq'], '\t',
                           data['bid_no'], '\t', data['ask_no'], '\t', Decimal(data['price']).quantize(Decimal('0.000000')), '\t',
                           data['qty'], '\t', data['trade_flag'], '\t', data['data_time'], '\t'))
            wf.write('\n')

#逐笔成交
def save_trade(data, filepath, stock_code=''):
    save_trade_path = filepath
    if stock_code == '':
        code = data['ticker']
    else:
        code = stock_code

    if str(data['exchange_id']) == '1':
        if str(data['ticker'])[0:3] != '000':
            code = 'SH' + code
    elif str(data['exchange_id']) == '2':
        if str(data['ticker'])[0:3] != '399':
            code = 'SZ' + code

    with open(save_trade_path + stock_code, 'a') as wf:
        wf.write(
                '%s%s%d%s%d%s%d%s'
                '%d%s%d%s%f%s'
                '%d%s%d%s%d' % (code, '\t', data['data_time'], '\t', data['channel_no'], '\t', data['seq'], '\t',
                       data['bid_no'], '\t', data['ask_no'], '\t', Decimal(data['price']).quantize(Decimal('0.000000')), '\t',
                       data['qty'], '\t', data['trade_flag'], '\t', data['data_time']))
        wf.write('\n')

def save_query_all_tickers(data, client_id):
    conn = connectMysql()
    try:
        cur = conn.cursor()
        sql = "insert into tickers_api values(%f,'%s',%d,%f,%f,'%s',%f,'%s',%d,'%s')" % \
        (data['price_tick'], unicode(data['ticker_name']), data['buy_qty_unit'],
            data['pre_close_price'], data['lower_limit_price'],
            data['ticker_type'], data['upper_limit_price'],
            data['exchange_id'], data['sell_qty_unit'], data['ticker'])
        print sql
        cur.execute(sql)
        conn.commit()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        conn.close()

if __name__ == '__main__':
    save_path = '/home/yhl2/workspace/xtp_test/log/'


