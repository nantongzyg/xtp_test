#!/usr/bin/python
# -*- coding: utf-8 -*-

import xlrd
filename = 'sa_test.xlsx'
#sheet_name =u'上海市价跨市场'
#data = xlrd.open_workbook(filename, encoding_override='utf-8')
data = xlrd.open_workbook(filename)
table = data.sheet_by_name(u'深圳限价')
value = table.row_values(2)
print value[2]
print table.cell(2,2).value
