#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import time
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from log import *
import ServiceConfig
from mainService import *

def getPosition():
    def on_QueryPosition(data, error, request_id, is_last):
        print data

    stkcode = {
        'ticker': '',
    }

    Api.trade.setQueryPositionHandle(on_QueryPosition)
    Api.trade.QueryPosition(stkcode)


getPosition()