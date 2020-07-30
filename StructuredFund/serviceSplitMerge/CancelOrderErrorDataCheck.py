#!/usr/bin/python
# -*- encoding: utf-8 -*-
from log import *
import ServiceConfig

def cancelOrderErrorDataCheck(case_goal,error_info):
    logger.info('当前是撤废数据检查函数')
    reslut={
        '检查状态':'init',
        '测试结果':False,
        '错误原因':'',
    }
    #获取配置，是否检查ErrMSG
    isCheckErrMSG=ServiceConfig.IS_CHECK_ERRMSG_FROM_CANCELERR

    if case_goal['errorID'] != error_info['error_id']:
        logger.error('错误，errorID与期望不一致，撤废返回的errID和期望errID分别是'+str(case_goal['errorID'])+','+str(error_info['error_id']))
        reslut['检查状态']='end'
        reslut['测试结果']=False
        reslut['错误原因'] = '撤废返回的errorID与期望不一致'
    else:
        if isCheckErrMSG:
            if case_goal['errorMSG'] != error_info['error_msg'].strip():
                logger.error('错误，errorMSG与期望不一致，撤废返回的errorMSG和期望errorMSG分别是' + str(case_goal['errorMSG']) + ',' + str(
                    error_info['error_msg']))
                reslut['检查状态'] = 'end'
                reslut['测试结果'] = False
                reslut['错误原因'] = '撤废返回的errorMSG与期望不一致'
            else:
                reslut['检查状态'] = 'end'
                reslut['测试结果'] = True
        else:
            reslut['检查状态'] = 'end'
            reslut['测试结果'] = True

    return reslut
