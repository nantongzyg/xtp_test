#!/usr/bin/python
# -*- encoding: utf-8 -*-

import datetime
import sys
sys.path.append('/home/yhl2/workspace/xtp_test/service')
from log import *

def unsub_data_handle():
    '''
    检查行情取消订阅后，是否还有推送
    :return:
    '''
    # curr_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')
    curr_date = '20170823'
    unsub_begin_match_str = 'unsub begin'
    sub_succ_match_str = 'sub succeeded'
    file_name = '/home/yhl2/workspace/xtp_test/Quote/20170823_258.log'
    unsub_begin_time = '999999999'
    with open(file_name,'r') as f:
        for line in f:
            if line.find(unsub_begin_match_str) != -1:
                unsub_begin_time_list = []
                unsub_begin_time_origin = line[11:23]
                unsub_begin_time_list.append(unsub_begin_time_origin[0:2])
                unsub_begin_time_list.append(unsub_begin_time_origin[3:5])
                unsub_begin_time_list.append(unsub_begin_time_origin[6:8])
                unsub_begin_time_list.append(unsub_begin_time_origin[9:12])
                unsub_begin_time = ('').join(unsub_begin_time_list)
            elif line.find(sub_succ_match_str) != -1:
                unsub_begin_time = '999999999'

            quote_time_index = line.find(curr_date)
            if quote_time_index != -1:
                quote_time = line[line.find(curr_date)+8: line.index(curr_date)+17]
                # logger.info(quote_time)
                # if quote_time == '103510493':
                #     print unsub_begin_time
                if quote_time >= unsub_begin_time:
                    logger.logger.info('取消订阅后仍有行情推送, 取消订阅时间: ' + unsub_begin_time + ',行情推送时间: ' + quote_time)
                    # print('取消订阅后仍有行情推送, 取消订阅时间: ' + unsub_begin_time + ',行情推送时间: ' + quote_time)


if __name__ == '__main__':
    unsub_data_handle()