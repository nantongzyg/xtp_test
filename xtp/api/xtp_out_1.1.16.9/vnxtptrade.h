
//说明部分

//系统
/*
#ifdef WIN32
#include "stdafx.h"
#endif
*/
#include <string>
#include <queue>

//Boost
#define BOOST_PYTHON_STATIC_LIB
#include <boost/python/enum.hpp>
#include <boost/python/module.hpp>	//python封装
#include <boost/python/def.hpp>		//python封装
#include <boost/python/dict.hpp>	//python封装
#include <boost/python/object.hpp>	//python封装
#include <boost/python.hpp>			//python封装
#include <boost/thread.hpp>			//任务队列的线程功能
#include <boost/bind.hpp>			//任务队列的线程功能
#include <boost/any.hpp>			//任务队列的任务实现

//API
#include "xtp_trader_api.h"

//命名空间
using namespace std;
using namespace boost::python;
using namespace boost;
using namespace XTP::API;

//常量

#define ONDISCONNECTED 1
#define ONERROR 2
#define ONORDEREVENT 3
#define ONTRADEEVENT 4
#define ONCANCELORDERERROR 5
#define ONQUERYORDER 6
#define ONQUERYTRADE 7
#define ONQUERYPOSITION 8
#define ONQUERYASSET 9
#define ONQUERYSTRUCTUREDFUND 10
#define ONQUERYFUNDTRANSFER 11
#define ONFUNDTRANSFER 12
#define ONQUERYETF 13
#define ONQUERYETFBASKET 14
#define ONQUERYIPOINFOLIST 15
#define ONQUERYIPOQUOTAINFO 16

///-------------------------------------------------------------------------------------
///API中的部分组件
///-------------------------------------------------------------------------------------

//GIL全局锁简化获取用，
//用于帮助C++线程获得GIL锁，从而防止python崩溃
class PyLock {
private:
    PyGILState_STATE gil_state;

public:
    //在某个函数方法中创建该对象时，获得GIL锁
    PyLock() {
        gil_state = PyGILState_Ensure();
    }

    //在某个函数完成后销毁该对象时，解放GIL锁
    ~PyLock() {
        PyGILState_Release(gil_state);
    }
};


//任务结构体
struct Task {
    uint64_t task_name;		//回调函数名称对应的常量
    any task_data;		//数据结构体
    any task_error;		//错误结构体
    uint64_t task_session_id;		//Session id
    uint64_t task_id;		//请求id
    bool task_last;		//是否为最后返回
};


///线程安全的队列
template<typename Data>

class ConcurrentQueue {
private:
    queue<Data> the_queue;								//标准库队列
    mutable mutex the_mutex;							//boost互斥锁
    condition_variable the_condition_variable;			//boost条件变量

public:
    //存入新的任务
    void push(Data const& data) {
        mutex::scoped_lock lock(the_mutex);				//获取互斥锁
        the_queue.push(data);							//向队列中存入数据
        lock.unlock();									//释放锁
        the_condition_variable.notify_one();			//通知正在阻塞等待的线程
    }

    //检查队列是否为空
    bool empty() const {
        mutex::scoped_lock lock(the_mutex);
        return the_queue.empty();
    }

    //取出
    Data wait_and_pop() {
        mutex::scoped_lock lock(the_mutex);

        while(the_queue.empty()) {					//当队列为空时
            the_condition_variable.wait(lock);			//等待条件变量通知
        }

        Data popped_value = the_queue.front();			//获取队列中的最后一个任务
        the_queue.pop();								//删除该任务
        return popped_value;							//返回该任务
    }

};


//从字典中获取某个建值对应的数值，并赋值到请求结构体对象的值上
template<typename T>
void getValue(dict d, string key, T *value);

//从字典中获取某个建值对应的字符串，并赋值到请求结构体对象的值上
void getChar(dict d, string key, char* value);


///-------------------------------------------------------------------------------------
///C++ SPI的回调函数方法实现
///-------------------------------------------------------------------------------------


//API的继承实现
class xtpTradeApi : public TraderSpi {
private:
    uint64_t last_session_id;
    TraderApi* api;			//API对象
    thread *task_thread;				//工作线程指针（向python中推送数据）
    ConcurrentQueue<Task> task_queue;	//任务队列

    const int wait_time_sec_ = 5;

    dict FundTransfer_data_;
    boost::atomic< uint64_t > FundTransfer_sync_;
    boost::mutex FundTransfer_mutex_;
    boost::condition_variable FundTransfer_cond_var_;

    dict QueryOrderByXTPID_data_;
    boost::atomic< uint64_t > QueryOrderByXTPID_sync_;
    boost::mutex QueryOrderByXTPID_mutex_;
    boost::condition_variable QueryOrderByXTPID_cond_var_;

    dict QueryOrders_data_;
    boost::atomic< uint64_t > QueryOrders_sync_;
    boost::mutex QueryOrders_mutex_;
    boost::condition_variable QueryOrders_cond_var_;

    dict QueryTradesByXTPID_data_;
    boost::atomic< uint64_t > QueryTradesByXTPID_sync_;
    boost::mutex QueryTradesByXTPID_mutex_;
    boost::condition_variable QueryTradesByXTPID_cond_var_;

    dict QueryTrades_data_;
    boost::atomic< uint64_t > QueryTrades_sync_;
    boost::mutex QueryTrades_mutex_;
    boost::condition_variable QueryTrades_cond_var_;

    dict QueryPosition_data_;
    boost::atomic< uint64_t > QueryPosition_sync_;
    boost::mutex QueryPosition_mutex_;
    boost::condition_variable QueryPosition_cond_var_;

    dict QueryAsset_data_;
    boost::atomic< uint64_t > QueryAsset_sync_;
    boost::mutex QueryAsset_mutex_;
    boost::condition_variable QueryAsset_cond_var_;

    dict QueryStructuredFund_data_;
    boost::atomic< uint64_t > QueryStructuredFund_sync_;
    boost::mutex QueryStructuredFund_mutex_;
    boost::condition_variable QueryStructuredFund_cond_var_;

    dict QueryFundTransfer_data_;
    boost::atomic< uint64_t > QueryFundTransfer_sync_;
    boost::mutex QueryFundTransfer_mutex_;
    boost::condition_variable QueryFundTransfer_cond_var_;

    dict QueryETF_data_;
    boost::atomic< uint64_t > QueryETF_sync_;
    boost::mutex QueryETF_mutex_;
    boost::condition_variable QueryETF_cond_var_;

    dict QueryETFTickerBasket_data_;
    boost::atomic< uint64_t > QueryETFTickerBasket_sync_;
    boost::mutex QueryETFTickerBasket_mutex_;
    boost::condition_variable QueryETFTickerBasket_cond_var_;

    dict QueryIPOInfoList_data_;
    boost::atomic< uint64_t > QueryIPOInfoList_sync_;
    boost::mutex QueryIPOInfoList_mutex_;
    boost::condition_variable QueryIPOInfoList_cond_var_;

    dict QueryIPOQuotaInfo_data_;
    boost::atomic< uint64_t > QueryIPOQuotaInfo_sync_;
    boost::mutex QueryIPOQuotaInfo_mutex_;
    boost::condition_variable QueryIPOQuotaInfo_cond_var_;

public:
    xtpTradeApi() {

        QueryOrderByXTPID_sync_ = 0;

        QueryOrders_sync_ = 0;

        QueryTradesByXTPID_sync_ = 0;

        QueryTrades_sync_ = 0;

        QueryPosition_sync_ = 0;

        QueryAsset_sync_ = 0;

        QueryStructuredFund_sync_ = 0;

        QueryFundTransfer_sync_ = 0;

        QueryETF_sync_ = 0;

        QueryETFTickerBasket_sync_ = 0;

        QueryIPOInfoList_sync_ = 0;

        QueryIPOQuotaInfo_sync_ = 0;

        function0<void> f = boost::bind(&xtpTradeApi::processTask, this);
        this->task_thread = new thread(f);
    };

    ~xtpTradeApi() {
        this->task_thread->detach();
    };

    //-------------------------------------------------------------------------------------
    //API回调函数
    //-------------------------------------------------------------------------------------

    virtual void OnDisconnected(uint64_t session_id, int reason);

    virtual void OnError(XTPRI * error_info);

    virtual void OnOrderEvent(XTPOrderInfo * order_info, XTPRI * error_info, uint64_t session_id);

    virtual void OnTradeEvent(XTPTradeReport * trade_info, uint64_t session_id);

    virtual void OnCancelOrderError(XTPOrderCancelInfo * cancel_info, XTPRI * error_info, uint64_t session_id);

    virtual void OnQueryOrder(XTPQueryOrderRsp * order_info, XTPRI * error_info, int request_id, bool is_last, uint64_t session_id);

    virtual void OnQueryTrade(XTPQueryTradeRsp * trade_info, XTPRI * error_info, int request_id, bool is_last, uint64_t session_id);

    virtual void OnQueryPosition(XTPQueryStkPositionRsp * position, XTPRI * error_info, int request_id, bool is_last, uint64_t session_id);

    virtual void OnQueryAsset(XTPQueryAssetRsp * asset, XTPRI * error_info, int request_id, bool is_last, uint64_t session_id);

    virtual void OnQueryStructuredFund(XTPStructuredFundInfo * fund_info, XTPRI * error_info, int request_id, bool is_last, uint64_t session_id);

    virtual void OnQueryFundTransfer(XTPFundTransferNotice * fund_transfer_info, XTPRI * error_info, int request_id, bool is_last, uint64_t session_id);

    virtual void OnFundTransfer(XTPFundTransferNotice * fund_transfer_info, XTPRI * error_info, uint64_t session_id);

    virtual void OnQueryETF(XTPQueryETFBaseRsp * etf_info, XTPRI * error_info, int request_id, bool is_last, uint64_t session_id);

    virtual void OnQueryETFBasket(XTPQueryETFComponentRsp * etf_component_info, XTPRI * error_info, int request_id, bool is_last, uint64_t session_id);

    virtual void OnQueryIPOInfoList(XTPQueryIPOTickerRsp * ipo_info, XTPRI * error_info, int request_id, bool is_last, uint64_t session_id);

    virtual void OnQueryIPOQuotaInfo(XTPQueryIPOQuotaRsp * quota_info, XTPRI * error_info, int request_id, bool is_last, uint64_t session_id);

    //-------------------------------------------------------------------------------------
    //task：任务
    //-------------------------------------------------------------------------------------
    void processTask();

    void processDisconnected(Task task);

    void processError(Task task);

    void processOrderEvent(Task task);

    void processTradeEvent(Task task);

    void processCancelOrderError(Task task);

    void processQueryOrder(Task task);

    void processQueryTrade(Task task);

    void processQueryPosition(Task task);

    void processQueryAsset(Task task);

    void processQueryStructuredFund(Task task);

    void processQueryFundTransfer(Task task);

    void processFundTransfer(Task task);

    void processQueryETF(Task task);

    void processQueryETFBasket(Task task);

    void processQueryIPOInfoList(Task task);

    void processQueryIPOQuotaInfo(Task task);

    //-------------------------------------------------------------------------------------
    //data：回调函数的数据字典
    //error：回调函数的错误字典
    //id：请求id
    //last：是否为最后返回
    //i：整数
    //-------------------------------------------------------------------------------------

    virtual void onDisconnected(uint64_t session_id, int reason) {};

    virtual void onError(dict error_info) {};

    virtual void onOrderEvent(dict data, dict error_info) {};

    virtual void onTradeEvent(dict data) {};

    virtual void onCancelOrderError(dict data, dict error_info) {};

    virtual void onQueryOrder(dict data, dict error_info, int request_id, bool is_last) {};

    virtual void onQueryTrade(dict data, dict error_info, int request_id, bool is_last) {};

    virtual void onQueryPosition(dict data, dict error_info, int request_id, bool is_last) {};

    virtual void onQueryAsset(dict data, dict error_info, int request_id, bool is_last) {};

    virtual void onQueryStructuredFund(dict data, dict error_info, int request_id, bool is_last) {};

    virtual void onQueryFundTransfer(dict data, dict error_info, int request_id, bool is_last) {};

    virtual void onFundTransfer(dict data, dict error_info) {};

    virtual void onQueryETF(dict data, dict error_info, int request_id, bool is_last) {};

    virtual void onQueryETFBasket(dict data, dict error_info, int request_id, bool is_last) {};

    virtual void onQueryIPOInfoList(dict data, dict error_info, int request_id, bool is_last) {};

    virtual void onQueryIPOQuotaInfo(dict data, dict error_info, int request_id, bool is_last) {};

    //-------------------------------------------------------------------------------------
    //req:主动函数的请求字典
    //-------------------------------------------------------------------------------------
    void CreateTradeApi(uint64_t client_id, string save_file_path);

    void Release();

    void init();

    // uint64_t join();

    uint64_t exit();

    void RegisterSpi();

    void SetSoftwareVersion(string version);

    void SetSoftwareKey(string key);

    dict GetApiLastError();

    string GetTradingDay();

    string GetApiVersion();

    uint8_t GetClientIDByXTPID(uint64_t order_xtp_id);

    string GetAccountByXTPID(uint64_t order_xtp_id);

    void SubscribePublicTopic(dict req);

    uint64_t Login(dict req);

    uint64_t Logout(uint64_t session_id);

    uint64_t InsertOrder(dict req, uint64_t session_id);

    uint64_t CancelOrder(const uint64_t order_xtp_id, uint64_t session_id);

    uint64_t FundTransfer(dict req, uint64_t session_id);

    int QueryOrderByXTPID(const uint64_t order_xtp_id, uint64_t session_id, int request_id);

    int QueryOrders(dict req, uint64_t session_id, int request_id);

    int QueryTradesByXTPID(const uint64_t order_xtp_id, uint64_t session_id, int request_id);

    int QueryTrades(dict req, uint64_t session_id, int request_id);

    int QueryPosition(dict req, uint64_t session_id, int request_id);

    int QueryAsset(uint64_t session_id, int request_id);

    int QueryStructuredFund(dict req, uint64_t session_id, int request_id);

    int QueryFundTransfer(dict req, uint64_t session_id, int request_id);

    int QueryETF(dict req, uint64_t session_id, int request_id);

    int QueryETFTickerBasket(dict req, uint64_t session_id, int request_id);

    int QueryIPOInfoList(uint64_t session_id, int request_id);

    int QueryIPOQuotaInfo(uint64_t session_id, int request_id);

//-------------------------------------------------------------------------------------
//同步测试接口
//-------------------------------------------------------------------------------------

    dict QueryOrderByXTPIDSync(const uint64_t order_xtp_id, uint64_t session_id, int request_id);

    dict QueryOrdersSync(dict req, uint64_t session_id, int request_id);

    dict QueryTradesByXTPIDSync(const uint64_t order_xtp_id, uint64_t session_id, int request_id);

    dict QueryTradesSync(dict req, uint64_t session_id, int request_id);

    dict QueryPositionSync(dict req, uint64_t session_id, int request_id);

    dict QueryAssetSync(uint64_t session_id, int request_id);

    dict QueryStructuredFundSync(dict req, uint64_t session_id, int request_id);

    dict QueryFundTransferSync(dict req, uint64_t session_id, int request_id);

    dict QueryETFSync(dict req, uint64_t session_id, int request_id);

    dict QueryETFTickerBasketSync(dict req, uint64_t session_id, int request_id);

    dict QueryIPOInfoListSync(uint64_t session_id, int request_id);

    dict QueryIPOQuotaInfoSync(uint64_t session_id, int request_id);

};
