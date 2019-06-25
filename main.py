from ib.opt import Connection, message
from ib.ext.Contract import Contract
from ib.ext.Order import Order

ibConnection = None

def make_contract(symbol, sec_type, exch, prim_exchange, curr):
    Contract.m_symbol = symbol
    Contract.m_secType = sec_type
    Contract.m_exchange = exch
    Contract.m_primaryExch = prim_exchange
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

#Step 1. Establish connection
ibConnection = Connection.create(port=7497, clientId=999)
ibConnection.connect()

#Step 2. But 123 NVDA
oid = 300
cont = make_contract('TSLA', 'STK', 'SMART', 'SMART', 'USD')
order = make_order('BUY', 130, 200)
ibConnection.placeOrder(oid, cont, order)

#Step 3. Disconnect
ibConnection.disconnect();