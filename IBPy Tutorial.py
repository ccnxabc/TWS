from ib.opt import Connection, message
from ib.ext.Contract import Contract
from ib.ext.Order import Order
import time



#https://pythonprogramming.net/ibpy-tutorial-using-interactive-brokers-api-python/
#IBPy Tutorial for using Interactive Brokers API with Python

#watcher(msg) copy from github  ...\IbPy\demo\fancy_marketdata
# print all messages from TWS
def watcher(msg):
    print msg

def makeStkContract(contractTuple):
    newContract = Contract()
    newContract.m_symbol = contractTuple[0]
    newContract.m_secType = contractTuple[1]
    newContract.m_exchange = contractTuple[2]
    newContract.m_currency = contractTuple[3]
    newContract.m_expiry = contractTuple[4]
    newContract.m_strike = contractTuple[5]
    newContract.m_right = contractTuple[6]
    print 'Contract Values:%s,%s,%s,%s,%s,%s,%s:' % contractTuple
    return newContract

def make_contract(symbol, sec_type, exch, prim_exch, curr):

    Contract.m_symbol = symbol
    Contract.m_secType = sec_type
    Contract.m_exchange = exch
    Contract.m_primaryExch = prim_exch
    Contract.m_currency = curr
    return Contract



def make_order(action,quantity, price = None):

    if price is not None:
        order = Order()
        order.m_orderType = 'LMT'
        order.m_totalQuantity = quantity
        order.m_action = action
        order.m_lmtPrice = price

    else:
        order = Order()
        order.m_orderType = 'MKT'
        order.m_totalQuantity = quantity
        order.m_action = action


    return order


#cid = 303
#Use the time as random cid
cid=int(time.time())

while __name__ == "__main__":

    #because of there is no define for clientID in TWS,delete it here.
    conn = Connection.create(port=7496, clientId=999)
    #conn = Connection.create(port=7496)

    #registerAll(watcher) copy from github  ...\IbPy\demo\fancy_marketdata
    conn.registerAll(watcher)

    conn.connect()
    oid = cid

    #USA Stock Exchange
    #cont = make_contract('TSLA', 'STK', 'SMART', 'SMART', 'USD')
    #offer = make_order('BUY', 1, 200)

    #HK Stock Exchange
    cont = make_contract('177', 'STK', 'SEHK', 'SEHK', 'HKD')
    offer = make_order('BUY', 2000, 10.00)

    conn.placeOrder(oid, cont, offer)

    conn.disconnect()
    x = raw_input('enter to resend')
    cid += 1
