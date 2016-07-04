#! /usr/bin/env python
# -*- coding: utf-8 -*-

from ib.ext.Contract import Contract
from ib.opt import ibConnection, message
from time import sleep
import time
from datetime import datetime


# print all messages from TWS
def watcher(msg):
    print msg

# show Bid and Ask quotes
def my_BidAsk(msg):
    '''
    if msg.field == 1:
        print '%s:%s: bid: %s' % (contractTuple[0],
                       contractTuple[6], msg.price)
    elif msg.field == 2:
        print '%s:%s: ask: %s' % (contractTuple[0], contractTuple[6], msg.price)
    elif msg.field == 9:
        print '%s:%s: shoupan: %s' % (contractTuple[0], contractTuple[6], msg.price)
    elif msg.field == 6:
        print '%s:%s: High: %s' % (contractTuple[0], contractTuple[6], msg.price)
    elif msg.field == 7:
        print '%s:%s: Low: %s' % (contractTuple[0], contractTuple[6], msg.price)
    elif msg.field == 4:
        print '%s:%s: ZuiHou: %s' % (contractTuple[0], contractTuple[6], msg.price)
    '''

    if msg.field == 4:
        print '%s:%s: ZuiHou: %s' % (contractTuple[0], contractTuple[6], msg.price)

    if msg.tickType==48:
        data_stock=msg.value.split(';')
        last_price=data_stock[0]
        last_volume=data_stock[1]
        last_time=datetime.fromtimestamp(float(data_stock[2])/1000).strftime("%Y-%m-%d %H:%M:%S")
        last_trade_independant=data_stock[5]
        print '%s:%s: ZuiHou: %s' % (contractTuple[0], contractTuple[6], msg.value)
        #Warning!!!!!
        if int(last_volume)>0:
            print '%s   %s' % (last_time,last_price)

def makeStkContract(contractTuple):
    newContract = Contract()
    newContract.m_symbol = contractTuple[0]
    newContract.m_secType = contractTuple[1]
    newContract.m_exchange = contractTuple[2]
    newContract.m_currency = contractTuple[3]
    newContract.m_expiry = contractTuple[4]
    newContract.m_strike = contractTuple[5]
    newContract.m_right = contractTuple[6]
    if contractTuple[0]=='ASHR':
        newContract.m_primaryExch = 'ARCA'
    print 'Contract Values:%s,%s,%s,%s,%s,%s,%s:' % contractTuple
    return newContract

if __name__ == '__main__':
    con = ibConnection()
    con.registerAll(watcher)
    showBidAskOnly = True  # set False to see the raw messages
    '''
    if showBidAskOnly:
        con.unregister(watcher, message.tickSize, message.tickPrice,
                       message.tickString, message.tickOptionComputation)
        #con.register(my_BidAsk, message.tickPrice)
        con.register(my_BidAsk, message.tickString)
    '''
    con.connect()
    sleep(1)
    tickId = 130

    # Note: Option quotes will give an error if they aren't shown in TWS
    '''
    <error id=-1, errorCode=2104, errorMsg=Market data farm connection is OK:usfarm.us>
<error id=130, errorCode=10090, errorMsg=Part of requested market data is not subscribed. Subscription-independent ticks are still active.BABA NYSE/TOP/BID_ASK>
<error id=130, errorCode=354, errorMsg=Requested market data is not subscribed.Error&NYSE/STK/Top>
<error id=-1, errorCode=2108, errorMsg=Market data farm connection is inactive but should be available upon demand.usfarm.us>
<error id=-1, errorCode=2108, errorMsg=Market data farm connection is inactive but should be available upon demand.usfarm.us>
<error id=-1, errorCode=2108, errorMsg=Market data farm connection is inactive but should be available upon demand.cashfarm>
    '''
    #contractTuple = ('INDU', 'IND', 'NYSE', 'USD', '', 0.0, '')
    #contractTuple = ('BABA', 'STK', 'NYSE', 'USD', '', 0.0, '')
    contractTuple = ('NDX', 'IND', 'NASDAQ', 'USD', '', 0.0, '')
    #error id=15, errorCode=10090, errorMsg=Part of requested market data is not subscribed. Subscription-independent ticks are still active.ASHR ARCA/TOP/BID_ASK
    #只是显示一次数据就停下来
    '''
    此聊天相关咨询单号码为484855
    Siteng J: US Value Bundle只包含一些交易所
    Siteng J: 但并不包括ARCA
    wzrib2015: 那我需要订哪个市场数据？
    Siteng J: Network B (AMEX/CTA) (NP,L1)
    wzrib2015: 这个Network B包括 BABA，GOOG这些市场数据吗
    Siteng J: 市场数据不是指定具体股票的
    Siteng J: 而是指定exchange
    Siteng J: 比如说Network B提供所有ARCA交易所的市场数据
    Siteng J: 比如GOOG您需要Network C (NASDAQ/UTP)(NP,L1)
    Siteng J: BABA需要Network A (NYSE/CTA) (NP,L1)
    Siteng J: 简单来说基本上US Value Bundle加上三个Network就可以包含所有US Stocks数据了
    '''
    #contractTuple = ('ASHR', 'STK', 'ARCA', 'USD', '', 0.0, '')

    #contractTuple = ('700', 'STK', 'SEHK', 'HKD', '', 0.0, '')
    #contractTuple = ('QQQQ', 'OPT', 'SMART', 'USD', '20070921', 47.0, 'CALL')
    #contractTuple = ('ES', 'FUT', 'GLOBEX', 'USD', '200709', 0.0, '')
    #contractTuple = ('ES', 'FOP', 'GLOBEX', 'USD', '20070920', 1460.0, 'CALL')
    #contractTuple = ('EUR', 'CASH', 'IDEALPRO', 'USD', '', 0.0, '')
    stkContract = makeStkContract(contractTuple)
    print '* * * * REQUESTING MARKET DATA * * * *'
    con.reqMktData(tickId, stkContract, '233', False)
    sleep(1)
    print '* * * * CANCELING MARKET DATA * * * *'
    con.cancelMktData(tickId)
    con.disconnect()
    sleep(1)
    tickId =tickId+ 1
    con.reqMktData(tickId, stkContract, '', False)
    sleep(15)
    print '* * * * CANCELING MARKET DATA * * * *'
    con.cancelMktData(tickId)
    con.disconnect()
    sleep(1)
