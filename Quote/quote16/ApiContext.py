#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
from contextlib import contextmanager
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtp_test_case import *

@contextmanager
def ApiManage():
    client_id = 68
    try:
        print 111111111111
        Api = XTPQuoteApi(client_id)
        print 333333333333
        Api.Login()
        print 444444444444
        yield Api
        print 555555555555
    finally: 
        print 222222222222 
        Api.Logout()
        
