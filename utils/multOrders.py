#!/usr/bin/python
# -*- encoding: utf-8 -*-
import os
import sys
import time
from multiprocessing import Pool
sys.path.append("/home/yhl/workspace/xtp_test/xtp/api")
from xtp_test_case import *
from config import Config
from attribute import Attribute

users = {
    'user1': {
          'CONST_TRADE_CLIENT_ID': 123,
          'CONST_TRADE_SAVE_FILE_PATH': '/home/yhl/workspace/xtp_test/Autocase_Result',
          'CONST_TRADE_IP': '10.25.24.199',
          'CONST_TRADE_PORT': 8088,
          'CONST_TRADE_USER': 'testshopt03tgt',
          'CONST_TRADE_PASSWORD': '123456',
          'CONST_TRADE_SOCK_TYPE': 2,
          'CONST_TRADE_AUTO_LOGIN': True,
          'CONST_TRADE_KEY': 'b8aa7173bba3470e390d787219b2112e'
    },
    'user2': {
          'CONST_TRADE_CLIENT_ID': 124,
          'CONST_TRADE_SAVE_FILE_PATH': '/home/yhl/workspace/xtp_test/Autocase_Result',
          'CONST_TRADE_IP': '10.25.24.199',
          'CONST_TRADE_PORT': 8088,
          'CONST_TRADE_USER': 'testshopt04tgt',
          'CONST_TRADE_PASSWORD': '123456',
          'CONST_TRADE_SOCK_TYPE': 2,
          'CONST_TRADE_AUTO_LOGIN': True,
          'CONST_TRADE_KEY': 'b8aa7173bba3470e390d787219b2112e'
    },
    'user3': {
          'CONST_TRADE_CLIENT_ID': 125,
          'CONST_TRADE_SAVE_FILE_PATH': '/home/yhl/workspace/xtp_test/Autocase_Result',
          'CONST_TRADE_IP': '10.25.24.199',
          'CONST_TRADE_PORT': 8088,
          'CONST_TRADE_USER': 'testshopt05tgt',
          'CONST_TRADE_PASSWORD': '123456',
          'CONST_TRADE_SOCK_TYPE': 2,
          'CONST_TRADE_AUTO_LOGIN': True,
          'CONST_TRADE_KEY': 'b8aa7173bba3470e390d787219b2112e'
    },
    'user4': {
          'CONST_TRADE_CLIENT_ID': 125,
          'CONST_TRADE_SAVE_FILE_PATH': '/home/yhl/workspace/xtp_test/Autocase_Result',
          'CONST_TRADE_IP': '10.25.24.199',
          'CONST_TRADE_PORT': 8088,
          'CONST_TRADE_USER': 'testshopt01tgt',
          'CONST_TRADE_PASSWORD': '123456',
          'CONST_TRADE_SOCK_TYPE': 2,
          'CONST_TRADE_AUTO_LOGIN': True,
          'CONST_TRADE_KEY': 'b8aa7173bba3470e390d787219b2112e'
    },
    'user5': {
          'CONST_TRADE_CLIENT_ID': 125,
          'CONST_TRADE_SAVE_FILE_PATH': '/home/yhl/workspace/xtp_test/Autocase_Result',
          'CONST_TRADE_IP': '10.25.24.199',
          'CONST_TRADE_PORT': 8088,
          'CONST_TRADE_USER': 'testshopt02tgt',
          'CONST_TRADE_PASSWORD': '123456',
          'CONST_TRADE_SOCK_TYPE': 2,
          'CONST_TRADE_AUTO_LOGIN': True,
          'CONST_TRADE_KEY': 'b8aa7173bba3470e390d787219b2112e'
    },
    'user6': {
          'CONST_TRADE_CLIENT_ID': 123,
          'CONST_TRADE_SAVE_FILE_PATH': '/home/yhl/workspace/xtp_test/Autocase_Result',
          'CONST_TRADE_IP': '10.25.24.199',
          'CONST_TRADE_PORT': 8088,
          'CONST_TRADE_USER': 'testshopt06tgt',
          'CONST_TRADE_PASSWORD': '123456',
          'CONST_TRADE_SOCK_TYPE': 2,
          'CONST_TRADE_AUTO_LOGIN': True,
          'CONST_TRADE_KEY': 'b8aa7173bba3470e390d787219b2112e'
    },
    'user7': {
          'CONST_TRADE_CLIENT_ID': 124,
          'CONST_TRADE_SAVE_FILE_PATH': '/home/yhl/workspace/xtp_test/Autocase_Result',
          'CONST_TRADE_IP': '10.25.24.199',
          'CONST_TRADE_PORT': 8088,
          'CONST_TRADE_USER': 'testshopt07tgt',
          'CONST_TRADE_PASSWORD': '123456',
          'CONST_TRADE_SOCK_TYPE': 2,
          'CONST_TRADE_AUTO_LOGIN': True,
          'CONST_TRADE_KEY': 'b8aa7173bba3470e390d787219b2112e'
    },
    'user8': {
          'CONST_TRADE_CLIENT_ID': 125,
          'CONST_TRADE_SAVE_FILE_PATH': '/home/yhl/workspace/xtp_test/Autocase_Result',
          'CONST_TRADE_IP': '10.25.24.199',
          'CONST_TRADE_PORT': 8088,
          'CONST_TRADE_USER': 'testshopt08tgt',
          'CONST_TRADE_PASSWORD': '123456',
          'CONST_TRADE_SOCK_TYPE': 2,
          'CONST_TRADE_AUTO_LOGIN': True,
          'CONST_TRADE_KEY': 'b8aa7173bba3470e390d787219b2112e'
    },
    'user9': {
          'CONST_TRADE_CLIENT_ID': 125,
          'CONST_TRADE_SAVE_FILE_PATH': '/home/yhl/workspace/xtp_test/Autocase_Result',
          'CONST_TRADE_IP': '10.25.24.199',
          'CONST_TRADE_PORT': 8088,
          'CONST_TRADE_USER': 'testshopt09tgt',
          'CONST_TRADE_PASSWORD': '123456',
          'CONST_TRADE_SOCK_TYPE': 2,
          'CONST_TRADE_AUTO_LOGIN': True,
          'CONST_TRADE_KEY': 'b8aa7173bba3470e390d787219b2112e'
    },
    'user10': {
          'CONST_TRADE_CLIENT_ID': 125,
          'CONST_TRADE_SAVE_FILE_PATH': '/home/yhl/workspace/xtp_test/Autocase_Result',
          'CONST_TRADE_IP': '10.25.24.199',
          'CONST_TRADE_PORT': 8088,
          'CONST_TRADE_USER': 'testshopt10tgt',
          'CONST_TRADE_PASSWORD': '123456',
          'CONST_TRADE_SOCK_TYPE': 2,
          'CONST_TRADE_AUTO_LOGIN': True,
          'CONST_TRADE_KEY': 'b8aa7173bba3470e390d787219b2112e'
    },
}

trade1 = Attribute({
            'client_id': 123,
            'save_file_path': '/home/yhl/workspace/xtp_test/Autocase_Result',
            'ip': '10.25.24.199',
            'port': 8088,
            'user': 'testshopt03tgt',
            'password': '123456',
            'sock_type': 2,
            'auto_login': True,
            'key': 'b8aa7173bba3470e390d787219b2112e',
        })

trade2 = Attribute({
            'client_id': 124,
            'save_file_path': '/home/yhl/workspace/xtp_test/Autocase_Result',
            'ip': '10.25.24.199',
            'port': 8088,
            'user': 'testshopt04tgt',
            'password': '123456',
            'sock_type': 2,
            'auto_login': True,
            'key': 'b8aa7173bba3470e390d787219b2112e',
        })

trade3 = Attribute({
            'client_id': 125,
            'save_file_path': '/home/yhl/workspace/xtp_test/Autocase_Result',
            'ip': '10.25.24.199',
            'port': 8088,
            'user': 'testshopt05tgt',
            'password': '123456',
            'sock_type': 2,
            'auto_login': True,
            'key': 'b8aa7173bba3470e390d787219b2112e',
        })


trade4 = Attribute({
            'client_id': 125,
            'save_file_path': '/home/yhl/workspace/xtp_test/Autocase_Result',
            'ip': '10.25.24.199',
            'port': 8088,
            'user': 'testshopt01tgt',
            'password': '123456',
            'sock_type': 2,
            'auto_login': True,
            'key': 'b8aa7173bba3470e390d787219b2112e',
        })

trade5 = Attribute({
            'client_id': 125,
            'save_file_path': '/home/yhl/workspace/xtp_test/Autocase_Result',
            'ip': '10.25.24.199',
            'port': 8088,
            'user': 'testshopt02tgt',
            'password': '123456',
            'sock_type': 2,
            'auto_login': True,
            'key': 'b8aa7173bba3470e390d787219b2112e',
        })

trade6 = Attribute({
            'client_id': 123,
            'save_file_path': '/home/yhl/workspace/xtp_test/Autocase_Result',
            'ip': '10.25.24.199',
            'port': 8088,
            'user': 'testshopt06tgt',
            'password': '123456',
            'sock_type': 2,
            'auto_login': True,
            'key': 'b8aa7173bba3470e390d787219b2112e',
        })

trade7 = Attribute({
            'client_id': 124,
            'save_file_path': '/home/yhl/workspace/xtp_test/Autocase_Result',
            'ip': '10.25.24.199',
            'port': 8088,
            'user': 'testshopt07tgt',
            'password': '123456',
            'sock_type': 2,
            'auto_login': True,
            'key': 'b8aa7173bba3470e390d787219b2112e',
        })

trade8 = Attribute({
            'client_id': 125,
            'save_file_path': '/home/yhl/workspace/xtp_test/Autocase_Result',
            'ip': '10.25.24.199',
            'port': 8088,
            'user': 'testshopt08tgt',
            'password': '123456',
            'sock_type': 2,
            'auto_login': True,
            'key': 'b8aa7173bba3470e390d787219b2112e',
        })


trade9 = Attribute({
            'client_id': 125,
            'save_file_path': '/home/yhl/workspace/xtp_test/Autocase_Result',
            'ip': '10.25.24.199',
            'port': 8088,
            'user': 'testshopt09tgt',
            'password': '123456',
            'sock_type': 2,
            'auto_login': True,
            'key': 'b8aa7173bba3470e390d787219b2112e',
        })

trade10 = Attribute({
            'client_id': 125,
            'save_file_path': '/home/yhl/workspace/xtp_test/Autocase_Result',
            'ip': '10.25.24.199',
            'port': 8088,
            'user': 'testshopt10tgt',
            'password': '123456',
            'sock_type': 2,
            'auto_login': True,
            'key': 'b8aa7173bba3470e390d787219b2112e',
        })

class MultOrders(xtp_test_case):

    def test_MultOrders(self):
        print('Parent process %s.' % os.getpid())
        pool_count = 10
        p = Pool(pool_count)
        for i in range(pool_count):
            
            p.apply_async(InsertOrdersSz, args=(i,))
        p.close()
        p.join()

def InsertOrdersSz(name):
    print 'pool num: {}'.format(name)
    #定义要下单的股票信息，在行情中寻找有对手方的股票。
    codes = ['000001', '000002', '000004', '000006', '000007']
    if name == 0:
        trade_api = XTPTradeApi(trade1, users['user1'])
        trade_api.Login(trade1)
    elif name == 1:
        trade_api = XTPTradeApi(trade2, users['user2'])
        trade_api.Login(trade2)
    elif name == 2:
        trade_api = XTPTradeApi(trade3, users['user3'])
        trade_api.Login(trade3)
    elif name == 3:
        trade_api = XTPTradeApi(trade4, users['user4'])
        trade_api.Login(trade4)
    elif name == 4:
        trade_api = XTPTradeApi(trade5, users['user5'])
        trade_api.Login(trade5)
    elif name == 5:
        trade_api = XTPTradeApi(trade6, users['user6'])
        trade_api.Login(trade6)
    elif name == 6:
        trade_api = XTPTradeApi(trade7, users['user7'])
        trade_api.Login(trade7)
    elif name == 7:
        trade_api = XTPTradeApi(trade8, users['user8'])
        trade_api.Login(trade8)
    elif name == 8:
        trade_api = XTPTradeApi(trade9, users['user9'])
        trade_api.Login(trade9)
    elif name == 9:
        trade_api = XTPTradeApi(trade10, users['user10'])
        trade_api.Login(trade10)
       
    count = 0
    order_client_id = 1
    while 1:
        for ticker in codes:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_CASH'],
                # 'order_client_id': order_client_id,
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT'],
                'market': Api.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A'],
                'ticker': ticker,
                'side': Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY'],
                'price_type': Api.const.XTP_PRICE_TYPE['XTP_PRICE_FORWARD_BEST'],
                'quantity': 200
            }
            trade_api.InsertOrder(wt_reqs)
            count += 1
            order_client_id = (order_client_id % 3 + 1)
            if count % 2 == 0:
                time.sleep(0.2)
            if count >= 100:
                trade_api.Logout()
                return

def InsertOrdersSh(name):
    #定义要下单的股票信息，在行情中寻找有对手方的股票。
    codes = ['600015', '600025', '600027', '600029', '600068', '600071']
    if name == 0:
        trade_api = XTPTradeApi(trade1, users['user1'])
        trade_api.Login(trade1)
    elif name == 1:
        trade_api = XTPTradeApi(trade2, users['user2'])
        trade_api.Login(trade2)
    elif name == 2:
        trade_api = XTPTradeApi(trade3, users['user3'])
        trade_api.Login(trade3)
    elif name == 3:
        trade_api = XTPTradeApi(trade4, users['user4'])
        trade_api.Login(trade4)
       
    count = 0
    order_client_id = 1
    while 1:
        for ticker in codes:
            wt_reqs = {
                'business_type': Api.const.XTP_BUSINESS_TYPE['XTP_BUSINESS_TYPE_CASH'],
                'order_client_id': order_client_id,
                'position_effect': Api.const.XTP_POSITION_EFFECT_TYPE['XTP_POSITION_EFFECT_INIT'],
                'market': Api.const.XTP_MARKET_TYPE['XTP_MKT_SH_A'],
                'ticker': ticker,
                'side': Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY'],
                'price_type': Api.const.XTP_PRICE_TYPE['XTP_PRICE_BEST5_OR_LIMIT'],
                'quantity': 200
            }
            trade_api.InsertOrder(wt_reqs)
            count += 1
            order_client_id = (order_client_id % 3 + 1)
            if count % 200 == 0:
                time.sleep(0.2)
            if count >= 125000:
                trade_api.Logout()
                return

def checkFund(filename, before_restart=True):
    asset = Api.trade.QueryAssetSync() 
    if before_restart:
        with open(filename + 'fund_rs_before_restart', 'w') as f:
            f.write(str(asset))
    else:
        with open(filename + 'fund_rs_after_restart', 'w') as f:
            f.write(str(asset))

def checkStk(filename, before_restart=True):
    pos = Api.trade.QueryPositionsSync()
    if before_restart:
        with open(filename + 'stk_rs_before_restart', 'w') as f:
            for k, v in pos['data'].items():
                f.write(str(v))
                f.write('\n')
    else:
        with open(filename + 'stk_rs_after_restart', 'w') as f:
            for k, v in pos['data'].items():
                f.write(str(v))
                f.write('\n')

        

if __name__ == '__main__':
    unittest.main()
    # checkFund('0069', True)
    # checkStk('0069', True)

