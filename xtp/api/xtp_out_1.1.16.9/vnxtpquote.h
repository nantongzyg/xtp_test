
//说明部分

//系统
#ifdef WIN32
#include "stdafx.h"
#endif
#include <string>
#include <queue>

//Boost
#define BOOST_PYTHON_STATIC_LIB
#include <boost/python/module.hpp>    //python封装
#include <boost/python/def.hpp>        //python封装
#include <boost/python/dict.hpp>    //python封装
#include <boost/python/object.hpp>    //python封装
#include <boost/python.hpp>            //python封装
#include <boost/thread.hpp>            //任务队列的线程功能
#include <boost/bind.hpp>            //任务队列的线程功能
#include <boost/any.hpp>            //任务队列的任务实现

//API
#include "xtp_quote_api.h"

//命名空间
using namespace std;
using namespace boost::python;
using namespace boost;

//常量

#define ONDISCONNECTED 1
#define ONERROR 2
#define ONSUBMARKETDATA 3
#define ONUNSUBMARKETDATA 4
#define ONDEPTHMARKETDATA 5
#define ONSUBORDERBOOK 6
#define ONUNSUBORDERBOOK 7
#define ONORDERBOOK 8
#define ONSUBTICKBYTICK 9
#define ONUNSUBTICKBYTICK 10
#define ONTICKBYTICK 11
#define ONSUBSCRIBEALLMARKETDATA 12
#define ONUNSUBSCRIBEALLMARKETDATA 13
#define ONSUBSCRIBEALLORDERBOOK 14
#define ONUNSUBSCRIBEALLORDERBOOK 15
#define ONSUBSCRIBEALLTICKBYTICK 16
#define ONUNSUBSCRIBEALLTICKBYTICK 17
#define ONQUERYALLTICKERS 18
#define ONQUERYTICKERSPRICEINFO 19

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
    int task_name;        //回调函数名称对应的常量
    any task_data;        //数据结构体
    any task_error;        //错误结构体
    int task_id;        //请求id
    bool task_last;        //是否为最后返回
};


///线程安全的队列
template<typename Data>
class ConcurrentQueue {
private:
    queue<Data> the_queue;                                //标准库队列
    mutable mutex the_mutex;                            //boost互斥锁
    condition_variable the_condition_variable;            //boost条件变量

public:

    //存入新的任务
    void push(Data const& data) {
        mutex::scoped_lock lock(the_mutex);                //获取互斥锁
        the_queue.push(data);                            //向队列中存入数据
        lock.unlock();                                    //释放锁
        the_condition_variable.notify_one();            //通知正在阻塞等待的线程
    }

    //检查队列是否为空
    bool empty() const {
        mutex::scoped_lock lock(the_mutex);
        return the_queue.empty();
    }

    //取出
    Data wait_and_pop() {
        mutex::scoped_lock lock(the_mutex);

        while (the_queue.empty()) {                    //当队列为空时
            the_condition_variable.wait(lock);            //等待条件变量通知
        }

        Data popped_value = the_queue.front();            //获取队列中的最后一个任务
        the_queue.pop();                                //删除该任务
        return popped_value;                            //返回该任务
    }

};


//从字典中获取某个建值对应的整数，并赋值到请求结构体对象的值上
void getInt(dict d, string key, int* value);


//从字典中获取某个建值对应的浮点数，并赋值到请求结构体对象的值上
void getDouble(dict d, string key, double* value);


//从字典中获取某个建值对应的字符串，并赋值到请求结构体对象的值上
void getChar(dict d, string key, char* value);


///-------------------------------------------------------------------------------------
///C++ SPI的回调函数方法实现
///-------------------------------------------------------------------------------------

//API的继承实现
class xtpQuoteApi : public XTP::API::QuoteSpi {
private:
    bool running;
    XTP::API::QuoteApi* api;            //API对象
    thread *task_thread;                //工作线程指针（向python中推送数据）
    ConcurrentQueue<Task> task_queue;    //任务队列

    dict QueryAllTickers_data_;
    boost::atomic< bool > QueryAllTickers_sync_;
    boost::mutex QueryAllTickers_mutex_;
    boost::condition_variable QueryAllTickers_cond_var_;

    dict QueryTickersPriceInfo_data_;
    boost::atomic< bool > QueryTickersPriceInfo_sync_;
    boost::mutex QueryTickersPriceInfo_mutex_;
    boost::condition_variable QueryTickersPriceInfo_cond_var_;

    dict QueryAllTickersPriceInfo_data_;
    boost::atomic< bool > QueryAllTickersPriceInfo_sync_;
    boost::mutex QueryAllTickersPriceInfo_mutex_;
    boost::condition_variable QueryAllTickersPriceInfo_cond_var_;

public:
    xtpQuoteApi() {
        function0<void> f = boost::bind(&xtpQuoteApi::processTask, this);
        thread t(f);
        this->task_thread = &t;

        running = true;

        QueryAllTickers_sync_ = false;

        QueryTickersPriceInfo_sync_ = false;

        QueryAllTickersPriceInfo_sync_ = false;

    };

    ~xtpQuoteApi() {
        running = false;
    };


    //-------------------------------------------------------------------------------------
    //API回调函数
    //-------------------------------------------------------------------------------------

    virtual void OnDisconnected(int reason);

    virtual void OnError(XTPRI * error_info);

    virtual void OnSubMarketData(XTPST * ticker, XTPRI * error_info, bool is_last);

    virtual void OnUnSubMarketData(XTPST * ticker, XTPRI * error_info, bool is_last);

    virtual void OnDepthMarketData(XTPMD * market_data, int64_t bid1_qty[], int32_t bid1_count, int32_t max_bid1_count, int64_t ask1_qty[], int32_t ask1_count, int32_t max_ask1_count);

    virtual void OnSubOrderBook(XTPST * ticker, XTPRI * error_info, bool is_last);

    virtual void OnUnSubOrderBook(XTPST * ticker, XTPRI * error_info, bool is_last);

    virtual void OnOrderBook(XTPOB * order_book);

    virtual void OnSubTickByTick(XTPST * ticker, XTPRI * error_info, bool is_last);

    virtual void OnUnSubTickByTick(XTPST * ticker, XTPRI * error_info, bool is_last);

    virtual void OnTickByTick(XTPTBT * tbt_data);

    virtual void OnSubscribeAllMarketData(XTPRI * error_info);

    virtual void OnUnSubscribeAllMarketData(XTPRI * error_info);

    virtual void OnSubscribeAllOrderBook(XTPRI * error_info);

    virtual void OnUnSubscribeAllOrderBook(XTPRI * error_info);

    virtual void OnSubscribeAllTickByTick(XTPRI * error_info);

    virtual void OnUnSubscribeAllTickByTick(XTPRI * error_info);

    virtual void OnQueryAllTickers(XTPQSI * ticker_info, XTPRI * error_info, bool is_last);

    virtual void OnQueryTickersPriceInfo(XTPTPI * ticker_info, XTPRI * error_info, bool is_last);

    //-------------------------------------------------------------------------------------
    //task：任务
    //-------------------------------------------------------------------------------------
    void processTask();

    void processDisconnected(Task task);

    void processError(Task task);

    void processSubMarketData(Task task);

    void processUnSubMarketData(Task task);

    void processDepthMarketData(Task task);

    void processSubOrderBook(Task task);

    void processUnSubOrderBook(Task task);

    void processOrderBook(Task task);

    void processSubTickByTick(Task task);

    void processUnSubTickByTick(Task task);

    void processTickByTick(Task task);

    void processSubscribeAllMarketData(Task task);

    void processUnSubscribeAllMarketData(Task task);

    void processSubscribeAllOrderBook(Task task);

    void processUnSubscribeAllOrderBook(Task task);

    void processSubscribeAllTickByTick(Task task);

    void processUnSubscribeAllTickByTick(Task task);

    void processQueryAllTickers(Task task);

    void processQueryTickersPriceInfo(Task task);

    //-------------------------------------------------------------------------------------
    //data：回调函数的数据字典
    //error：回调函数的错误字典
    //id：请求id
    //last：是否为最后返回
    //i：整数
    //-------------------------------------------------------------------------------------

    virtual void onDisconnected(int reason) {};

    virtual void onError(dict data, int id, bool last) {};

    virtual void onSubMarketData(dict data, dict error, bool last) {};

    virtual void onUnSubMarketData(dict data, dict error, bool last) {};

    virtual void onDepthMarketData(dict data) {};

    virtual void onSubOrderBook(dict data, dict error, bool last) {};

    virtual void onUnSubOrderBook(dict data, dict error, bool last) {};

    virtual void onOrderBook(dict data) {};

    virtual void onSubTickByTick(dict data, dict error, bool last) {};

    virtual void onUnSubTickByTick(dict data, dict error, bool last) {};

    virtual void onTickByTick(dict data) {};

    virtual void onSubscribeAllMarketData(dict error) {};

    virtual void onUnSubscribeAllMarketData(dict error) {};

    virtual void onSubscribeAllOrderBook(dict error) {};

    virtual void onUnSubscribeAllOrderBook(dict error) {};

    virtual void onSubscribeAllTickByTick(dict error) {};

    virtual void onUnSubscribeAllTickByTick(dict error) {};

    virtual void onQueryAllTickers(dict data, dict error, bool last) {};

    virtual void onQueryTickersPriceInfo(dict data, dict error, bool last) {};

    //-------------------------------------------------------------------------------------
    //req:主动函数的请求字典
    //-------------------------------------------------------------------------------------
    void CreateQuoteApi(int client_id, string save_file_path, int log_level);

    void Release();

    int Exit();

    string GetTradingDay ();

    string GetApiVersion();

    dict GetApiLastError();
    
    void SetUDPBufferSize(uint32_t buff_size);

    int Login(dict req);

    int Logout();

    int SubscribeMarketData(dict req);

    int UnSubscribeMarketData(dict req);

    int SubscribeOrderBook(dict req);

    int UnSubscribeOrderBook(dict req);

    int SubscribeTickByTick(dict req);

    int UnSubscribeTickByTick(dict req);

    int SubscribeAllMarketData();

    int UnSubscribeAllMarketData();

    int SubscribeAllOrderBook();

    int UnSubscribeAllOrderBook();

    int SubscribeAllTickByTick();

    int UnSubscribeAllTickByTick();

    int QueryAllTickers(dict req);

    int QueryTickersPriceInfo(dict req);

    int QueryAllTickersPriceInfo();

    //-------------------------------------------------------------------------------------
    //同步测试接口
    //-------------------------------------------------------------------------------------

    dict QueryAllTickersSync(dict req);

    dict QueryTickersPriceInfoSync(dict req);

    dict QueryAllTickersPriceInfoSync();

};
