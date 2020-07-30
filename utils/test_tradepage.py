#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys,time
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from QueryStkPriceQty import *
from log import *


a = []
i = 0

class Test_tradepage(xtp_test_case):

    # 成交分页查询
    def test_orderpage(self):
        title = '成交回报数量/分页请求的最大数量(req_count) < 1，reference=-1'
        logger.warning(title)
        def pagedate(data, req_count, trade_sequence, query_reference, request_id, is_last):
            global i
	    for k in data.keys():
                if 'business_type' in k:
                    i +=1
                    a.append(i)

        Api.trade.setQueryTradeByPageHandle(pagedate)
        Api.trade.QueryTradesByPage({'req_count':13,'reference':385})
        time.sleep(0.5)
        rs = a[-1]
        self.assertEqual(rs, 2) 

if __name__ == '__main__':
    unittest.main()
