
// MdApi.cpp : 定义 DLL 应用程序的导出函数。
//
/*
#ifdef WIN32
#include <stdafx.h>
#endif
*/
#include <string>
#include "./vnxtptrade.h"


template<typename T>
T identity_(T x) {
    return x;
}

///-------------------------------------------------------------
/// 从Python对象到C++类型转换用的函数
///-------------------------------------------------------------

template<typename T>
void getValue(dict d, string key, T *value) {
    if (d.has_key(key)) {        //检查字典中是否存在该键值
        object o = d[key];    //获取该键值
        extract<T> x(o);    //创建提取器
        if (x.check()) {        //如果可以提取
            *value = x();    //对目标整数指针赋值
        }
    }
}

void getChar(dict d, string key, char *value) {
    if (d.has_key(key)) {
        object o = d[key];
        extract<string> x(o);
        if (x.check()) {
            string s = x();
            const char *buffer = s.c_str();
#ifdef WIN32
            strcpy_s(value, strlen(buffer) + 1, buffer);
#else
            strncpy(value, buffer, strlen(buffer) + 1);
#endif
        }
    }
}


//-------------------------------------------------------------------------------------
//C++的回调函数将数据保存到队列中
//-------------------------------------------------------------------------------------

void xtpTradeApi::OnDisconnected(uint64_t session_id, int reason) {
    Task task = Task();
    task.task_name = ONDISCONNECTED;
    task.task_session_id = session_id;
    task.task_id = reason;
    this->task_queue.push(task);
}

void xtpTradeApi::OnError(XTPRI * error_info) {

    Task task = Task();
    task.task_name = ONERROR;

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


void xtpTradeApi::OnOrderEvent(XTPOrderInfo * order_info, XTPRI * error_info, uint64_t session_id) {

    Task task = Task();
    task.task_name = ONORDEREVENT;

    if (order_info) {
        task.task_data = *order_info;
    } else {
        XTPOrderInfo empty_data = XTPOrderInfo();
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
    task.task_last = true;
    this->task_queue.push(task);
}


void xtpTradeApi::OnTradeEvent(XTPTradeReport * trade_info, uint64_t session_id) {

    Task task = Task();
    task.task_name = ONTRADEEVENT;

    if (trade_info) {
        task.task_data = *trade_info;
    } else {
        XTPTradeReport empty_data = XTPTradeReport();
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


void xtpTradeApi::OnCancelOrderError(XTPOrderCancelInfo * cancel_info, XTPRI * error_info, uint64_t session_id) {

    Task task = Task();
    task.task_name = ONCANCELORDERERROR;

    if (cancel_info) {
        task.task_data = *cancel_info;
    } else {
        XTPOrderCancelInfo empty_data = XTPOrderCancelInfo();
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
    task.task_last = true;
    this->task_queue.push(task);
}


void xtpTradeApi::OnQueryOrder(XTPQueryOrderRsp *order_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) {
    boost::mutex::scoped_lock lock1(QueryOrderByXTPID_mutex_);
    boost::mutex::scoped_lock lock2(QueryOrders_mutex_);
    // std::cout << __PRETTY_FUNCTION__ << " request_id=" << request_id << " is_last=" << is_last  << std::endl;

    if (QueryOrders_sync_ > 0 && (QueryOrders_sync_ == request_id)) {
        dict data;
        dict odr;

        if (order_info) {

            data["order_xtp_id"] = order_info->order_xtp_id;
            data["order_client_id"] = order_info->order_client_id;
            data["order_cancel_client_id"] = order_info->order_cancel_client_id;
            data["order_cancel_xtp_id"] = order_info->order_cancel_xtp_id;
            data["ticker"] = order_info->ticker;
            data["market"] = order_info->market;
            data["price"] = order_info->price;
            data["quantity"] = order_info->quantity;
            data["price_type"] = order_info->price_type;
            data["side"] = order_info->side;
            data["business_type"] = order_info->business_type;
            data["qty_traded"] = order_info->qty_traded;
            data["qty_left"] = order_info->qty_left;
            data["insert_time"] = order_info->insert_time;
            data["update_time"] = order_info->update_time;
            data["cancel_time"] = order_info->cancel_time;
            data["trade_amount"] = order_info->trade_amount;
            data["order_local_id"] = order_info->order_local_id;
            data["order_status"] = order_info->order_status;
            data["order_submit_status"] = order_info->order_submit_status;
            data["order_type"] = order_info->order_type;

            odr["order_info"] = data;
        } else {
            odr["order_info"] = NULL;
        }

        dict error;
        error["error_msg"] = error_info->error_msg;
        error["error_id"] = error_info->error_id;
        odr["error_info"] = error;

        if (!QueryOrderByXTPID_data_.has_key("order_info")) {
            QueryOrderByXTPID_data_["order_info"] =  dict();
        }
        if (!QueryOrders_data_.has_key("order_info")) {
            QueryOrders_data_["order_info"] =  dict();
        }

        if (QueryOrderByXTPID_sync_ > 0 ) {
            QueryOrderByXTPID_data_["order_info"][boost::python::len(QueryOrderByXTPID_data_["order_info"])] = odr;
            QueryOrderByXTPID_data_["request_id"] = request_id;
            QueryOrderByXTPID_data_["is_last"] = is_last;
            if (is_last) {
                QueryOrderByXTPID_sync_ = 0;
                QueryOrderByXTPID_cond_var_.notify_all();
            }
        }
        if (QueryOrders_sync_ > 0) {
            QueryOrders_data_["order_info"][boost::python::len(QueryOrders_data_["order_info"])] = odr;
            QueryOrders_data_["request_id"] = request_id;
            QueryOrders_data_["is_last"] = is_last;
            if (is_last) {
                QueryOrders_sync_ = 0;
                QueryOrders_cond_var_.notify_all();
            }
        }
        return;
    }

    Task task = Task();
    task.task_name = ONQUERYORDER;
    if (order_info) {
        task.task_data = *order_info;
    } else {
        XTPQueryOrderRsp empty_data = XTPQueryOrderRsp();
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
    task.task_id = (uint64_t) request_id;
    task.task_last = is_last;
    this->task_queue.push(task);
}

void xtpTradeApi::OnQueryTrade(XTPQueryTradeRsp *trade_info, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) {
    boost::mutex::scoped_lock lock1(QueryTradesByXTPID_mutex_);
    boost::mutex::scoped_lock lock2(QueryTrades_mutex_);

//    std::cout << __PRETTY_FUNCTION__ << " request_id=" << request_id << " is_last=" << is_last << std::endl;
//    std::cout << "error_info=" << error_info->error_id << ", QueryTradesByXTPID_sync_=" << QueryTradesByXTPID_sync_ << ", QueryTrades_sync_=" << QueryTrades_sync_ << std::endl;

    if ( request_id > 0 && (QueryTradesByXTPID_sync_> 0 || QueryTrades_sync_> 0) ) {

        dict data;
        dict trd;

        if (trade_info) {

            data["order_xtp_id"] = trade_info->order_xtp_id;
            data["order_client_id"] = trade_info->order_client_id;
            data["ticker"] = trade_info->ticker;
            data["market"] = trade_info->market;
            data["local_order_id"] = trade_info->local_order_id;
            data["exec_id"] = trade_info->exec_id;
            data["price"] = trade_info->price;
            data["quantity"] = trade_info->quantity;
            data["trade_time"] = trade_info->trade_time;
            data["trade_amount"] = trade_info->trade_amount;
            data["report_index"] = trade_info->report_index;
            data["order_exch_id"] = trade_info->order_exch_id;
            data["trade_type"] = trade_info->trade_type;
            data["side"] = trade_info->side;
            data["business_type"] = trade_info->business_type;
            data["branch_pbu"] = trade_info->branch_pbu;
            trd["trade_info"] = data;
        } else {

            trd["trade_info"] = NULL;
        }

        dict error;
        error["error_msg"] = error_info->error_msg;
        error["error_id"] = error_info->error_id;
        trd["error_info"] = error;

        if (!QueryTradesByXTPID_data_.has_key("trade_info")) {
            QueryTradesByXTPID_data_["trade_info"] =  dict();
        }
        if (!QueryTrades_data_.has_key("trade_info")) {
            QueryTrades_data_["trade_info"] =  dict();
        }

        if (QueryTradesByXTPID_sync_ > 0) {
            QueryTradesByXTPID_data_["trade_info"][boost::python::len(QueryTradesByXTPID_data_["trade_info"])] = trd;

            QueryTradesByXTPID_data_["request_id"] = request_id;

            QueryTradesByXTPID_data_["is_last"] = is_last;
            if (is_last) {
                QueryTradesByXTPID_sync_ = 0;
                QueryTradesByXTPID_cond_var_.notify_all();
            }
        }

        if (QueryTrades_sync_ > 0) {
            QueryTrades_data_["trade_info"][boost::python::len(QueryTrades_data_["trade_info"])] = trd;
            QueryTrades_data_["request_id"] = request_id;
            QueryTrades_data_["is_last"] = is_last;

            if (is_last) {
                QueryTrades_sync_ = 0;
                QueryTrades_cond_var_.notify_all();
            }
        }

        return;
    }

    Task task = Task();
    task.task_name = ONQUERYTRADE;

    if (trade_info) {
        task.task_data = *trade_info;
    } else {
        XTPQueryTradeRsp empty_data = XTPQueryTradeRsp();
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
    task.task_id = (uint64_t) request_id;
    task.task_last = is_last;

    this->task_queue.push(task);
}

void xtpTradeApi::OnQueryPosition(XTPQueryStkPositionRsp *position, XTPRI *error_info, int request_id, bool is_last, uint64_t session_id) {
    boost::mutex::scoped_lock lock(QueryPosition_mutex_);
        // std::cout << __PRETTY_FUNCTION__ << " request_id=" << request_id << std::endl;

    if (QueryPosition_sync_ > 0) {
        dict data;
        if (position) {

            data["ticker"] = position->ticker;
            data["ticker_name"] = position->ticker_name;
            data["market"] = position->market;
            data["total_qty"] = position->total_qty;
            data["sellable_qty"] = position->sellable_qty;
            data["avg_price"] = position->avg_price;
            data["unrealized_pnl"] = position->unrealized_pnl;
            data["yesterday_position"] = position->yesterday_position;
            data["purchase_redeemable_qty"] = position->purchase_redeemable_qty;
            //data["unknown"] = position->unknown;
        }

        dict error;
        error["error_msg"] = error_info->error_msg;
        error["error_id"] = error_info->error_id;

        dict pos;
        pos["position"] = data;
        pos["error_info"] = error;

        if (!QueryPosition_data_.has_key("position")) {
            QueryPosition_data_["position"] =  dict();
        }

        QueryPosition_data_["position"][boost::python::len(QueryPosition_data_["position"])] = pos;
        QueryPosition_data_["request_id"] = request_id;
        QueryPosition_data_["is_last"] = is_last;

        if (is_last) {
            QueryPosition_sync_ = 0;
            QueryPosition_cond_var_.notify_all();
        }
        return;
    }

    Task task = Task();
    task.task_name = ONQUERYPOSITION;

    if (position) {
        task.task_data = *position;
    } else {
        XTPQueryStkPositionRsp empty_data = XTPQueryStkPositionRsp();
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
    task.task_id = (uint64_t) request_id;
    task.task_last = true;
    this->task_queue.push(task);
}

void xtpTradeApi::OnQueryAsset(XTPQueryAssetRsp * asset, XTPRI * error_info, int request_id, bool is_last, uint64_t session_id) {

    boost::mutex::scoped_lock lock(QueryAsset_mutex_);

    if (QueryAsset_sync_ > 0 ) {
        dict data;

        if (asset) {

            data["total_asset"] = asset->total_asset;
            data["buying_power"] = asset->buying_power;
            data["security_asset"] = asset->security_asset;
            data["fund_buy_amount"] = asset->fund_buy_amount;
            data["fund_buy_fee"] = asset->fund_buy_fee;
            data["fund_sell_amount"] = asset->fund_sell_amount;
            data["fund_sell_fee"] = asset->fund_sell_fee;
            data["withholding_amount"] = asset->withholding_amount;
            data["account_type"] = asset->account_type;
            //data["unknown"] = asset->unknown;
        }

        dict error;
        error["error_msg"] = error_info->error_msg;
        error["error_id"] = error_info->error_id;

        QueryAsset_data_["asset"] = data;
        QueryAsset_data_["error_info"] = error;

        QueryAsset_data_["request_id"] = request_id;

        QueryAsset_data_["is_last"] = is_last;
        if (is_last) {
            QueryAsset_sync_ = 0;
            QueryAsset_cond_var_.notify_all();
        }

        return;
    }

    Task task = Task();
    task.task_name = ONQUERYASSET;

    if (asset) {
        task.task_data = *asset;
    } else {
        XTPQueryAssetRsp empty_data = XTPQueryAssetRsp();
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
    
    task.task_id = (uint64_t) request_id;
    task.task_last = true;
    this->task_queue.push(task);
}


void xtpTradeApi::OnQueryStructuredFund(XTPStructuredFundInfo * fund_info, XTPRI * error_info, int request_id, bool is_last, uint64_t session_id) {

    boost::mutex::scoped_lock lock(QueryStructuredFund_mutex_);

    if (QueryStructuredFund_sync_ > 0 ) {
        dict data;

        if (fund_info) {

            data["exchange_id"] = fund_info->exchange_id;
            data["sf_ticker"] = fund_info->sf_ticker;
            data["sf_ticker_name"] = fund_info->sf_ticker_name;
            data["ticker"] = fund_info->ticker;
            data["ticker_name"] = fund_info->ticker_name;
            data["split_merge_status"] = fund_info->split_merge_status;
            data["ratio"] = fund_info->ratio;
            data["min_split_qty"] = fund_info->min_split_qty;
            data["min_merge_qty"] = fund_info->min_merge_qty;
            data["net_price"] = fund_info->net_price;
        }

        dict error;
        error["error_msg"] = error_info->error_msg;
        error["error_id"] = error_info->error_id;

        QueryStructuredFund_data_["fund_info"] = data;
        QueryStructuredFund_data_["error_info"] = error;

        QueryStructuredFund_data_["request_id"] = request_id;

        QueryStructuredFund_data_["is_last"] = is_last;
        if (is_last) {
            QueryStructuredFund_sync_ = 0;
            QueryStructuredFund_cond_var_.notify_all();
        }

        return;
    }

    Task task = Task();
    task.task_name = ONQUERYSTRUCTUREDFUND;

    if (fund_info) {
        task.task_data = *fund_info;
    } else {
        XTPStructuredFundInfo empty_data = XTPStructuredFundInfo();
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
    
    task.task_id = (uint64_t) request_id;
    task.task_last = true;
    this->task_queue.push(task);
}


void xtpTradeApi::OnQueryFundTransfer(XTPFundTransferNotice * fund_transfer_info, XTPRI * error_info, int request_id, bool is_last, uint64_t session_id) {

    boost::mutex::scoped_lock lock(QueryFundTransfer_mutex_);

    if (QueryFundTransfer_sync_ > 0 ) {
        dict data;

        if (fund_transfer_info) {

            data["serial_id"] = fund_transfer_info->serial_id;
            data["transfer_type"] = fund_transfer_info->transfer_type;
            data["amount"] = fund_transfer_info->amount;
            data["oper_status"] = fund_transfer_info->oper_status;
            data["transfer_time"] = fund_transfer_info->transfer_time;
        }

        dict error;
        error["error_msg"] = error_info->error_msg;
        error["error_id"] = error_info->error_id;

        QueryFundTransfer_data_["fund_transfer_info"] = data;
        QueryFundTransfer_data_["error_info"] = error;

        QueryFundTransfer_data_["request_id"] = request_id;

        QueryFundTransfer_data_["is_last"] = is_last;
        if (is_last) {
            QueryFundTransfer_sync_ = 0;
            QueryFundTransfer_cond_var_.notify_all();
        }

        return;
    }

    Task task = Task();
    task.task_name = ONQUERYFUNDTRANSFER;

    if (fund_transfer_info) {
        task.task_data = *fund_transfer_info;
    } else {
        XTPFundTransferNotice empty_data = XTPFundTransferNotice();
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
    
    task.task_id = (uint64_t) request_id;
    task.task_last = true;
    this->task_queue.push(task);
}


void xtpTradeApi::OnFundTransfer(XTPFundTransferNotice * fund_transfer_info, XTPRI * error_info, uint64_t session_id) {

    boost::mutex::scoped_lock lock(FundTransfer_mutex_);

    if (FundTransfer_sync_ > 0 ) {
        dict data;

        if (fund_transfer_info) {

            data["serial_id"] = fund_transfer_info->serial_id;
            data["transfer_type"] = fund_transfer_info->transfer_type;
            data["amount"] = fund_transfer_info->amount;
            data["oper_status"] = fund_transfer_info->oper_status;
            data["transfer_time"] = fund_transfer_info->transfer_time;
        }

        dict error;
        error["error_msg"] = error_info->error_msg;
        error["error_id"] = error_info->error_id;

        FundTransfer_data_["fund_transfer_info"] = data;
        FundTransfer_data_["error_info"] = error;

        return;
    }

    Task task = Task();
    task.task_name = ONFUNDTRANSFER;

    if (fund_transfer_info) {
        task.task_data = *fund_transfer_info;
    } else {
        XTPFundTransferNotice empty_data = XTPFundTransferNotice();
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
    task.task_last = true;
    this->task_queue.push(task);
}


void xtpTradeApi::OnQueryETF(XTPQueryETFBaseRsp * etf_info, XTPRI * error_info, int request_id, bool is_last, uint64_t session_id) {

    boost::mutex::scoped_lock lock(QueryETF_mutex_);

    if (QueryETF_sync_ > 0 ) {
        dict data;

        if (etf_info) {

            data["market"] = etf_info->market;
            data["etf"] = etf_info->etf;
            data["subscribe_redemption_ticker"] = etf_info->subscribe_redemption_ticker;
            data["unit"] = etf_info->unit;
            data["subscribe_status"] = etf_info->subscribe_status;
            data["redemption_status"] = etf_info->redemption_status;
            data["max_cash_ratio"] = etf_info->max_cash_ratio;
            data["estimate_amount"] = etf_info->estimate_amount;
            data["cash_component"] = etf_info->cash_component;
            data["net_value"] = etf_info->net_value;
            data["total_amount"] = etf_info->total_amount;
        }

        dict error;
        error["error_msg"] = error_info->error_msg;
        error["error_id"] = error_info->error_id;

        QueryETF_data_["etf_info"] = data;
        QueryETF_data_["error_info"] = error;

        QueryETF_data_["request_id"] = request_id;

        QueryETF_data_["is_last"] = is_last;
        if (is_last) {
            QueryETF_sync_ = 0;
            QueryETF_cond_var_.notify_all();
        }

        return;
    }

    Task task = Task();
    task.task_name = ONQUERYETF;

    if (etf_info) {
        task.task_data = *etf_info;
    } else {
        XTPQueryETFBaseRsp empty_data = XTPQueryETFBaseRsp();
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
    
    task.task_id = (uint64_t) request_id;
    task.task_last = true;
    this->task_queue.push(task);
}


void xtpTradeApi::OnQueryETFBasket(XTPQueryETFComponentRsp * etf_component_info, XTPRI * error_info, int request_id, bool is_last, uint64_t session_id) {

    boost::mutex::scoped_lock lock(QueryETFTickerBasket_mutex_);

    if (QueryETFTickerBasket_sync_ > 0 ) {
        dict data;

        if (etf_component_info) {

            data["market"] = etf_component_info->market;
            data["ticker"] = etf_component_info->ticker;
            data["component_ticker"] = etf_component_info->component_ticker;
            data["component_name"] = etf_component_info->component_name;
            data["quantity"] = etf_component_info->quantity;
            data["component_market"] = etf_component_info->component_market;
            data["replace_type"] = etf_component_info->replace_type;
            data["premium_ratio"] = etf_component_info->premium_ratio;
            data["amount"] = etf_component_info->amount;
        }

        dict error;
        error["error_msg"] = error_info->error_msg;
        error["error_id"] = error_info->error_id;

        QueryETFTickerBasket_data_["etf_component_info"] = data;
        QueryETFTickerBasket_data_["error_info"] = error;

        QueryETFTickerBasket_data_["request_id"] = request_id;

        QueryETFTickerBasket_data_["is_last"] = is_last;
        if (is_last) {
            QueryETFTickerBasket_sync_ = 0;
            QueryETFTickerBasket_cond_var_.notify_all();
        }

        return;
    }

    Task task = Task();
    task.task_name = ONQUERYETFBASKET;

    if (etf_component_info) {
        task.task_data = *etf_component_info;
    } else {
        XTPQueryETFComponentRsp empty_data = XTPQueryETFComponentRsp();
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
    
    task.task_id = (uint64_t) request_id;
    task.task_last = true;
    this->task_queue.push(task);
}


void xtpTradeApi::OnQueryIPOInfoList(XTPQueryIPOTickerRsp * ipo_info, XTPRI * error_info, int request_id, bool is_last, uint64_t session_id) {

    boost::mutex::scoped_lock lock(QueryIPOInfoList_mutex_);

    if (QueryIPOInfoList_sync_ > 0 ) {
        dict data;

        if (ipo_info) {

            data["market"] = ipo_info->market;
            data["ticker"] = ipo_info->ticker;
            data["ticker_name"] = ipo_info->ticker_name;
            data["price"] = ipo_info->price;
            data["unit"] = ipo_info->unit;
            data["qty_upper_limit"] = ipo_info->qty_upper_limit;
        }

        dict error;
        error["error_msg"] = error_info->error_msg;
        error["error_id"] = error_info->error_id;

        QueryIPOInfoList_data_["ipo_info"] = data;
        QueryIPOInfoList_data_["error_info"] = error;

        QueryIPOInfoList_data_["request_id"] = request_id;

        QueryIPOInfoList_data_["is_last"] = is_last;
        if (is_last) {
            QueryIPOInfoList_sync_ = 0;
            QueryIPOInfoList_cond_var_.notify_all();
        }

        return;
    }

    Task task = Task();
    task.task_name = ONQUERYIPOINFOLIST;

    if (ipo_info) {
        task.task_data = *ipo_info;
    } else {
        XTPQueryIPOTickerRsp empty_data = XTPQueryIPOTickerRsp();
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
    
    task.task_id = (uint64_t) request_id;
    task.task_last = true;
    this->task_queue.push(task);
}


void xtpTradeApi::OnQueryIPOQuotaInfo(XTPQueryIPOQuotaRsp * quota_info, XTPRI * error_info, int request_id, bool is_last, uint64_t session_id) {

    boost::mutex::scoped_lock lock(QueryIPOQuotaInfo_mutex_);

    if (QueryIPOQuotaInfo_sync_ > 0 ) {
        dict data;

        if (quota_info) {

            data["market"] = quota_info->market;
            data["quantity"] = quota_info->quantity;
        }

        dict error;
        error["error_msg"] = error_info->error_msg;
        error["error_id"] = error_info->error_id;

        QueryIPOQuotaInfo_data_["quota_info"] = data;
        QueryIPOQuotaInfo_data_["error_info"] = error;

        QueryIPOQuotaInfo_data_["request_id"] = request_id;

        QueryIPOQuotaInfo_data_["is_last"] = is_last;
        if (is_last) {
            QueryIPOQuotaInfo_sync_ = 0;
            QueryIPOQuotaInfo_cond_var_.notify_all();
        }

        return;
    }

    Task task = Task();
    task.task_name = ONQUERYIPOQUOTAINFO;

    if (quota_info) {
        task.task_data = *quota_info;
    } else {
        XTPQueryIPOQuotaRsp empty_data = XTPQueryIPOQuotaRsp();
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
    
    task.task_id = (uint64_t) request_id;
    task.task_last = true;
    this->task_queue.push(task);
}


//-------------------------------------------------------------------------------------
//工作线程从队列中取出数据，转化为python对象后，进行推送
//-------------------------------------------------------------------------------------

void xtpTradeApi::processTask() {
    while (1) {
        Task task = this->task_queue.wait_and_pop();
        switch (task.task_name) {

            case ONDISCONNECTED: {
                this->processDisconnected(task);
                break;
            }

            case ONERROR: {
                this->processError(task);
                break;
            }

            case ONORDEREVENT: {
                this->processOrderEvent(task);
                break;
            }

            case ONTRADEEVENT: {
                this->processTradeEvent(task);
                break;
            }

            case ONCANCELORDERERROR: {
                this->processCancelOrderError(task);
                break;
            }

            case ONQUERYORDER: {
                this->processQueryOrder(task);
                break;
            }

            case ONQUERYTRADE: {
                this->processQueryTrade(task);
                break;
            }

            case ONQUERYPOSITION: {
                this->processQueryPosition(task);
                break;
            }

            case ONQUERYASSET: {
                this->processQueryAsset(task);
                break;
            }

            case ONQUERYSTRUCTUREDFUND: {
                this->processQueryStructuredFund(task);
                break;
            }

            case ONQUERYFUNDTRANSFER: {
                this->processQueryFundTransfer(task);
                break;
            }

            case ONFUNDTRANSFER: {
                this->processFundTransfer(task);
                break;
            }

            case ONQUERYETF: {
                this->processQueryETF(task);
                break;
            }

            case ONQUERYETFBASKET: {
                this->processQueryETFBasket(task);
                break;
            }

            case ONQUERYIPOINFOLIST: {
                this->processQueryIPOInfoList(task);
                break;
            }

            case ONQUERYIPOQUOTAINFO: {
                this->processQueryIPOQuotaInfo(task);
                break;
            }

        }
    }
}


void xtpTradeApi::processDisconnected(Task task) {
    PyLock lock;

    this->onDisconnected(task.task_session_id, task.task_id);
}

void xtpTradeApi::processError(Task task) {
    PyLock lock;


    XTPRI task_error = any_cast<XTPRI>(task.task_error);
    dict error;
    error["error_msg"] = task_error.error_msg;
    error["error_id"] = task_error.error_id;

    this->onError(error);
}

void xtpTradeApi::processOrderEvent(Task task) {
    PyLock lock;

    XTPOrderInfo task_data = any_cast<XTPOrderInfo>(task.task_data);
    dict data;

    data["order_xtp_id"] = task_data.order_xtp_id;
    data["order_client_id"] = task_data.order_client_id;
    data["order_cancel_client_id"] = task_data.order_cancel_client_id;
    data["order_cancel_xtp_id"] = task_data.order_cancel_xtp_id;
    data["ticker"] = task_data.ticker;
    data["market"] = task_data.market;
    data["price"] = task_data.price;
    data["quantity"] = task_data.quantity;
    data["price_type"] = task_data.price_type;
    data["side"] = task_data.side;
    data["business_type"] = task_data.business_type;
    data["qty_traded"] = task_data.qty_traded;
    data["qty_left"] = task_data.qty_left;
    data["insert_time"] = task_data.insert_time;
    data["update_time"] = task_data.update_time;
    data["cancel_time"] = task_data.cancel_time;
    data["trade_amount"] = task_data.trade_amount;
    data["order_local_id"] = task_data.order_local_id;
    data["order_status"] = task_data.order_status;
    data["order_submit_status"] = task_data.order_submit_status;
    data["order_type"] = task_data.order_type;

    XTPRI task_error = any_cast<XTPRI>(task.task_error);
    dict error;
    error["error_msg"] = task_error.error_msg;
    error["error_id"] = task_error.error_id;

    this->onOrderEvent(data, error);
}

void xtpTradeApi::processTradeEvent(Task task) {
    PyLock lock;

    XTPTradeReport task_data = any_cast<XTPTradeReport>(task.task_data);
    dict data;

    data["order_xtp_id"] = task_data.order_xtp_id;
    data["order_client_id"] = task_data.order_client_id;
    data["ticker"] = task_data.ticker;
    data["market"] = task_data.market;
    data["local_order_id"] = task_data.local_order_id;
    data["exec_id"] = task_data.exec_id;
    data["price"] = task_data.price;
    data["quantity"] = task_data.quantity;
    data["trade_time"] = task_data.trade_time;
    data["trade_amount"] = task_data.trade_amount;
    data["report_index"] = task_data.report_index;
    data["order_exch_id"] = task_data.order_exch_id;
    data["trade_type"] = task_data.trade_type;
    data["side"] = task_data.side;
    data["business_type"] = task_data.business_type;
    data["branch_pbu"] = task_data.branch_pbu;
    this->onTradeEvent(data);
}

void xtpTradeApi::processCancelOrderError(Task task) {
    PyLock lock;

    XTPOrderCancelInfo task_data = any_cast<XTPOrderCancelInfo>(task.task_data);
    dict data;

    data["order_cancel_xtp_id"] = task_data.order_cancel_xtp_id;
    data["order_xtp_id"] = task_data.order_xtp_id;

    XTPRI task_error = any_cast<XTPRI>(task.task_error);
    dict error;
    error["error_msg"] = task_error.error_msg;
    error["error_id"] = task_error.error_id;

    this->onCancelOrderError(data, error);
}

void xtpTradeApi::processQueryOrder(Task task) {
    PyLock lock;

    XTPQueryOrderRsp task_data = any_cast<XTPQueryOrderRsp>(task.task_data);
    dict data;

    data["order_xtp_id"] = task_data.order_xtp_id;
    data["order_client_id"] = task_data.order_client_id;
    data["order_cancel_client_id"] = task_data.order_cancel_client_id;
    data["order_cancel_xtp_id"] = task_data.order_cancel_xtp_id;
    data["ticker"] = task_data.ticker;
    data["market"] = task_data.market;
    data["price"] = task_data.price;
    data["quantity"] = task_data.quantity;
    data["price_type"] = task_data.price_type;
    data["side"] = task_data.side;
    data["business_type"] = task_data.business_type;
    data["qty_traded"] = task_data.qty_traded;
    data["qty_left"] = task_data.qty_left;
    data["insert_time"] = task_data.insert_time;
    data["update_time"] = task_data.update_time;
    data["cancel_time"] = task_data.cancel_time;
    data["trade_amount"] = task_data.trade_amount;
    data["order_local_id"] = task_data.order_local_id;
    data["order_status"] = task_data.order_status;
    data["order_submit_status"] = task_data.order_submit_status;
    data["order_type"] = task_data.order_type;

    XTPRI task_error = any_cast<XTPRI>(task.task_error);
    dict error;
    error["error_msg"] = task_error.error_msg;
    error["error_id"] = task_error.error_id;

    this->onQueryOrder(data, error, task.task_id, task.task_last);
}

void xtpTradeApi::processQueryTrade(Task task) {
    PyLock lock;

    XTPQueryTradeRsp task_data = any_cast<XTPQueryTradeRsp>(task.task_data);
    dict data;

    data["order_xtp_id"] = task_data.order_xtp_id;
    data["order_client_id"] = task_data.order_client_id;
    data["ticker"] = task_data.ticker;
    data["market"] = task_data.market;
    data["local_order_id"] = task_data.local_order_id;
    data["exec_id"] = task_data.exec_id;
    data["price"] = task_data.price;
    data["quantity"] = task_data.quantity;
    data["trade_time"] = task_data.trade_time;
    data["trade_amount"] = task_data.trade_amount;
    data["report_index"] = task_data.report_index;
    data["order_exch_id"] = task_data.order_exch_id;
    data["trade_type"] = task_data.trade_type;
    data["side"] = task_data.side;
    data["business_type"] = task_data.business_type;
    data["branch_pbu"] = task_data.branch_pbu;

    XTPRI task_error = any_cast<XTPRI>(task.task_error);
    dict error;
    error["error_msg"] = task_error.error_msg;
    error["error_id"] = task_error.error_id;

    this->onQueryTrade(data, error, task.task_id, task.task_last);
}

void xtpTradeApi::processQueryPosition(Task task) {
    PyLock lock;

    XTPQueryStkPositionRsp task_data = any_cast<XTPQueryStkPositionRsp>(task.task_data);
    dict data;

    data["ticker"] = task_data.ticker;
    data["ticker_name"] = task_data.ticker_name;
    data["market"] = task_data.market;
    data["total_qty"] = task_data.total_qty;
    data["sellable_qty"] = task_data.sellable_qty;
    data["avg_price"] = task_data.avg_price;
    data["unrealized_pnl"] = task_data.unrealized_pnl;
    data["yesterday_position"] = task_data.yesterday_position;
    data["purchase_redeemable_qty"] = task_data.purchase_redeemable_qty;
    data["unknown"] = task_data.unknown;

    XTPRI task_error = any_cast<XTPRI>(task.task_error);
    dict error;
    error["error_msg"] = task_error.error_msg;
    error["error_id"] = task_error.error_id;

    this->onQueryPosition(data, error, task.task_id, task.task_last);
}

void xtpTradeApi::processQueryAsset(Task task) {
    PyLock lock;

    XTPQueryAssetRsp task_data = any_cast<XTPQueryAssetRsp>(task.task_data);
    dict data;

    data["total_asset"] = task_data.total_asset;
    data["buying_power"] = task_data.buying_power;
    data["security_asset"] = task_data.security_asset;
    data["fund_buy_amount"] = task_data.fund_buy_amount;
    data["fund_buy_fee"] = task_data.fund_buy_fee;
    data["fund_sell_amount"] = task_data.fund_sell_amount;
    data["fund_sell_fee"] = task_data.fund_sell_fee;
    data["withholding_amount"] = task_data.withholding_amount;
    data["account_type"] = task_data.account_type;
    data["unknown"] = task_data.unknown;

    XTPRI task_error = any_cast<XTPRI>(task.task_error);
    dict error;
    error["error_msg"] = task_error.error_msg;
    error["error_id"] = task_error.error_id;

    this->onQueryAsset(data, error, task.task_id, task.task_last);
}

void xtpTradeApi::processQueryStructuredFund(Task task) {
    PyLock lock;

    XTPStructuredFundInfo task_data = any_cast<XTPStructuredFundInfo>(task.task_data);
    dict data;

    data["exchange_id"] = task_data.exchange_id;
    data["sf_ticker"] = task_data.sf_ticker;
    data["sf_ticker_name"] = task_data.sf_ticker_name;
    data["ticker"] = task_data.ticker;
    data["ticker_name"] = task_data.ticker_name;
    data["split_merge_status"] = task_data.split_merge_status;
    data["ratio"] = task_data.ratio;
    data["min_split_qty"] = task_data.min_split_qty;
    data["min_merge_qty"] = task_data.min_merge_qty;
    data["net_price"] = task_data.net_price;

    XTPRI task_error = any_cast<XTPRI>(task.task_error);
    dict error;
    error["error_msg"] = task_error.error_msg;
    error["error_id"] = task_error.error_id;

    this->onQueryStructuredFund(data, error, task.task_id, task.task_last);
}

void xtpTradeApi::processQueryFundTransfer(Task task) {
    PyLock lock;

    XTPFundTransferNotice task_data = any_cast<XTPFundTransferNotice>(task.task_data);
    dict data;

    data["serial_id"] = task_data.serial_id;
    data["transfer_type"] = task_data.transfer_type;
    data["amount"] = task_data.amount;
    data["oper_status"] = task_data.oper_status;
    data["transfer_time"] = task_data.transfer_time;

    XTPRI task_error = any_cast<XTPRI>(task.task_error);
    dict error;
    error["error_msg"] = task_error.error_msg;
    error["error_id"] = task_error.error_id;

    this->onQueryFundTransfer(data, error, task.task_id, task.task_last);
}

void xtpTradeApi::processFundTransfer(Task task) {
    PyLock lock;

    XTPFundTransferNotice task_data = any_cast<XTPFundTransferNotice>(task.task_data);
    dict data;

    data["serial_id"] = task_data.serial_id;
    data["transfer_type"] = task_data.transfer_type;
    data["amount"] = task_data.amount;
    data["oper_status"] = task_data.oper_status;
    data["transfer_time"] = task_data.transfer_time;

    XTPRI task_error = any_cast<XTPRI>(task.task_error);
    dict error;
    error["error_msg"] = task_error.error_msg;
    error["error_id"] = task_error.error_id;

    this->onFundTransfer(data, error);
}

void xtpTradeApi::processQueryETF(Task task) {
    PyLock lock;

    XTPQueryETFBaseRsp task_data = any_cast<XTPQueryETFBaseRsp>(task.task_data);
    dict data;

    data["market"] = task_data.market;
    data["etf"] = task_data.etf;
    data["subscribe_redemption_ticker"] = task_data.subscribe_redemption_ticker;
    data["unit"] = task_data.unit;
    data["subscribe_status"] = task_data.subscribe_status;
    data["redemption_status"] = task_data.redemption_status;
    data["max_cash_ratio"] = task_data.max_cash_ratio;
    data["estimate_amount"] = task_data.estimate_amount;
    data["cash_component"] = task_data.cash_component;
    data["net_value"] = task_data.net_value;
    data["total_amount"] = task_data.total_amount;

    XTPRI task_error = any_cast<XTPRI>(task.task_error);
    dict error;
    error["error_msg"] = task_error.error_msg;
    error["error_id"] = task_error.error_id;

    this->onQueryETF(data, error, task.task_id, task.task_last);
}

void xtpTradeApi::processQueryETFBasket(Task task) {
    PyLock lock;

    XTPQueryETFComponentRsp task_data = any_cast<XTPQueryETFComponentRsp>(task.task_data);
    dict data;

    data["market"] = task_data.market;
    data["ticker"] = task_data.ticker;
    data["component_ticker"] = task_data.component_ticker;
    data["component_name"] = task_data.component_name;
    data["quantity"] = task_data.quantity;
    data["component_market"] = task_data.component_market;
    data["replace_type"] = task_data.replace_type;
    data["premium_ratio"] = task_data.premium_ratio;
    data["amount"] = task_data.amount;

    XTPRI task_error = any_cast<XTPRI>(task.task_error);
    dict error;
    error["error_msg"] = task_error.error_msg;
    error["error_id"] = task_error.error_id;

    this->onQueryETFBasket(data, error, task.task_id, task.task_last);
}

void xtpTradeApi::processQueryIPOInfoList(Task task) {
    PyLock lock;

    XTPQueryIPOTickerRsp task_data = any_cast<XTPQueryIPOTickerRsp>(task.task_data);
    dict data;

    data["market"] = task_data.market;
    data["ticker"] = task_data.ticker;
    data["ticker_name"] = task_data.ticker_name;
    data["price"] = task_data.price;
    data["unit"] = task_data.unit;
    data["qty_upper_limit"] = task_data.qty_upper_limit;

    XTPRI task_error = any_cast<XTPRI>(task.task_error);
    dict error;
    error["error_msg"] = task_error.error_msg;
    error["error_id"] = task_error.error_id;

    this->onQueryIPOInfoList(data, error, task.task_id, task.task_last);
}

void xtpTradeApi::processQueryIPOQuotaInfo(Task task) {
    PyLock lock;

    XTPQueryIPOQuotaRsp task_data = any_cast<XTPQueryIPOQuotaRsp>(task.task_data);
    dict data;

    data["market"] = task_data.market;
    data["quantity"] = task_data.quantity;

    XTPRI task_error = any_cast<XTPRI>(task.task_error);
    dict error;
    error["error_msg"] = task_error.error_msg;
    error["error_id"] = task_error.error_id;

    this->onQueryIPOQuotaInfo(data, error, task.task_id, task.task_last);
}

//-------------------------------------------------------------------------------------
//req:主动函数的实现
//-------------------------------------------------------------------------------------

/*********************************************
//以下为人工填充的函数
*********************************************/

void xtpTradeApi::Release() {
    this->api->RegisterSpi(NULL);
    this->api->Release();
    this->api = NULL;
}

void xtpTradeApi::CreateTradeApi(uint64_t client_id, string save_file_path) {
    this->api = XTP::API::TraderApi::CreateTraderApi(client_id, save_file_path.c_str());
    if(!this->api) {
        cout<<"api init fault.\n"<<endl;
        return;
    }

    RegisterSpi();
}

void xtpTradeApi::init() {
    if (!this->api) {
        CreateTradeApi(1, "./");
    }
}

uint64_t xtpTradeApi::exit() {
    this->Release();
    return 1;
}

uint64_t xtpTradeApi::Login(dict req) {

    char ip[256];
    int port;
    char user[256];
    char password[256];
    uint64_t sock_type;

    getChar(req, "ip", ip);
    getValue(req, "port", &port);
    getChar(req, "user", user);
    getChar(req, "password", password);
    getValue(req, "sock_type", &sock_type);

    uint64_t session_id = this->api->Login(ip, port, user, password, XTP_PROTOCOL_TCP);
    printf("ip[%s] port[%d] user[%s] password[%s]\n", ip, port, user, password);
    std::cout << "debug:" << session_id << " size:" << sizeof(session_id) << std::endl;
    if (session_id> 0) {
        last_session_id = session_id;
    }

    return session_id;
}

uint64_t xtpTradeApi::Logout(uint64_t session_id = 0) {
    if(!session_id) session_id = last_session_id;

    uint64_t i = (uint64_t) this->api->Logout((uint64_t) session_id);
    return i;
}

void xtpTradeApi::RegisterSpi() {
    this->api->RegisterSpi(this);
}

dict xtpTradeApi::GetApiLastError() {
    XTPRI *error = this->api->GetApiLastError();
    dict ret;
    ret["error_msg"] = error->error_msg;
    ret["error_id"] = error->error_id;

    return ret;
}

string xtpTradeApi::GetTradingDay() {
    return this->api->GetTradingDay();
}

void xtpTradeApi::SetSoftwareVersion (string version) {
    this->api->SetSoftwareVersion(version.c_str());
}

void xtpTradeApi::SetSoftwareKey(string key) {
    this->api->SetSoftwareKey(key.c_str());
}

string xtpTradeApi::GetApiVersion () {
    return this->api->GetApiVersion();
}

uint8_t xtpTradeApi::GetClientIDByXTPID (uint64_t order_xtp_id) {
    return this->api->GetClientIDByXTPID(order_xtp_id);
}

string xtpTradeApi::GetAccountByXTPID (uint64_t order_xtp_id) {
    return this->api->GetAccountByXTPID(order_xtp_id);
}

void xtpTradeApi::SubscribePublicTopic(dict req) {

    XTP_TE_RESUME_TYPE resume_type;
    getValue(req, "resume_type", &resume_type);

    return this->api->SubscribePublicTopic(resume_type);
}

uint64_t xtpTradeApi::CancelOrder(const uint64_t order_xtp_id, uint64_t session_id = 0) {
    if(!session_id) session_id = last_session_id;
    return this->api->CancelOrder(order_xtp_id, session_id);
}

/*********************************************
//以下为自动生成的函数
*********************************************/

uint64_t xtpTradeApi::InsertOrder(dict req, uint64_t session_id) {

    if(!session_id) session_id = last_session_id;

    XTPOrderInsertInfo query_param;
    memset(&query_param, 0, sizeof(query_param));

    getValue(req, "order_xtp_id", &query_param.order_xtp_id);
    getValue(req, "order_client_id", &query_param.order_client_id);
    getChar(req, "ticker", query_param.ticker);
    getValue(req, "market", &query_param.market);
    getValue(req, "price", &query_param.price);
    getValue(req, "stop_price", &query_param.stop_price);
    getValue(req, "quantity", &query_param.quantity);
    getValue(req, "price_type", &query_param.price_type);
    getValue(req, "side", &query_param.side);
    getValue(req, "business_type", &query_param.business_type);
    return this->api->InsertOrder(&query_param, session_id);
}

int xtpTradeApi::QueryOrderByXTPID(const uint64_t order_xtp_id, uint64_t session_id, int request_id) {

    if(!session_id) session_id = last_session_id;

    return this->api->QueryOrderByXTPID(order_xtp_id, session_id, request_id);
}

int xtpTradeApi::QueryOrders(dict req, uint64_t session_id, int request_id) {

    if(!session_id) session_id = last_session_id;

    XTPQueryOrderReq query_param;
    memset(&query_param, 0, sizeof(query_param));

    getChar(req, "ticker", query_param.ticker);
    getValue(req, "begin_time", &query_param.begin_time);
    getValue(req, "end_time", &query_param.end_time);
    return this->api->QueryOrders(&query_param, session_id, request_id);
}

int xtpTradeApi::QueryTradesByXTPID(const uint64_t order_xtp_id, uint64_t session_id, int request_id) {

    if(!session_id) session_id = last_session_id;

    return this->api->QueryTradesByXTPID(order_xtp_id, session_id, request_id);
}

int xtpTradeApi::QueryTrades(dict req, uint64_t session_id, int request_id) {

    if(!session_id) session_id = last_session_id;

    XTPQueryTraderReq query_param;
    memset(&query_param, 0, sizeof(query_param));

    getChar(req, "ticker", query_param.ticker);
    getValue(req, "begin_time", &query_param.begin_time);
    getValue(req, "end_time", &query_param.end_time);
    return this->api->QueryTrades(&query_param, session_id, request_id);
}

int xtpTradeApi::QueryPosition(dict req, uint64_t session_id, int request_id) {

    if(!session_id) session_id = last_session_id;

    char ticker[256];
    getChar(req, "ticker", ticker);

    return this->api->QueryPosition(ticker, session_id, request_id);
}

int xtpTradeApi::QueryAsset(uint64_t session_id, int request_id) {

    if(!session_id) session_id = last_session_id;

    return this->api->QueryAsset(session_id, request_id);
}

int xtpTradeApi::QueryStructuredFund(dict req, uint64_t session_id, int request_id) {

    if(!session_id) session_id = last_session_id;

    XTPQueryStructuredFundInfoReq query_param;
    memset(&query_param, 0, sizeof(query_param));

    getValue(req, "exchange_id", &query_param.exchange_id);
    getChar(req, "sf_ticker", query_param.sf_ticker);
    return this->api->QueryStructuredFund(&query_param, session_id, request_id);
}

uint64_t xtpTradeApi::FundTransfer(dict req, uint64_t session_id) {

    if(!session_id) session_id = last_session_id;

    XTPFundTransferReq query_param;
    memset(&query_param, 0, sizeof(query_param));

    getValue(req, "serial_id", &query_param.serial_id);
    getChar(req, "fund_account", query_param.fund_account);
    getChar(req, "password", query_param.password);
    getValue(req, "amount", &query_param.amount);
    getValue(req, "transfer_type", &query_param.transfer_type);
    return this->api->FundTransfer(&query_param, session_id);
}

int xtpTradeApi::QueryFundTransfer(dict req, uint64_t session_id, int request_id) {

    if(!session_id) session_id = last_session_id;

    XTPQueryFundTransferLogReq query_param;
    memset(&query_param, 0, sizeof(query_param));

    getValue(req, "serial_id", &query_param.serial_id);
    return this->api->QueryFundTransfer(&query_param, session_id, request_id);
}

int xtpTradeApi::QueryETF(dict req, uint64_t session_id, int request_id) {

    if(!session_id) session_id = last_session_id;

    XTPQueryETFBaseReq query_param;
    memset(&query_param, 0, sizeof(query_param));

    getValue(req, "market", &query_param.market);
    getChar(req, "ticker", query_param.ticker);
    return this->api->QueryETF(&query_param, session_id, request_id);
}

int xtpTradeApi::QueryETFTickerBasket(dict req, uint64_t session_id, int request_id) {

    if(!session_id) session_id = last_session_id;

    XTPQueryETFComponentReq query_param;
    memset(&query_param, 0, sizeof(query_param));

    getValue(req, "market", &query_param.market);
    getChar(req, "ticker", query_param.ticker);
    return this->api->QueryETFTickerBasket(&query_param, session_id, request_id);
}

int xtpTradeApi::QueryIPOInfoList(uint64_t session_id, int request_id) {

    if(!session_id) session_id = last_session_id;

    return this->api->QueryIPOInfoList(session_id, request_id);
}

int xtpTradeApi::QueryIPOQuotaInfo(uint64_t session_id, int request_id) {

    if(!session_id) session_id = last_session_id;

    return this->api->QueryIPOQuotaInfo(session_id, request_id);
}

//-------------------------------------------------------------------------------------
//同步测试接口
//-------------------------------------------------------------------------------------

dict xtpTradeApi::QueryOrderByXTPIDSync(const uint64_t order_xtp_id, uint64_t session_id, int request_id) {
    boost::mutex::scoped_lock lock(QueryOrderByXTPID_mutex_);

    if(!session_id) session_id = last_session_id;

    QueryOrderByXTPID_data_ = dict();
    QueryOrderByXTPID_sync_ = request_id;
    int result = this->api->QueryOrderByXTPID(order_xtp_id, session_id, request_id);

    if (QueryOrderByXTPID_cond_var_.timed_wait(lock, boost::get_system_time() + boost::posix_time::seconds(wait_time_sec_))) {
        QueryOrderByXTPID_data_["result"] = result;
        return QueryOrderByXTPID_data_;
    } else { //time out
        QueryOrderByXTPID_data_["result"] = "timeout";
        return QueryOrderByXTPID_data_;
    }
}

dict xtpTradeApi::QueryOrdersSync(dict req, uint64_t session_id, int request_id) {
    boost::mutex::scoped_lock lock(QueryOrders_mutex_);

    if(!session_id) session_id = last_session_id;

    XTPQueryOrderReq query_param;
    memset(&query_param, 0, sizeof(query_param));

    getChar(req, "ticker", query_param.ticker);
    getValue(req, "begin_time", &query_param.begin_time);
    getValue(req, "end_time", &query_param.end_time);
    QueryOrders_data_ = dict();
    QueryOrders_sync_ = request_id;
    int result = this->api->QueryOrders(&query_param, session_id, request_id);

    if (QueryOrders_cond_var_.timed_wait(lock, boost::get_system_time() + boost::posix_time::seconds(wait_time_sec_))) {
        QueryOrders_data_["result"] = result;
        return QueryOrders_data_;
    } else { //time out
        QueryOrders_data_["result"] = "timeout";
        return QueryOrders_data_;
    }
}

dict xtpTradeApi::QueryTradesByXTPIDSync(const uint64_t order_xtp_id, uint64_t session_id, int request_id) {
    boost::mutex::scoped_lock lock(QueryTradesByXTPID_mutex_);

    if(!session_id) session_id = last_session_id;

    QueryTradesByXTPID_data_ = dict();
    QueryTradesByXTPID_sync_ = request_id;
    int result = this->api->QueryTradesByXTPID(order_xtp_id, session_id, request_id);

    if (QueryTradesByXTPID_cond_var_.timed_wait(lock, boost::get_system_time() + boost::posix_time::seconds(wait_time_sec_))) {
        QueryTradesByXTPID_data_["result"] = result;
        return QueryTradesByXTPID_data_;
    } else { //time out
        QueryTradesByXTPID_data_["result"] = "timeout";
        return QueryTradesByXTPID_data_;
    }
}

dict xtpTradeApi::QueryTradesSync(dict req, uint64_t session_id, int request_id) {
    boost::mutex::scoped_lock lock(QueryTrades_mutex_);

    if(!session_id) session_id = last_session_id;

    XTPQueryTraderReq query_param;
    memset(&query_param, 0, sizeof(query_param));

    getChar(req, "ticker", query_param.ticker);
    getValue(req, "begin_time", &query_param.begin_time);
    getValue(req, "end_time", &query_param.end_time);
    QueryTrades_data_ = dict();
    QueryTrades_sync_ = request_id;
    int result = this->api->QueryTrades(&query_param, session_id, request_id);

    if (QueryTrades_cond_var_.timed_wait(lock, boost::get_system_time() + boost::posix_time::seconds(wait_time_sec_))) {
        QueryTrades_data_["result"] = result;
        return QueryTrades_data_;
    } else { //time out
        QueryTrades_data_["result"] = "timeout";
        return QueryTrades_data_;
    }
}

dict xtpTradeApi::QueryPositionSync(dict req, uint64_t session_id, int request_id) {
    boost::mutex::scoped_lock lock(QueryPosition_mutex_);

    if(!session_id) session_id = last_session_id;

    char ticker[256];
    getChar(req, "ticker", ticker);

    QueryPosition_data_ = dict();
    QueryPosition_sync_ = request_id;
    int result = this->api->QueryPosition(ticker, session_id, request_id);

    if (QueryPosition_cond_var_.timed_wait(lock, boost::get_system_time() + boost::posix_time::seconds(wait_time_sec_))) {
        QueryPosition_data_["result"] = result;
        return QueryPosition_data_;
    } else { //time out
        QueryPosition_data_["result"] = "timeout";
        return QueryPosition_data_;
    }
}

dict xtpTradeApi::QueryAssetSync(uint64_t session_id, int request_id) {
    boost::mutex::scoped_lock lock(QueryAsset_mutex_);

    if(!session_id) session_id = last_session_id;

    QueryAsset_data_ = dict();
    QueryAsset_sync_ = request_id;
    int result = this->api->QueryAsset(session_id, request_id);

    if (QueryAsset_cond_var_.timed_wait(lock, boost::get_system_time() + boost::posix_time::seconds(wait_time_sec_))) {
        QueryAsset_data_["result"] = result;
        return QueryAsset_data_;
    } else { //time out
        QueryAsset_data_["result"] = "timeout";
        return QueryAsset_data_;
    }
}

dict xtpTradeApi::QueryStructuredFundSync(dict req, uint64_t session_id, int request_id) {
    boost::mutex::scoped_lock lock(QueryStructuredFund_mutex_);

    if(!session_id) session_id = last_session_id;

    XTPQueryStructuredFundInfoReq query_param;
    memset(&query_param, 0, sizeof(query_param));

    getValue(req, "exchange_id", &query_param.exchange_id);
    getChar(req, "sf_ticker", query_param.sf_ticker);
    QueryStructuredFund_data_ = dict();
    QueryStructuredFund_sync_ = request_id;
    int result = this->api->QueryStructuredFund(&query_param, session_id, request_id);

    if (QueryStructuredFund_cond_var_.timed_wait(lock, boost::get_system_time() + boost::posix_time::seconds(wait_time_sec_))) {
        QueryStructuredFund_data_["result"] = result;
        return QueryStructuredFund_data_;
    } else { //time out
        QueryStructuredFund_data_["result"] = "timeout";
        return QueryStructuredFund_data_;
    }
}

dict xtpTradeApi::QueryFundTransferSync(dict req, uint64_t session_id, int request_id) {
    boost::mutex::scoped_lock lock(QueryFundTransfer_mutex_);

    if(!session_id) session_id = last_session_id;

    XTPQueryFundTransferLogReq query_param;
    memset(&query_param, 0, sizeof(query_param));

    getValue(req, "serial_id", &query_param.serial_id);
    QueryFundTransfer_data_ = dict();
    QueryFundTransfer_sync_ = request_id;
    int result = this->api->QueryFundTransfer(&query_param, session_id, request_id);

    if (QueryFundTransfer_cond_var_.timed_wait(lock, boost::get_system_time() + boost::posix_time::seconds(wait_time_sec_))) {
        QueryFundTransfer_data_["result"] = result;
        return QueryFundTransfer_data_;
    } else { //time out
        QueryFundTransfer_data_["result"] = "timeout";
        return QueryFundTransfer_data_;
    }
}

dict xtpTradeApi::QueryETFSync(dict req, uint64_t session_id, int request_id) {
    boost::mutex::scoped_lock lock(QueryETF_mutex_);

    if(!session_id) session_id = last_session_id;

    XTPQueryETFBaseReq query_param;
    memset(&query_param, 0, sizeof(query_param));

    getValue(req, "market", &query_param.market);
    getChar(req, "ticker", query_param.ticker);
    QueryETF_data_ = dict();
    QueryETF_sync_ = request_id;
    int result = this->api->QueryETF(&query_param, session_id, request_id);

    if (QueryETF_cond_var_.timed_wait(lock, boost::get_system_time() + boost::posix_time::seconds(wait_time_sec_))) {
        QueryETF_data_["result"] = result;
        return QueryETF_data_;
    } else { //time out
        QueryETF_data_["result"] = "timeout";
        return QueryETF_data_;
    }
}

dict xtpTradeApi::QueryETFTickerBasketSync(dict req, uint64_t session_id, int request_id) {
    boost::mutex::scoped_lock lock(QueryETFTickerBasket_mutex_);

    if(!session_id) session_id = last_session_id;

    XTPQueryETFComponentReq query_param;
    memset(&query_param, 0, sizeof(query_param));

    getValue(req, "market", &query_param.market);
    getChar(req, "ticker", query_param.ticker);
    QueryETFTickerBasket_data_ = dict();
    QueryETFTickerBasket_sync_ = request_id;
    int result = this->api->QueryETFTickerBasket(&query_param, session_id, request_id);

    if (QueryETFTickerBasket_cond_var_.timed_wait(lock, boost::get_system_time() + boost::posix_time::seconds(wait_time_sec_))) {
        QueryETFTickerBasket_data_["result"] = result;
        return QueryETFTickerBasket_data_;
    } else { //time out
        QueryETFTickerBasket_data_["result"] = "timeout";
        return QueryETFTickerBasket_data_;
    }
}

dict xtpTradeApi::QueryIPOInfoListSync(uint64_t session_id, int request_id) {
    boost::mutex::scoped_lock lock(QueryIPOInfoList_mutex_);

    if(!session_id) session_id = last_session_id;

    QueryIPOInfoList_data_ = dict();
    QueryIPOInfoList_sync_ = request_id;
    int result = this->api->QueryIPOInfoList(session_id, request_id);

    if (QueryIPOInfoList_cond_var_.timed_wait(lock, boost::get_system_time() + boost::posix_time::seconds(wait_time_sec_))) {
        QueryIPOInfoList_data_["result"] = result;
        return QueryIPOInfoList_data_;
    } else { //time out
        QueryIPOInfoList_data_["result"] = "timeout";
        return QueryIPOInfoList_data_;
    }
}

dict xtpTradeApi::QueryIPOQuotaInfoSync(uint64_t session_id, int request_id) {
    boost::mutex::scoped_lock lock(QueryIPOQuotaInfo_mutex_);

    if(!session_id) session_id = last_session_id;

    QueryIPOQuotaInfo_data_ = dict();
    QueryIPOQuotaInfo_sync_ = request_id;
    int result = this->api->QueryIPOQuotaInfo(session_id, request_id);

    if (QueryIPOQuotaInfo_cond_var_.timed_wait(lock, boost::get_system_time() + boost::posix_time::seconds(wait_time_sec_))) {
        QueryIPOQuotaInfo_data_["result"] = result;
        return QueryIPOQuotaInfo_data_;
    } else { //time out
        QueryIPOQuotaInfo_data_["result"] = "timeout";
        return QueryIPOQuotaInfo_data_;
    }
}

//-------------------------------------------------------------------------------------
//Boost.Python封装
//-------------------------------------------------------------------------------------

struct TradeApiWrap : xtpTradeApi, wrapper<xtpTradeApi> {

    virtual void onDisconnected(uint64_t session_id, int reason) {
        PyLock lock;

        try {
            this->get_override("onDisconnected")(session_id, reason);
        } catch (error_already_set const &) {
            PyErr_Print();
        }
    };

    virtual void onError(dict error_info) {
        PyLock lock;

        try {
            this->get_override("onError")(error_info);
        } catch (error_already_set const &) {
            PyErr_Print();
        }
    };

    virtual void onOrderEvent(dict data, dict error_info) {
        PyLock lock;

        try {
            this->get_override("onOrderEvent")(data, error_info);
        } catch (error_already_set const &) {
            PyErr_Print();
        }
    };

    virtual void onTradeEvent(dict data) {
        PyLock lock;

        try {
            this->get_override("onTradeEvent")(data);
        } catch (error_already_set const &) {
            PyErr_Print();
        }
    };

    virtual void onCancelOrderError(dict data, dict error_info) {
        PyLock lock;

        try {
            this->get_override("onCancelOrderError")(data, error_info);
        } catch (error_already_set const &) {
            PyErr_Print();
        }
    };

    virtual void onQueryOrder(dict data, dict error_info, int request_id, bool is_last) {
        PyLock lock;

        try {
            this->get_override("onQueryOrder")(data, error_info, request_id, is_last);
        } catch (error_already_set const &) {
            PyErr_Print();
        }
    };

    virtual void onQueryTrade(dict data, dict error_info, int request_id, bool is_last) {
        PyLock lock;

        try {
            this->get_override("onQueryTrade")(data, error_info, request_id, is_last);
        } catch (error_already_set const &) {
            PyErr_Print();
        }
    };

    virtual void onQueryPosition(dict data, dict error_info, int request_id, bool is_last) {
        PyLock lock;

        try {
            this->get_override("onQueryPosition")(data, error_info, request_id, is_last);
        } catch (error_already_set const &) {
            PyErr_Print();
        }
    };

    virtual void onQueryAsset(dict data, dict error_info, int request_id, bool is_last) {
        PyLock lock;

        try {
            this->get_override("onQueryAsset")(data, error_info, request_id, is_last);
        } catch (error_already_set const &) {
            PyErr_Print();
        }
    };

    virtual void onQueryStructuredFund(dict data, dict error_info, int request_id, bool is_last) {
        PyLock lock;

        try {
            this->get_override("onQueryStructuredFund")(data, error_info, request_id, is_last);
        } catch (error_already_set const &) {
            PyErr_Print();
        }
    };

    virtual void onQueryFundTransfer(dict data, dict error_info, int request_id, bool is_last) {
        PyLock lock;

        try {
            this->get_override("onQueryFundTransfer")(data, error_info, request_id, is_last);
        } catch (error_already_set const &) {
            PyErr_Print();
        }
    };

    virtual void onFundTransfer(dict data, dict error_info) {
        PyLock lock;

        try {
            this->get_override("onFundTransfer")(data, error_info);
        } catch (error_already_set const &) {
            PyErr_Print();
        }
    };

    virtual void onQueryETF(dict data, dict error_info, int request_id, bool is_last) {
        PyLock lock;

        try {
            this->get_override("onQueryETF")(data, error_info, request_id, is_last);
        } catch (error_already_set const &) {
            PyErr_Print();
        }
    };

    virtual void onQueryETFBasket(dict data, dict error_info, int request_id, bool is_last) {
        PyLock lock;

        try {
            this->get_override("onQueryETFBasket")(data, error_info, request_id, is_last);
        } catch (error_already_set const &) {
            PyErr_Print();
        }
    };

    virtual void onQueryIPOInfoList(dict data, dict error_info, int request_id, bool is_last) {
        PyLock lock;

        try {
            this->get_override("onQueryIPOInfoList")(data, error_info, request_id, is_last);
        } catch (error_already_set const &) {
            PyErr_Print();
        }
    };

    virtual void onQueryIPOQuotaInfo(dict data, dict error_info, int request_id, bool is_last) {
        PyLock lock;

        try {
            this->get_override("onQueryIPOQuotaInfo")(data, error_info, request_id, is_last);
        } catch (error_already_set const &) {
            PyErr_Print();
        }
    };

};


BOOST_PYTHON_MODULE(vnxtptrade) {
    PyEval_InitThreads();    // 导入时运行，保证先创建GIL

    class_<TradeApiWrap, boost::noncopyable>("TradeApi")
        .def("onDisconnected", &xtpTradeApi::onDisconnected)
        .def("onError", &xtpTradeApi::onError)
        .def("onOrderEvent", &xtpTradeApi::onOrderEvent)
        .def("onTradeEvent", &xtpTradeApi::onTradeEvent)
        .def("onCancelOrderError", &xtpTradeApi::onCancelOrderError)
        .def("onQueryOrder", &xtpTradeApi::onQueryOrder)
        .def("onQueryTrade", &xtpTradeApi::onQueryTrade)
        .def("onQueryPosition", &xtpTradeApi::onQueryPosition)
        .def("onQueryAsset", &xtpTradeApi::onQueryAsset)
        .def("onQueryStructuredFund", &xtpTradeApi::onQueryStructuredFund)
        .def("onQueryFundTransfer", &xtpTradeApi::onQueryFundTransfer)
        .def("onFundTransfer", &xtpTradeApi::onFundTransfer)
        .def("onQueryETF", &xtpTradeApi::onQueryETF)
        .def("onQueryETFBasket", &xtpTradeApi::onQueryETFBasket)
        .def("onQueryIPOInfoList", &xtpTradeApi::onQueryIPOInfoList)
        .def("onQueryIPOQuotaInfo", &xtpTradeApi::onQueryIPOQuotaInfo)
        .def("CreateTradeApi", &xtpTradeApi::CreateTradeApi)
        .def("Release", &xtpTradeApi::Release)
        .def("init", &xtpTradeApi::init)
        .def("exit", &xtpTradeApi::exit)
        .def("RegisterSpi", &xtpTradeApi::RegisterSpi)
        .def("SetSoftwareVersion", &xtpTradeApi::SetSoftwareVersion)
        .def("SetSoftwareKey", &xtpTradeApi::SetSoftwareKey)
        .def("GetApiLastError", &xtpTradeApi::GetApiLastError)
        .def("GetTradingDay", &xtpTradeApi::GetTradingDay)
        .def("GetApiVersion", &xtpTradeApi::GetApiVersion)
        .def("GetClientIDByXTPID", &xtpTradeApi::GetClientIDByXTPID)
        .def("GetAccountByXTPID", &xtpTradeApi::GetAccountByXTPID)
        .def("SubscribePublicTopic", &xtpTradeApi::SubscribePublicTopic)
        .def("Login", &xtpTradeApi::Login)
        .def("Logout", &xtpTradeApi::Logout)
        .def("InsertOrder", &xtpTradeApi::InsertOrder)
        .def("CancelOrder", &xtpTradeApi::CancelOrder)
        .def("FundTransfer", &xtpTradeApi::FundTransfer)
        .def("QueryOrderByXTPID", &xtpTradeApi::QueryOrderByXTPID)
        .def("QueryOrders", &xtpTradeApi::QueryOrders)
        .def("QueryTradesByXTPID", &xtpTradeApi::QueryTradesByXTPID)
        .def("QueryTrades", &xtpTradeApi::QueryTrades)
        .def("QueryPosition", &xtpTradeApi::QueryPosition)
        .def("QueryAsset", &xtpTradeApi::QueryAsset)
        .def("QueryStructuredFund", &xtpTradeApi::QueryStructuredFund)
        .def("QueryFundTransfer", &xtpTradeApi::QueryFundTransfer)
        .def("QueryETF", &xtpTradeApi::QueryETF)
        .def("QueryETFTickerBasket", &xtpTradeApi::QueryETFTickerBasket)
        .def("QueryIPOInfoList", &xtpTradeApi::QueryIPOInfoList)
        .def("QueryIPOQuotaInfo", &xtpTradeApi::QueryIPOQuotaInfo)
        .def("QueryOrderByXTPIDSync", &xtpTradeApi::QueryOrderByXTPIDSync)
        .def("QueryOrdersSync", &xtpTradeApi::QueryOrdersSync)
        .def("QueryTradesByXTPIDSync", &xtpTradeApi::QueryTradesByXTPIDSync)
        .def("QueryTradesSync", &xtpTradeApi::QueryTradesSync)
        .def("QueryPositionSync", &xtpTradeApi::QueryPositionSync)
        .def("QueryAssetSync", &xtpTradeApi::QueryAssetSync)
        .def("QueryStructuredFundSync", &xtpTradeApi::QueryStructuredFundSync)
        .def("QueryFundTransferSync", &xtpTradeApi::QueryFundTransferSync)
        .def("QueryETFSync", &xtpTradeApi::QueryETFSync)
        .def("QueryETFTickerBasketSync", &xtpTradeApi::QueryETFTickerBasketSync)
        .def("QueryIPOInfoListSync", &xtpTradeApi::QueryIPOInfoListSync)
        .def("QueryIPOQuotaInfoSync", &xtpTradeApi::QueryIPOQuotaInfoSync)
    ;

    enum_<XTP_PROTOCOL_TYPE>("XTP_PROTOCOL_TYPE")
            .value("XTP_PROTOCOL_TCP", XTP_PROTOCOL_TCP)
            .value("XTP_PROTOCOL_UDP", XTP_PROTOCOL_UDP)
            ;

    enum_<XTP_EXCHANGE_TYPE>("XTP_EXCHANGE_TYPE")
            .value("XTP_EXCHANGE_SH", XTP_EXCHANGE_SH)
            .value("XTP_EXCHANGE_SZ", XTP_EXCHANGE_SZ)
            .value("XTP_EXCHANGE_UNKNOWN", XTP_EXCHANGE_UNKNOWN)
            ;

    enum_<XTP_MARKET_TYPE>("XTP_MARKET_TYPE")
            .value("XTP_MKT_INIT", XTP_MKT_INIT)
            .value("XTP_MKT_SZ_A", XTP_MKT_SZ_A)
            .value("XTP_MKT_SH_A", XTP_MKT_SH_A)
            .value("XTP_MKT_UNKNOWN", XTP_MKT_UNKNOWN)
            ;

    enum_<XTP_PRICE_TYPE>("XTP_PRICE_TYPE")
            .value("XTP_PRICE_LIMIT", XTP_PRICE_LIMIT)
            .value("XTP_PRICE_BEST_OR_CANCEL", XTP_PRICE_BEST_OR_CANCEL)
            .value("XTP_PRICE_BEST5_OR_LIMIT", XTP_PRICE_BEST5_OR_LIMIT)
            .value("XTP_PRICE_BEST5_OR_CANCEL", XTP_PRICE_BEST5_OR_CANCEL)
            .value("XTP_PRICE_ALL_OR_CANCEL", XTP_PRICE_ALL_OR_CANCEL)
            .value("XTP_PRICE_FORWARD_BEST", XTP_PRICE_FORWARD_BEST)
            .value("XTP_PRICE_REVERSE_BEST_LIMIT", XTP_PRICE_REVERSE_BEST_LIMIT)
            .value("XTP_PRICE_TYPE_UNKNOWN", XTP_PRICE_TYPE_UNKNOWN)
            ;


    enum_<XTP_SIDE_TYPE>("XTP_SIDE_TYPE")
            .value("XTP_SIDE_BUY", XTP_SIDE_BUY)
            .value("XTP_SIDE_SELL", XTP_SIDE_SELL)
            .value("XTP_SIDE_BUY_OPEN", XTP_SIDE_BUY_OPEN)
            .value("XTP_SIDE_SELL_OPEN", XTP_SIDE_SELL_OPEN)
            .value("XTP_SIDE_BUY_CLOSE", XTP_SIDE_BUY_CLOSE)
            .value("XTP_SIDE_SELL_CLOSE", XTP_SIDE_SELL_CLOSE)
            .value("XTP_SIDE_PURCHASE", XTP_SIDE_PURCHASE)
            .value("XTP_SIDE_REDEMPTION", XTP_SIDE_REDEMPTION)
            .value("XTP_SIDE_SPLIT", XTP_SIDE_SPLIT)
            .value("XTP_SIDE_MERGE", XTP_SIDE_MERGE)
            ;

    enum_<XTP_ORDER_ACTION_STATUS_TYPE>("XTP_ORDER_ACTION_STATUS_TYPE")
            .value("XTP_ORDER_ACTION_STATUS_SUBMITTED", XTP_ORDER_ACTION_STATUS_SUBMITTED)
            .value("XTP_ORDER_ACTION_STATUS_ACCEPTED", XTP_ORDER_ACTION_STATUS_ACCEPTED)
            .value("XTP_ORDER_ACTION_STATUS_REJECTED", XTP_ORDER_ACTION_STATUS_REJECTED)
            ;

    enum_<XTP_ORDER_STATUS_TYPE>("XTP_ORDER_STATUS_TYPE")
            .value("XTP_ORDER_STATUS_INIT", XTP_ORDER_STATUS_INIT)
            .value("XTP_ORDER_STATUS_ALLTRADED", XTP_ORDER_STATUS_ALLTRADED)
            .value("XTP_ORDER_STATUS_PARTTRADEDQUEUEING", XTP_ORDER_STATUS_PARTTRADEDQUEUEING)
            .value("XTP_ORDER_STATUS_PARTTRADEDNOTQUEUEING", XTP_ORDER_STATUS_PARTTRADEDNOTQUEUEING)
            .value("XTP_ORDER_STATUS_NOTRADEQUEUEING", XTP_ORDER_STATUS_NOTRADEQUEUEING)
            .value("XTP_ORDER_STATUS_CANCELED", XTP_ORDER_STATUS_CANCELED)
            .value("XTP_ORDER_STATUS_REJECTED", XTP_ORDER_STATUS_REJECTED)
            .value("XTP_ORDER_STATUS_UNKNOWN", XTP_ORDER_STATUS_UNKNOWN)
            ;

    enum_<XTP_ORDER_SUBMIT_STATUS_TYPE>("XTP_ORDER_SUBMIT_STATUS_TYPE")
            .value("XTP_ORDER_SUBMIT_STATUS_INSERT_SUBMITTED", XTP_ORDER_SUBMIT_STATUS_INSERT_SUBMITTED)
            .value("XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED", XTP_ORDER_SUBMIT_STATUS_INSERT_ACCEPTED)
            .value("XTP_ORDER_SUBMIT_STATUS_INSERT_REJECTED", XTP_ORDER_SUBMIT_STATUS_INSERT_REJECTED)
            .value("XTP_ORDER_SUBMIT_STATUS_CANCEL_SUBMITTED", XTP_ORDER_SUBMIT_STATUS_CANCEL_SUBMITTED)
            .value("XTP_ORDER_SUBMIT_STATUS_CANCEL_REJECTED", XTP_ORDER_SUBMIT_STATUS_CANCEL_REJECTED)
            .value("XTP_ORDER_SUBMIT_STATUS_CANCEL_ACCEPTED", XTP_ORDER_SUBMIT_STATUS_CANCEL_ACCEPTED)
            ;

    enum_<XTP_TE_RESUME_TYPE>("XTP_TE_RESUME_TYPE")
            .value("XTP_TERT_RESTART", XTP_TERT_RESTART)
            .value("XTP_TERT_RESUME", XTP_TERT_RESUME)
            .value("XTP_TERT_QUICK", XTP_TERT_QUICK)
            ;

    enum_<XTP_BUSINESS_TYPE>("XTP_BUSINESS_TYPE")
            .value("XTP_BUSINESS_TYPE_CASH", XTP_BUSINESS_TYPE_CASH)
            .value("XTP_BUSINESS_TYPE_IPOS", XTP_BUSINESS_TYPE_IPOS)
            .value("XTP_BUSINESS_TYPE_REPO", XTP_BUSINESS_TYPE_REPO)
            .value("XTP_BUSINESS_TYPE_ETF", XTP_BUSINESS_TYPE_ETF)
            .value("XTP_BUSINESS_TYPE_MARGIN", XTP_BUSINESS_TYPE_MARGIN)
            .value("XTP_BUSINESS_TYPE_DESIGNATION", XTP_BUSINESS_TYPE_DESIGNATION)
            .value("XTP_BUSINESS_TYPE_ALLOTMENT", XTP_BUSINESS_TYPE_ALLOTMENT)
            .value("XTP_BUSINESS_TYPE_STRUCTURED_FUND_PURCHASE_REDEMPTION", XTP_BUSINESS_TYPE_STRUCTURED_FUND_PURCHASE_REDEMPTION)
            .value("XTP_BUSINESS_TYPE_STRUCTURED_FUND_SPLIT_MERGE", XTP_BUSINESS_TYPE_STRUCTURED_FUND_SPLIT_MERGE)
            .value("XTP_BUSINESS_TYPE_MONEY_FUND", XTP_BUSINESS_TYPE_MONEY_FUND)
            .value("XTP_BUSINESS_TYPE_UNKNOWN", XTP_BUSINESS_TYPE_UNKNOWN)
            ;

    enum_<ETF_REPLACE_TYPE>("ETF_REPLACE_TYPE")
            .value("ERT_CASH_FORBIDDEN", ERT_CASH_FORBIDDEN)
            .value("ERT_CASH_OPTIONAL", ERT_CASH_OPTIONAL)
            .value("ERT_CASH_MUST", ERT_CASH_MUST)
            .value("EPT_INVALID", EPT_INVALID)
            ;

    enum_<XTP_TICKER_TYPE>("XTP_TICKER_TYPE")
            .value("XTP_TICKER_TYPE_STOCK", XTP_TICKER_TYPE_STOCK)
            .value("XTP_TICKER_TYPE_INDEX", XTP_TICKER_TYPE_INDEX)
            .value("XTP_TICKER_TYPE_FUND", XTP_TICKER_TYPE_FUND)
            .value("XTP_TICKER_TYPE_BOND", XTP_TICKER_TYPE_BOND)
            .value("XTP_TICKER_TYPE_UNKNOWN", XTP_TICKER_TYPE_UNKNOWN)
            ;

    enum_<XTP_ACCOUNT_TYPE>("XTP_ACCOUNT_TYPE")
            .value("XTP_ACCOUNT_TYPE", XTP_ACCOUNT_NORMAL)
            .value("XTP_ACCOUNT_CREDIT", XTP_ACCOUNT_CREDIT)
            .value("XTP_ACCOUNT_DERIVE", XTP_ACCOUNT_DERIVE)
            .value("XTP_ACCOUNT_UNKNOWN", XTP_ACCOUNT_UNKNOWN)
            ;

    enum_<XTP_FUND_TRANSFER_TYPE>("XTP_FUND_TRANSFER_TYPE")
            .value("XTP_FUND_TRANSFER_OUT", XTP_FUND_TRANSFER_OUT)
            .value("XTP_FUND_TRANSFER_IN", XTP_FUND_TRANSFER_IN)
            .value("XTP_FUND_TRANSFER_UNKNOWN", XTP_FUND_TRANSFER_UNKNOWN)
            ;

    enum_<XTP_FUND_OPER_STATUS>("XTP_FUND_OPER_STATUS")
            .value("XTP_FUND_OPER_PROCESSING", XTP_FUND_OPER_PROCESSING)
            .value("XTP_FUND_OPER_SUCCESS", XTP_FUND_OPER_SUCCESS)
            .value("XTP_FUND_OPER_FAILED", XTP_FUND_OPER_FAILED)
            .value("XTP_FUND_OPER_SUBMITTED", XTP_FUND_OPER_SUBMITTED)
            .value("XTP_FUND_OPER_UNKNOWN", XTP_FUND_OPER_UNKNOWN)
            ;

    enum_<XTP_SPLIT_MERGE_STATUS>("XTP_SPLIT_MERGE_STATUS")
            .value("XTP_SPLIT_MERGE_STATUS_ALLOW", XTP_SPLIT_MERGE_STATUS_ALLOW)
            .value("XTP_SPLIT_MERGE_STATUS_ONLY_SPLIT", XTP_SPLIT_MERGE_STATUS_ONLY_SPLIT)
            .value("XTP_SPLIT_MERGE_STATUS_ONLY_MERGE", XTP_SPLIT_MERGE_STATUS_ONLY_MERGE)
            .value("XTP_SPLIT_MERGE_STATUS_FORBIDDEN", XTP_SPLIT_MERGE_STATUS_FORBIDDEN)
            ;

    enum_<XTP_TBT_TYPE>("XTP_TBT_TYPE")
            .value("XTP_TBT_ENTRUST", XTP_TBT_ENTRUST)
            .value("XTP_TBT_TRADE", XTP_TBT_TRADE)
            ;

}
