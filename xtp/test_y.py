#!/usr/bin/python
# -*- encoding: utf-8 -*-

# 导入单元测试模块
from api.xtp_test_case import *

# 单元测试01
############################################################################
class Test_y(xtp_test_case):

    def test_limit_SZa(self):
        print '深圳Ａ股股票限价买入全成测试'


        #下单参数
        wt_reqs = {
            'market': Api.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A'],
            'ticker': '000725',
            'side': Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY'],
            'price_type': Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT'],
            'price': 30,
            'quantity': 100,
        }


        stkcode = {
            'ticker': ''
        }


        stkasset0 = Api.trade.QueryPositionSync(stkcode)
        print '000725键是否存在has_key',stkasset0['data'].has_key(wt_reqs['ticker'])

        print '000725键是否存在keys',wt_reqs['ticker']in stkasset0['data'].keys()

        print '000998键是否存在has_key', stkasset0['data'].has_key('000998')

        print '000998键是否存在keys', '000998' in stkasset0['data'].keys()

        # print '000725键是否存在', stkasset0.has_key(wt_reqs['ticker'])
        # print '000998键是否存在', stkasset0.has_key('000998')





        # def on_order(data,error):
        #     print '这里是on_order',data,error
        #
        # def on_trade(data,error):
        #     print '这里是on_trade',data,error
        #
        # def on_queryOrder(data, error, request_id, is_last):
        #     print '这里是on_queryOrder',request_id,data,error,
        #
        # def on_cancelOrderError(data, error):
        #     print '这里是撤废！'
        #     print '撤废data=',data
        #     print '撤废error=', error
        #
        # Api.trade.setOrderEventHandle(on_order)
        # Api.trade.setTradeEventHandle(on_trade)
        # Api.trade.setQueryOrderHandle(on_queryOrder)
        # Api.trade.setCancelOrderErrorHandle(on_cancelOrderError)
        #
        #
        # #下单
        # xtp_ID=Api.trade.InsertOrder(wt_reqs)
        #
        # #报单查询
        # rs_QueryOrder = Api.trade.QueryOrderByXTPID(xtp_ID, 1)
        # print 'rs_QueryOrder',rs_QueryOrder

        # rs_QueryOrderSync = Api.trade.QueryOrderByXTPIDSync(xtp_ID, 1)
        # print rs_QueryOrderSync

        sleep(3)
        canceOrder_xtpID=Api.trade.CancelOrder(xtp_ID)
        rs_canceOrder=Api.trade.QueryOrderByXTPID(canceOrder_xtpID, 2)

        while 1:
            sleep(1)



if __name__ == '__main__':
    unittest.main()
