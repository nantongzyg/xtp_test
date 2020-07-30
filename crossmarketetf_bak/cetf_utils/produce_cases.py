#!/usr/bin/python
# -*- encoding: utf-8 -*-
import xlrd
from cetf_templet import *
import collections
import os
import logging


class produce_cases():

    def __init__(self,excel_file,sheet_name):
        self.excel_file = excel_file
        self.sheet_name = sheet_name
        self.log_file=excel_file+'.log'
        logging.basicConfig(filename=self.log_file, filemode="w",
                            format=("%(asctime)s-%(name)s-" +
                                     "%(levelname)s-%(message)s"),
                            level=logging.INFO)
        self.logger = logging.getLogger("log_demo")

    def read_excel(self):
        """
        用于读取excel的文件
        :param excel_file: excel文件名
        :param sheet_name: sheet页名称
        :return:
        """
        data = xlrd.open_workbook(self.excel_file, encoding_override='utf-8')
        # 获取一个工作表
        table = data.sheet_by_name(self.sheet_name)
        nrows = table.nrows
        # 获取EXCEL第一行内容
        title_list = table.row_values(0)
        title_list = map(lambda x: x.encode('utf-8'), title_list)
        # 构造用户一个测试用例文件名(pyname)为key，参数为value的字典
        testcase_name_para_dict = {}
        # 循环excel表数据，将每一行数据放入testcase_name_para_dict中
        for i in range(1, nrows):
            para_list = table.row_values(i)
            # 将每一行数据与第一行列名组成字典
            para_dict = self.list_todict(title_list, para_list)
            # 将每一行参数字典有序化
            para_dict = self.encode_dict_value(para_dict)
            if para_dict:
                testcase_name_para_dict[para_dict['pyname']] = para_dict
        return testcase_name_para_dict

    def gen_specify_casepy(self, pyname, casepath, case_name_para_dict):
        """
        生成casename对应的casepy文件
        :param pyname: 用例名称
        :param casepath: case的存放路径
        :param case_name_para_dict:
        :return:
        """
        try:
            case_para_dict = case_name_para_dict[pyname]
            case_para_list = list(case_para_dict.values())
            # 用例使用pyname参数个数不相同，先插入两次，后续根据用例情况对参数切片
            for i in range(2):
                case_para_list.insert(0,pyname)
            case_para_tuple=tuple(case_para_list)
            if case_para_tuple[-1] == 1:
                case_str = templet_cetf_str1 % case_para_tuple[:-1]
            elif case_para_tuple[-1] == 2:
                case_str = templet_cetf_str2 % case_para_tuple[1:-1]
            elif case_para_tuple[-1] == 3:
                case_str = templet_cetf_str3 % case_para_tuple[1:-1]
            elif case_para_tuple[-1] == 4:
                case_str = templet_cetf_str4 % case_para_tuple[1:-1]
            elif case_para_tuple[-1] == 5:
                case_str = templet_cetf_str5 % case_para_tuple[:-1]
            elif case_para_tuple[-1] == 6:
                case_para_list.insert(-1,pyname)
                case_para_tuple = tuple(case_para_list)
                case_str = templet_cetf_str6 % case_para_tuple[:-1]
            elif case_para_tuple[-1] == 7:
                case_str = templet_cetf_str7 % case_para_tuple[1:-1]
            elif case_para_tuple[-1] == 8:
                case_str = templet_cetf_str8 % case_para_tuple[1:-1]
            elif case_para_tuple[-1] == 9:
                case_str = templet_cetf_str9 % case_para_tuple[1:-1]
            elif case_para_tuple[-1] == 11:
                case_str = templet_cetf_str11 % case_para_tuple[:-1]
            elif case_para_tuple[-1] == 12:
                case_str = templet_cetf_str12 % case_para_tuple[1:-1]
            elif case_para_tuple[-1] == 13:
                case_str = templet_cetf_str13 % case_para_tuple[1:-1]
            elif case_para_tuple[-1] == 14:
                case_str = templet_cetf_str14 % case_para_tuple[1:-1]
            elif case_para_tuple[-1] == 15:
                case_str = templet_cetf_str15 % case_para_tuple[:-1]
            elif case_para_tuple[-1] == 16:
                case_para_list.insert(0, pyname)
                case_para_list.insert(-1,pyname)
                case_para_tuple = tuple(case_para_list[:-1])
                case_str = templet_cetf_str16 % case_para_tuple
            elif case_para_tuple[-1] == 17:
                case_para_tuple = tuple(case_para_list[1:-1])
                case_str = templet_cetf_str17 % case_para_tuple
            elif case_para_tuple[-1] == 18:
                case_str = templet_cetf_str18 % case_para_tuple[1:-1]
            elif case_para_tuple[-1] == 19:
                case_str = templet_cetf_str19 % case_para_tuple[1:-1]
            elif case_para_tuple[-1] == 20:
                case_str = templet_cetf_str20 % case_para_tuple[1:-1]
            elif case_para_tuple[-1] == 21:
                case_str = templet_cetf_str21 % case_para_tuple[1:-1]
            elif case_para_tuple[-1] == 22:
                case_str = templet_cetf_str22 % case_para_tuple[1:-1]
            elif case_para_tuple[-1] == 23:
                case_str = templet_cetf_str23 % case_para_tuple[1:-1]
            else:
                pass

            Autocasefile = os.path.join('../', casepath, pyname + '.py')
            with open(Autocasefile, 'w') as f:
                f.write(case_str)
            self.logger.info("gen_testcase" + pyname + ",success")
        except:
            self.logger.info("gen_testcase" + pyname + ",failed")
        return 0

    def gen_all_casepy(self,casepath):
        """
        生成excel中所有的casename对应的casepy文件
        :param casepath: case的存放路径
        :return:
        """
        case_name_para_dict = self.read_excel()
        for key,value in case_name_para_dict.items():
            pyname = key
            try:
                self.gen_specify_casepy(pyname,casepath,case_name_para_dict)
            except:
                pass

    def list_todict(self,l1, l2):
        """两个list打包成一个dict"""
        return dict(zip(l1, l2))

    def encode_dict_value(self,D1):
        """对字典的value值进行编码，处理成想要的格式"""
        D2 = collections.OrderedDict()
        # 对象为o的用例
        if D1['对象'].encode('utf-8') == '○':
            D2['pyname'] = D1['pyname'].encode('utf-8')
            D2['title'] = D1['title'].encode('utf-8')
            D2['期望状态'] = D1['期望状态'].encode('utf-8')
            D2['errorID'] = int(D1['errorID'])
            D2['errorMSG'] = (D1['errorMSG'].encode('utf-8')
                              if D1['errorMSG'] else "''")
            D2['是否生成报单'] = D1['是否生成报单'].encode('utf-8')
            D2['是否是撤废'] = D1['是否是撤废'].encode('utf-8')
            D2['ticker'] = str(int(D1['ticker'])).zfill(6)  # 证券代码补全0
            # if int(D1['case_type']) in (3,8,9,13):
            if D1['etf买入单位']:
                D2['etf买入单位'] = float(D1['etf买入单位'])
            if D1['etf申赎单位']:
                D2['etf申赎单位'] = float(D1['etf申赎单位'])
            if D1['etf卖出单位']:
                D2['etf卖出单位'] = float(D1['etf卖出单位'])
            if D1['成分股卖出单位']:
                D2['成分股卖出单位'] = float(D1['成分股卖出单位'])
            D2['business_type'] = D1['business_type'].encode('utf-8')
            D2['market_wt'] = D1['market_wt'].encode('utf-8')
            D2['side'] = D1['side'].encode('utf-8')
            D2['price_type'] = D1['price_type'].encode('utf-8')

            if D1['期望状态_2']:
                D2['期望状态_2'] = D1['期望状态_2'].encode('utf-8')
                D2['errorID_2'] = int(D1['errorID_2'])
                D2['errorMSG_2'] = (D1['errorMSG_2'].encode('utf-8')
                              if D1['errorMSG_2'] else "''")
                D2['business_type_2'] = D1['business_type_2'].encode('utf-8')
                D2['market_wt_2'] = D1['market_wt_2'].encode('utf-8')
                D2['side_2'] = D1['side_2'].encode('utf-8')
                D2['price_type_2'] = D1['price_type_2'].encode('utf-8')

            if D1['期望状态_3']:
                D2['期望状态_3'] = D1['期望状态_3'].encode('utf-8')
                D2['errorID_3'] = int(D1['errorID_3'])
                D2['errorMSG_3'] = (D1['errorMSG_3'].encode('utf-8')
                                  if D1['errorMSG_3'] else "''")
                D2['business_type_3'] = D1['business_type_3'].encode('utf-8')
                D2['market_wt_3'] = D1['market_wt_3'].encode('utf-8')
                D2['side_3'] = D1['side_3'].encode('utf-8')
                D2['price_type_3'] = D1['price_type_3'].encode('utf-8')

            D2['case_type'] = int(D1['case_type'])
        # # 对象为√的用例
        # elif D1['对象'].encode('utf-8') == '√':
        #     D2['pyname'] = D1['pyname'].encode('utf-8')
        #     D2['title'] = D1['title'].encode('utf-8')
        #     D2['期望状态'] = D1['期望状态'].encode('utf-8')
        #     D2['errorID'] = int(D1['errorID'])
        #     D2['errorMSG'] = (D1['errorMSG'].encode('utf-8')
        #                       if D1['errorMSG'] else "''")
        #     D2['是否生成报单'] = D1['是否生成报单'].encode('utf-8')
        #     D2['是否是撤废'] = D1['是否是撤废'].encode('utf-8')
        #     D2['ticker'] = str(int(D1['ticker'])).zfill(6)  # 证券代码补全0
        #     # casetype列的列名是 '期望状态_2'
        #     if int(D1['期望状态_2']) in (4,5):
        #         # '买入允许现金单位' 列的列名是 'etf买入单位'
        #         # '买入禁止现金单位' 列的列名是 'etf申赎单位'
        #         D2['买入允许现金单位'] = float(D1['etf买入单位'])
        #         D2['买入禁止现金单位'] = float(D1['etf申赎单位'])
        #     D2['etf申赎单位'] = float(D1['etf卖出单位'])
        #     if int(D1['期望状态_2']) in (4,5):
        #         # 'etf市场代码' 列的列名是 '成分股卖出单位'
        #         D2['etf市场代码'] = int(D1['成分股卖出单位'])
        #     D2['business_type'] = D1['business_type'].encode('utf-8')
        #     D2['market_wt'] = D1['market_wt'].encode('utf-8')
        #     D2['side'] = D1['side'].encode('utf-8')
        #     D2['price_type'] = D1['price_type'].encode('utf-8')
        #     D2['case_type'] = int(D1['期望状态_2'])
        return D2

if __name__ == '__main__':
    p = produce_cases(r'cetf_creation_redemption.xlsx',r'Creation_HA')
    p.gen_all_casepy('crossmarket_creation_HA')
    p1 = produce_cases(r'cetf_creation_redemption.xlsx',r'Redemption_HA')
    p1.gen_all_casepy('crossmarket_redemption_HA')
