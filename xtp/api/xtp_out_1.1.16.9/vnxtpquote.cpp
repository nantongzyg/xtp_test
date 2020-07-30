
// QuoteApi.cpp : 定义 DLL 应用程序的导出函数。
//

#ifdef WIN32
#include "stdafx.h"
#endif
#include "vnxtpquote.h"



///-------------------------------------------------------------------------------------
///从Python对象到C++类型转换用的函数
///-------------------------------------------------------------------------------------

void getInt(dict d, string key, int *value) {
    if (d.has_key(key)) {      //检查字典中是否存在该键值
        object o = d[key];    //获取该键值
        extract<int> x(o);    //创建提取器
        if (x.check()) {      //如果可以提取
            *value = x();    //对目标整数指针赋值
        }
    }
};

void getDouble(dict d, string key, double *value) {
    if (d.has_key(key)) {
        object o = d[key];
        extract<double> x(o);
        if (x.check()) {
            *value = x();
        }
    }
};

void getChar(dict d, string key, char *value) {
    if (d.has_key(key)) {
        object o = d[key];
        extract<string> x(o);
        if (x.check()) {
            string s = x();
            const char *buffer = s.c_str();
            //对字符串指针赋值必须使用strcpy_s, vs2013使用strcpy编译通不过
            //+1应该是因为C++字符串的结尾符号？不是特别确定，不加这个1会出错
#ifdef WIN32
            strcpy_s(value, strlen(buffer) + 1, buffer);
#else
            strncpy(value, buffer, strlen(buffer) + 1);
#endif
        }
    }
};


//-------------------------------------------------------------------------------------
//C++的回调函数将数据保存到队列中
//-------------------------------------------------------------------------------------

void xtpQuoteApi::OnDisconnected(int nReason) {
    Task task = Task();
    task.task_name = ONDISCONNECTED;
    task.task_id = nReason;
    this->task_queue.push(task);
};

void xtpQuoteApi::OnError(XTPRI *error_info) {
    Task task = Task();
    task.task_name = ONERROR;
    task.task_error = *error_info;
    task.task_id = 0;
    task.task_last = 1;
    this->task_queue.push(task);
};

namespace {
    struct DepthData {
        int64_t bid1_qty[100];
        int32_t bid1_count;
        int32_t max_bid1_count;
        int64_t ask1_qty[100];
        int32_t ask1_count;
        int32_t max_ask1_count;
    };
}

void xtpQuoteApi::OnDepthMarketData(XTPMD *market_data, int64_t bid1_qty[], int32_t bid1_count, int32_t max_bid1_count, int64_t ask1_qty[], int32_t ask1_count, int32_t max_ask1_count) {
    //printf("OnDepthMarketData\n");
    Task task = Task();
    task.task_name = ONDEPTHMARKETDATA;
    task.task_data = *market_data;

    DepthData depth_data;
    depth_data.bid1_count = bid1_count;
    depth_data.max_bid1_count = max_bid1_count;
    depth_data.ask1_count = ask1_count;
    depth_data.max_ask1_count = max_ask1_count;
    int32_t count = bid1_count > 100 ? 100 : bid1_count;
    for (int i = 0; i < count ; ++i)
        depth_data.bid1_qty[i] = bid1_qty[i];
    count = ask1_count > 100 ? 100 : ask1_count;
    for (int i = 0; i < count ; ++i)
        depth_data.ask1_qty[i] = ask1_qty[i];
    task.task_error = depth_data;
    this->task_queue.push(task);
}

void xtpQuoteApi::OnSubMarketData(XTPST * ticker, XTPRI * error_info, bool is_last) {

    Task task = Task();
    task.task_name = ONSUBMARKETDATA;

    if (ticker) {
        task.task_data = *ticker;
    } else {
        XTPST empty_data = XTPST();
        memset(&empty_data, 0, sizeof(empty_data));
        task.task_data = empty_data;
    }

    if (error_info) {
        task.task_error = *error_info;
    } else {
        XTPRI empty_error = XTPRI();
        memset(&empty_error, 0, sizeof(empty_error));
        task.task_error = empty_error;
    }
    
    task.task_id = 0;
    task.task_last = is_last;
    this->task_queue.push(task);
}


void xtpQuoteApi::OnUnSubMarketData(XTPST * ticker, XTPRI * error_info, bool is_last) {

    Task task = Task();
    task.task_name = ONUNSUBMARKETDATA;

    if (ticker) {
        task.task_data = *ticker;
    } else {
        XTPST empty_data = XTPST();
        memset(&empty_data, 0, sizeof(empty_data));
        task.task_data = empty_data;
    }

    if (error_info) {
        task.task_error = *error_info;
    } else {
        XTPRI empty_error = XTPRI();
        memset(&empty_error, 0, sizeof(empty_error));
        task.task_error = empty_error;
    }
    
    task.task_id = 0;
    task.task_last = is_last;
    this->task_queue.push(task);
}


void xtpQuoteApi::OnSubOrderBook(XTPST * ticker, XTPRI * error_info, bool is_last) {

    Task task = Task();
    task.task_name = ONSUBORDERBOOK;

    if (ticker) {
        task.task_data = *ticker;
    } else {
        XTPST empty_data = XTPST();
        memset(&empty_data, 0, sizeof(empty_data));
        task.task_data = empty_data;
    }

    if (error_info) {
        task.task_error = *error_info;
    } else {
        XTPRI empty_error = XTPRI();
        memset(&empty_error, 0, sizeof(empty_error));
        task.task_error = empty_error;
    }
    
    task.task_id = 0;
    task.task_last = is_last;
    this->task_queue.push(task);
}


void xtpQuoteApi::OnUnSubOrderBook(XTPST * ticker, XTPRI * error_info, bool is_last) {

    Task task = Task();
    task.task_name = ONUNSUBORDERBOOK;

    if (ticker) {
        task.task_data = *ticker;
    } else {
        XTPST empty_data = XTPST();
        memset(&empty_data, 0, sizeof(empty_data));
        task.task_data = empty_data;
    }

    if (error_info) {
        task.task_error = *error_info;
    } else {
        XTPRI empty_error = XTPRI();
        memset(&empty_error, 0, sizeof(empty_error));
        task.task_error = empty_error;
    }
    
    task.task_id = 0;
    task.task_last = is_last;
    this->task_queue.push(task);
}


void xtpQuoteApi::OnOrderBook(XTPOB * order_book) {

    Task task = Task();
    task.task_name = ONORDERBOOK;

    if (order_book) {
        task.task_data = *order_book;
    } else {
        XTPOB empty_data = XTPOB();
        memset(&empty_data, 0, sizeof(empty_data));
        task.task_data = empty_data;
    }

    XTPRI empty_error = XTPRI();
    memset(&empty_error, 0, sizeof(empty_error));
    task.task_error = empty_error;

    task.task_id = 0;
    task.task_last = true;
    this->task_queue.push(task);
}


void xtpQuoteApi::OnSubTickByTick(XTPST * ticker, XTPRI * error_info, bool is_last) {

    Task task = Task();
    task.task_name = ONSUBTICKBYTICK;

    if (ticker) {
        task.task_data = *ticker;
    } else {
        XTPST empty_data = XTPST();
        memset(&empty_data, 0, sizeof(empty_data));
        task.task_data = empty_data;
    }

    if (error_info) {
        task.task_error = *error_info;
    } else {
        XTPRI empty_error = XTPRI();
        memset(&empty_error, 0, sizeof(empty_error));
        task.task_error = empty_error;
    }
    
    task.task_id = 0;
    task.task_last = is_last;
    this->task_queue.push(task);
}


void xtpQuoteApi::OnUnSubTickByTick(XTPST * ticker, XTPRI * error_info, bool is_last) {

    Task task = Task();
    task.task_name = ONUNSUBTICKBYTICK;

    if (ticker) {
        task.task_data = *ticker;
    } else {
        XTPST empty_data = XTPST();
        memset(&empty_data, 0, sizeof(empty_data));
        task.task_data = empty_data;
    }

    if (error_info) {
        task.task_error = *error_info;
    } else {
        XTPRI empty_error = XTPRI();
        memset(&empty_error, 0, sizeof(empty_error));
        task.task_error = empty_error;
    }
    
    task.task_id = 0;
    task.task_last = is_last;
    this->task_queue.push(task);
}


void xtpQuoteApi::OnTickByTick(XTPTBT * tbt_data) {

    Task task = Task();
    task.task_name = ONTICKBYTICK;

    if (tbt_data) {
        task.task_data = *tbt_data;
    } else {
        XTPTBT empty_data = XTPTBT();
        memset(&empty_data, 0, sizeof(empty_data));
        task.task_data = empty_data;
    }

    XTPRI empty_error = XTPRI();
    memset(&empty_error, 0, sizeof(empty_error));
    task.task_error = empty_error;

    task.task_id = 0;
    task.task_last = true;
    this->task_queue.push(task);
}


void xtpQuoteApi::OnSubscribeAllMarketData(XTPRI * error_info) {

    Task task = Task();
    task.task_name = ONSUBSCRIBEALLMARKETDATA;

    if (error_info) {
        task.task_error = *error_info;
    } else {
        XTPRI empty_error = XTPRI();
        memset(&empty_error, 0, sizeof(empty_error));
        task.task_error = empty_error;
    }
    
    task.task_id = 0;
    task.task_last = true;
    this->task_queue.push(task);
}


void xtpQuoteApi::OnUnSubscribeAllMarketData(XTPRI * error_info) {

    Task task = Task();
    task.task_name = ONUNSUBSCRIBEALLMARKETDATA;

    if (error_info) {
        task.task_error = *error_info;
    } else {
        XTPRI empty_error = XTPRI();
        memset(&empty_error, 0, sizeof(empty_error));
        task.task_error = empty_error;
    }
    
    task.task_id = 0;
    task.task_last = true;
    this->task_queue.push(task);
}


void xtpQuoteApi::OnSubscribeAllOrderBook(XTPRI * error_info) {

    Task task = Task();
    task.task_name = ONSUBSCRIBEALLORDERBOOK;

    if (error_info) {
        task.task_error = *error_info;
    } else {
        XTPRI empty_error = XTPRI();
        memset(&empty_error, 0, sizeof(empty_error));
        task.task_error = empty_error;
    }
    
    task.task_id = 0;
    task.task_last = true;
    this->task_queue.push(task);
}


void xtpQuoteApi::OnUnSubscribeAllOrderBook(XTPRI * error_info) {

    Task task = Task();
    task.task_name = ONUNSUBSCRIBEALLORDERBOOK;

    if (error_info) {
        task.task_error = *error_info;
    } else {
        XTPRI empty_error = XTPRI();
        memset(&empty_error, 0, sizeof(empty_error));
        task.task_error = empty_error;
    }
    
    task.task_id = 0;
    task.task_last = true;
    this->task_queue.push(task);
}


void xtpQuoteApi::OnSubscribeAllTickByTick(XTPRI * error_info) {

    Task task = Task();
    task.task_name = ONSUBSCRIBEALLTICKBYTICK;

    if (error_info) {
        task.task_error = *error_info;
    } else {
        XTPRI empty_error = XTPRI();
        memset(&empty_error, 0, sizeof(empty_error));
        task.task_error = empty_error;
    }
    
    task.task_id = 0;
    task.task_last = true;
    this->task_queue.push(task);
}


void xtpQuoteApi::OnUnSubscribeAllTickByTick(XTPRI * error_info) {

    Task task = Task();
    task.task_name = ONUNSUBSCRIBEALLTICKBYTICK;

    if (error_info) {
        task.task_error = *error_info;
    } else {
        XTPRI empty_error = XTPRI();
        memset(&empty_error, 0, sizeof(empty_error));
        task.task_error = empty_error;
    }
    
    task.task_id = 0;
    task.task_last = true;
    this->task_queue.push(task);
}


void xtpQuoteApi::OnQueryAllTickers(XTPQSI * ticker_info, XTPRI * error_info, bool is_last) {

    boost::mutex::scoped_lock lock(QueryAllTickers_mutex_);

    if (QueryAllTickers_sync_ > 0 ) {
        dict data;

        if (ticker_info) {

            data["exchange_id"] = ticker_info->exchange_id;
            data["ticker"] = ticker_info->ticker;
            data["ticker_name"] = ticker_info->ticker_name;
            data["ticker_type"] = ticker_info->ticker_type;
            data["pre_close_price"] = ticker_info->pre_close_price;
            data["upper_limit_price"] = ticker_info->upper_limit_price;
            data["lower_limit_price"] = ticker_info->lower_limit_price;
            data["price_tick"] = ticker_info->price_tick;
            data["buy_qty_unit"] = ticker_info->buy_qty_unit;
            data["sell_qty_unit"] = ticker_info->sell_qty_unit;
        }

        dict error;
        error["error_msg"] = error_info->error_msg;
        error["error_id"] = error_info->error_id;

        QueryAllTickers_data_["ticker_info"] = data;
        QueryAllTickers_data_["error_info"] = error;

        QueryAllTickers_data_["is_last"] = is_last;

        QueryAllTickers_sync_ = false;
        QueryAllTickers_cond_var_.notify_all();
        return;
    }

    Task task = Task();
    task.task_name = ONQUERYALLTICKERS;

    if (ticker_info) {
        task.task_data = *ticker_info;
    } else {
        XTPQSI empty_data = XTPQSI();
        memset(&empty_data, 0, sizeof(empty_data));
        task.task_data = empty_data;
    }

    if (error_info) {
        task.task_error = *error_info;
    } else {
        XTPRI empty_error = XTPRI();
        memset(&empty_error, 0, sizeof(empty_error));
        task.task_error = empty_error;
    }
    
    task.task_id = 0;
    task.task_last = is_last;
    this->task_queue.push(task);
}


void xtpQuoteApi::OnQueryTickersPriceInfo(XTPTPI * ticker_info, XTPRI * error_info, bool is_last) {

    boost::mutex::scoped_lock lock(QueryTickersPriceInfo_mutex_);

    if (QueryTickersPriceInfo_sync_ > 0 ) {
        dict data;

        if (ticker_info) {

            data["exchange_id"] = ticker_info->exchange_id;
            data["ticker"] = ticker_info->ticker;
            data["last_price"] = ticker_info->last_price;
        }

        dict error;
        error["error_msg"] = error_info->error_msg;
        error["error_id"] = error_info->error_id;

        QueryTickersPriceInfo_data_["ticker_info"] = data;
        QueryTickersPriceInfo_data_["error_info"] = error;

        QueryTickersPriceInfo_data_["is_last"] = is_last;

        QueryTickersPriceInfo_sync_ = false;
        QueryTickersPriceInfo_cond_var_.notify_all();
        return;
    }

    Task task = Task();
    task.task_name = ONQUERYTICKERSPRICEINFO;

    if (ticker_info) {
        task.task_data = *ticker_info;
    } else {
        XTPTPI empty_data = XTPTPI();
        memset(&empty_data, 0, sizeof(empty_data));
        task.task_data = empty_data;
    }

    if (error_info) {
        task.task_error = *error_info;
    } else {
        XTPRI empty_error = XTPRI();
        memset(&empty_error, 0, sizeof(empty_error));
        task.task_error = empty_error;
    }
    
    task.task_id = 0;
    task.task_last = is_last;
    this->task_queue.push(task);
}


//-------------------------------------------------------------------------------------
//工作线程从队列中取出数据，转化为python对象后，进行推送
//-------------------------------------------------------------------------------------

void xtpQuoteApi::processTask()
{
    while (running)
    {
        Task task = this->task_queue.wait_and_pop();

        switch (task.task_name)
        {

            case ONDISCONNECTED: {
                this->processDisconnected(task);
                break;
            }

            case ONERROR: {
                this->processError(task);
                break;
            }

            case ONSUBMARKETDATA: {
                this->processSubMarketData(task);
                break;
            }

            case ONUNSUBMARKETDATA: {
                this->processUnSubMarketData(task);
                break;
            }

            case ONDEPTHMARKETDATA: {
                this->processDepthMarketData(task);
                break;
            }

            case ONSUBORDERBOOK: {
                this->processSubOrderBook(task);
                break;
            }

            case ONUNSUBORDERBOOK: {
                this->processUnSubOrderBook(task);
                break;
            }

            case ONORDERBOOK: {
                this->processOrderBook(task);
                break;
            }

            case ONSUBTICKBYTICK: {
                this->processSubTickByTick(task);
                break;
            }

            case ONUNSUBTICKBYTICK: {
                this->processUnSubTickByTick(task);
                break;
            }

            case ONTICKBYTICK: {
                this->processTickByTick(task);
                break;
            }

            case ONSUBSCRIBEALLMARKETDATA: {
                this->processSubscribeAllMarketData(task);
                break;
            }

            case ONUNSUBSCRIBEALLMARKETDATA: {
                this->processUnSubscribeAllMarketData(task);
                break;
            }

            case ONSUBSCRIBEALLORDERBOOK: {
                this->processSubscribeAllOrderBook(task);
                break;
            }

            case ONUNSUBSCRIBEALLORDERBOOK: {
                this->processUnSubscribeAllOrderBook(task);
                break;
            }

            case ONSUBSCRIBEALLTICKBYTICK: {
                this->processSubscribeAllTickByTick(task);
                break;
            }

            case ONUNSUBSCRIBEALLTICKBYTICK: {
                this->processUnSubscribeAllTickByTick(task);
                break;
            }

            case ONQUERYALLTICKERS: {
                this->processQueryAllTickers(task);
                break;
            }

            case ONQUERYTICKERSPRICEINFO: {
                this->processQueryTickersPriceInfo(task);
                break;
            }

            default:
                break;
        }
    }
}


void xtpQuoteApi::processDisconnected(Task task)
{
    PyLock lock;
    this->onDisconnected(task.task_id);
};

void xtpQuoteApi::processError(Task task)
{
    PyLock lock;
    XTPRI task_error = any_cast<XTPRspInfoStruct>(task.task_error);
    dict error;
    error["error_msg"] = task_error.error_msg;
    error["error_id"] = task_error.error_id;

    this->onError(error, task.task_id, task.task_last);
};

void xtpQuoteApi::processTickByTick(Task task) {
    PyLock lock;
    XTPTBT task_data = any_cast<XTPTBT>(task.task_data);
    dict data;

    ///交易所代码
    data["exchange_id"] = task_data.exchange_id;
    ///合约代码（不包含交易所信息），不带空格，以'\0'结尾
    data["ticker"] = task_data.ticker;
    ///预留
    data["seq"] = task_data.seq;
    ///委托时间 or 成交时间
    data["data_time"] = task_data.data_time;
    ///委托 or 成交
    data["type"] = task_data.type;

    if (task_data.type == XTP_TBT_ENTRUST) {
        ///频道代码
        data["channel_no"] = task_data.entrust.channel_no;
        ///委托序号(在同一个channel_no内唯一，从1开始连续)
        data["seq"] = task_data.entrust.seq;
        ///委托价格
        data["price"] = task_data.entrust.price;
        ///委托数量
        data["qty"] = task_data.entrust.qty;
        ///'1':买; '2':卖; 'G':借入; 'F':出借
        data["side"] = task_data.entrust.side;
        ///订单类别: '1': 市价; '2': 限价; '3': 本方最优
        data["ord_type"] = task_data.entrust.ord_type;
    } else {
        ///频道代码
        data["channel_no"] = task_data.trade.channel_no;
        ///委托序号(在同一个channel_no内唯一，从1开始连续)
        data["seq"] = task_data.trade.seq;
        ///成交价格
        data["price"] = task_data.trade.price;
        ///成交量
        data["qty"] = task_data.trade.qty;
        ///成交金额(仅适用上交所)
        data["money"] = task_data.trade.money;
        ///买方订单号
        data["bid_no"] = task_data.trade.bid_no;
        ///卖方订单号
        data["ask_no"] = task_data.trade.ask_no;
        /// SH: 内外盘标识('B':主动买; 'S':主动卖; 'N':未知)
        /// SZ: 成交标识('4':撤; 'F':成交)
        data["trade_flag"] = task_data.trade.trade_flag;
    }

    this->onTickByTick(data);
}

void xtpQuoteApi::processDepthMarketData(Task task) {
    PyLock lock;
    XTPMD task_data = any_cast<XTPMD>(task.task_data);
    DepthData depth_data = any_cast<DepthData>(task.task_error);
    dict data;

    data["exchange_id"] = task_data.exchange_id;
    data["ticker"] = task_data.ticker;
    data["last_price"] = task_data.last_price;
    data["pre_close_price"] = task_data.pre_close_price;
    data["open_price"] = task_data.open_price;
    data["high_price"] = task_data.high_price;
    data["low_price"] = task_data.low_price;
    data["close_price"] = task_data.close_price;
    data["pre_open_interest"] = task_data.pre_open_interest;
    data["open_interest"] = task_data.open_interest;
    data["pre_settlement_price"] = task_data.pre_settlement_price;
    data["settlement_price"] = task_data.settlement_price;
    data["upper_limit_price"] = task_data.upper_limit_price;
    data["lower_limit_price"] = task_data.lower_limit_price;
    data["pre_delta"] = task_data.pre_delta;
    data["curr_delta"] = task_data.curr_delta;
    data["data_time"] = task_data.data_time;
    data["qty"] = task_data.qty;
    data["turnover"] = task_data.turnover;
    data["avg_price"] = task_data.avg_price;
    data["trades_count"] = task_data.trades_count;
    data["ticker_status"] = task_data.ticker_status;
    data["total_bid_qty"] = task_data.total_bid_qty;
    data["total_ask_qty"] = task_data.total_ask_qty;
    data["ma_bid_price"] = task_data.ma_bid_price;
    data["ma_ask_price"] = task_data.ma_ask_price;
    data["ma_bond_bid_price"] = task_data.ma_bond_bid_price;
    data["ma_bond_ask_price"] = task_data.ma_bond_ask_price;
    data["yield_to_maturity"] = task_data.yield_to_maturity;
    data["iopv"] = task_data.iopv;
    data["etf_buy_count"] = task_data.etf_buy_count;
    data["etf_sell_count"] = task_data.etf_sell_count;
    data["etf_buy_qty"] = task_data.etf_buy_qty;
    data["etf_buy_money"] = task_data.etf_buy_money;
    data["etf_sell_qty"] = task_data.etf_sell_qty;
    data["etf_sell_money"] = task_data.etf_sell_money;
    data["total_warrant_exec_qty"] = task_data.total_warrant_exec_qty;
    data["warrant_lower_price"] = task_data.warrant_lower_price;
    data["warrant_upper_price"] = task_data.warrant_upper_price;
    data["cancel_buy_count"] = task_data.cancel_buy_count;
    data["cancel_sell_count"] = task_data.cancel_sell_count;
    data["cancel_buy_qty"] = task_data.cancel_buy_qty;
    data["cancel_sell_qty"] = task_data.cancel_sell_qty;
    data["cancel_buy_money"] = task_data.cancel_buy_money;
    data["cancel_sell_money"] = task_data.cancel_sell_money;
    data["total_buy_count"] = task_data.total_buy_count;
    data["total_sell_count"] = task_data.total_sell_count;
    data["duration_after_buy"] = task_data.duration_after_buy;
    data["duration_after_sell"] = task_data.duration_after_sell;
    data["num_bid_orders"] = task_data.num_bid_orders;
    data["num_ask_orders"] = task_data.num_ask_orders;
    data["exec_time"] = task_data.exec_time;
    data["is_market_closed"] = task_data.is_market_closed;
    data["total_position"] = task_data.total_position;
    data["pe_ratio1"] = task_data.pe_ratio1;
    data["pe_ratio2"] = task_data.pe_ratio2;
    data["bid1"] = task_data.bid[0];
    data["bid2"] = task_data.bid[1];
    data["bid3"] = task_data.bid[2];
    data["bid4"] = task_data.bid[3];
    data["bid5"] = task_data.bid[4];
    data["bid6"] = task_data.bid[5];
    data["bid7"] = task_data.bid[6];
    data["bid8"] = task_data.bid[7];
    data["bid9"] = task_data.bid[8];
    data["bid10"] = task_data.bid[9];
    data["ask1"] = task_data.ask[0];
    data["ask2"] = task_data.ask[1];
    data["ask3"] = task_data.ask[2];
    data["ask4"] = task_data.ask[3];
    data["ask5"] = task_data.ask[4];
    data["ask6"] = task_data.ask[5];
    data["ask7"] = task_data.ask[6];
    data["ask8"] = task_data.ask[7];
    data["ask9"] = task_data.ask[8];
    data["ask10"] = task_data.ask[9];
    data["bid_qty1"] = task_data.bid_qty[0];
    data["bid_qty2"] = task_data.bid_qty[1];
    data["bid_qty3"] = task_data.bid_qty[2];
    data["bid_qty4"] = task_data.bid_qty[3];
    data["bid_qty5"] = task_data.bid_qty[4];
    data["bid_qty6"] = task_data.bid_qty[5];
    data["bid_qty7"] = task_data.bid_qty[6];
    data["bid_qty8"] = task_data.bid_qty[7];
    data["bid_qty9"] = task_data.bid_qty[8];
    data["bid_qty10"] = task_data.bid_qty[9];
    data["ask_qty1"] = task_data.ask_qty[0];
    data["ask_qty2"] = task_data.ask_qty[1];
    data["ask_qty3"] = task_data.ask_qty[2];
    data["ask_qty4"] = task_data.ask_qty[3];
    data["ask_qty5"] = task_data.ask_qty[4];
    data["ask_qty6"] = task_data.ask_qty[5];
    data["ask_qty7"] = task_data.ask_qty[6];
    data["ask_qty8"] = task_data.ask_qty[7];
    data["ask_qty9"] = task_data.ask_qty[8];
    data["ask_qty10"] = task_data.ask_qty[9];
    data["bid1_count"] = depth_data.bid1_count;
    data["max_bid1_count"] = depth_data.max_bid1_count;
    boost::python::list bid1_qty_list;
    int count = depth_data.bid1_count < 100 ? depth_data.bid1_count : 100;
    for (int i = 0; i < count; ++i)
        bid1_qty_list.append(depth_data.bid1_qty[i]);
    data["bid1_qty_list"] = bid1_qty_list;

    data["ask1_count"] = depth_data.ask1_count;
    data["max_ask1_count"] = depth_data.max_ask1_count;
    boost::python::list ask1_qty_list;
    count = depth_data.ask1_count < 100 ? depth_data.ask1_count : 100;
    for (int i = 0; i < count; ++i)
        ask1_qty_list.append(depth_data.ask1_qty[i]);
    data["ask1_qty_list"] = ask1_qty_list;

    this->onDepthMarketData(data);
}

void xtpQuoteApi::processSubMarketData(Task task) {
    PyLock lock;

    XTPST task_data = any_cast<XTPST>(task.task_data);
    dict data;

    data["exchange_id"] = task_data.exchange_id;
    data["ticker"] = task_data.ticker;

    XTPRI task_error = any_cast<XTPRI>(task.task_error);
    dict error;
    error["error_msg"] = task_error.error_msg;
    error["error_id"] = task_error.error_id;

    this->onSubMarketData(data, error, task.task_last);
}

void xtpQuoteApi::processUnSubMarketData(Task task) {
    PyLock lock;

    XTPST task_data = any_cast<XTPST>(task.task_data);
    dict data;

    data["exchange_id"] = task_data.exchange_id;
    data["ticker"] = task_data.ticker;

    XTPRI task_error = any_cast<XTPRI>(task.task_error);
    dict error;
    error["error_msg"] = task_error.error_msg;
    error["error_id"] = task_error.error_id;

    this->onUnSubMarketData(data, error, task.task_last);
}

void xtpQuoteApi::processSubOrderBook(Task task) {
    PyLock lock;

    XTPST task_data = any_cast<XTPST>(task.task_data);
    dict data;

    data["exchange_id"] = task_data.exchange_id;
    data["ticker"] = task_data.ticker;

    XTPRI task_error = any_cast<XTPRI>(task.task_error);
    dict error;
    error["error_msg"] = task_error.error_msg;
    error["error_id"] = task_error.error_id;

    this->onSubOrderBook(data, error, task.task_last);
}

void xtpQuoteApi::processUnSubOrderBook(Task task) {
    PyLock lock;

    XTPST task_data = any_cast<XTPST>(task.task_data);
    dict data;

    data["exchange_id"] = task_data.exchange_id;
    data["ticker"] = task_data.ticker;

    XTPRI task_error = any_cast<XTPRI>(task.task_error);
    dict error;
    error["error_msg"] = task_error.error_msg;
    error["error_id"] = task_error.error_id;

    this->onUnSubOrderBook(data, error, task.task_last);
}

void xtpQuoteApi::processOrderBook(Task task) {
    PyLock lock;

    XTPOB task_data = any_cast<XTPOB>(task.task_data);
    dict data;

    data["exchange_id"] = task_data.exchange_id;
    data["ticker"] = task_data.ticker;
    data["last_price"] = task_data.last_price;
    data["qty"] = task_data.qty;
    data["turnover"] = task_data.turnover;
    data["trades_count"] = task_data.trades_count;
    data["data_time"] = task_data.data_time;
    data["bid1"] = task_data.bid[0];
    data["bid2"] = task_data.bid[1];
    data["bid3"] = task_data.bid[2];
    data["bid4"] = task_data.bid[3];
    data["bid5"] = task_data.bid[4];
    data["bid6"] = task_data.bid[5];
    data["bid7"] = task_data.bid[6];
    data["bid8"] = task_data.bid[7];
    data["bid9"] = task_data.bid[8];
    data["bid10"] = task_data.bid[9];
    data["ask1"] = task_data.ask[0];
    data["ask2"] = task_data.ask[1];
    data["ask3"] = task_data.ask[2];
    data["ask4"] = task_data.ask[3];
    data["ask5"] = task_data.ask[4];
    data["ask6"] = task_data.ask[5];
    data["ask7"] = task_data.ask[6];
    data["ask8"] = task_data.ask[7];
    data["ask9"] = task_data.ask[8];
    data["ask10"] = task_data.ask[9];
    data["bid_qty1"] = task_data.bid_qty[0];
    data["bid_qty2"] = task_data.bid_qty[1];
    data["bid_qty3"] = task_data.bid_qty[2];
    data["bid_qty4"] = task_data.bid_qty[3];
    data["bid_qty5"] = task_data.bid_qty[4];
    data["bid_qty6"] = task_data.bid_qty[5];
    data["bid_qty7"] = task_data.bid_qty[6];
    data["bid_qty8"] = task_data.bid_qty[7];
    data["bid_qty9"] = task_data.bid_qty[8];
    data["bid_qty10"] = task_data.bid_qty[9];
    data["ask_qty1"] = task_data.ask_qty[0];
    data["ask_qty2"] = task_data.ask_qty[1];
    data["ask_qty3"] = task_data.ask_qty[2];
    data["ask_qty4"] = task_data.ask_qty[3];
    data["ask_qty5"] = task_data.ask_qty[4];
    data["ask_qty6"] = task_data.ask_qty[5];
    data["ask_qty7"] = task_data.ask_qty[6];
    data["ask_qty8"] = task_data.ask_qty[7];
    data["ask_qty9"] = task_data.ask_qty[8];
    data["ask_qty10"] = task_data.ask_qty[9];
    this->onOrderBook(data);
}

void xtpQuoteApi::processSubTickByTick(Task task) {
    PyLock lock;

    XTPST task_data = any_cast<XTPST>(task.task_data);
    dict data;

    data["exchange_id"] = task_data.exchange_id;
    data["ticker"] = task_data.ticker;

    XTPRI task_error = any_cast<XTPRI>(task.task_error);
    dict error;
    error["error_msg"] = task_error.error_msg;
    error["error_id"] = task_error.error_id;

    this->onSubTickByTick(data, error, task.task_last);
}

void xtpQuoteApi::processUnSubTickByTick(Task task) {
    PyLock lock;

    XTPST task_data = any_cast<XTPST>(task.task_data);
    dict data;

    data["exchange_id"] = task_data.exchange_id;
    data["ticker"] = task_data.ticker;

    XTPRI task_error = any_cast<XTPRI>(task.task_error);
    dict error;
    error["error_msg"] = task_error.error_msg;
    error["error_id"] = task_error.error_id;

    this->onUnSubTickByTick(data, error, task.task_last);
}

void xtpQuoteApi::processSubscribeAllMarketData(Task task) {
    PyLock lock;


    XTPRI task_error = any_cast<XTPRI>(task.task_error);
    dict error;
    error["error_msg"] = task_error.error_msg;
    error["error_id"] = task_error.error_id;

    this->onSubscribeAllMarketData(error);
}

void xtpQuoteApi::processUnSubscribeAllMarketData(Task task) {
    PyLock lock;


    XTPRI task_error = any_cast<XTPRI>(task.task_error);
    dict error;
    error["error_msg"] = task_error.error_msg;
    error["error_id"] = task_error.error_id;

    this->onUnSubscribeAllMarketData(error);
}

void xtpQuoteApi::processSubscribeAllOrderBook(Task task) {
    PyLock lock;


    XTPRI task_error = any_cast<XTPRI>(task.task_error);
    dict error;
    error["error_msg"] = task_error.error_msg;
    error["error_id"] = task_error.error_id;

    this->onSubscribeAllOrderBook(error);
}

void xtpQuoteApi::processUnSubscribeAllOrderBook(Task task) {
    PyLock lock;


    XTPRI task_error = any_cast<XTPRI>(task.task_error);
    dict error;
    error["error_msg"] = task_error.error_msg;
    error["error_id"] = task_error.error_id;

    this->onUnSubscribeAllOrderBook(error);
}

void xtpQuoteApi::processSubscribeAllTickByTick(Task task) {
    PyLock lock;


    XTPRI task_error = any_cast<XTPRI>(task.task_error);
    dict error;
    error["error_msg"] = task_error.error_msg;
    error["error_id"] = task_error.error_id;

    this->onSubscribeAllTickByTick(error);
}

void xtpQuoteApi::processUnSubscribeAllTickByTick(Task task) {
    PyLock lock;


    XTPRI task_error = any_cast<XTPRI>(task.task_error);
    dict error;
    error["error_msg"] = task_error.error_msg;
    error["error_id"] = task_error.error_id;

    this->onUnSubscribeAllTickByTick(error);
}

void xtpQuoteApi::processQueryAllTickers(Task task) {
    PyLock lock;

    XTPQSI task_data = any_cast<XTPQSI>(task.task_data);
    dict data;

    data["exchange_id"] = task_data.exchange_id;
    data["ticker"] = task_data.ticker;
    data["ticker_name"] = task_data.ticker_name;
    data["ticker_type"] = task_data.ticker_type;
    data["pre_close_price"] = task_data.pre_close_price;
    data["upper_limit_price"] = task_data.upper_limit_price;
    data["lower_limit_price"] = task_data.lower_limit_price;
    data["price_tick"] = task_data.price_tick;
    data["buy_qty_unit"] = task_data.buy_qty_unit;
    data["sell_qty_unit"] = task_data.sell_qty_unit;

    XTPRI task_error = any_cast<XTPRI>(task.task_error);
    dict error;
    error["error_msg"] = task_error.error_msg;
    error["error_id"] = task_error.error_id;

    this->onQueryAllTickers(data, error, task.task_last);
}

void xtpQuoteApi::processQueryTickersPriceInfo(Task task) {
    PyLock lock;

    XTPTPI task_data = any_cast<XTPTPI>(task.task_data);
    dict data;

    data["exchange_id"] = task_data.exchange_id;
    data["ticker"] = task_data.ticker;
    data["last_price"] = task_data.last_price;

    XTPRI task_error = any_cast<XTPRI>(task.task_error);
    dict error;
    error["error_msg"] = task_error.error_msg;
    error["error_id"] = task_error.error_id;

    this->onQueryTickersPriceInfo(data, error, task.task_last);
}

//-------------------------------------------------------------------------------------
//req:主动函数的实现
//-------------------------------------------------------------------------------------

void xtpQuoteApi::Release() {
    running = false;

    if (this->api) {
        this->api->Release();
        this->api = NULL;
    }
};

void xtpQuoteApi::CreateQuoteApi(int client_id, string save_file_path, int log_level) {
    this->api = XTP::API::QuoteApi::CreateQuoteApi(client_id, save_file_path.c_str(), (XTP_LOG_LEVEL)log_level);
    if(!this->api) {
        cout<<"api init fault.\n"<<endl;
        return;
    }
    this->api->RegisterSpi(this);
}

int xtpQuoteApi::Exit() {
//    this->api->RegisterSpi(NULL);
    this->Release();

    return 1;
};

string xtpQuoteApi::GetTradingDay() {
    return this->api->GetTradingDay();
}

string xtpQuoteApi::GetApiVersion() {
    return this->api->GetApiVersion();
}

dict xtpQuoteApi::GetApiLastError() {
    XTPRI *_error = this->api->GetApiLastError();
    dict error;
    error["error_msg"] = _error->error_msg;
    error["error_id"] = _error->error_id;

    return error;
}

void xtpQuoteApi::SetUDPBufferSize(uint32_t buff_size) {
    this->api->SetUDPBufferSize(buff_size);
}

int xtpQuoteApi::Login(dict req)
{

    char ip[256];
    int port;
    char user[256];
    char password[256];
    int sock_type;

    getChar(req, "ip", ip);
    getInt(req, "port", &port);
    getChar(req, "user", user);
    getChar(req, "password", password);
    getInt(req, "sock_type", &sock_type);

    printf("try login tcp[%s:%d]\n", ip, port);
    int i = this->api->Login(ip, port, user, password, (XTP_PROTOCOL_TYPE)sock_type);
    return i;
};

int xtpQuoteApi::Logout()
{
    int i = this->api->Logout();
    return i;
};


/*********************************************
//以下为自动生成的函数
*********************************************/

int xtpQuoteApi::SubscribeMarketData(dict req) {

    char ticker[256];
    getChar(req, "ticker", ticker);
    char* myreq[1] = { ticker };

    int exchange_id;
    getInt(req, "exchange_id", &exchange_id);

    return this->api->SubscribeMarketData(myreq, 1, (XTP_EXCHANGE_TYPE) exchange_id);
}

int xtpQuoteApi::UnSubscribeMarketData(dict req) {

    char ticker[256];
    getChar(req, "ticker", ticker);
    char* myreq[1] = { ticker };

    int exchange_id;
    getInt(req, "exchange_id", &exchange_id);

    return this->api->UnSubscribeMarketData(myreq, 1, (XTP_EXCHANGE_TYPE) exchange_id);
}

int xtpQuoteApi::SubscribeOrderBook(dict req) {

    char ticker[256];
    getChar(req, "ticker", ticker);
    char* myreq[1] = { ticker };

    int exchange_id;
    getInt(req, "exchange_id", &exchange_id);

    return this->api->SubscribeOrderBook(myreq, 1, (XTP_EXCHANGE_TYPE) exchange_id);
}

int xtpQuoteApi::UnSubscribeOrderBook(dict req) {

    char ticker[256];
    getChar(req, "ticker", ticker);
    char* myreq[1] = { ticker };

    int exchange_id;
    getInt(req, "exchange_id", &exchange_id);

    return this->api->UnSubscribeOrderBook(myreq, 1, (XTP_EXCHANGE_TYPE) exchange_id);
}

int xtpQuoteApi::SubscribeTickByTick(dict req) {

    char ticker[256];
    getChar(req, "ticker", ticker);
    char* myreq[1] = { ticker };

    int exchange_id;
    getInt(req, "exchange_id", &exchange_id);

    return this->api->SubscribeTickByTick(myreq, 1, (XTP_EXCHANGE_TYPE) exchange_id);
}

int xtpQuoteApi::UnSubscribeTickByTick(dict req) {

    char ticker[256];
    getChar(req, "ticker", ticker);
    char* myreq[1] = { ticker };

    int exchange_id;
    getInt(req, "exchange_id", &exchange_id);

    return this->api->UnSubscribeTickByTick(myreq, 1, (XTP_EXCHANGE_TYPE) exchange_id);
}

int xtpQuoteApi::SubscribeAllMarketData() {

    return this->api->SubscribeAllMarketData();
}

int xtpQuoteApi::UnSubscribeAllMarketData() {

    return this->api->UnSubscribeAllMarketData();
}

int xtpQuoteApi::SubscribeAllOrderBook() {

    return this->api->SubscribeAllOrderBook();
}

int xtpQuoteApi::UnSubscribeAllOrderBook() {

    return this->api->UnSubscribeAllOrderBook();
}

int xtpQuoteApi::SubscribeAllTickByTick() {

    return this->api->SubscribeAllTickByTick();
}

int xtpQuoteApi::UnSubscribeAllTickByTick() {

    return this->api->UnSubscribeAllTickByTick();
}

int xtpQuoteApi::QueryAllTickers(dict req) {

    int exchange_id;
    getInt(req, "exchange_id", &exchange_id);

    return this->api->QueryAllTickers((XTP_EXCHANGE_TYPE) exchange_id);
}

int xtpQuoteApi::QueryTickersPriceInfo(dict req) {

    char ticker[256];
    getChar(req, "ticker", ticker);
    char* myreq[1] = { ticker };

    int exchange_id;
    getInt(req, "exchange_id", &exchange_id);

    return this->api->QueryTickersPriceInfo(myreq, 1, (XTP_EXCHANGE_TYPE) exchange_id);
}

int xtpQuoteApi::QueryAllTickersPriceInfo() {

    return this->api->QueryAllTickersPriceInfo();
}

//-------------------------------------------------------------------------------------
//同步测试接口
//-------------------------------------------------------------------------------------

dict xtpQuoteApi::QueryAllTickersSync(dict req) {
    boost::mutex::scoped_lock lock(QueryAllTickers_mutex_);

    int exchange_id;
    getInt(req, "exchange_id", &exchange_id);

    QueryAllTickers_data_ = dict();
    QueryAllTickers_sync_ = true;
    int result = this->api->QueryAllTickers((XTP_EXCHANGE_TYPE) exchange_id);

    if (QueryAllTickers_cond_var_.timed_wait(lock, boost::get_system_time() + boost::posix_time::seconds(30))) {
        return QueryAllTickers_data_;
    } else { //time out
        return QueryAllTickers_data_;
    }
}

dict xtpQuoteApi::QueryTickersPriceInfoSync(dict req) {
    boost::mutex::scoped_lock lock(QueryTickersPriceInfo_mutex_);

    char ticker[256];
    getChar(req, "ticker", ticker);
    char* myreq[1] = { ticker };

    int exchange_id;
    getInt(req, "exchange_id", &exchange_id);

    QueryTickersPriceInfo_data_ = dict();
    QueryTickersPriceInfo_sync_ = true;
    int result = this->api->QueryTickersPriceInfo(myreq, 1, (XTP_EXCHANGE_TYPE) exchange_id);

    if (QueryTickersPriceInfo_cond_var_.timed_wait(lock, boost::get_system_time() + boost::posix_time::seconds(30))) {
        return QueryTickersPriceInfo_data_;
    } else { //time out
        return QueryTickersPriceInfo_data_;
    }
}

dict xtpQuoteApi::QueryAllTickersPriceInfoSync() {
    boost::mutex::scoped_lock lock(QueryAllTickersPriceInfo_mutex_);

    QueryAllTickersPriceInfo_data_ = dict();
    QueryAllTickersPriceInfo_sync_ = true;
    int result = this->api->QueryAllTickersPriceInfo();

    if (QueryAllTickersPriceInfo_cond_var_.timed_wait(lock, boost::get_system_time() + boost::posix_time::seconds(30))) {
        return QueryAllTickersPriceInfo_data_;
    } else { //time out
        return QueryAllTickersPriceInfo_data_;
    }
}

//-------------------------------------------------------------------------------------
//Boost.Python封装
//-------------------------------------------------------------------------------------

struct QuoteApiWrap : xtpQuoteApi, wrapper < xtpQuoteApi > {
    virtual void onDisconnected(int i) {
        try {
            this->get_override("onDisconnected")(i);
        } catch (error_already_set const &) {
            PyErr_Print();
        }
    };

    virtual void onError(dict data, int id, bool last) {
        try {
            this->get_override("onError")(data, id, last);
        } catch (error_already_set const &) {
            PyErr_Print();
        }
    };

    virtual void onSubMarketData(dict data, dict error, bool last) {
        PyLock lock;

        try {
            this->get_override("onSubMarketData")(data, error, last);
        } catch (error_already_set const &) {
            PyErr_Print();
        }
    };
    
    virtual void onUnSubMarketData(dict data, dict error, bool last) {
        PyLock lock;

        try {
            this->get_override("onUnSubMarketData")(data, error, last);
        } catch (error_already_set const &) {
            PyErr_Print();
        }
    };
    
    virtual void onDepthMarketData(dict data) {
        PyLock lock;

        try {
            this->get_override("onDepthMarketData")(data);
        } catch (error_already_set const &) {
            PyErr_Print();
        }
    };
    
    virtual void onSubOrderBook(dict data, dict error, bool last) {
        PyLock lock;

        try {
            this->get_override("onSubOrderBook")(data, error, last);
        } catch (error_already_set const &) {
            PyErr_Print();
        }
    };
    
    virtual void onUnSubOrderBook(dict data, dict error, bool last) {
        PyLock lock;

        try {
            this->get_override("onUnSubOrderBook")(data, error, last);
        } catch (error_already_set const &) {
            PyErr_Print();
        }
    };
    
    virtual void onOrderBook(dict data) {
        PyLock lock;

        try {
            this->get_override("onOrderBook")(data);
        } catch (error_already_set const &) {
            PyErr_Print();
        }
    };
    
    virtual void onSubTickByTick(dict data, dict error, bool last) {
        PyLock lock;

        try {
            this->get_override("onSubTickByTick")(data, error, last);
        } catch (error_already_set const &) {
            PyErr_Print();
        }
    };
    
    virtual void onUnSubTickByTick(dict data, dict error, bool last) {
        PyLock lock;

        try {
            this->get_override("onUnSubTickByTick")(data, error, last);
        } catch (error_already_set const &) {
            PyErr_Print();
        }
    };
    
    virtual void onTickByTick(dict data) {
        PyLock lock;

        try {
            this->get_override("onTickByTick")(data);
        } catch (error_already_set const &) {
            PyErr_Print();
        }
    };
    
    virtual void onSubscribeAllMarketData(dict error) {
        PyLock lock;

        try {
            this->get_override("onSubscribeAllMarketData")(error);
        } catch (error_already_set const &) {
            PyErr_Print();
        }
    };
    
    virtual void onUnSubscribeAllMarketData(dict error) {
        PyLock lock;

        try {
            this->get_override("onUnSubscribeAllMarketData")(error);
        } catch (error_already_set const &) {
            PyErr_Print();
        }
    };
    
    virtual void onSubscribeAllOrderBook(dict error) {
        PyLock lock;

        try {
            this->get_override("onSubscribeAllOrderBook")(error);
        } catch (error_already_set const &) {
            PyErr_Print();
        }
    };
    
    virtual void onUnSubscribeAllOrderBook(dict error) {
        PyLock lock;

        try {
            this->get_override("onUnSubscribeAllOrderBook")(error);
        } catch (error_already_set const &) {
            PyErr_Print();
        }
    };
    
    virtual void onSubscribeAllTickByTick(dict error) {
        PyLock lock;

        try {
            this->get_override("onSubscribeAllTickByTick")(error);
        } catch (error_already_set const &) {
            PyErr_Print();
        }
    };
    
    virtual void onUnSubscribeAllTickByTick(dict error) {
        PyLock lock;

        try {
            this->get_override("onUnSubscribeAllTickByTick")(error);
        } catch (error_already_set const &) {
            PyErr_Print();
        }
    };
    
    virtual void onQueryAllTickers(dict data, dict error, bool last) {
        PyLock lock;

        try {
            this->get_override("onQueryAllTickers")(data, error, last);
        } catch (error_already_set const &) {
            PyErr_Print();
        }
    };
    
    virtual void onQueryTickersPriceInfo(dict data, dict error, bool last) {
        PyLock lock;

        try {
            this->get_override("onQueryTickersPriceInfo")(data, error, last);
        } catch (error_already_set const &) {
            PyErr_Print();
        }
    };
    
};


BOOST_PYTHON_MODULE(vnxtpquote) {
    PyEval_InitThreads();

    class_<QuoteApiWrap, boost::noncopyable>("QuoteApi")

        .def("onDisconnected", &QuoteApiWrap::onDisconnected)
        .def("onError", &QuoteApiWrap::onError)
        .def("onSubMarketData", &QuoteApiWrap::onSubMarketData)
        .def("onUnSubMarketData", &QuoteApiWrap::onUnSubMarketData)
        .def("onDepthMarketData", &QuoteApiWrap::onDepthMarketData)
        .def("onSubOrderBook", &QuoteApiWrap::onSubOrderBook)
        .def("onUnSubOrderBook", &QuoteApiWrap::onUnSubOrderBook)
        .def("onOrderBook", &QuoteApiWrap::onOrderBook)
        .def("onSubTickByTick", &QuoteApiWrap::onSubTickByTick)
        .def("onUnSubTickByTick", &QuoteApiWrap::onUnSubTickByTick)
        .def("onTickByTick", &QuoteApiWrap::onTickByTick)
        .def("onSubscribeAllMarketData", &QuoteApiWrap::onSubscribeAllMarketData)
        .def("onUnSubscribeAllMarketData", &QuoteApiWrap::onUnSubscribeAllMarketData)
        .def("onSubscribeAllOrderBook", &QuoteApiWrap::onSubscribeAllOrderBook)
        .def("onUnSubscribeAllOrderBook", &QuoteApiWrap::onUnSubscribeAllOrderBook)
        .def("onSubscribeAllTickByTick", &QuoteApiWrap::onSubscribeAllTickByTick)
        .def("onUnSubscribeAllTickByTick", &QuoteApiWrap::onUnSubscribeAllTickByTick)
        .def("onQueryAllTickers", &QuoteApiWrap::onQueryAllTickers)
        .def("onQueryTickersPriceInfo", &QuoteApiWrap::onQueryTickersPriceInfo)
        .def("CreateQuoteApi", &QuoteApiWrap::CreateQuoteApi)
        .def("Release", &QuoteApiWrap::Release)
        .def("Exit", &QuoteApiWrap::Exit)
        .def("GetTradingDay", &QuoteApiWrap::GetTradingDay)
        .def("GetApiVersion", &QuoteApiWrap::GetApiVersion)
        .def("GetApiLastError", &QuoteApiWrap::GetApiLastError)
        .def("SetUDPBufferSize", &QuoteApiWrap::SetUDPBufferSize)
        .def("Login", &QuoteApiWrap::Login)
        .def("Logout", &QuoteApiWrap::Logout)
        .def("SubscribeMarketData", &QuoteApiWrap::SubscribeMarketData)
        .def("UnSubscribeMarketData", &QuoteApiWrap::UnSubscribeMarketData)
        .def("SubscribeOrderBook", &QuoteApiWrap::SubscribeOrderBook)
        .def("UnSubscribeOrderBook", &QuoteApiWrap::UnSubscribeOrderBook)
        .def("SubscribeTickByTick", &QuoteApiWrap::SubscribeTickByTick)
        .def("UnSubscribeTickByTick", &QuoteApiWrap::UnSubscribeTickByTick)
        .def("SubscribeAllMarketData", &QuoteApiWrap::SubscribeAllMarketData)
        .def("UnSubscribeAllMarketData", &QuoteApiWrap::UnSubscribeAllMarketData)
        .def("SubscribeAllOrderBook", &QuoteApiWrap::SubscribeAllOrderBook)
        .def("UnSubscribeAllOrderBook", &QuoteApiWrap::UnSubscribeAllOrderBook)
        .def("SubscribeAllTickByTick", &QuoteApiWrap::SubscribeAllTickByTick)
        .def("UnSubscribeAllTickByTick", &QuoteApiWrap::UnSubscribeAllTickByTick)
        .def("QueryAllTickers", &QuoteApiWrap::QueryAllTickers)
        .def("QueryTickersPriceInfo", &QuoteApiWrap::QueryTickersPriceInfo)
        .def("QueryAllTickersPriceInfo", &QuoteApiWrap::QueryAllTickersPriceInfo)
        .def("QueryAllTickersSync", &QuoteApiWrap::QueryAllTickersSync)
        .def("QueryTickersPriceInfoSync", &QuoteApiWrap::QueryTickersPriceInfoSync)
        .def("QueryAllTickersPriceInfoSync", &QuoteApiWrap::QueryAllTickersPriceInfoSync)
    ;
};
