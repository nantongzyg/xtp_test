#!/usr/bin/python
# -*- encoding: utf-8 -*-

import xlrd
import sys
from templet import *
import collections
import os
import logging

reload(sys)
sys.setdefaultencoding('utf-8')


def list_todict(l1, l2):
    ###两个list打包成一个dict
    return dict(zip(l1, l2))


def encode_dict_value(D1):
    # 对字典的value值进行编码，处理成想要的格式。
    # case_type -1:不生成模板 0：正常模板 2：错误的证券代码 3：改oms配置文件，并重启环境
    # 4：清上海接口库，改资金，重启环境 5：清深圳接口库，改资金，重启环境
    D2 = collections.OrderedDict()
    # 不取对象外的case
    if D1['对象'].encode('utf-8') != '-':
        if int(D1['case_type']) != -1:
            D2['pyname'] = D1['pyname'].encode('utf-8')
            D2['stkcode'] = str(D1['stkcode']).encode('utf-8')
            if D2['stkcode'] == '0.0':
                D2['stkcode'] = ''
            elif D2['stkcode'].endswith('.0'):
                D2['stkcode'] = D2['stkcode'][0:-2]
            else:
                pass

            if len(D2['stkcode']) < 6 and D2['stkcode'] != '':
                D2['stkcode'] = D2['stkcode'].zfill(6)

            D2['market'] = str(int(D1['market']))
            D2['errorID'] = int(D1['errorID'])
            D2['errorMSG'] = D1['errorMSG'].encode('utf-8')
            D2['case_type'] = int(D1['case_type'])
        else:
            D2['pyname'] = D1['pyname'].encode('utf-8')
            D2['case_type'] = int(D1['case_type'])
    else:
        D2['pyname'] = ''
        D2['case_type'] = 0

    return D2

def pyname_seq(D1):
    # 对字典的value值进行编码，处理成想要的格式。
    pyname_seq_dict = collections.OrderedDict()
    pyname_seq_dict['pyname'] = D1['pyname'].encode('utf-8')
    if D1['对象'].encode('utf-8') != '-':
        pyname_seq_dict['seq'] = int(D1['seq'])
    # pyname_seq_dict['case_type'] = int(D1['case_type'])
    return pyname_seq_dict

class CaseService():
    def __init__(self,excel_file,sheet_name):
        #self.excel_file = u'股票买卖自动化case参数模板.xlsx'
        excel_rs = self.read_excel(excel_file,sheet_name)
        self.testcase_name_para_dict = excel_rs[0]
        self.testcase_seq_dict = excel_rs[1]
        self.log_file=excel_file+'.log'
        logging.basicConfig(filename=self.log_file, filemode="w",
                            format="%(asctime)s-%(name)s-%(levelname)s-%(message)s",
                            level=logging.INFO)
        self.logger = logging.getLogger("log_demo")

    def read_excel(self, excel_file,sheet_name):
        ###用于读取excel的文件，
        data = xlrd.open_workbook(excel_file, encoding_override='utf-8')
        # 获取一个工作表
        table = data.sheet_by_name(sheet_name)
        # table = data.sheets()[0]
        nrows = table.nrows
        ncols = table.ncols
        title_list = table.row_values(0)
        title_list = map(lambda x: x.encode('utf-8'), title_list)
        # 构造用户一个测试例文件名(pyname)-测试例名参数表
        testcase_name_para_dict = {}
        testcase_seq_dict = {}
        # 循环行列表数据
        for i in range(1, nrows):
            para_list = table.row_values(i)
            para_dict = list_todict(title_list, para_list)
            pyname_seq_dict = pyname_seq(para_dict)
            para_dict = encode_dict_value(para_dict)
            if para_dict['pyname'] != '':
                testcase_name_para_dict[para_dict['pyname']] = para_dict
                testcase_seq_dict[pyname_seq_dict['seq']] = pyname_seq_dict
        return testcase_name_para_dict, testcase_seq_dict

    def gen_allcase(self):
        # 根据excel，生成所有case类
        case_class_dict = {}
        for (d, x) in self.testcase_name_para_dict.items():
            case_class = basecase(d, x)
            case_class_dict[d] = case_class
        return case_class_dict

    def gen_specify(self, case_name):
        # 生成特定的case类
        case_para_dict = self.testcase_name_para_dict[case_name]
        case_class = basecase(case_name, case_para_dict)
        return case_class

    def gen_specify_casepy(self, pyname,casepath):
        #生成casename对应的casepy文件
        #生成参数元组
        try:
            case_para_dict = self.testcase_name_para_dict[pyname]
            case_para_list =list(case_para_dict.values())
            for i in xrange(2):
                case_para_list.insert(0, pyname)
            case_para_tuple=tuple(case_para_list)
            if case_para_tuple[-1] == 0:
                case_str=templet_case_str26 % case_para_tuple
            elif case_para_tuple[-1] == 1:
                case_str=templet_case_str27 % case_para_tuple
            elif case_para_tuple[-1] == 2:
                case_str=templet_case_str28 % case_para_tuple
            elif case_para_tuple[-1] == 3:
                case_str = templet_case_str29 % case_para_tuple
            elif case_para_tuple[-1] == 4:
                case_str = templet_case_str30 % case_para_tuple
            elif case_para_tuple[-1] == 5:
                case_str = templet_case_str31 % case_para_tuple
            elif case_para_tuple[-1] == 6:
                case_str = templet_case_str36 % case_para_tuple
            else:
                pass

            # 不生成模板和对象外的case，都不生成自动化py
            if case_para_tuple[-1] != -1 and case_para_dict != {}:
                Autocasefile=os.path.join('../Autocase_Result', casepath,pyname+'.py')
                with open(Autocasefile, 'w') as f:
                    f.write(case_str)
            self.logger.info("gen_testcase" + pyname + ",success")
        except:
            self.logger.info("gen_testcase" + pyname + ",failed")
        return 0

    def gen_all_casepy(self,casepath):
        #生成excel中所有的casename对应的casepy文件
        flag_list=[]
        for key,value in self.testcase_name_para_dict.items():
            pyname=key
            try:
                self.gen_specify_casepy(pyname,casepath)
            except:
                pass


class basecase():
    def __init__(self, case_name, case_para):
        # 根据case名，case参数生成测试例实例
        self.case_name = case_name
        self.case_para = case_para

    def print_result(self):
        case_goal = {
            '期望状态': self.case_para['期望状态'],
            'errorID': 0,
            'errorMSG': '',
            '是否生成报单': self.case_para['是否生成报单'],
            '是否是撤废': self.case_para['是否是撤废'],
            'xtp_ID': 0,
            'cancel_xtpID':0,
        }
        stkparm = (
            self.case_para['stkcode'], self.case_para['market'], self.case_para['security_type'],
            self.case_para['security_status'], self.case_para['trade_status'], self.case_para['bsflag'])
        wt_reqs = {
            'business_type': self.case_para['business_type'],
            'market': self.case_para['market_wt'],
            'ticker': 000000,
            'side': self.case_para['side'],
            'price_type': self.case_para['price_type'],
            'price': self.case_para['price'],
            'quantity': self.case_para['quantity']
        }
        case_goal2 = {
            '期望状态': '全成',
            'errorID': 0,
            'errorMSG': '',
            '是否生成报单': '是',
            '是否是撤废': '否',
            'xtp_ID': 0,
            'cancel_xtpID': 0,
        }
        wt_reqs2 = {
            'business_type': 'XTP_BUSINESS_TYPE_CASH',
            'market': 'XTP_MKT_SZ_A',
            'ticker': 000000,
            'side': 'XTP_SIDE_BUY',
            'price_type': 'XTP_PRICE_LIMIT',
            'price': '随机中间价',
            'quantity': 200
        }
        stkparm2 = ('999999', '2', '0', '2', '0', 'B')

        title = self.case_para['title']
        title2 = '深圳Ａ股股票限价买入全成测试'

    def test_B_XJ_SA_GP(self):
        # title = '深圳Ａ股股票限价买入全成测试'
        title = self.case_para['title']
        # 定义当前测试用例的期待值
        # 期望状态：初始、未成交、部成、全成、部撤已报、部撤、已报待撤、已撤、废单、撤废、内部撤单
        # xtp_ID和cancel_xtpID默认为0，不需要变动
        case_goal = {
            '期望状态': self.case_para['期望状态'],
            'errorID': int(self.case_para['errorID']),
            'errorMSG': str(self.case_para['errorMSG']),
            '是否生成报单': self.case_para['是否生成报单'],
            '是否是撤废': self.case_para['是否是撤废'],
            'xtp_ID': self.case_para['xtp_ID'],
            'cancel_xtpID': self.case_para['cancel_xtpID'],
        }
        # 定义委托参数信息------------------------------------------
        # 参数：证券代码、市场、证券类型、证券状态、交易状态、买卖方向（Ｂ买Ｓ卖）、期望状态、Api
        # stkparm = QueryStkPriceQty('999999', '2', '0', '2', '0', 'B', case_goal['期望状态'], Api)
        stkparm = (self.case_para['stkcode'], self.case_para['market'], self.case_para['security_type'],
                   self.case_para['security_status'], self.case_para['trade_status'], self.case_para['bsflag'])
        # 如果下单参数获取失败，则用例失败
        if False:
            print "k"
        else:
            wt_reqs = {
                'business_type': self.case_para['business_type'],
                'market': self.case_para['market_wt'],
                'ticker': stkparm['证券代码'],
                'side': self.case_para['side'],
                'price_type': self.case_para['price_type'],
                'price': self.case_para['price'],
                'quantity': self.case_para['quantity']
            }


