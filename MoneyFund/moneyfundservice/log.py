#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging
import datetime
import ServiceConfig

#设置日志文件名字
date=datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')
filename= ServiceConfig.LOGPATH + date + '.log'
#设置日志输出格式
fmt= '%(asctime)s - %(filename)s:%(lineno)s - %(message)s'
formatter=logging.Formatter(fmt)
#创建一个文件日志输出和一个控制台日志输出
handler_file=logging.FileHandler(filename)
handler_file.setFormatter(formatter)
handler_file.setLevel(ServiceConfig.LEVEL_FILE)
handler_console=logging.StreamHandler()
handler_console.setFormatter(formatter)
handler_console.setLevel(ServiceConfig.LEVEL_console)
#创建一个名字为filename的logger对象
logger=logging.getLogger('myloger')
logger.setLevel(ServiceConfig.LEVEL_FILE)
logger.addHandler(handler_file)
logger.addHandler(handler_console)

#日志级别大小关系为：CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET

# 打印dict类型数据
def dictLogging(dict):
    for (k, v) in dict.items():
        logger.info(k+':'+str(v))



