#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
import time
from collections import defaultdict
sys.path.append('/home/yhl2/workspace/xtp_test/xtp/api')
import config
import logging
from random import randint
#---------------------------------------------费率配置------------------------------------
#股票etf买卖
#买入费率
FEE_RATE_BUY = 0.003
#卖出费率
FEE_RATE_SELL = 0.003
#最少收费
FEE_MIN = 5

#买入费率
FEE_RATE_ETF_CREATION = 0.0005
#卖出费率
FEE_RATE_ETF_REDEMPTION = 0.0005
#最少收费
FEE_ETF_MIN = 6

#逆回购费率
FEE_RATE_REVERSE_REPO = 0.002
#最少收费
FEE_REVERSE_REPO_MIN = 3

# 分级基金申购手续费
FEE_RATE_STRUCTURED_FUND_CREATION = 0.002
FEE_RATE_STRUCTURED_FUND_REDEMPTION = 0.002
FEE_MIN_STRUCTURED_FUND_CREATION_REDEMPTION = 10

# 个股期权费用设置
FEE_RATE_OPTION_BUY_OPEN = 1.6
FEE_RATE_OPTION_SELL_CLOSE = 1.6
FEE_RATE_OPTION_SELL_OPEN = 1.6
FEE_RATE_OPTION_BUY_CLOSE = 1.6
FEE_RATE_OPTION_EXECUTE = 0.6

#---------------------------------------------etf持仓成本保留小数位---------------------------
AVG_PRICE_DECIMALPLACES=3

#---------------------------------------------个股期权持仓成本保留小数位---------------------------
AVG_PRICE_DECIMALPLACES_OPTION=4

# 分级基金申购预扣价格
STRUCTURED_FUND_CREATION_PRICE = 1

#分级基金测赎回随机获取代码时，不能取下列代码，这几个代码固定用于几个case作测试。
stock_code_black_list = ('168201', '168203', '168204', '168205')
#---------------------------------------------日志信息配置--------------------------------
#设置日志显示级别
#日志级别大小关系为：CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET
LEVEL={
    'NOTSET':logging.NOTSET,
    'INFO':logging.INFO,
    'DEBUG':logging.DEBUG,
    'WARNING':logging.WARNING,
    'ERROR':logging.ERROR,
    'CRITICAL':logging.CRITICAL
}
#设置日志文件的级别
LEVEL_FILE=LEVEL['WARNING']
#设置控制台日志的级别
LEVEL_console=LEVEL['WARNING']
#设置日志保存路径
LOGPATH='/home/yhl2/workspace/xtp_test/log/'

#-------------------------------------------等待时间设置---------------------------------
#根据不同的状态设置不一样的用例超时时间
TIMEPENDING={
    'DEFAULT':3,
    'CHUSHI':30,
    'WEICHENGJIAO':120,
    'BUCHENG':10,
    'QUANCHENG':60,
    'YICHE':10,
    'BUCHE':30,
    'FEIDAN':10,
    'NEIBUCHEDAN':30,
    'YIBAODAICHE':30,
    'BUCHEYIBAO':30,
    'CHEFEI':4,
    'CREATION':500,
    'REDEMPTION':500
}

# 验资验券case随机生成成交模式
# 1-未成交 2-全成 3-部成
trade_type = randint(0, 2)

trade_type_allpart = randint(0, 1)

#-------------成交次数（全成或部成累计分笔成交次数）-----
MATCHTIMES=1


#-----------------------------------------match type=EqualHigh开市与休市配置-----
#当前是否为交易所休市，True是，False不是
IS_EXCHANGE_CLOSE=False
#深Amatch配置,当IS_EXCHANGE_CLOSE＝True时，以下配置不起作用
#开市时间：0-9秒，20-29秒，40-49秒
TIME_MARKET_OPEN=((0,9),(20,29),(40,49))
#开市时间第4秒开始：4-9秒，24-29秒，44-49秒
TIME_MARKET_OPEN_FOUR_SEC=((5,9),(25,29),(45,49))
#休市时间：10-19秒,30-39秒,50-59秒
TIME_MARKET_CLOSE=((10,19),(30,39),(50,59))
#延时时间，单位‘秒’。注：下委托的服务器时间和offer和match程序所在的服务器时间存在误差
TIME_DELAY=3


#-------------------------------------------（卖）委托上下限数量设置---------------------------------
#买卖最大委托数量
MAX_QTY=1000000
#分级基金赎回最大委托数量
MAX_QTY_STRUCTURED_FUND_CREATION=10000000000
#最大委托数量,测T+0Sell_HavePosition用到
MAX_QTY_HAVE_POSITION=500000
#最小委托数量－部成,部撤,部撤已报
PART_MIN_QTY=200
#最小委托数量－其它
ORTHER_MIN_QTY=1

#---------------------------------------------期望状态为废单时，是否校验errID,err_msg-----------------------
#False 不校验；True　校验
#（报单推送）是否校验errID和err_msg
IS_CHECK_ERRID_FROM_BDTS=True
IS_CHECK_ERR_MSG_FROM_BDTS=True
#(报单查询)是否校验errID和err_msg
IS_CHECK_ERRID_FROM_BDQUERY=False
IS_CHECK_ERRMSG_FROM_BDQUERY=False

#---------------------------------------------期望状态为撤废时，是否校验err_msg-----------------------
IS_CHECK_ERRMSG_FROM_CANCELERR=True


#-------------------------------------------是否校验上海的撮合价格（成交回报价格应该是在跌停和涨停之间，但撮合实际是１块钱)----------
#False 不校验，True　校验
IS_CHECK_HA_HB_PRICE=False

#-------------------------------------------验资验券测试使用证券代码设置--------------------------------
#沪A
STK_CODE_HA = '600006'
#深A
STK_CODE_SA = '000002'

#-------------------------------------------ETF申购单位数设置--------------------------------
CREATION_QUANTITY = 1
REDEMPTION_QUANTITY = 1

ETF_CODE_HA = '510880'
ETF_CODE_SA = '159906'

#-------------------------------------逆回购成交价格------------------------------------------------
Reverse_price = 100

# etf资金成交回报数量定义，若成交金额小于ETF_FUND_AMOUNT元，则返回一条资金回报，数量为1。
# 否则返回两条资金回报，数量分别为1,1000000,对应的资金分别为小于1000元和1000的整数倍。
ETF_FUND_QUANTITY_MIN = 1
ETF_FUND_QUANTITY_MAX = 1000000

ETF_FUND_AMOUNT = 1000


# num = str(config.CONST_TRADE_PORT)[-1]
portnum = str(config.CONST_TRADE_PORT)
if portnum[-2] == '0':
    num = portnum[-1]
else:
    num = portnum[-2:]


# oms机器连接信息
login_info = {
    #'ip': '10.26.134.198',
    'ip': '10.29.181.88',
    'port': 22,
    'user_name': 'xtp' + num,
    'password': 'xtp' + num,
}

# 上海环境重启
#win 197环境
# restart_path_sh = [
#             'http://10.26.134.197:8080/localexec?dir=xtptest/match_sh/match_sh' + num + '&execfile=KILL_MATCH_SH' + num + '.bat',
#             'http://10.26.134.197:8080/localexec?dir=xtptest/match_sh/match_sh' + num + '&execfile=MATCH_SH' + num + '.bat',
#             'http://10.26.134.197:8080/localexec?dir=xtptest/xogwsh/xogwsh'+ num +'/stop&execfile=stopogwsh' + num + '.bat',
#             'http://10.26.134.197:8080/localexec?dir=xtptest/xogwsh/xogwsh'+ num +'/start&execfile=startogwsh' + num + '.bat',
#         ]
#自动化win 环境79
restart_path_sh = [
            'http://10.29.181.79:8080/localexec?dir=xtptest/match_sh/match_sh' + num + '&execfile=KILL_MATCH_SH' + num + '.bat',
            'http://10.29.181.79:8080/localexec?dir=xtptest/match_sh/match_sh' + num + '&execfile=MATCH_SH' + num + '.bat',
            #'http://10.29.181.79:8080/localexec?dir=xtptest/xogwsh/xogwsh'+ num +'/stop&execfile=stopogwsh' + num + '.bat',
            'http://10.29.181.79:8080/localexec?dir=xtptest/xogwsh/xogwsh'+ num +'/start&execfile=startogwsh' + num + '.bat',
        ]

# 深圳环境重启
sz_cmds = [
    'cd /home/xtp' + num + '/shell/;source /home/xtp' + num + '/.bash_profile;sh stopall.sh',
    'cd /home/xtp' + num + '/shell/;source /home/xtp' + num + '/.bash_profile;sh startall.sh',
    'cd /home/xtp' + num + '/shell/;source /home/xtp' + num + '/.bash_profile;sh startall.sh xoms',
    'cd /home/xtp' + num + '/shell/;source /home/xtp' + num + '/.bash_profile;sh showall.sh',
]

# oms重启
oms_cmds = [
    'cd /home/xtp' + num + '/shell/;source /home/xtp' + num + '/.bash_profile;sh stopall.sh xoms',
    'cd /home/xtp' + num + '/shell/;source /home/xtp' + num + '/.bash_profile;sh startall.sh xoms',
    'cd /home/xtp' + num + '/shell/;source /home/xtp' + num + '/.bash_profile;sh showall.sh',
]

# oms关闭服务
oms_stop_cmds = 'cd /home/xtp' + num + '/shell/;source /home/xtp' + num + '/.bash_profile;sh stopall.sh xoms'

# 深圳match数据文件路径
match_data_path = 'cd /home/xtp' + num + '/match/data;rm -rf *' + time.strftime('%Y%m%d', time.localtime(time.time())) + '*'

# 深圳ogw数据文件路径
ogw_data_path = 'cd /home/xtp' + num + '/xogwsz/data;rm -rf *' + time.strftime('%Y%m%d', time.localtime(time.time())) + '*'

# oms启动失败报出的错误信息
oms_error_msg = 'xoms            :  is  \x1b[7moffline\x1b[0m\n'

#上海需要清除的接口库表名
truncate_tables_sh = [
    'ashare_cjhb',
    'ashare_ordwth',
    'ashare_ordwth2',
    'reqresp',
    'execreport',
    'ashare_ordwth_cancel'
]
# 修改本地的oms文件后，再上传到oms服务器
# oms目标路径
omsDstDir = '/home/xtp' + num + '/xoms/config/xoms.xml'
# match目标路径
matchDstDir = '/home/xtp' + num + '/match/config/match_src.xml'
# 修改后的oms源文件路径
srcFileAfterUpdate = '/home/yhl2/workspace/xtp_test/utils/xoms.xml'
# 修改前的oms源路径
srcFileBeforeUpdate = '/home/yhl2/workspace/xtp_test/utils/xoms_src.xml'

# 修改后的match源文件路径
srcMatchAfterUpdate = '/home/yhl2/workspace/xtp_test/utils/match.xml'
# 修改前的match源路径
srcMatchBeforeUpdate = '/home/yhl2/workspace/xtp_test/utils/match_src.xml'

# oms配置文件中分级基金费用各配置项
fee_min_structured_fund_creation_redemption_str = 3003
fee_rate_structured_fund_creation_str = 3001
fee_rate_structured_fund_redemption_str = 3002

# 分级基金申赎费用修改配置，通过以下配置，修改oms服务器上的费用设置
fee_structured_fund_creation_redemption = defaultdict(lambda: '')
fee_structured_fund_creation_redemption = {
    'YW_FJJJ_SZSS_007':
        {3003: '10',
         3001: '0.002',
         3002: '0.002'},
    'YW_FJJJ_SZSS_030':
        {3003: '0',
         3001: '0.00005',
         3002: '0.00005'},
    'YW_FJJJ_SZSS_031':
        {3003: '0',
         3001: '0.00006',
         3002: '0.00006'},
    'YW_FJJJ_SZSS_032':
        {3003: '0',
         3001: '0.00004',
         3002: '0.00004'},
    'YW_FJJJ_SZSS_039':
        {3003: '10',
         3001: '0.002',
         3002: '0.002'},
    'YW_FJJJ_SZSS_060':
        {3003: '0',
         3001: '0.00005',
         3002: '0.00005'},
    'YW_FJJJ_SZSS_061':
        {3003: '0',
         3001: '0.00006',
         3002: '0.00006'},
    'YW_FJJJ_SZSS_062':
        {3003: '0',
         3001: '0.00004',
         3002: '0.00004'},
}

# oms配置文件中etf费用各配置项
fee_etf_min_str = 4003
fee_rate_etf_creation_str = 4001
fee_rate_etf_redemption_str = 4002

# ETF申赎费用修改配置，通过以下配置，修改oms服务器上的费用设置
fee_etf_creation_redemption = defaultdict(lambda: '')
fee_etf_creation_redemption = {
    'YW_ETFSS_SHSG_059':
        {4003: '500',
         4001: '0.0005',
         4002: '0.0005'},
    'YW_ETFSS_SHSG_065_2':
        {4003: '5',
         4001: '0.0005',
         4002: '0.0005'},
    'YW_ETFSS_SHSH_040':
        {4003: '500',
         4001: '0.0005',
         4002: '0.0005'},
    'YW_ETFSS_SHSH_046_2':
        {4003: '5',
         4001: '0.0005',
         4002: '0.0005'},
    'YW_ETFSS_SZSG_058':
        {4003: '500',
         4001: '0.0005',
         4002: '0.0005'},
    'YW_ETFSS_SZSG_064_2':
        {4003: '5',
         4001: '0.0005',
         4002: '0.0005'},
    'YW_ETFSS_SZSH_041':
        {4003: '500',
         4001: '0.0005',
         4002: '0.0005'},
    'YW_ETFSS_SZSH_047_2':
        {4003: '5',
         4001: '0.0005',
         4002: '0.0005'},
}

