# -*- encoding: utf-8 -*-
import sys
sys.path.append("/home/yhl2/workspace/xtp_test")
from vnxtpquote import *
from vnxtptrade import *
from config import Config
from xtp.api.utils import *

############################################################################
class XTPConst():
    # ------------------------------------------------------------------------
    def __init__(self):
        self.XTP_PROTOCOL_TYPE = {
            'XTP_PROTOCOL_TCP': XTP_PROTOCOL_TYPE.XTP_PROTOCOL_TCP,
            'XTP_PROTOCOL_UDP': XTP_PROTOCOL_TYPE.XTP_PROTOCOL_UDP
        }

        self.XTP_EXCHANGE_TYPE = {
            'XTP_EXCHANGE_SH': XTP_EXCHANGE_TYPE.XTP_EXCHANGE_SH,
            'XTP_EXCHANGE_SZ': XTP_EXCHANGE_TYPE.XTP_EXCHANGE_SZ
        }

        self.XTP_MARKET_TYPE = {
            'XTP_MKT_INIT': XTP_MARKET_TYPE.XTP_MKT_INIT,
            'XTP_MKT_SZ_A': XTP_MARKET_TYPE.XTP_MKT_SZ_A,
            'XTP_MKT_SH_A': XTP_MARKET_TYPE.XTP_MKT_SH_A
        }

        self.XTP_PRICE_TYPE = {
            #限价单
            'XTP_PRICE_LIMIT': XTP_PRICE_TYPE.XTP_PRICE_LIMIT,
            #即时成交剩余转撤销，市价单
            'XTP_PRICE_BEST_OR_CANCEL': XTP_PRICE_TYPE.XTP_PRICE_BEST_OR_CANCEL,
            #最优五档即时成交剩余转限价，市价单
            'XTP_PRICE_BEST5_OR_LIMIT': XTP_PRICE_TYPE.XTP_PRICE_BEST5_OR_LIMIT,
            #最优5档即时成交剩余转撤销，市价单
            'XTP_PRICE_BEST5_OR_CANCEL': XTP_PRICE_TYPE.XTP_PRICE_BEST5_OR_CANCEL,
            #全部成交或撤销,市价单
            'XTP_PRICE_ALL_OR_CANCEL': XTP_PRICE_TYPE.XTP_PRICE_ALL_OR_CANCEL,
            #本方最优，市价单
            'XTP_PRICE_FORWARD_BEST': XTP_PRICE_TYPE.XTP_PRICE_FORWARD_BEST,
            #对方最优剩余转限价，市价单
            'XTP_PRICE_REVERSE_BEST_LIMIT': XTP_PRICE_TYPE.XTP_PRICE_REVERSE_BEST_LIMIT,
            #期权限价申报FOK
            'XTP_PRICE_LIMIT_OR_CANCEL': XTP_PRICE_TYPE.XTP_PRICE_LIMIT_OR_CANCEL,
            #未知类型
            'XTP_PRICE_TYPE_UNKNOWN': XTP_PRICE_TYPE.XTP_PRICE_TYPE_UNKNOWN
        }

        self.XTP_BUSINESS_TYPE = {
            # 普通股票业务，股票买卖，etf买卖等
            'XTP_BUSINESS_TYPE_CASH': XTP_BUSINESS_TYPE.XTP_BUSINESS_TYPE_CASH,
            # 新股申购业务
            'XTP_BUSINESS_TYPE_IPOS': XTP_BUSINESS_TYPE.XTP_BUSINESS_TYPE_IPOS,
            # 回购业务
            'XTP_BUSINESS_TYPE_REPO': XTP_BUSINESS_TYPE.XTP_BUSINESS_TYPE_REPO,
            # 配股缴款
            'XTP_BUSINESS_TYPE_ALLOTMENT': XTP_BUSINESS_TYPE.XTP_BUSINESS_TYPE_ALLOTMENT,
            # etf申赎业务(暂未支持)
            'XTP_BUSINESS_TYPE_ETF': XTP_BUSINESS_TYPE.XTP_BUSINESS_TYPE_ETF,
            # 期权买卖业务
            'XTP_BUSINESS_TYPE_OPTION': XTP_BUSINESS_TYPE.XTP_BUSINESS_TYPE_OPTION,
            # 融资融券业务(暂未支持)
            'XTP_BUSINESS_TYPE_MARGIN': XTP_BUSINESS_TYPE.XTP_BUSINESS_TYPE_MARGIN,
            # 行权
            'XTP_BUSINESS_TYPE_EXECUTE': XTP_BUSINESS_TYPE.XTP_BUSINESS_TYPE_EXECUTE,
            # 转托管(暂未支持)
            'XTP_BUSINESS_TYPE_DESIGNATION': XTP_BUSINESS_TYPE.XTP_BUSINESS_TYPE_DESIGNATION,
            # 分级基金申购
            'XTP_BUSINESS_TYPE_STRUCTURED_FUND_PURCHASE_REDEMPTION': XTP_BUSINESS_TYPE.XTP_BUSINESS_TYPE_STRUCTURED_FUND_PURCHASE_REDEMPTION,
            # 分级基金拆分合并
            'XTP_BUSINESS_TYPE_STRUCTURED_FUND_SPLIT_MERGE': XTP_BUSINESS_TYPE.XTP_BUSINESS_TYPE_STRUCTURED_FUND_SPLIT_MERGE,
            # 未知类型
            'XTP_BUSINESS_TYPE_UNKNOWN': XTP_BUSINESS_TYPE.XTP_BUSINESS_TYPE_UNKNOWN,
        }

        self.XTP_POSITION_DIRECTION_TYPE = {
            'XTP_POSITION_DIRECTION_NET': XTP_POSITION_DIRECTION_TYPE.XTP_POSITION_DIRECTION_NET,
            'XTP_POSITION_DIRECTION_LONG': XTP_POSITION_DIRECTION_TYPE.XTP_POSITION_DIRECTION_LONG,
            'XTP_POSITION_DIRECTION_SHORT': XTP_POSITION_DIRECTION_TYPE.XTP_POSITION_DIRECTION_SHORT,
            'XTP_POSITION_DIRECTION_COVERED': XTP_POSITION_DIRECTION_TYPE.XTP_POSITION_DIRECTION_COVERED,
        }

        XTP_POSITION_EFFECT_INIT = 0
        XTP_POSITION_EFFECT_OPEN = 1
        XTP_POSITION_EFFECT_CLOSE = 2
        XTP_POSITION_EFFECT_FORCECLOSE = 3
        XTP_POSITION_EFFECT_CLOSETODAY = 4
        XTP_POSITION_EFFECT_CLOSEYESTERDAY = 5
        XTP_POSITION_EFFECT_FORCEOFF = 6
        XTP_POSITION_EFFECT_LOCALFORCECLOSE = 7
        XTP_POSITION_EFFECT_UNKNOWN = 8
        self.XTP_POSITION_EFFECT_TYPE = {
            # 初始值或未知值
            'XTP_POSITION_EFFECT_INIT': XTP_POSITION_EFFECT_INIT,
            # 开
            'XTP_POSITION_EFFECT_OPEN': XTP_POSITION_EFFECT_OPEN,
            # 平
            'XTP_POSITION_EFFECT_CLOSE': XTP_POSITION_EFFECT_CLOSE,
            # 强平
            'XTP_POSITION_EFFECT_FORCECLOSE': XTP_POSITION_EFFECT_FORCECLOSE,
            # 平今
            'XTP_POSITION_EFFECT_CLOSETODAY': XTP_POSITION_EFFECT_CLOSETODAY,
            # 平昨
            'XTP_POSITION_EFFECT_CLOSEYESTERDAY': XTP_POSITION_EFFECT_CLOSEYESTERDAY,
            # 强减
            'XTP_POSITION_EFFECT_FORCEOFF': XTP_POSITION_EFFECT_FORCEOFF,
            # 本地强平
            'XTP_POSITION_EFFECT_LOCALFORCECLOSE': XTP_POSITION_EFFECT_LOCALFORCECLOSE,
            # 未知的类型
            'XTP_POSITION_EFFECT_UNKNOWN': XTP_POSITION_EFFECT_UNKNOWN
        }

        XTP_SIDE_BUY = 1
        XTP_SIDE_SELL = 2
        XTP_SIDE_PURCHASE = 7
        XTP_SIDE_REDEMPTION = 8
        XTP_SIDE_SPLIT = 9
        XTP_SIDE_MERGE = 10
        XTP_SIDE_COVER = 11
        XTP_SIDE_FREEZE = 12
        XTP_SIDE_MARGIN_TRADE = 21
        XTP_SIDE_SHORT_SELL = 22
        XTP_SIDE_REPAY_MARGIN = 23
        XTP_SIDE_REPAY_STOCK = 24
        XTP_SIDE_CASH_REPAY_MARGIN = 25
        XTP_SIDE_STOCK_REPAY_STOCK = 26
        XTP_SIDE_UNKNOWN = 27
        self.XTP_SIDE_TYPE = {
            'XTP_SIDE_BUY': XTP_SIDE_BUY,
            'XTP_SIDE_SELL': XTP_SIDE_SELL,
            'XTP_SIDE_PURCHASE': XTP_SIDE_PURCHASE,
            'XTP_SIDE_REDEMPTION': XTP_SIDE_REDEMPTION,
            'XTP_SIDE_SPLIT': XTP_SIDE_SPLIT,
            'XTP_SIDE_MERGE': XTP_SIDE_MERGE,
            'XTP_SIDE_COVER': XTP_SIDE_COVER,
            'XTP_SIDE_FREEZE': XTP_SIDE_FREEZE,
            'XTP_SIDE_MARGIN_TRADE': XTP_SIDE_MARGIN_TRADE,
            'XTP_SIDE_SHORT_SELL': XTP_SIDE_SHORT_SELL,
            'XTP_SIDE_REPAY_MARGIN': XTP_SIDE_REPAY_MARGIN,
            'XTP_SIDE_REPAY_STOCK': XTP_SIDE_REPAY_STOCK,
            'XTP_SIDE_CASH_REPAY_MARGIN': XTP_SIDE_CASH_REPAY_MARGIN,
            'XTP_SIDE_STOCK_REPAY_STOCK': XTP_SIDE_STOCK_REPAY_STOCK,
            'XTP_SIDE_UNKNOWN': XTP_SIDE_UNKNOWN,
        }

        self.XTP_ORDER_ACTION_STATUS_TYPE = {
            'XTP_ORDER_ACTION_STATUS_SUBMITTED': XTP_ORDER_ACTION_STATUS_TYPE.XTP_ORDER_ACTION_STATUS_SUBMITTED,
            'XTP_ORDER_ACTION_STATUS_ACCEPTED': XTP_ORDER_ACTION_STATUS_TYPE.XTP_ORDER_ACTION_STATUS_ACCEPTED,
            'XTP_ORDER_ACTION_STATUS_REJECTED': XTP_ORDER_ACTION_STATUS_TYPE.XTP_ORDER_ACTION_STATUS_REJECTED,
        }

        self.XTP_ORDER_STATUS_TYPE = {
            'XTP_ORDER_STATUS_INIT': XTP_ORDER_STATUS_TYPE.XTP_ORDER_STATUS_INIT,
            'XTP_ORDER_STATUS_ALLTRADED': XTP_ORDER_STATUS_TYPE.XTP_ORDER_STATUS_ALLTRADED,
            'XTP_ORDER_STATUS_PARTTRADEDQUEUEING': XTP_ORDER_STATUS_TYPE.XTP_ORDER_STATUS_PARTTRADEDQUEUEING,
            'XTP_ORDER_STATUS_PARTTRADEDNOTQUEUEING': XTP_ORDER_STATUS_TYPE.XTP_ORDER_STATUS_PARTTRADEDNOTQUEUEING,
            'XTP_ORDER_STATUS_NOTRADEQUEUEING': XTP_ORDER_STATUS_TYPE.XTP_ORDER_STATUS_NOTRADEQUEUEING,
            'XTP_ORDER_STATUS_CANCELED': XTP_ORDER_STATUS_TYPE.XTP_ORDER_STATUS_CANCELED,
            'XTP_ORDER_STATUS_REJECTED': XTP_ORDER_STATUS_TYPE.XTP_ORDER_STATUS_REJECTED,
            'XTP_ORDER_STATUS_UNKNOWN': XTP_ORDER_STATUS_TYPE.XTP_ORDER_STATUS_UNKNOWN
        }

        self.XTP_ORDER_SUBMIT_STATUS_TYPE = {
            'XTP_ORDER_SUBMIT_STATUS_INSERT_SUBMITTED': XTP_ORDER_SUBMIT_STATUS_TYPE.XTP_ORDER_SUBMIT_STATUS_INSERT_SUBMITTED,
            'XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED': XTP_ORDER_SUBMIT_STATUS_TYPE.XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED,
            'XTP_ORDER_SUBMIT_STATUS_INSERT_REJECTED': XTP_ORDER_SUBMIT_STATUS_TYPE.XTP_ORDER_SUBMIT_STATUS_INSERT_REJECTED,
            'XTP_ORDER_SUBMIT_STATUS_CANCEL_SUBMITTED': XTP_ORDER_SUBMIT_STATUS_TYPE.XTP_ORDER_SUBMIT_STATUS_CANCEL_SUBMITTED,
            'XTP_ORDER_SUBMIT_STATUS_CANCEL_REJECTED': XTP_ORDER_SUBMIT_STATUS_TYPE.XTP_ORDER_SUBMIT_STATUS_CANCEL_REJECTED,
            'XTP_ORDER_SUBMIT_STATUS_CANCEL_ACCEPTED': XTP_ORDER_SUBMIT_STATUS_TYPE.XTP_ORDER_SUBMIT_STATUS_CANCEL_ACCEPTED
        }

        self.XTP_TE_RESUME_TYPE = {
            'XTP_TERT_RESTART': XTP_TE_RESUME_TYPE.XTP_TERT_RESTART,
            'XTP_TERT_RESUME': XTP_TE_RESUME_TYPE.XTP_TERT_RESUME,
            'XTP_TERT_QUICK': XTP_TE_RESUME_TYPE.XTP_TERT_QUICK,
        }

        self.ETF_REPLACE_TYPE = {
            'ERT_CASH_FORBIDDEN': ETF_REPLACE_TYPE.ERT_CASH_FORBIDDEN,
            'ERT_CASH_OPTIONAL': ETF_REPLACE_TYPE.ERT_CASH_OPTIONAL,
            'ERT_CASH_MUST': ETF_REPLACE_TYPE.ERT_CASH_MUST,
            'EPT_INVALID': ETF_REPLACE_TYPE.EPT_INVALID,
        }

        self.XTP_TBT_TYPE = {
            'XTP_TBT_ENTRUST': XTP_TBT_TYPE.XTP_TBT_ENTRUST,
            'XTP_TBT_TRADE': XTP_TBT_TYPE.XTP_TBT_TRADE
        }


############################################################################
class XTPQuoteApi(QuoteApi):
    """行情API"""

    #----------------------------------------------------------------------
    def __init__(self, client_id):
        """Constructor"""
        super(XTPQuoteApi, self).__init__()
        self.session_id = 0
        self.subscribeMarketDataHandle = lambda data, error, last: data
        self.unSubscribeMarketDataHandle = lambda data, error, last: data
        self.unSubscribeOrderBookHandle = lambda data, error, last: data
        self.UnSubscribeTickByTickHandle = lambda data, error, last: data
        self.unSubAllOptionMarketDataHandle = lambda exchange_id, data: data
        self.unSubAllTickByTickHandle = lambda exchange_id, data: data
        self.subAllOptionOrderBookHandle = lambda exchange_id, data: data
        self.subAllOptionTickByTickHandle = lambda exchange_id, data: data
        self.marketDataHandle = lambda data: data
        self.depthMarketDataHandle = lambda data: data
        self.queryAllTickersHandle = lambda data, error, last: data
        self.queryTickersPriceInfoHandle = lambda data, error, last: data
        self.subAllMarketDataHandle = lambda exchange_id, data: data
        self.queryAllTickersPriceInfoHandle = lambda data, error, last: data
        self.subAllOrderBookHandle = lambda data : data
        self.subAllTickByTickHandle = lambda data : data
        self.tickByTickHandle = lambda data : data
        self.orderBookHandle = lambda data : data
        self.unSubAllMarketDataHandle = lambda exchange_id, data : data
        self.unSubAllOrderBookHandle = lambda exchange_id, data : data

        self.CreateQuoteApi(client_id, Config.quote.save_file_path, 3)
        self.SetUDPBufferSize(1024)

    
    # ----------------------------------------------------------------------
    def SetUDPBufferSize(self, buffer_size):
        """
        设置采用UDP方式连接时的接收缓冲区大小
        需要在Login之前调用，默认大小和最小设置均为64MB。
        此缓存大小单位为MB，请输入2的次方数，例如128MB请输入128。
        """
        return super(XTPQuoteApi, self).SetUDPBufferSize(buffer_size)

    # ----------------------------------------------------------------------
    def onDisconnected(self, n):
        """掉线通知, 没有自动断线重连, 需要在这里主动调用登录"""
        pass

    # ----------------------------------------------------------------------
    def onError(self, error, n, last):
        """错误通知"""

    # ----------------------------------------------------------------------
    def onSubMarketData(self, data, error, last):
        """订阅合约回报"""
        if self.subMarketDataHandle:
            self.subMarketDataHandle(data, error, last)

    # ----------------------------------------------------------------------
    def onUnSubMarketData(self, data, error, last):
        """退订合约回报"""
        if self.unSubscribeMarketDataHandle:
            self.unSubscribeMarketDataHandle(data, error, last)

    # ----------------------------------------------------------------------
    def onUnSubOrderBook(self, data, error, last):
        """退订合约回报"""
        if self.unSubscribeOrderBookHandle:
            self.unSubscribeOrderBookHandle(data, error, last)

    # ----------------------------------------------------------------------
    def onUnSubTickByTick(self, data, error, last):
        """退订合约回报"""
        if self.UnSubscribeTickByTickHandle:
            self.UnSubscribeTickByTickHandle(data, error, last)


    # ----------------------------------------------------------------------
    def onSubscribeAllMarketData(self, exchange_id, data):
        """订阅合约回报"""
        if self.subAllMarketDataHandle:
            self.subAllMarketDataHandle(exchange_id, data)

    # ----------------------------------------------------------------------
    def onUnSubscribeAllMarketData(self, exchange_id, data):
        """订阅合约回报"""
        if self.unSubAllMarketDataHandle:
            self.unSubAllMarketDataHandle(exchange_id, data)

    # ----------------------------------------------------------------------
    def onUnSubscribeAllOrderBook(self, exchange_id, data):
        """订阅合约回报"""
        if self.unSubAllOrderBookHandle:
            self.unSubAllOrderBookHandle(exchange_id, data)

    # ----------------------------------------------------------------------
    def onTickByTick(self, data):
        if self.tickByTickHandle:
            self.tickByTickHandle(data)
    
    # -----------------------------------------------------------------------
    def onDepthMarketData(self, data):
        if self.depthMarketDataHandle:
            self.depthMarketDataHandle(data)

    # -----------------------------------------------------------------------
    def onOrderBook(self, data):
        if self.orderBookHandle:
            self.orderBookHandle(data)
    
    # ----------------------------------------------------------------------
    def onSubscribeAllOrderBook(self, exchange_id, data):
        if self.subAllOrderBookHandle:
            self.subAllOrderBookHandle(exchange_id, data)

    # ----------------------------------------------------------------------
    def onSubscribeAllOptionMarketData(self, exchange_id, data):
        if self.subAllOptionMarketDataHandle:
            self.subAllOptionMarketDataHandle(exchange_id, data)

    # ----------------------------------------------------------------------
    def onSubscribeAllOptionOrderBook(self, exchange_id, data):
        if self.subAllOptionOrderBookHandle:
            self.subAllOptionOrderBookHandle(exchange_id, data)

    # ----------------------------------------------------------------------
    def onSubscribeAllOptionTickByTick(self, exchange_id, data):
        if self.subAllOptionTickByTickHandle:
            self.subAllOptionTickByTickHandle(exchange_id, data)

    # ----------------------------------------------------------------------
    def onUnSubscribeAllOptionMarketData(self, exchange_id, data):
        if self.unSubAllOptionMarketDataHandle:
            self.unSubAllOptionMarketDataHandle(exchange_id, data)

    # ----------------------------------------------------------------------
    def onUnSubscribeAllOptionOrderBook(self, exchange_id, data):
        if self.unSubAllOptionOrderBookHandle:
            self.unSubAllOptionOrderBookHandle(exchange_id, data)

    # ----------------------------------------------------------------------
    def onUnSubscribeAllOptionTickByTick(self, exchange_id, data):
        if self.unSubAllOptionTickByTickHandle:
            self.unSubAllOptionTickByTickHandle(exchange_id, data)

    # ----------------------------------------------------------------------
    def onSubOrderBook(self, data, error, last):
        if self.subOrderBookHandle:
            self.subOrderBookHandle(data, error, last)
    
    # ----------------------------------------------------------------------
    def onSubscribeAllTickByTick(self, exchange_id, data):
        if self.subAllTickByTickHandle:
            self.subAllTickByTickHandle(exchange_id, data)

    # ----------------------------------------------------------------------
    def onUnSubscribeAllTickByTick(self, exchange_id, data):
        if self.unSubAllTickByTickHandle:
            self.unSubAllTickByTickHandle(exchange_id, data)

    # ----------------------------------------------------------------------
    def onSubTickByTick(self, data, error, last):
        if self.subTickByTickHandle:
            self.subTickByTickHandle(data, error, last)
    
    # ----------------------------------------------------------------------
    def onQueryAllTickers(self, data, error, last):
        """查询合约"""
        if self.queryAllTickersHandle:
            self.queryAllTickersHandle(data, error, last)

    # ----------------------------------------------------------------------
    def onQueryTickersPriceInfo(self, data, error, last):
        """查询合约"""
        if self.queryTickersPriceInfoHandle:
            self.queryTickersPriceInfoHandle(data, error, last)

    # ----------------------------------------------------------------------
    def CreateQuoteApi(self, client_id, save_file_path, log_level):
        """创建api"""
        return super(XTPQuoteApi, self).CreateQuoteApi(client_id, save_file_path, log_level)

    # ----------------------------------------------------------------------
    def GetTradingDay(self):
        """获取当前交易日"""
        return super(XTPQuoteApi, self).GetTradingDay()

    # ----------------------------------------------------------------------
    def GetApiVersion(self):
        """获取API的发行版本号"""
        return super(XTPQuoteApi, self).GetApiVersion()

    # ----------------------------------------------------------------------
    def GetApiLastError(self):
        """获取API的系统错误"""
        return super(XTPQuoteApi, self).GetApiLastError()

    # ----------------------------------------------------------------------
    def Login(self, req=False):
        """登录"""
        if not req:
            req = Config.quote.all()
        if not self.session_id:
            self.session_id = super(XTPQuoteApi, self).Login(req)
        return self.session_id

    # ----------------------------------------------------------------------
    def Logout(self):
        """登出"""
        ret = super(XTPQuoteApi, self).Logout()
        self.session_id = 0
        return ret

    # ----------------------------------------------------------------------
    def SubscribeMarketData(self, req):
        """订阅行情"""
        return super(XTPQuoteApi, self).SubscribeMarketData(req)

    # ----------------------------------------------------------------------
    def SubscribeTickByTick(self, req):
        """订阅行情"""
        return super(XTPQuoteApi, self).SubscribeTickByTick(req)
    
    # ----------------------------------------------------------------------
    def SubscribeAllTickByTick(self, req):
        """订阅行情"""
        return super(XTPQuoteApi, self).SubscribeAllTickByTick(req)
    
    # ----------------------------------------------------------------------
    def UnSubscribeAllTickByTick(self, req):
        """订阅行情"""
        return super(XTPQuoteApi, self).UnSubscribeAllTickByTick(req)
    
    # ----------------------------------------------------------------------
    def UnSubscribeMarketData(self, req):
        """退订"""
        return super(XTPQuoteApi, self).UnSubscribeMarketData(req)

    # ----------------------------------------------------------------------
    def QueryAllTickers(self, req):
        """查询合约"""
        return super(XTPQuoteApi, self).QueryAllTickers(req)

    # ----------------------------------------------------------------------
    def QueryAllTickersPriceInfo(self):
        """查询合约"""
        return super(XTPQuoteApi, self).QueryAllTickersPriceInfo()

    # ----------------------------------------------------------------------
    def QueryTickersPriceInfo(self, req):
        """查询合约"""
        return super(XTPQuoteApi, self).QueryTickersPriceInfo(req)

    # ----------------------------------------------------------------------
    def SubscribeAllMarketData(self, req):
        return super(XTPQuoteApi, self).SubscribeAllMarketData(req)

    # ----------------------------------------------------------------------
    def SubscribeAllOptionMarketData(self, req):
        """订阅全市场的期权行情"""
        print 'SubscribeAllOptionMarketData calling'
        return super(XTPQuoteApi, self).SubscribeAllOptionMarketData(req)

    # ----------------------------------------------------------------------
    def SubscribeAllOptionOrderBook(self, req):
        """订阅全市场的期权行情订单簿"""
        return super(XTPQuoteApi, self).SubscribeAllOptionOrderBook(req)

    # ----------------------------------------------------------------------
    def SubscribeAllOptionTickByTick(self, req):
        """订阅全市场的期权逐笔行情"""
        return super(XTPQuoteApi, self).SubscribeAllOptionTickByTick(req)
   
    # ----------------------------------------------------------------------
    def UnSubscribeAllMarketData(self, req):
        return super(XTPQuoteApi, self).UnSubscribeAllMarketData(req)

    # ----------------------------------------------------------------------
    def UnSubscribeAllOptionMarketData(self, req):
        """退订全市场的期权行情"""
        return super(XTPQuoteApi, self).UnSubscribeAllOptionMarketData(req)

    # ----------------------------------------------------------------------
    def UnSubscribeAllOptionOrderBook(self, req):
        """退订全市场的期权行情订单簿"""
        return super(XTPQuoteApi, self).UnSubscribeAllOptionOrderBook(req)

    # ----------------------------------------------------------------------
    def UnSubscribeAllOptionTickByTick(self, req):
        """退订全市场的期权逐笔行情"""
        return super(XTPQuoteApi, self).UnSubscribeAllOptionTickByTick(req)
   
    # ----------------------------------------------------------------------
    def SubscribeAllOrderBook(self, req):
        return super(XTPQuoteApi, self).SubscribeAllOrderBook(req)

    # ----------------------------------------------------------------------
    def UnSubscribeAllOrderBook(self, req):
        return super(XTPQuoteApi, self).UnSubscribeAllOrderBook(req)

    # ----------------------------------------------------------------------
    def SubscribeOrderBook(self, req):
        return super(XTPQuoteApi, self).SubscribeOrderBook(req)

    # ----------------------------------------------------------------------
    def setSubMarketDataHandle(self, func):
        """设置订阅回调"""
        self.subMarketDataHandle = func

    # ----------------------------------------------------------------------
    def setSubAllMarketDataHandle(self, func):
        """设置订阅回调"""
        self.subAllMarketDataHandle = func

    # ----------------------------------------------------------------------
    def setUnSubMarketDataHandle(self, func):
        """设置退订回调"""
        self.unSubMarketDataHandle = func

    # ----------------------------------------------------------------------
    def setUnSubscribeTickByTickHandle(self, func):
        """设置退订回调"""
        self.UnSubscribeTickByTickHandle = func

    # ----------------------------------------------------------------------
    def setUnSubscribeOrderBookHandle(self, func):
        """设置退订回调"""
        self.UnSubscribeOrderBookHandle = func

    # ----------------------------------------------------------------------
    def setUnSubAllMarketDataHandle(self, func):
        """设置退订回调"""
        self.unSubAllMarketDataHandle = func

    # ----------------------------------------------------------------------
    def setDepthMarketDataHandle(self, func):
        """设置数据回调"""
        self.depthMarketDataHandle = func

    # ----------------------------------------------------------------------
    def setSubAllOrderBookHandle(self, func):
        """设置数据回调"""
        self.subAllOrderBookHandle = func

    # ----------------------------------------------------------------------
    def setUnSubAllOrderBookHandle(self, func):
        """设置数据回调"""
        self.unSubAllOrderBookHandle = func

    # ----------------------------------------------------------------------
    def setSubOrderBookHandle(self, func):
        """设置数据回调"""
        self.subOrderBookHandle = func
    
    # ----------------------------------------------------------------------
    def setOrderBookHandle(self, func):
        """设置数据回调"""
        self.orderBookHandle = func
    
    # ----------------------------------------------------------------------
    def setSubAllTickByTickHandle(self, func):
        """设置数据回调"""
        self.subAllTickByTickHandle = func
    
    # ----------------------------------------------------------------------
    def setSubTickByTickHandle(self, func):
        """设置数据回调"""
        self.subTickByTickHandle = func
    
    # ----------------------------------------------------------------------
    def setTickByTickHandle(self, func):
        """设置数据回调"""
        self.tickByTickHandle = func
    
    # -----------------------------------------------------------------------
    def setQueryAllTickersHandle(self, func):
        """设置查询合约回调"""
        self.queryAllTickersHandle = func

    # ----------------------------------------------------------------------
    def setQueryAllTickersPriceInfoHandle(self, func):
        self.queryTickersPriceInfoHandle = func

    # ----------------------------------------------------------------------
    def setQueryTickersPriceInfoHandle(self, func):
        self.queryTickersPriceInfoHandle = func

    # ----------------------------------------------------------------------
    def setSubAllOptionMarketDataHandle(self, func):
        """设置订阅全市场的期权行情回调"""
        self.subAllOptionMarketDataHandle = func

    # ----------------------------------------------------------------------
    def setSubAllOptionOrderBookHandle(self, func):
        """设置订阅全市场的期权行情订单簿回调"""
        self.subAllOptionOrderBookHandle = func

    # ----------------------------------------------------------------------
    def setSubAllOptionTickByTickHandle(self, func):
        """设置订阅全市场的期权逐笔行情回调"""
        self.subAllOptionTickByTickHandle = func

    # ----------------------------------------------------------------------
    def setUnSubAllOptionMarketDataHandle(self, func):
        """设置退订全市场的期权行情回调"""
        self.unSubAllOptionMarketDataHandle = func

    # ----------------------------------------------------------------------
    def setUnSubAllOptionOrderBookHandle(self, func):
        """设置退订全市场的期权行情订单簿回调"""
        self.unSubAllOptionMarketDataHandle = func

    # ----------------------------------------------------------------------
    def setUnSubAllOptionTickByTickHandle(self, func):
        """设置退订全市场的期权逐笔行情回调"""
        self.unSubAllOptionTickByTickHandle = func


############################################################################
class XTPTradeApi(TradeApi):
    """交易API"""

    # ----------------------------------------------------------------------
    #新股申购同一个账号不同client_id测试时使用
    # def __init__(self,client_id):
    #     """Constructor"""
    #     super(XTPTradeApi, self).__init__()
    #
    #     self.disconnectedHandle = lambda session_id, reason: session_id
    #     self.errorHandle = lambda error: error
    #     self.orderEventHandle = lambda data, error: data
    #     self.tradeEventHandle = lambda data: data
    #     self.cancelOrderErrorHandle = lambda data, error: data
    #     self.queryOrderHandle = lambda data, error, request_id, is_last: data
    #     self.queryTradeHandle = lambda data, error, request_id, is_last: data
    #     self.queryPositionHandle = lambda data, error, request_id, is_last: data
    #     self.queryAssetHandle = lambda data, error, request_id, is_last: data
    #
    #     self.request_id = 0
    #     self.session_id = 0
    #     self.CreateTradeApi(client_id, Config.trade.save_file_path)
    #     self.SetSoftwareKey('b8aa7173bba3470e390d787219b2112e')
    #     self.SetSoftwareVersion('1.0')

    def __init__(self):
        """Constructor"""
        super(XTPTradeApi, self).__init__()

        self.disconnectedHandle = lambda session_id, reason: session_id
        self.errorHandle = lambda error: error
        self.orderEventHandle = lambda data, error: data
        self.tradeEventHandle = lambda data: data
        self.cancelOrderErrorHandle = lambda data, error: data
        self.queryOrderHandle = lambda data, error, request_id, is_last: data
        self.queryTradeHandle = lambda data, error, request_id, is_last: data
        self.queryPositionHandle = lambda data, error, request_id, is_last: data
        self.queryAssetHandle = lambda data, error, request_id, is_last: data
        self.queryETFHandle = lambda data, error, request_id, is_last: data
        self.queryETFBasketHandle = lambda data, error, request_id, is_last: data

        self.request_id = 0
        self.session_id = 0
        self.CreateTradeApi(Config.trade.client_id, Config.trade.save_file_path)
        self.SetSoftwareKey('b8aa7173bba3470e390d787219b2112e')
        self.SetSoftwareVersion('1.0')
        if Config.trade.auto_login:
            self.Login()

    #----------------------------------------------------------------------
    def onDisconnected(self, session_id, reason):
        """掉线通知, 没有自动断线重连, 需要在这里主动调用登录"""
        if self.disconnectedHandle:
            self.disconnectedHandle(session_id, reason)

    #----------------------------------------------------------------------
    def onError(self, error):
        """错误通知"""
        if self.errorHandle:
            self.errorHandle(error)

    #----------------------------------------------------------------------
    def onOrderEvent(self, data, error):
        """报单通知"""
        if self.orderEventHandle:
            self.orderEventHandle(data, error)

    #----------------------------------------------------------------------
    def onTradeEvent(self, data):
        """成交通知"""
        if self.tradeEventHandle:
            self.tradeEventHandle(data)

    #----------------------------------------------------------------------
    def onCancelOrderError(self, data, error):
        """撤单出错响应"""
        if self.cancelOrderErrorHandle:
            self.cancelOrderErrorHandle(data, error)

    #----------------------------------------------------------------------
    def onQueryOrder(self, data, error, request_id, is_last):
        """请求查询报单响应"""
        if self.queryOrderHandle:
            self.queryOrderHandle(data, error, request_id, is_last)

    #----------------------------------------------------------------------
    def onQueryTrade(self, data, error, request_id, is_last):
        """请求查询成交响应"""
        if self.queryTradeHandle:
            self.queryTradeHandle(data, error, request_id, is_last)

    #----------------------------------------------------------------------
    def onQueryPosition(self, data, error, request_id, is_last):
        """请求查询持仓响应"""
        if self.queryPositionHandle:
            self.queryPositionHandle(data, error, request_id, is_last)

    #----------------------------------------------------------------------
    def onQueryAsset(self, data, error, request_id, is_last):
        """请求查询资金响应"""
        if self.queryAssetHandle:
            self.queryAssetHandle(data, error, request_id, is_last)

    # ----------------------------------------------------------------------
    def onQueryETF(self, data, error, request_id, is_last):
        """请求查询ETF清单文件的响应"""
        if self.queryETFHandle:
            self.queryETFHandle(data, error, request_id, is_last)

    # ----------------------------------------------------------------------
    def onQueryETFBasket(self, data, error, request_id, is_last):
        """请求查询ETF股票篮的响应"""
        if self.queryETFBasketHandle:
            self.queryETFBasketHandle(data, error, request_id, is_last)

    # ----------------------------------------------------------------------
    def CreateTradeApi(self, client_id, save_file_path):
        """创建api"""
        return super(XTPTradeApi, self).CreateTradeApi(client_id, save_file_path)

    # ----------------------------------------------------------------------
    def GetTradingDay(self):
        """获取当前交易日"""
        return super(XTPTradeApi, self).GetTradingDay()

    # ----------------------------------------------------------------------
    def GetApiVersion(self):
        """获取API的发行版本号"""
        return super(XTPTradeApi, self).GetApiVersion()

    # ----------------------------------------------------------------------
    def GetApiLastError(self):
        """获取API的系统错误"""
        return super(XTPTradeApi, self).GetApiLastError()

    def Login(self, req=False):
        """登录"""
        if not req:
            req = Config.trade.all()
        if not self.session_id:
            self.session_id = super(XTPTradeApi, self).Login(req)
        return self.session_id

    # ----------------------------------------------------------------------
    def Logout(self):
        """登出"""

        ret = super(XTPTradeApi, self).Logout(self.session_id)
        self.session_id = 0
        return ret

    # ----------------------------------------------------------------------
    def SetSoftwareCode(self, code):
        """设置软件开发代码"""
        super(XTPTradeApi, self).SetSoftwareCode(code)

    # ----------------------------------------------------------------------
    def SetSoftwareVersion(self, version):
        """设置软件开发版本号"""
        super(XTPTradeApi, self).SetSoftwareVersion(version)

    # ----------------------------------------------------------------------
    def GetClientIDByXTPID(self, order_xtp_id):
        """通过报单在xtp系统中的ID获取下单的客户端id"""
        return super(XTPTradeApi, self).GetClientIDByXTPID(order_xtp_id)

    # ----------------------------------------------------------------------
    def GetAccountByXTPID(self, order_xtp_id):
        """通过报单在xtp系统中的ID获取相关资金账户名"""
        return super(XTPTradeApi, self).GetAccountByXTPID(order_xtp_id)

    # ----------------------------------------------------------------------
    def SubscribePublicTopic(self, resume_type):
        """订阅公共流"""
        return super(XTPTradeApi, self).SubscribePublicTopic(resume_type)

    # ----------------------------------------------------------------------
    def InsertOrder(self, order):
        """报单"""
        return super(XTPTradeApi, self).InsertOrder(order, self.session_id)

    # ----------------------------------------------------------------------
    def CancelOrder(self, order_xtp_id):
        """撤单"""
        return super(XTPTradeApi, self).CancelOrder(order_xtp_id, self.session_id)

    # ----------------------------------------------------------------------
    def QueryOrderByXTPID(self, order_xtp_id, request_id=0):
        """根据报单ID请求查询报单"""
        if request_id == 0:
            request_id = self.getRequestId()
        return super(XTPTradeApi, self).QueryOrderByXTPID(order_xtp_id, self.session_id, request_id)

    # ----------------------------------------------------------------------
    def QueryOrders(self, query, request_id=0):
        """请求查询报单"""
        if request_id == 0:
            request_id = self.getRequestId()
        return super(XTPTradeApi, self).QueryOrders(query, self.session_id, request_id)

    # ----------------------------------------------------------------------
    def QueryTradesByXTPID(self, order_xtp_id, request_id=0):
        """根据委托编号请求查询相关成交"""
        if request_id == 0:
            request_id = self.getRequestId()
        return super(XTPTradeApi, self).QueryTradesByXTPID(order_xtp_id, self.session_id, request_id)

    # ----------------------------------------------------------------------
    def QueryTrades(self, query, request_id=0):
        """请求查询已成交"""
        if request_id == 0:
            request_id = self.getRequestId()
        return super(XTPTradeApi, self).QueryTrades(query, self.session_id, request_id)

    # ----------------------------------------------------------------------
    def QueryPosition(self, ticker, request_id=0):
        """请求查询投资者持仓"""
        if request_id == 0:
            request_id = self.getRequestId()
        return super(XTPTradeApi, self).QueryPosition(ticker, self.session_id, request_id)

    # ----------------------------------------------------------------------
    def QueryAsset(self, request_id=0):
        """请求查询资产"""
        if request_id == 0:
            request_id = self.getRequestId()
        return super(XTPTradeApi, self).QueryAsset(0, request_id)

    # -----------------------------------------------------------------------
    def QueryETF(self, query, request_id=0):
        """"请求查询ETF清单文件"""
        if request_id == 0:
            request_id = self.getRequestId()
        # return pretty_data(super(XTPTradeApi, self).QueryETF(query, self.session_id, request_id))
        return super(XTPTradeApi, self).QueryETF(query, self.session_id, request_id)

    # -----------------------------------------------------------------------
    def QueryETFTickerBasket(self, query, request_id=0):
        """请求查询ETF股票篮"""
        if request_id == 0:
            request_id = self.getRequestId()
        # return pretty_data(super(XTPTradeApi, self).QueryETFBasket(query, self.session_id, request_id))
        return super(XTPTradeApi, self).QueryETFTickerBasket(query, self.session_id, request_id)

    # ----------------------------------------------------------------------
    def QueryOrderByXTPIDSync(self, order_xtp_id, request_id=0):
        """根据报单ID请求查询报单"""
        if request_id == 0:
            request_id = self.getRequestId()
        return pretty_data(super(XTPTradeApi, self).QueryOrderByXTPIDSync(order_xtp_id, self.session_id, request_id))

    # ----------------------------------------------------------------------
    def QueryOrdersSync(self, query, request_id=0):
        """请求查询报单"""
        if request_id == 0:
            request_id = self.getRequestId()
        return pretty_data(super(XTPTradeApi, self).QueryOrdersSync(query, self.session_id, request_id))

    # ----------------------------------------------------------------------
    def QueryTradesByXTPIDSync(self, order_xtp_id, request_id=0):
        """根据委托编号请求查询相关成交"""
        if request_id == 0:
            request_id = self.getRequestId()
        return pretty_data(super(XTPTradeApi, self).QueryTradesByXTPIDSync(order_xtp_id, self.session_id, request_id))

    # ----------------------------------------------------------------------
    def QueryTradesSync(self, query, request_id=0):
        """请求查询已成交"""
        if request_id == 0:
            request_id = self.getRequestId()
        return pretty_data(super(XTPTradeApi, self).QueryTradesSync(query, self.session_id, request_id))

    # ----------------------------------------------------------------------
    def QueryPositionSync(self, ticker, request_id=0):
        """请求查询投资者持仓"""
        if request_id == 0:
            request_id = self.getRequestId()
        # 18版本期权
        # return pretty_data_list(super(XTPTradeApi, self).QueryPositionSync(ticker, self.session_id, request_id))
        # 18版本除期权
        return pretty_data(super(XTPTradeApi, self).QueryPositionSync(ticker, self.session_id, request_id))

    # ----------------------------------------------------------------------
    def QueryPositionListSync(self, ticker, request_id=0):
        """请求查询投资者持仓"""
        if request_id == 0:
            request_id = self.getRequestId()
        # 18版本期权
        return pretty_data_list(super(XTPTradeApi, self).QueryPositionSync(ticker, self.session_id, request_id))

    # ----------------------------------------------------------------------
    def QueryPositionsSync(self, request_id=0):
        """请求查询投资者所有持仓"""
        if request_id == 0:
            request_id = self.getRequestId()
        ticker = {'ticker': ''}

        return pretty_data(self.QueryPositionSync(ticker, request_id))

    # ----------------------------------------------------------------------
    def QueryAssetSync(self, request_id=0):
        if request_id == 0:
            request_id = self.getRequestId()
        return pretty_data(super(XTPTradeApi, self).QueryAssetSync(0, request_id))

    # -----------------------------------------------------------------------
    def QueryETFSync(self, query, request_id=0):
        """请求查询ETF清单文件"""
        if request_id == 0:
            request_id = self.getRequestId()
        return pretty_data(
            super(XTPTradeApi, self).QueryETFSync(query, self.session_id, request_id))

    # -----------------------------------------------------------------------
    def QueryETFBasketSync(self, query, request_id=0):
        """请求查询ETF股票篮"""
        if request_id == 0:
            request_id = self.getRequestId()
        return pretty_data(
            super(XTPTradeApi, self).QueryETFBasketSync(query, self.session_id, request_id))

    # ----------------------------------------------------------------------
    def setDisconnectedHandle(self, func):
        """掉线通知调"""

    # ----------------------------------------------------------------------
    def setErrorHandle(self, func):
        """错误通知回调"""
        self.errorHandle = func

    # ----------------------------------------------------------------------
    def setOrderEventHandle(self, func):
        """报单通知回调"""
        self.orderEventHandle = func

    # ----------------------------------------------------------------------
    def setTradeEventHandle(self, func):
        """成交通知回调"""
        self.tradeEventHandle = func

    # ----------------------------------------------------------------------
    def setCancelOrderErrorHandle(self, func):
        """撤单出错响应回调"""
        self.cancelOrderErrorHandle = func

    # ----------------------------------------------------------------------
    def setQueryOrderHandle(self, func):
        """请求查询报单响应回调"""
        self.queryOrderHandle = func

    # ----------------------------------------------------------------------
    def setQueryTradeHandle(self, func):
        """请求查询成交响应回调"""
        self.queryTradeHandle = func

    # ----------------------------------------------------------------------
    def setQueryPositionHandle(self, func):
        """请求查询持仓响应回调"""
        self.queryPositionHandle = func

    # ----------------------------------------------------------------------
    def setQueryAssetHandle(self, func):
        """请求查询资金响应回调"""
        self.queryAssetHandle = func

    # ----------------------------------------------------------------------
    def setQueryETFHandle(self, func):
        """"""
        self.queryETFHandle = func

    # ----------------------------------------------------------------------
    def setQueryETFBasketHandle(self, func):
        """"""
        self.queryETFBasketHandle = func

    # ----------------------------------------------------------------------
    def getRequestId(self):
        """新的request id"""
        self.request_id += 1
        return self.request_id


############################################################################
class Api(object):
    # 枚举定义
    const = XTPConst()
    # 行情
    # quote = XTPQuoteApi(129)
    # # 交易
    trade = XTPTradeApi()


    # --------------------------------------------------
    def __init__(self):
        """Constructor"""
        raise NotImplementedError()
