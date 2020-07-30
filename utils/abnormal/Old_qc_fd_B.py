#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp")
from testcase import *

sys.path.append("/home/yhl2/workspace/xtp_test/ETF_mysql")
from QueryStkDB import *

sys.path.append("/home/yhl2/workspace/xtp_test/HB_old_bak")
from CJHB import *
from BDTS import *

class ATC_DPC_qc_fd_B(XTPTestCase):

    def test_limit_SZa(self):

        # 定义当前测试用例覆盖的功能－－最终的报单状态（包括撤单）
        case_goal = {
            '期望状态': Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_PARTTRADEDQUEUEING'],
            'errorID': 0,
            'errorMSG': '',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
            '报单状态': None,
            '提交状态': None,
        }


        #定义委托参数信息------------------------------------------
        stkparm=QueryStkprice('000423','2','0')
        wt_reqs={
            'market':Api.const.XTP_MARKET_TYPE['XTP_MKT_SZ_A'],
            'ticker':stkparm['证券代码'],
            'side':Api.const.XTP_SIDE_TYPE['XTP_SIDE_BUY'],
            'price_type':Api.const.XTP_PRICE_TYPE['XTP_PRICE_LIMIT'],
            'price': stkparm['随机中间价'],
            'quantity':200
            }

        #定义下单前资金持仓全局变量－----------------
        QueryInit={
            '可用资金': 0.00,
            '买入资金':0.00,
            '买入费用':0.00,
            '卖出资金':0.00,
            '卖出费用':0.00,
            '股票代码':None,
            '市场':None,
            '拥股数量':0,
            '可用股份数':0,
            '持仓成本':0.000,
            '浮动盈亏':0

        }

        #定义下单后的资金持仓全局变量----------------------
        QueryEnd={
            '可用资金': 0.00,
            '买入资金': 0.00,
            '买入费用': 0.00,
            '卖出资金': 0.00,
            '卖出费用': 0.00,
            '股票代码': None,
            '市场': None,
            '拥股数量': 0,
            '可用股份数': 0,
            '持仓成本': 0.000,
            '浮动盈亏': 0

        }

        #下单前资金查询-------------------------------------
        fundasset0 = Api.trade.QueryAssetSync()
        print "初始资金为",fundasset0
        QueryInit['可用资金']=fundasset0['asset']['buying_power']
        QueryInit['买入资金']=fundasset0['asset']['fund_buy_amount']
        QueryInit['买入费用']=fundasset0['asset']['fund_buy_fee']
        QueryInit['卖出资金']=fundasset0['asset']['fund_sell_amount']
        QueryInit['卖出费用']=fundasset0['asset']['fund_sell_fee']


        #下单前查询持仓------------------------------------------
        stkcode={
            'ticker':''
        }
        stkasset0 = Api.trade.QueryPositionSync(stkcode)
        for j in stkasset0['position']:
            if stkasset0['position'][j]['position']['ticker'] == wt_reqs['ticker']:
                QueryInit['股票代码'] = stkasset0['position'][j]['position']['ticker']
                QueryInit['市场'] = stkasset0['position'][j]['position']['market']
                QueryInit['拥股数量'] = stkasset0['position'][j]['position']['total_qty']
                QueryInit['可用股份数'] = stkasset0['position'][j]['position']['sellable_qty']
                QueryInit['持仓成本'] = stkasset0['position'][j]['position']['avg_price']
                QueryInit['浮动盈亏'] = stkasset0['position'][j]['position']['unrealized_pnl']
                print '初始持仓为:',QueryInit

        if QueryInit['股票代码'] != wt_reqs['ticker']:
            QueryInit['股票代码'] = wt_reqs['ticker']
            QueryInit['市场'] = wt_reqs['market']
            QueryInit['拥股数量'] = 0
            QueryInit['可用股份数'] = 0
            QueryInit['持仓成本'] = 0
            QueryInit['浮动盈亏'] = 0
            print '初始持仓为:', QueryInit



        #下单前初始化　bd_time（各个状态的报单时间）为空
        bdTimeInit()

        #下单-----------------------------------------------------
        xtp_id = Api.trade.InsertOrder(wt_reqs)
        case_goal['xtp_ID']=xtp_id
        print "下单的xtpID=",xtp_id

        # 撤单，如果测试用例期望的状态是已撤、部撤，则执行撤单---------------------
        if case_goal['期望状态'] in(Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_CANCELED'],Api.const.XTP_ORDER_STATUS_TYPE['XTP_ORDER_STATUS_PARTTRADEDNOTQUEUEING']):
            sleep(5)
            case_goal['cancel_xtpID'] = Api.trade.CancelOrder(xtp_id)
            print '撤单的xtp_id=', case_goal['cancel_xtpID']
        else:
            case_goal['cancel_xtpID'] = 0

        #报单回报业务处理
        def on_order(data, error):

            bdhb_reslut=bdhb(Api,wt_reqs,case_goal,data,error)
            print 'on_order结果', bdhb_reslut

        #成交回报业务处理
        def on_trade(hb_data):
            print "交易数据回报",hb_data

            #收到成交回报后查询资金-------------------------------------
            fundasset9 = Api.trade.QueryAssetSync()
            if fundasset0['is_last'] == True:
                QueryEnd['可用资金'] = fundasset9['asset']['buying_power']
                QueryEnd['买入资金'] = fundasset9['asset']['fund_buy_amount']
                QueryEnd['买入费用'] = fundasset9['asset']['fund_buy_fee']
                QueryEnd['卖出资金'] = fundasset9['asset']['fund_sell_amount']
                QueryEnd['卖出费用'] = fundasset9['asset']['fund_sell_fee']
            else:
                print "收到成交回报资金查询：查询的资金返回值非is_last"

            # 收到成交回报后查询持仓-------------------------------------
            stkasset9 = Api.trade.QueryPositionSync(stkcode)
            for j in stkasset9['position']:
                if stkasset9['position'][j]['position']['ticker'] == wt_reqs['ticker']:
                    QueryEnd['股票代码'] = stkasset9['position'][j]['position']['ticker']
                    QueryEnd['市场'] = stkasset9['position'][j]['position']['market']
                    QueryEnd['拥股数量'] = stkasset9['position'][j]['position']['total_qty']
                    QueryEnd['可用股份数'] = stkasset9['position'][j]['position']['sellable_qty']
                    QueryEnd['持仓成本'] = stkasset9['position'][j]['position']['avg_price']
                    QueryEnd['浮动盈亏'] = stkasset9['position'][j]['position']['unrealized_pnl']


            #　收到成交回报后进行业务处理，返回值为为一个dict
            cjhb_reslut=CJHB(Api,QueryInit,wt_reqs,xtp_id,QueryEnd,hb_data)
            print cjhb_reslut

        def on_cancelorder_error(cancel_info,error_info):
            print '撤单信息',cancel_info
            print '撤单错误信息', error_info

        Api.trade.setOrderEventHandle(on_order)
        Api.trade.setTradeEventHandle(on_trade)
        Api.trade.setCancelOrderErrorHandle(on_cancelorder_error)

        while 1:
            sleep(1)


if __name__ == '__main__':
    unittest.main()


