#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
import time
import math
from decimal import Decimal
from decimal import ROUND_HALF_UP
sys.path.append("/home/yhl2/workspace/xtp_test/option/mysql")
from opt_database_manager import QueryTable
from OptQueryTgtPreclose import queryTgtPreclose
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from config import CONST_TRADE_USER

today = time.strftime('%Y%m%d', time.localtime(time.time()))

def cal_margin_call(cntrt_id, cntrt_quantity, yesterday_position):
    """计算认购期权保证金"""

    # xtp_opt_cntrt_info_xxxxxxxx表保证金参数一
    opt_cntrt_eles = QueryTable('xtp_opt_cntrt_info_' + today,
                                ['settl_price', 'margin_ratio_param1', 'margin_ratio_param2',
                                'exercise_price', 'cntrt_mul_unit'], {'cntrt_id': cntrt_id}, 2)

    # 资金账号
    fund_acc = QueryTable('xtp_user', ['fundid'], {'user_name': CONST_TRADE_USER}, 2)

    # xtp_opt_margin_rate_cfg_xxxxxxxx表保证金参数一
    opt_margin_eles = QueryTable('xtp_opt_margin_rate_cfg_' + today,
                            ['mrg_ratio1', 'mrg_ratio2', 'float_rate'],
                            {'fund_acc': fund_acc['fundid'], 'opt_code': cntrt_id}, 2)

    tmp_max1 = queryTgtPreclose(cntrt_id) * \
                    (opt_cntrt_eles['margin_ratio_param1'] + opt_margin_eles['mrg_ratio1']) / 10000.0 -\
                    max((opt_cntrt_eles['exercise_price']/10000.0 - queryTgtPreclose(cntrt_id)), 0)

    tmp_max2 = queryTgtPreclose(cntrt_id) * \
               (opt_cntrt_eles['margin_ratio_param2'] + opt_margin_eles['mrg_ratio2']) / 10000.0

    tmp_max = float(Decimal(Decimal(str(max(tmp_max1, tmp_max2))).quantize(Decimal('.000001'),
                                                                           rounding=ROUND_HALF_UP)))

    # 上浮比率
    float_rate = 1 + opt_margin_eles['float_rate'] / 10000.0

    # print opt_cntrt_eles, opt_margin_eles, queryTgtPreclose(cntrt_id)
    # 保证金
    if yesterday_position > 0:
        asset_eles = QueryTable('xtp_opt_asset_' + today,
                                ['opt_avl_qty', 'margin'],
                                {'fund_acc': fund_acc['fundid'], 'cntrt_code': cntrt_id}, 2)
        margin = float(asset_eles['margin']) / float(asset_eles['opt_avl_qty'])

    else:
        margin = float(Decimal(Decimal(str(opt_cntrt_eles['cntrt_mul_unit'] * float_rate *
                            (opt_cntrt_eles['settl_price'] / 10000.0 + tmp_max))).quantize(
                             Decimal('.01'), rounding=ROUND_HALF_UP)))

        # return math.ceil(margin * 10000) / 10000.0 * cntrt_quantity

    return margin * cntrt_quantity

def cal_margin_put(cntrt_id, cntrt_quantity, yesterday_position):
    """计算认沽期权保证金"""
    # xtp_opt_cntrt_info_xxxxxxxx表保证金参数一
    opt_cntrt_eles = QueryTable('xtp_opt_cntrt_info_' + today,
                                ['settl_price', 'margin_ratio_param1', 'margin_ratio_param2',
                                 'exercise_price', 'cntrt_mul_unit'], {'cntrt_id': cntrt_id}, 2)

    # 资金账号
    fund_acc = QueryTable('xtp_user', ['fundid'], {'user_name': CONST_TRADE_USER}, 2)

    # xtp_opt_margin_rate_cfg_xxxxxxxx表保证金参数一
    opt_margin_eles = QueryTable('xtp_opt_margin_rate_cfg_' + today,
                                 ['mrg_ratio1', 'mrg_ratio2', 'float_rate'],
                                 {'fund_acc': fund_acc['fundid'], 'opt_code': cntrt_id}, 2)

    tmp_max1 = queryTgtPreclose(cntrt_id) * \
               (opt_cntrt_eles['margin_ratio_param1'] + opt_margin_eles['mrg_ratio1']) / 10000.0 - \
               max((queryTgtPreclose(cntrt_id) - opt_cntrt_eles['exercise_price'] / 10000.0), 0)

    tmp_max2 = opt_cntrt_eles['exercise_price'] * \
               (opt_cntrt_eles['margin_ratio_param2'] + opt_margin_eles['mrg_ratio2']) / 10000.0 / 10000.0

    tmp_max = float(Decimal(Decimal(str(max(tmp_max1, tmp_max2))).quantize(Decimal('.000001'),
                                                                           rounding=ROUND_HALF_UP)))

    tmp_min1 = tmp_max + opt_cntrt_eles['settl_price'] / 10000.0

    tmp_min2 = opt_cntrt_eles['exercise_price'] / 10000.0

    tmp_min = float(Decimal(Decimal(str(min(tmp_min1, tmp_min2))).quantize(Decimal('.000001'),
                                                                           rounding=ROUND_HALF_UP)))
    # 上浮比率
    float_rate = 1 + opt_margin_eles['float_rate'] / 10000.0

    if yesterday_position > 0:
        asset_eles = QueryTable('xtp_opt_asset_' + today,
                              ['opt_avl_qty', 'margin'],
                              {'fund_acc': fund_acc['fundid'], 'cntrt_code': cntrt_id}, 2)
        margin = float(asset_eles['margin']) / float(asset_eles['opt_avl_qty'])
    else:
        margin = float(Decimal(Decimal(str(tmp_min * opt_cntrt_eles['cntrt_mul_unit'] *
                                           float_rate)).quantize(Decimal('.01'),
                                            rounding=ROUND_HALF_UP)))
    return margin * cntrt_quantity

# print cal_margin_call('11002388', 1, 1)
