#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
sys.path.append("/home/yhl2/workspace/xtp_test")
from service.log import *
from service import ServiceConfig

# 因为普通买卖每次最大下单数量1000000，所以需要将总的数量拆分
def split_etf_quantity(quantity):
    max_qty = ServiceConfig.MAX_QTY
    quantity_list = []
    while quantity > max_qty:
        quantity_list.append(max_qty)
        quantity = quantity - max_qty
    if quantity < max_qty:
        quantity_list.append(quantity)
    elif quantity == max_qty:
        quantity_list.append(quantity)

    return quantity_list

def etf_query_log(case_goal,rs):
    logger.warning(' etf申购的执行结果为: '
                   + str(rs['用例测试结果'])
                   + ', ' + str(rs['用例错误原因']))

def etf_creation_log(case_goal,rs):
    logger.warning(' etf申赎的执行结果为: '
                   + str(rs['用例测试结果'])
                   + ', ' + str(rs['用例错误源'])
                   + ', ' + str(rs['用例错误原因']))

def etf_sell_log(case_goal,rs):
    logger.warning('etf二级市场卖出的执行结果为: '
                   + str(rs['用例测试结果'])
                   + ', ' + str(rs['用例错误源'])
                   + ', ' + str(rs['用例错误原因']))

def etf_components_sell_log(case_goal,rs):
    logger.warning('成份股二级市场卖出的执行结果为: '
                   + str(rs['用例测试结果'])
                   + ', ' + str(rs['用例错误源'])
                   + ', ' + str(rs['用例错误原因']))


# T日买入或者卖出etf成分股数量不为100整数倍时，转为100整数倍，
# 如申购1unit需要成分股数量1500，则买入0.5unit成分股为750，需要将数量转为800.
def get_valid_amount(component_quantity):
    quantity = component_quantity + 50 \
        if component_quantity * 1.0 / 100 - component_quantity / 100 > 0 \
        else component_quantity
    return quantity


if __name__ =='__main__':
    print get_valid_amount(750)