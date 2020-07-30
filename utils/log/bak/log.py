#!/usr/bin/python
# -*- encoding: utf-8 -*-


import logging
import datetime

date=datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')
filename='/home/yhl2/workspace/xtp_test/ETF_log/'+date+'.ETF_log'

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S",
                    filename=filename,
                    filemode='w'
                    )

logging.debug('This is debug message')
logging.info('This is info message')
logging.warning('This is warning message')












