#! /bin/bash

source /home/yhl7/.bashrc
nohup python /home/yhl2/workspace/xtp_test/Quote/SUB_ALL_MARKET_DATA.py &
nohup python /home/yhl2/workspace/xtp_test/Quote/SUB_ALL_ORDER_BOOK.py &
nohup python /home/yhl2/workspace/xtp_test/Quote/SUB_ALL_TICK_BY_TICK.py &
