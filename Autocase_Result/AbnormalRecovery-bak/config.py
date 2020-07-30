# -*- encoding: utf-8 -*-
import random

########################################################
# 配置文件
#
# 行情服务器的交易服务器的配置
#
# 使用示例:
#   from config import Config
#
#   ip = Config.quote.ip
#   port = Config.quote.port
#   print ip + ':' + str(port)
#
#   all = Config.trade.all()
#   print all
#
########################################################

from attribute import Attribute

########################################################
# 交易服务器配置
#
# Config.trade.client_id
# CONST_TRADE_CLIENT_ID = {'id1':278,'id2':279,'id3':280,'id4':281,'id5':282,'id6':283,'id7':284,'id8':285,'id9':286,'id10':287}
CONST_TRADE_CLIENT_ID = 77            # 客户端 id
# Config.trade.save_file_path
CONST_TRADE_SAVE_FILE_PATH = '/dev/null'   # 存贮订阅信息文件的目录
# Config.trade.ip
CONST_TRADE_IP = '10.29.182.38'    # 服务器地址
# Config.trade.port
CONST_TRADE_PORT = 8012            # 端口号
# Config.trade.name
CONST_TRADE_USER = 'testshopt01tgt'          # 帐号
# Config.trade.password
CONST_TRADE_PASSWORD = '123456'     # 密码MNouK4xbWi  STZl0lp7QS
# Config.trade.sock_type
CONST_TRADE_SOCK_TYPE = 1           # 传输方式  1: 采用TCP方式传输,  2: 采用UDP方式传输
# Config.trade.auto_login
CONST_TRADE_AUTO_LOGIN = True       # 是否自动登录
# Config.trade.key
CONST_TRADE_KEY = "b8aa7173bba3470e390d787219b2112e"    #  f11dcc367a5963df20be15408df9a86c d85222c3bbce4f1ea013b7406012bd51   1be803b8d12d6926f422b4d75f61b529
#CONST_TRADE_KEY = "d85222c3bbce4f1ea013b7406012bd51"    #  f11dcc367a5963df20be15408df9a86c d85222c3bbce4f1ea013b7406012bd51   1be803b8d12d6926f422b4d75f61b529

# ORDER_CLIENT_ID = random.randint(1,4) # 1-初始 2-未成交 3-部成 4-全成

########################################################
# 行情服务器配置
#
# Config.quote.client_id
CONST_QUOTE_CLIENT_ID = {'id1':168,'id2':169,'id3':170,'id4':171,'id5':172,'id6':173,'id7':174,'id8':175,'id9':176,'id10':177
                         ,'id11': 158, 'id12': 159, 'id13': 160, 'id14': 161, 'id15': 162, 'id16': 163, 'id17': 164, 'id18': 165,'id19': 166, 'id20': 167,
                         'id21': 157, 'id22': 156, 'id23': 155, 'id24': 154, 'id25': 153, 'id26': 152, 'id27': 151, 'id28': 150, 'id29': 149, 'id30': 148}
# CONST_QUOTE_CLIENT_ID = 278          # 客户端 id
# Config.quote.save_file_path
CONST_QUOTE_SAVE_FILE_PATH = '/home/yhl2/workspace/xtp_test/Quote'   # 存贮订阅信息文件的目录
# Config.quote.ip
CONST_QUOTE_IP = '10.25.24.48'   # 服务器地址
# Config.quote.port
CONST_QUOTE_PORT = 6662             # 端口号
# Config.quote.name
CONST_QUOTE_USER = 'xtp_intr'          # 帐号 xtp_intr testshopt01tgt/123456
# Config.quote.password
CONST_QUOTE_PASSWORD = '123456'     # 密码 #zts_xtp_1.0#  MNouK4xbWi
# Config.quote.sock_type
CONST_QUOTE_SOCK_TYPE = 1           # 传输方式  1: 采用TCP方式传输,  2: 采用UDP方式传输

CONST_QUOTE_AUTO_LOGIN = False       # 是否自动登录


########################################################
#
# 配置信息结束
#
########################################################


########################################################
# 配置类
#
class Config:
    # 行情
    quote = Attribute({
            'client_id': CONST_QUOTE_CLIENT_ID,
            'save_file_path': CONST_QUOTE_SAVE_FILE_PATH,
            'ip': CONST_QUOTE_IP,
            'port': CONST_QUOTE_PORT,
            'user': CONST_QUOTE_USER,
            'password': CONST_QUOTE_PASSWORD,
            'sock_type': CONST_QUOTE_SOCK_TYPE,
            'auto_login': CONST_QUOTE_AUTO_LOGIN
        })

    # 交易
    trade = Attribute({
            'client_id': CONST_TRADE_CLIENT_ID,
            'save_file_path': CONST_TRADE_SAVE_FILE_PATH,
            'ip': CONST_TRADE_IP,
            'port': CONST_TRADE_PORT,
            'user': CONST_TRADE_USER,
            'password': CONST_TRADE_PASSWORD,
            'sock_type': CONST_TRADE_SOCK_TYPE,
            'auto_login': CONST_TRADE_AUTO_LOGIN,
            'key': CONST_TRADE_KEY
        })

    # --------------------------------------------------
    def __init__(self):
        """Constructor"""
        raise NotImplementedError()

# 异常恢复测试使用的用户名配置
def config_trade(username):
    """
    根据用户名返回一个用户配置
    :param username:用户名
    :return:
    """
    user_config = {
            'client_id': CONST_TRADE_CLIENT_ID,
            'save_file_path': CONST_TRADE_SAVE_FILE_PATH,
            'ip': CONST_TRADE_IP,
            'port': CONST_TRADE_PORT,
            'user': username,
            'password': CONST_TRADE_PASSWORD,
            'sock_type': CONST_TRADE_SOCK_TYPE,
            'auto_login': CONST_TRADE_AUTO_LOGIN,
            'key': CONST_TRADE_KEY
        }
    return user_config

# 异常恢复测试使用的用户名配置,
# 定义包含所有用户配置的列表,可以配置任意数量用户
ALL_USER = [
    config_trade('testshopt01tgt')
]

ALL_USER_OPTION = [
    config_trade('testshopt01'),
    config_trade('testshopt02')
]


