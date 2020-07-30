import sys
sys.path.append("/home/yhl2/workspace/xtp_test/xtp/api")
from xtpapi import Api
from xtp_test_case import xtp_test_case
from xtp_test_case import unittest
sys.path.append("/home/yhl2/workspace/xtp_test/service")
from log import logger
import ServiceConfig
from mainService import ParmIni
from mainService import serviceTest
sys.path.append("/home/yhl2/workspace/xtp_test/ETF/etf_service")
from ETF_mainService import EtfParmIni
from ETF_mainService import etfServiceTest
from QueryEtfQty import QueryEtfQty
from etf_utils import *
sys.path.append("/home/yhl2/workspace/xtp_test/mysql")
from CaseParmInsertMysql import CaseParmInsertMysql
from getUpOrDownPrice import getUpPrice
sys.path.append("/home/yhl2/workspace/xtp_test/ETF/etf_mysql")
from QueryEtfComponentsCodeDB import *
from QueryEtfComponentsDB import QueryEtfComponentsDB