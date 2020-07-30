#!/usr/bin/python
# -*- encoding: utf-8 -*-
import os
import time
import sys
from mainService import *
# sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
# from xtp_test_case import *


# 删除订单文件
def remove_order_files():
    os.system('rm -rf *order*')

def insert_orders(count, max_count, Api, case_goal, wt_reqs, filename):
    while count <= max_count:
        serviceTest(Api, case_goal, wt_reqs, filename)
        count += 1

def insert_orders_sleep(count, max_count, Api, case_goal, wt_reqs, filename):
    while count <= max_count:
        serviceTest(Api, case_goal, wt_reqs, filename)
        time.sleep(0.03)
        count += 1

# 风控14校验,rule0开启
def rule14_check(filename1, filename2):
    risk_index = -1
    # 触发rule14风控的订单xtp_id
    rule_xtp_id = ''
    begin_time = 0
    end_time = 0
    with open(filename1, 'r') as f:
        for line in f.readlines():
            index_rule_order = line.find('11011214')
            if index_rule_order != -1:
                risk_index = index_rule_order
                rule_xtp_id = eval(line).values()[0]['order_xtp_id']
                end_time = int(eval(line).values()[0]['insert_time'])

    # 检查是否触发rule14风控，触发rule14风控，应报'11011214'错误
    if risk_index == -1:
        logger.error('执行结果为False，未触发rule14风控！')
    else:
        # 触发风控的订单前面3000单，是否是在1秒内下的
        xtp_id = str(rule_xtp_id - 3000)
        with open(filename1, 'r') as f:
            for line in f.readlines():
                index_first_order = line.find(xtp_id)
                if index_first_order != -1:
                    begin_time = int(eval(line).values()[0]['insert_time'])

        # 触发风控的时间和前面第3000笔订单时间差
        time_diff = end_time - begin_time
        if time_diff > 1000:
            logger.error('执行结果为False，未在1秒内触发风控！')
        else:
            # 校验触发风控后面的一单是否报'11011314'错误
            enter_rule_error_id = 0
            enter_rule_xtp_id = str(int(rule_xtp_id) + 1)
            with open(filename1, 'r') as f:
                for line in f.readlines():
                    index_enter_rule = line.find(enter_rule_xtp_id)
                    if index_enter_rule != -1:
                        enter_rule_error_id = int(eval(line).values()[0]['error_id'])

            after_rule_xtpid = ''
            if enter_rule_error_id != 11011314:
                logger.error('执行结果为False，触发风控后下单，应报11011314错误!')
            else:
                # 校验风控触发后60秒下单是否正常
                after_rule_time = 0
                with open(filename2, 'r') as f:
                    for line in f.readlines():
                        # 截掉毫秒，用000替代
                        if eval(line).values()[0]['error_id'] == 0:
                            after_rule_xtpid = eval(line).values()[0]['order_xtp_id']
                            break

                if after_rule_xtpid == '':
                    logger.error('执行结果为False，熔断时间结束后，不能正常下单!')
                else:
                    logger.warning('执行结果为True，rule14风控校验正确!')

# 新股申购,风控14校验,rule0开启
def rule14_check_xgsg(filename1, filename2):
    risk_index = -1
    # 触发rule14风控的订单xtp_id
    rule_xtp_id = ''
    begin_time = 0
    end_time = 0
    with open(filename2, 'r') as f:
        for line in f.readlines():
            index_rule_order = line.find('11011314')
            if index_rule_order != -1:
                risk_index = index_rule_order
                rule_xtp_id = eval(line).values()[0][
                    'order_xtp_id']
                enter_rule_time = int(eval(line).values()[0]['insert_time'])
                break
            if int(eval(line).values()[0]['order_xtp_id']) == int(rule_xtp_id) - 1:
                end_time = int(eval(line).values()[0]['insert_time'])


    # 检查是否触发rule14风控，触发rule14风控，应报'11011314'错误
    if risk_index == -1:
        logger.error('执行结果为False，未触发rule14风控！')
    else:
        # 触发风控的订单前面3000单，是否是在1秒内下的
        xtp_id = str(rule_xtp_id - 3000)
        with open(filename1, 'r') as f:
            for line in f.readlines():
                index_first_order = line.find(xtp_id)
                if index_first_order != -1:
                    begin_time = int(eval(line).values()[0]['insert_time'])

        # 触发风控的时间和前面第3000笔订单时间差
        after_rule_xtpid = ''
        time_diff = end_time - begin_time
        if time_diff > 1000:
            logger.error('执行结果为False，未在1秒内触发风控！')
        else:
            # 校验风控触发后60秒下单是否正常
            after_rule_time = 0
            with open(filename2, 'r') as f:
                for line in f.readlines():
                    # 截掉毫秒，用000替代
                    if eval(line).values()[0]['error_id'] == 0:
                        after_rule_xtpid = eval(line).values()[0]['order_xtp_id']
                        break

            if after_rule_xtpid == '':
                logger.error('执行结果为False，熔断时间结束后，不能正常下单!')
            else:
                logger.warning('执行结果为True，rule14风控校验正确!')

# etf申赎，风控14校验,rule0开启
def rule14_check_etf(filename1, filename2):
    risk_index = -1
    # 触发rule14风控的订单xtp_id
    rule_xtp_id = ''
    begin_time = 0
    end_time = 0
    with open(filename1, 'r') as f:
        for line in f.readlines():
            index_rule_order = line.find('11011314')
            if index_rule_order != -1:
                risk_index = index_rule_order
                rule_xtp_id = eval(line).values()[0]['order_xtp_id']
                end_time = int(eval(line).values()[0]['insert_time'])
                break

    # 检查是否触发rule14风控，触发rule14风控，应报'11011314'错误
    if risk_index == -1:
        logger.error('执行结果为False，未触发rule14风控！')
    else:
        # 触发风控的订单前面3000单，是否是在1秒内下的
        xtp_id = str(rule_xtp_id - 3000)
        with open(filename1, 'r') as f:
            for line in f.readlines():
                index_first_order = line.find(xtp_id)
                if index_first_order != -1:
                    begin_time = int(eval(line).values()[0]['insert_time'])

        # 触发风控的时间和前面第3000笔订单时间差
        time_diff = end_time - begin_time
        if time_diff > 1000:
            logger.error('执行结果为False，未在1秒内触发风控！')
        else:
            # 校验风控触发后60秒下单是否正常
            after_rule_time = 0
            with open(filename2, 'r') as f:
                for line in f.readlines():
                    # 截掉毫秒，用000替代
                    if eval(line).values()[0][
                        'error_id'] == 0:
                        after_rule_time = \
                            int(str(eval(line).values()[0]['insert_time'])[0:-3] + '000')
                        break

            time_diff = after_rule_time - int(
                str(end_time)[0:-3] + '000')
            if time_diff != 100000:
                logger.error('执行结果为False，熔断时间结束后，不能正常下单!')
            else:
                logger.warning('执行结果为True，rule14风控校验正确!')

# 风控14校验,rule0关闭
def rule14_check2(filename):
    risk_index = -1
    with open(filename, 'r') as f:
        for line in f.readlines():
            index_rule_order = line.find('11011214')
            if index_rule_order != -1:
                risk_index = index_rule_order

    # 检查是否触发rule14风控，触发rule14风控，应报'11011214'错误
    if risk_index == -1:
        logger.error('执行结果为True，rule14风控校验正确！')
    else:
        logger.error('执行结果为False，触发rule14风控！')

# 新股申购，风控14校验,rule0关闭
def rule14_check_ipo2(filename):
    rule14_enter_check(filename)

# etf申赎，风控14校验,rule0关闭
def rule14_check_etf2(filename):
    rule14_enter_check(filename)

def rule14_enter_check(filename):
    risk_index = -1
    with open(filename, 'r') as f:
        for line in f.readlines():
            index_rule_order = line.find('11011314')
            if index_rule_order != -1:
                risk_index = index_rule_order

    # 检查是否触发rule14风控，触发rule14风控，应报'11011214'错误
    if risk_index == -1:
        logger.error('执行结果为True，rule14风控校验正确！')
    else:
        logger.error('执行结果为False，触发rule14风控！')

# 风控25校验,rule0开启
def rule25_check(filename):
    risk_index = -1
    rule_xtpid_id = 0
    # 获取触发风控订单的xtpid
    with open(filename, 'r') as f:
        for line in f.readlines():
            index_rule_order = line.find('11011225')
            if index_rule_order != -1:
                risk_index = index_rule_order
                rule_xtpid_id = eval(line).values()[0]['order_xtp_id']
                break

    count = 0
    with open(filename, 'r') as f:
        for line in f.readlines():
            xtpid_id = eval(line).values()[0]['order_xtp_id']
            error_id = eval(line).values()[0]['error_id']
            if xtpid_id < rule_xtpid_id and error_id != 0:
                count += 1

    if risk_index == -1:
        logger.error('执行结果为False, 未触发rule25风控!')
    else:
        if count != 101:
            logger.error('执行结果为False, 触发风控的下单数量错误!')
        else:
            logger.warning('执行结果为True，rule25风控校验正确!')

# 风控27校验,rule0关闭
def rule27_check2(filename):
    risk_index = -1
    with open(filename, 'r') as f:
        for line in f.readlines():
            index_rule_order = line.find('11011227')
            if index_rule_order != -1:
                risk_index = index_rule_order

    # 检查是否触发rule14风控，触发rule14风控，应报'11011214'错误
    if risk_index == -1:
        logger.error('执行结果为True，rule27风控校验正确！')
    else:
        logger.error('执行结果为False，触发rule27风控！')

# 风控27校验,rule0开启
def rule27_check(filename):
    risk_index = -1
    # 触发rule14风控的订单xtp_id
    rule_xtp_id = ''
    begin_time = 0
    end_time = 0
    with open(filename, 'r') as f:
        for line in f.readlines():
            index_rule_order = line.find('11011227')
            if index_rule_order != -1:
                risk_index = index_rule_order
                rule_xtp_id = eval(line).values()[0]['order_xtp_id']
                end_time = int(eval(line).values()[0]['insert_time'])

    # 检查是否触发rule127风控，触发rule27风控，应报'11011227'错误
    if risk_index == -1:
        logger.error('执行结果为False，未触发rule27风控！')
    else:
        # 触发风控的订单前面6单，是否是在10秒内下的
        xtp_id = str(rule_xtp_id - 6)
        with open(filename, 'r') as f:
            for line in f.readlines():
                index_first_order = line.find(xtp_id)
                if index_first_order != -1:
                    begin_time = int(eval(line).values()[0]['insert_time'])

        # 触发风控的时间和前面第3000笔订单时间差
        time_diff = end_time - begin_time
        if time_diff > 10000:
            logger.error('执行结果为False，未在1秒内触发风控！')
        else:
            # 校验触发风控后面的一单是否报'11011327'错误
            enter_rule_error_id = 0
            enter_rule_xtp_id = str(int(rule_xtp_id) + 1)
            with open(filename, 'r') as f:
                for line in f.readlines():
                    index_enter_rule = line.find(enter_rule_xtp_id)
                    if index_enter_rule != -1:
                        enter_rule_error_id = int(eval(line).values()[0]['error_id'])

            if enter_rule_error_id != 11011327:
                logger.error('执行结果为False，触发风控后下单，应报11011327错误!')
            else:
                # 校验风控触发后60秒下单是否正常
                after_rule_time = 0
                with open(filename, 'r') as f:
                    for line in f.readlines():
                        # 截掉毫秒，用000替代
                        if eval(line).values()[0]['error_id'] == 0:
                            after_rule_time = int(str(
                                eval(line).values()[0]['insert_time'])[
                                                  0:-3] + '000')
                            break

                time_diff = after_rule_time - int(
                    str(end_time)[0:-3] + '000')
                if time_diff < 100000:
                    logger.error('执行结果为False，熔断时间未结束，但是能正常下单!')
                else:
                    logger.warning('执行结果为True，rule27风控校验正确!')

# 新股申购，风控27校验,rule0开启
def rule27_check_xgsg(filename1, filename2):
    risk_index = -1
    # 触发rule14风控的订单xtp_id
    rule_xtp_id = ''
    begin_time = 0
    end_time = 0
    with open(filename1, 'r') as f:
        for line in f.readlines():
            index_rule_order = line.find('11011227')
            if index_rule_order != -1:
                risk_index = index_rule_order
                rule_xtp_id = eval(line).values()[0][
                    'order_xtp_id']
                end_time = int(eval(line).values()[0]['insert_time'])

    # 检查是否触发rule127风控，触发rule27风控，应报'11011227'错误
    if risk_index == -1:
        logger.error('执行结果为False，未触发rule27风控！')
    else:
        # 触发风控的订单前面6单，是否是在10秒内下的
        xtp_id = str(rule_xtp_id - 6)
        with open(filename1, 'r') as f:
            for line in f.readlines():
                index_first_order = line.find(xtp_id)
                if index_first_order != -1:
                    begin_time = int(
                        eval(line).values()[0]['insert_time'])

        # 触发风控的时间和前面第3000笔订单时间差
        time_diff = end_time - begin_time
        if time_diff > 10000:
            logger.error('执行结果为False，未在1秒内触发风控！')
        else:
            # 校验触发风控后面的一单是否报'11011327'错误
            enter_rule_error_id = 0
            enter_rule_xtp_id = str(int(rule_xtp_id) + 1)
            with open(filename1, 'r') as f:
                for line in f.readlines():
                    index_enter_rule = line.find(
                        enter_rule_xtp_id)
                    if index_enter_rule != -1:
                        enter_rule_error_id = int(
                            eval(line).values()[0]['error_id'])

            if enter_rule_error_id != 11011327:
                logger.error('执行结果为False，触发风控后下单，应报11011327错误!')
            else:
                # 校验风控触发后60秒下单是否正常
                after_rule_time = 0
                with open(filename2, 'r') as f:
                    for line in f.readlines():
                        # 截掉毫秒，用000替代
                        if eval(line).values()[0][
                            'error_id'] == 0:
                            after_rule_time = int(str(
                                eval(line).values()[0][
                                    'insert_time'])[
                                                  0:-3] + '000')
                            break
                print after_rule_time, int(str(end_time)[0:-3] + '000')
                time_diff = after_rule_time - int(str(end_time)[0:-3] + '000')
                if time_diff != 100000:
                    logger.error('执行结果为False，熔断时间结束后，不能正常下单!')
                else:
                    logger.warning('执行结果为True，rule27风控校验正确!')

# 风控25校验,rule0关闭
def rule25_check2(filename):
    risk_index = -1
    rule_xtpid_id = 0
    with open(filename, 'r') as f:
        for line in f.readlines():
            index_rule_order = line.find('11011225')
            if index_rule_order != -1:
                risk_index = index_rule_order
                break

    error_id_last  = 0
    xtp_id_last = 0
    with open(filename, 'r') as f:
        for line in f.readlines():
            error_id_last = eval(line).values()[0]['error_id']
            xtp_id_last = eval(line).values()[0]['order_xtp_id']

    count = 0
    with open(filename, 'r') as f:
        for line in f.readlines():
            xtp_id = eval(line).values()[0]['order_xtp_id']
            error_id = eval(line).values()[0]['error_id']
            if xtp_id < xtp_id_last and error_id != 0:
                count += 1

    if risk_index != -1:
        logger.error('执行结果为False, 触发rule25风控!')
    else:
        if error_id_last != 0:
            logger.error('执行结果为False, 最后一单为废单!')
        else:
            if count != 101:
                logger.error('执行结果为False, 触发rule25风控所需的废单数不够!')
            else:
                logger.warning('执行结果为True，rule25风控校验正确!')

# 风控26校验,rule0开启
def rule26_check(filename):
    risk_index = -1
    count = 0
    with open(filename, 'r') as f:
        for line in f.readlines():
            count += 1
            index_rule_order = line.find('11011226')
            if index_rule_order != -1:
                risk_index = index_rule_order
                break

    if count == 502 and risk_index != -1:
        logger.error('执行结果为True，rule26风控校验正确！')
    elif count != 502:
        logger.error('执行结果为False，下单数量错误！')
    elif risk_index == -1:
        logger.error('执行结果为False，未触发风控！')
    else:
        logger.error('执行结果为False，未知错误！')

# 风控26校验,rule0关闭
def rule26_check2(filename):
    risk_index = -1
    count = 0
    with open(filename, 'r') as f:
        for line in f.readlines():
            count += 1
            index_rule_order = line.find('11011226')
            if index_rule_order != -1:
                risk_index = index_rule_order
                break

    if count >= 502 and risk_index == -1:
        logger.error('执行结果为True，rule26风控校验正确！')
    elif count < 502:
        logger.error('执行结果为False，下单数量错误！')
    elif risk_index != -1:
        logger.error('执行结果为False，触发rule26风控！')
    else:
        logger.error('执行结果为False，未知错误！')

# 风控38校验,rule0开启
def rule38_check(filename):
    index_enter_rule = -1
    # 触发rule14风控的订单xtp_id
    rule_xtp_id = ''
    begin_time = 0
    end_time = 0
    with open(filename, 'r') as f:
        for line in f.readlines():
            index_enter_rule = line.find('11011338')
            if index_enter_rule != -1:
                rule_xtp_id = eval(line).values()[0]['order_xtp_id']
                break

    # 触发风控订单的报单时间
    with open(filename, 'r') as f:
        for line in f.readlines():
            xtp_id = eval(line).values()[0]['order_xtp_id']
            if xtp_id == int(rule_xtp_id) - 1:
                begin_time = int(str(eval(line).values()[0]['insert_time'])[0:-3] + '000')

    # 检查是否触发rule38风控，触发rule38风控，应报'11011338'错误
    if index_enter_rule == -1:
        logger.error('执行结果为False，未触发rule38风控！')
    else:
        # 触发风控的订单前面6单是否都为废单
        count = 0
        with open(filename, 'r') as f:
            for line in f.readlines():
                xtp_id = eval(line).values()[0]['order_xtp_id']
                error_id = eval(line).values()[0]['error_id']
                if xtp_id < rule_xtp_id and error_id != 0:
                    count += 1

        if count != 6:
            logger.error('执行结果为False，触发rule38风控的下单数量错误！')
        else:
            # 熔断时间校验
            with open(filename, 'r') as f:
                for line in f.readlines():
                    # 截掉毫秒，用000替代
                    if eval(line).values()[0]['error_id'] == 0:
                        end_time = int(str(eval(line).values()[0]['insert_time'])[0:-3] + '000')
                        break

            time_diff = end_time - begin_time
            if time_diff != 100000:
                logger.error('执行结果为False，熔断时间结束后，不能正常下单!')
            else:
                logger.warning('执行结果为True，rule38风控校验正确!')

# 风控38校验,rule0关闭
def rule38_check2(filename):
    index_enter_rule = -1
    # 触发rule14风控的订单xtp_id
    with open(filename, 'r') as f:
        for line in f.readlines():
            index_enter_rule = line.find('11011338')
            if index_enter_rule != -1:
                break

    if index_enter_rule != -1:
        logger.error('执行结果为False, 触发rule38风控!')
    else:
        logger.warning('执行结果为True，rule38风控校验正确!')

# 风控43校验
def rule43_check(filename1, filename2):
    risk_index = -1
    # 触发rule43风控的订单xtp_id
    rule_xtp_id = ''
    begin_time = 0
    end_time = 0
    with open(filename1, 'r') as f:
        for line in f.readlines():
            index_rule_order = line.find('11011243')
            if index_rule_order != -1:
                risk_index = index_rule_order
                rule_xtp_id = eval(line).values()[0]['order_xtp_id']
                end_time = int(eval(line).values()[0]['insert_time'])

    # 检查是否触发rule43风控，触发rule43风控，应报'11011243'错误
    if risk_index == -1:
        logger.error('执行结果为False，未触发rule43风控！')
    else:
        # 触发风控的订单前面3000单，是否是在1秒内下的
        xtp_id = str(rule_xtp_id - 1000)
        with open(filename1, 'r') as f:
            for line in f.readlines():
                index_first_order = line.find(xtp_id)
                if index_first_order != -1:
                    begin_time = int(eval(line).values()[0]['insert_time'])

        # 触发风控的时间和前面第3000笔订单时间差
        time_diff = end_time - begin_time
        if time_diff > 1000:
            logger.error('执行结果为False，未在1秒内触发风控！')
        else:
            # 校验触发风控后面的一单是否报'11011314'错误
            enter_rule_error_id = 0
            enter_rule_xtp_id = str(int(rule_xtp_id) + 1)
            with open(filename1, 'r') as f:
                for line in f.readlines():
                    index_enter_rule = line.find(enter_rule_xtp_id)
                    if index_enter_rule != -1:
                        enter_rule_error_id = int(eval(line).values()[0]['error_id'])

            after_enter_xtp_id = ''
            if enter_rule_error_id != 11011343:
                logger.error('执行结果为False，触发风控后下单，应报11011343错误!')
            else:
                # 校验风控触发后60秒下单是否正常
                after_rule_time = 0
                with open(filename2, 'r') as f:
                    for line in f.readlines():
                        # 截掉毫秒，用000替代
                        if eval(line).values()[0]['error_id'] == 0:
                            after_rule_time = int(str(eval(line).values()[0]['insert_time'])[0:-3] + '000')
                            after_enter_xtp_id = eval(line).values()[0]['order_xtp_id']
                            break

                time_diff = after_rule_time - int(str(end_time)[0:-3] + '000')
                if time_diff != 100000:
                    logger.error('执行结果为False，熔断时间结束后，不能正常下单，error_id为"11011243"的单子xtpid为%s，'
                                 'insert_time为%d,熔断结束后第一单xtpid为%s,insert_time为%d!' %
                                 (rule_xtp_id, end_time, after_enter_xtp_id, after_rule_time))
                else:
                    logger.warning('执行结果为True，rule43风控校验正确!')

# 新股申购和etf申赎，风控43校验
def rule43_check2(filename1, filename2):
    risk_index = -1
    # 触发rule43风控的订单xtp_id
    rule_xtp_id = ''
    begin_time = 0
    end_time = 0
    with open(filename2, 'r') as f:
        for line in f.readlines():
            index_rule_order = line.find('11011343')
            if index_rule_order != -1:
                risk_index = index_rule_order
                rule_xtp_id = eval(line).values()[0]['order_xtp_id']
                break
            if eval(line).values()[0]['order_xtp_id'] == rule_xtp_id - 1:
                end_time = int(eval(line).values()[0]['insert_time'])

    # 检查是否触发rule43风控，触发rule43风控，应报'11011343'错误
    if risk_index == -1:
        logger.error('执行结果为False，未触发rule43风控！')
    else:
        # 触发风控的订单前面3000单，是否是在1秒内下的
        xtp_id = str(rule_xtp_id - 3000)
        with open(filename1, 'r') as f:
            for line in f.readlines():
                index_first_order = line.find(xtp_id)
                if index_first_order != -1:
                    begin_time = int(eval(line).values()[0]['insert_time'])

        # 触发风控的时间和前面第3000笔订单时间差
        after_rule_xtpid = ''
        time_diff = end_time - begin_time
        if time_diff > 1000:
            logger.error('执行结果为False，未在1秒内触发风控！')
        else:
            # 校验风控触发后60秒下单是否正常
            after_rule_time = 0
            with open(filename2, 'r') as f:
                for line in f.readlines():
                    # 截掉毫秒，用000替代
                    if eval(line).values()[0]['error_id'] == 0:
                        after_rule_xtpid = eval(line).values()[0][
                            'order_xtp_id']
                        break

            if after_rule_xtpid == '':
                logger.error('执行结果为False，熔断时间结束后，不能正常下单!')
            else:
                logger.warning('执行结果为True，rule43风控校验正确!')

# 将订单文件按xtpid从小到大重新排序
def file_reorder(filename):
    order_list = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            order_list.append(line)

    if os.path.exists(filename):
        os.remove(filename)

    order_list.sort()
    with open(filename, 'a') as f:
        for line in order_list:
            f.write(line)

