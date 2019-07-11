from ibapi.wrapper import EWrapper, OrderId
from ibapi.client import EClient
from threading import Thread
from ibapi.order import Order
from ibapi.contract import Contract
from ibapi.common import ListOfContractDescription
from ibapi.common import BarData
from ibapi.common import TickerId
from ibapi.ticktype import TickType
from ibapi.common import TickAttrib
from ibapi.contract import ContractDetails
from ibapi.order_state import OrderState
from ibapi.tag_value import TagValue

from ibapi import order_condition

from datetime import datetime, timedelta
import queue, time

from time_util import *

from placeorder.pp33_bracket_order_builder import PP33BracketOrderBuilder


class TestWrapper(EWrapper):
    def __init__(self):
        super().__init__()
        self.order_id = 1
        self.next_valid_id_handler = None

    # def init_time(self):
    #     time_queue = queue.Queue()
    #     self._time_queue = time_queue
    #     return time_queue

    def currentTime(self, time_from_server):
        # self._time_queue.put(time_from_server)
        print(str(time_from_server))

    def nextValidId(self, order_id: int):
        self.order_id = order_id
        print("next valid id is " + str(order_id))
        handler = self.next_valid_id_handler
        if handler:
            handler(order_id)

    def symbolSamples(self, reqId:int,
                      contractDescriptions:ListOfContractDescription):
        print("SymbolSamples")
        print("reqId : " + str(reqId))
        for item in contractDescriptions:
            print(item)

    def historicalData(self, reqId: int, bar: BarData):
        print("HistoricalData")
        print("reqId : " + str(reqId))
        print("Date : " + bar.date
              + " barHigh : " + str(bar.high)
              + " barLow : " + str(bar.low)
              + " barOpen : " + str(bar.open)
              + " barClose : " + str(bar.close))
        # datetime_object = datetime.strptime(bar.date, '%Y%m%d %H:%M:%S')
        # print(datetime_object.strftime("%H"))

    def historicalDataUpdate(self, reqId: int, bar: BarData):
        print("HistoricalDataUpdate")
        print("reqId : " + str(reqId))
        print("Date : " + bar.date
              + " barHigh : " + str(bar.high)
              + " barLow : " + str(bar.low)
              + " barOpen : " + str(bar.open)
              + " barClose : " + str(bar.close))

    def historicalDataEnd(self, reqId:int, start:str, end:str):
        print("HistoricalDataEnd")
        print("reqId : " + str(reqId))
        print("Start : " + start + "End : " + end)

    def tickPrice(self, reqId:TickerId , tickType:TickType, price:float,
                  attrib:TickAttrib):
        print("tickPrice")
        print("reqId : " + str(reqId)
              + " tickType : " + str(tickType)
              + " price : " + str(price)
              )

    def tickSize(self, reqId:TickerId, tickType:TickType, size:int):
        print("tickSize")
        print("reqId : " + str(reqId)
              + " tickType : " + str(tickType)
              + " size : " + str(size))

    def tickString(self, reqId:TickerId, tickType:TickType, value:str):
        print("tickString")
        print("reqId : " + str(reqId)
              + " tickType : " + str(tickType)
              + " value : " + value)

    def tickEFP(self, reqId:TickerId, tickType:TickType, basisPoints:float,
                formattedBasisPoints:str, totalDividends:float,
                holdDays:int, futureLastTradeDate:str, dividendImpact:float,
                dividendsToLastTradeDate:float):
        print("tickEFP")
        print("reqId : " + str(reqId))

    def tickGeneric(self, reqId:TickerId, tickType:TickType, value:float):
        print("tickGeneric")
        print("reqId : " + str(reqId)
              + " tickType : " + str(tickType)
              + " value : " + str(value))

    def tickOptionComputation(self, reqId:TickerId, tickType:TickType ,
            impliedVol:float, delta:float, optPrice:float, pvDividend:float,
            gamma:float, vega:float, theta:float, undPrice:float):
        print("tickOptionComputation")
        print("reqId : " + str(reqId)
              + " tickType : " + str(tickType)
              + " optPrice : " + str(optPrice)
              + " delta : " + str(delta)
              + " gamma : " + str(gamma)
              + " theta : " + str(theta)
              + " undPrice : " + str(undPrice)
              + " IV : " + str(impliedVol))

    # def tickSnapshotEnd(self, reqId:int):
    #     print("tickSnapshotEnd")
    #     print("reqId : " + str(reqId))

    def contractDetails(self, reqId:int, contractDetails:ContractDetails):
        print("contractDetails")
        print("reqId : " + str(reqId)
              + " ConId : " + str(contractDetails.contract.conId)
              + " Symbol : " + contractDetails.contract.symbol
              + " ExpiryDate : " + contractDetails.contract.lastTradeDateOrContractMonth
              + " Exchange : " + contractDetails.contract.exchange
              + " Strike : " + str(contractDetails.contract.strike)
              + " RealExpirationDate : " + contractDetails.realExpirationDate
              + " evMultiplier : " + str(contractDetails.evMultiplier)
              + " multiplier : " + str(contractDetails.contract.multiplier)
              )

    def contractDetailsEnd(self, reqId:int):
        print("contractDetailsEnd")
        print("reqId : " + str(reqId))

    def realtimeBar(self, reqId: TickerId, time:int, open_: float, high: float, low: float, close: float,
                        volume: int, wap: float, count: int):
        print("realtimeBar")
        print("reqId : " + str(reqId)
              + " time : " + str(time)
              + " open_ : " + str(open_)
              + " close : " + str(close)
              + " high : " + str(high)
              + " low : " + str(low)
              )

    def accountSummary(self, reqId:int, account:str, tag:str, value:str,
                       currency:str):
        print("accountSummary")
        print("reqId : " + str(reqId)
              + " tag : " + tag + " value : " + value + " currency : " + currency
              )

    def accountSummaryEnd(self, reqId:int):
        print("accountSummaryEnd")
        print("reqId : " + str(reqId))

    def position(self, account:str, contract:Contract, position:float,
                 avgCost:float):
        print("Position")
        print("Account : " + account
              + "\ncon_id : " + str(contract.conId)
              + "\nSymbol : " + contract.symbol + " " + contract.lastTradeDateOrContractMonth + " " + contract.multiplier + " Positon : " + str(position))

    def positionEnd(self):
        print("PositionEnd")

    def positionMulti(self, reqId:int, account:str, modelCode:str,
        contract:Contract, pos:float, avgCost:float):
        print("PositionMulti")
        print("ReqId : " + str(reqId) + " Account : " + account + " ModelCode : " + modelCode
              + "\ncon_id : " + str(contract.conId)
              + "\nSymbol : " + contract.symbol + " " + contract.lastTradeDateOrContractMonth + " " + contract.multiplier + " Pos : " + str(pos))

    def positionMultiEnd(self, reqId:int):
        print("PositionMultiEnd")
        print("ReqId : " + str(reqId))

    def openOrder(self, orderId:OrderId, contract:Contract, order:Order,
                  orderState:OrderState):
        print("openOrder")
        print("OrderId : " + str(orderId) + " Order : " + order.orderType + " " + str(order.totalQuantity) + " " + order.action + " " + str(order.lmtPrice))

    def orderStatus(self, orderId:OrderId , status:str, filled:float,
                    remaining:float, avgFillPrice:float, permId:int,
                    parentId:int, lastFillPrice:float, clientId:int,
                    whyHeld:str, mktCapPrice: float):
        print("orderStatus")
        print("OrderId : " + str(orderId)
              + " Status : " + status
              + " Filled : " + str(filled)
              + " Remaining : " + str(remaining)
              + " AvgFillPrice : " + str(avgFillPrice)
              + " whyHeld : " + whyHeld
              + " mktCapPrice : " + str(mktCapPrice)
              )

    def openOrderEnd(self):
        print("openOrderEnd")

    def updateAccountValue(self, key:str, val:str, currency:str, accountName:str):
        print("")
        # print("updateAccountValue")
        # print("Key : " + key + " Val : " + val + " Currency : " + currency + " AccountName : " + accountName)

    def updatePortfolio(self, contract:Contract, position:float,
                        marketPrice:float, marketValue:float,
                        averageCost:float, unrealizedPNL:float,
                        realizedPNL:float, accountName:str):
        print("updatePortfolio")
        print("Contract : " + contract.symbol + " Position : " + str(position)
              + " unrealizedPNL : " + str(unrealizedPNL)
              + " realizedPNL : " + str(realizedPNL))

    def updateAccountTime(self, timeStamp:str):
        print("")
        # print("updateAccountTime")
        # print("TimeStamp : " + timeStamp)

    def pnl(self, reqId: int, dailyPnL: float, unrealizedPnL: float, realizedPnL: float):
        print("pnl")
        print("reqId : " + str(reqId)
              + " dailyPnl : " + str(dailyPnL) + " unrealizedPnL : " + str(unrealizedPnL)
              + " realizedPnL : " + str(realizedPnL))

    def pnlSingle(self, reqId: int, pos: int, dailyPnL: float, unrealizedPnL: float, realizedPnL: float, value: float):
        print("pnlSingle")
        print("reqId : " + str(reqId) + " pos : " + str(pos)
              + " dailyPnl : " + str(dailyPnL) + " unrealizedPnL : " + str(unrealizedPnL)
              + " realizedPnL : " + str(realizedPnL) + " value : " + str(value))


class TestClient(EClient):
    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)

    def retrieve_time(self):
        print("\nGetting the time from the server")
        time_storage = self.wrapper.init_time()
        self.reqCurrentTime()
        return time_storage.get()

    def testFunction(self, oid):
        print(self.wrapper.getNextReqId(oid=oid))

    def testPlaceOrder(self, oid, contract, order):
        self.placeOrder(self, orderId=oid, contract=contract, order=order)


class TestApp(TestWrapper, TestClient):
    def __init__(self, ipaddress, portid, clientid):
        TestWrapper.__init__(self)
        TestClient.__init__(self, wrapper=self)

        # self.next_valid_id_handler = self.put_single_order
        # self.next_valid_id_handler = self.put_oca_order
        # self.next_valid_id_handler = self.put_order_with_condition
        # self.next_valid_id_handler = self.basic_order
        # self.next_valid_id_handler = self.put_single_order
        # self.next_valid_id_handler = self.cancel_order

        # self.next_valid_id_handler = self.query_data

        self.connect(ipaddress, portid, clientid)

        thread = Thread(target=self.run)
        thread.start()
        setattr(self, "_thread", thread)

    def index_contract(self):
        spx_contract = Contract()
        spx_contract.symbol = 'SPX'
        spx_contract.secType = "IND"
        spx_contract.exchange = "CBOE"
        return spx_contract

    def stock_contract(self):
        amzn_contract = Contract()
        amzn_contract.symbol = 'AMZN'
        amzn_contract.secType = 'STK'
        amzn_contract.exchange = 'SMART'
        amzn_contract.currency = 'USD'
        return amzn_contract

    def forex_contract(self):
        forex_contract = Contract()
        forex_contract.symbol = 'EUR'
        forex_contract.secType = 'CASH'
        forex_contract.exchange = 'IDEALPRO'
        forex_contract.currency = 'GBP'

    def query_data(self, order_id:int):
        self.reqMktData(
            reqId=order_id,
            contract=self.stock_contract(),
            genericTickList='221',
            snapshot=False,
            regulatorySnapshot=False,
            mktDataOptions=[]
        )

    def replace_order(self, order_id:int, new_lmt_price, contract:Contract):
        parent = Order()
        parent.orderId = order_id
        parent.action = "buy"
        parent.orderType = "LMT"
        parent.totalQuantity = 1
        parent.lmtPrice = new_lmt_price
        parent.transmit = True

        self.placeOrder(order_id, contract, parent)

    def cancel_order(self, order_id:int):
        self.cancelOrder(870)

    def put_single_order(self, order_id:int):
        contract_opt = self.contract_spx()
        parent = Order()
        parent.orderId = order_id
        parent.action = "buy"
        parent.orderType = "LMT"
        parent.totalQuantity = 1
        parent.lmtPrice = 32.5
        parent.transmit = True

        self.placeOrder(order_id, contract_opt, parent)

    def basic_order(self, order_id:int):
        contract_aapl = self.contract_aapl()

        parent = Order()
        parent.orderId = order_id
        parent.action = "buy"
        parent.orderType = "LMT"
        parent.totalQuantity = 1
        parent.lmtPrice = 8
        parent.transmit = False

        option_contract = Contract()
        option_contract.symbol = 'TSLA'
        option_contract.secType = "OPT"
        option_contract.exchange = "SMART"
        option_contract.primaryExchange = "SMART"
        option_contract.currency = "USD"
        option_contract.strike = 310.0
        option_contract.lastTradeDateOrContractMonth = "20190315"
        option_contract.right = "P"

        pp33_order_builder = PP33BracketOrderBuilder(order_id, parent)

        for order_in_bracket in pp33_order_builder.bracket_order_list():
            self.placeOrder(order_in_bracket.orderId, option_contract, order_in_bracket)
            # time.sleep(5)



    def make_contract(self, symbol, secType, exchange,
                      primaryExchange, currency,
                      lastTradeDateOrContractMonth=None,
                      strike=None,
                      right=None,
                      multiplier=None,
                      tradingClass=None):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = secType
        contract.exchange = exchange
        contract.primaryExchange = primaryExchange
        contract.currency = currency
        if lastTradeDateOrContractMonth is not None:
            contract.lastTradeDateOrContractMonth = lastTradeDateOrContractMonth
        if strike is not None:
            contract.strike = strike
        if right is not None:
            contract.right = strike
        if multiplier is not None:
            contract.multiplier = multiplier
        if tradingClass is not None:
            contract.tradingClass = tradingClass

        return contract


    def contract_amzn_opt(self):
        incomplete_contract = Contract()
        incomplete_contract.symbol = 'AMZN'
        incomplete_contract.secType = "OPT"
        incomplete_contract.exchange = "SMART"
        incomplete_contract.currency = "USD"
        incomplete_contract.strike = 1900
        incomplete_contract.lastTradeDateOrContractMonth = "20190719"
        incomplete_contract.right = "C"
        return incomplete_contract


    def contract_aapl(self):
        return self.make_contract(
            symbol='AAPL',
            secType='STK',
            exchange='SMART',
            primaryExchange='SMART',
            currency='USD'
        )

    def contract_spx(self):
        contract =  make_contract(
            symbol='SPX',
            secType='OPT',
            exchange='SMART',
            primaryExchange='SMART',
            currency='USD',
            lastTradeDateOrContractMonth='20190710',
            strike=2935,
            right='P',
            multiplier='100'
        )
        # contract.conId = '370568877'
        contract.conId = '370568978'
        return contract

    def contract_es(self):
        return make_contract(
            symbol='ES',
            secType='FUT',
            exchange='GLOBEX',
            primaryExchange='GLOBEX',
            currency='USD',
            lastTradeDateOrContractMonth='201903'
        )

    def contract_bidu_option(self):
        # ! [optcontract]
        contract = Contract()
        contract.symbol = "BIDU"
        contract.secType = "OPT"
        contract.exchange = "SMART"
        contract.currency = "USD"
        contract.lastTradeDateOrContractMonth = "20190322"
        contract.strike = 165
        contract.right = "PUT"
        contract.multiplier = "100"
        # ! [optcontract]
        return contract

    def contract_spx_option(self):
        contract = Contract()
        contract.symbol = 'SPX'
        contract.secType = "OPT"
        contract.exchange = "SMART"
        contract.primaryExchange = "SMART"
        contract.currency = "USD"
        contract.strike = 2800
        contract.lastTradeDateOrContractMonth = "20190329"
        contract.right = "C"
        return contract

    def bracket_order(self, parent_order_id: int, action: str, quantity: float,
                      lmt_price: float, take_profit_lmt_price: float,
                      stop_loss_price: float):
        parent = Order()
        parent.orderId = parent_order_id
        parent.action = action
        # parent.orderType="MKT"
        parent.orderType = "LMT"
        parent.lmtPrice = lmt_price
        parent.totalQuantity = quantity
        self.fill_adaptive_params(parent, "Normal")
        # parent.conditions.append(
        #     self.price_condition(order_condition.PriceCondition.TriggerMethodEnum.Last, 265598, "SMART", 150, False,
        #                          True)
        # )
        parent.transmit = False
        print('parent_order_id : ' + str(parent_order_id))


        take_profit = Order()
        take_profit.orderId = parent.orderId + 1
        take_profit.action = "SELL" if action == "BUY" else "BUY"
        take_profit.orderType = "LMT"
        take_profit.totalQuantity = quantity
        take_profit.lmtPrice = take_profit_lmt_price
        take_profit.parentId = parent_order_id
        take_profit.transmit = False

        # stop_loss = Order()
        # stop_loss.orderId = parent.orderId + 2
        # stop_loss.action = "SELL" if action == "BUY" else "BUY"
        # # stop_loss.orderType = "STP"
        # stop_loss.orderType = "TRAIL"
        # stop_loss.trailingPercent = 20
        # # stop_loss.auxPrice = 2.00
        # stop_loss.totalQuantity = quantity
        # stop_loss.parentId = parent_order_id
        # stop_loss.transmit = False

        # trail_limit_order = Order()
        # trail_limit_order.action = action
        # trail_limit_order.orderType = "TRAIL LIMIT"
        # trail_limit_order.totalQuantity = quantity
        # # trail_limit_order.trailStopPrice = trailStopPrice
        # trail_limit_order.lmtPriceOffset = 2.00
        # trail_limit_order.auxPrice = 2.00

        stop_loss = Order()
        stop_loss.orderId = parent.orderId + 2
        stop_loss.action = "SELL" if action == "BUY" else "BUY"
        stop_loss.orderType = 'TRAIL'
        stop_loss.totalQuantity = quantity
        stop_loss.trailingPercent = PP33BracketOrderBuilder.TRAIL_STOP_PERCENTAGE
        stop_loss.parentId = parent_order_id
        stop_loss.transmit = True

        # expiry_quit = Order()
        # expiry_quit.orderId = parent.orderId + 3
        # expiry_quit.action = "SELL" if action == "BUY" else "BUY"
        # expiry_quit.orderType = "MKT"
        # expiry_quit.totalQuantity = quantity
        # expiry_quit.parentId = parent_order_id
        # current_time = datetime.today()
        # cancel_time = current_time + timedelta(minutes=3)
        # cancel_time_str = cancel_time.strftime("%Y%m%d %H:%M:%S")
        # expiry_quit.conditions.append(self.time_condition(True, cancel_time_str))
        # expiry_quit.transmit = True

        bracket_order_list = [parent, take_profit, stop_loss]
        return bracket_order_list

    def fill_adaptive_params(self, baseOrder: Order, priority: str):
        baseOrder.algoStrategy = "Adaptive"
        baseOrder.algoParams = []
        baseOrder.algoParams.append(TagValue("adaptivePriority", priority))

    def put_bracket_order(self, order_id: int):
        bracket = self.bracket_order(order_id, "BUY", 1, 200, 220, 180)
        contract_aapl = self.contract_aapl()
        contract_bidu_option = self.contract_bidu_option()
        for order_in_bracket in bracket:
            self.placeOrder(order_in_bracket.orderId, contract_aapl, order_in_bracket)

        time.sleep(10)
        bracket[0].lmtPrice = 205
        bracket[0].transmit = True
        self.placeOrder(bracket[0].orderId, contract_aapl, bracket[0])

    def one_cancels_all(self, oca_orders, oca_group, oca_type):
        for o in oca_orders:
            o.ocaGroup = oca_group
            o.ocaType = oca_type
        return oca_orders

    def put_oca_order(self, order_id:int):
        contract_opt = self.contract_spx()
        parent = Order()
        parent.orderId = order_id
        parent.action = "buy"
        parent.orderType = "LMT"
        parent.totalQuantity = 1
        parent.lmtPrice = 32.5
        parent.transmit = False

        self.placeOrder(order_id, contract_opt, parent)

        pp33_bracket = PP33BracketOrderBuilder(parent, contract_opt.symbol)

        order_id += 1
        self.take_profit_order = pp33_bracket.take_profit_order
        self.take_profit_order.orderId = order_id

        order_id += 1
        self.stop_loss_order = pp33_bracket.stop_loss_order
        self.stop_loss_order.orderId = order_id

        order_id += 1
        self.quit_before_close_order = pp33_bracket.quit_before_close_order
        self.quit_before_close_order.orderId = order_id

        self.placeOrder(self.take_profit_order.orderId, contract_opt, self.take_profit_order)
        self.placeOrder(self.stop_loss_order.orderId, contract_opt, self.stop_loss_order)
        self.placeOrder(self.quit_before_close_order.orderId, contract_opt, self.quit_before_close_order)


    def time_condition(self, is_more:bool, time:str):
        time_condition = order_condition.Create(order_condition.OrderCondition.Time)
        time_condition.isMore = is_more
        time_condition.time = time
        time_condition.isConjunctionConnection = True
        return time_condition

    def price_condition(self, trigger_method: int, con_id: int, exchange: str, price: float,
                       is_more: bool, is_conjunction: bool):

        priceCondition = order_condition.Create(order_condition.OrderCondition.Price)
        priceCondition.conId = con_id
        priceCondition.exchange = exchange
        priceCondition.isMore = is_more
        priceCondition.triggerMethod = trigger_method
        priceCondition.price = price
        priceCondition.isConjunctionConnection = is_conjunction
        return priceCondition

    def put_order_with_condition(self, order_id:int):
        order1 = Order()
        order1.orderId = order_id
        order1.action = "buy"
        order1.orderType = "LMT"
        order1.totalQuantity = 1
        order1.lmtPrice = 160
        current_time = datetime.today()
        cancel_time = current_time + timedelta(minutes=3)
        cancel_time_str = cancel_time.strftime("%Y%m%d %H:%M:%S")

        order1.conditions.append(self.time_condition(False, cancel_time_str))
        order1.conditions.append(
            self.price_condition(order_condition.PriceCondition.TriggerMethodEnum.Last, 265598, "SMART", 150, False, True)
        )
        contract_aapl = self.contract_aapl()

        # order2 = Order()
        # order2.orderId = order_id
        # order2.action = "buy"
        # order2.orderType = "MKT"
        # order2.totalQuantity = 1
        # order2.conditions.append(self.time_condition(False, "20190226 12:18:00"))
        # contract_es = self.contract_es()

        self.placeOrder(order_id, contract_aapl, order1)

def AAPLStockContract():
    # ! [usstockcfd_conract]
    contract = Contract()
    contract.symbol = "AMZN"
    contract.secType = "STK"
    contract.currency = "USD"
    contract.exchange = "SMART"
    contract.primaryExchange = "SMART"
    # ! [usstockcfd_conract]
    return contract


def default_order():
    order = Order()
    order.action = "BUY"
    order.orderType = "LMT"
    order.totalQuantity = 100
    order.lmtPrice = 100
    return order

def OptionWithLocalSymbol():
    contract = Contract()

    contract.localSymbol = "C SPX  JAN 16  2450"
    contract.secType = "OPT"
    contract.exchange = "SMART"
    contract.primaryExchange="SMART"
    contract.currency = "USD"

    return contract

def OptionWithTradingClass():
    contract = Contract()
    contract.symbol = "SPX"
    contract.secType = "OPT"
    contract.exchange = "SMART"
    contract.primaryExchange = "SMART"
    contract.currency = "USD"
    contract.lastTradeDateOrContractMonth = "20190219"
    contract.strike = 2520
    contract.right = "C"
    contract.multiplier = "100"
    contract.tradingClass = "SPX"
    return contract

def OptionAtBOX():
    #! [optcontract]
    contract = Contract()
    contract.symbol = "AMZN"
    contract.secType = "OPT"
    contract.exchange = "SMART"
    contract.currency = "USD"
    contract.lastTradeDateOrContractMonth = "20190125"
    contract.strike = 1570
    contract.right = "C"
    contract.multiplier = "100"
    #! [optcontract]
    return contract

def make_contract(symbol, secType, exchange,
                  primaryExchange, currency,
                  lastTradeDateOrContractMonth=None,
                  strike=None,
                  right=None,
                  multiplier=None,
                  tradingClass=None):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = secType
    contract.exchange = exchange
    contract.primaryExchange = primaryExchange
    contract.currency = currency
    if lastTradeDateOrContractMonth is not None:
        contract.lastTradeDateOrContractMonth = lastTradeDateOrContractMonth
    if strike is not None:
        contract.strike = strike
    if right is not None:
        contract.right = strike
    if multiplier is not None:
        contract.multiplier = multiplier
    if tradingClass is not None:
        contract.tradingClass = tradingClass

    return contract


def make_order(action, quantity, price=None):
    if price is not None:
        order = Order()
        order.orderType = "LMT"
        order.totalQuantity = quantity
        order.action = action
        order.lmtPrice = price

    else:
        order = Order()
        order.orderType = "MKT"
        order.totalQuantity = quantity
        order.action = action

    return order

def index_contract():
    spx_contract = Contract()
    spx_contract.conId = "416904"
    spx_contract.symbol = 'SPX'
    spx_contract.secType = "IND"
    spx_contract.exchange = "CBOE"
    return spx_contract

def stock_contract():
    amzn_contract = Contract()
    amzn_contract.symbol = 'AMZN'
    amzn_contract.secType = 'STK'
    amzn_contract.exchange = 'SMART'
    amzn_contract.currency = 'USD'
    return amzn_contract

def forex_contract():
    forex_contract = Contract()
    forex_contract.symbol = 'EUR'
    forex_contract.secType = 'CASH'
    forex_contract.exchange = 'IDEALPRO'
    forex_contract.currency = 'GBP'
    return forex_contract

def forex_contract2():
    forex_contract = Contract()
    forex_contract.symbol = 'USD'
    forex_contract.secType = 'CASH'
    forex_contract.exchange = 'IDEALPRO'
    forex_contract.currency = 'JPY'
    return forex_contract

def forex_contract3():
    forex_contract = Contract()
    forex_contract.symbol = 'EUR'
    forex_contract.secType = 'CASH'
    forex_contract.exchange = 'IDEALPRO'
    forex_contract.currency = 'JPY'
    return forex_contract


app = None


# def order_place():
#     if not app:
#         return
#     if app.wrapper.order_id >= 0:
#         return
#
#     contract = make_contract(symbol='AAPL', secType='STK', exchange='SMART', primaryExchange='SMART', currency='USD')
#     # contract = OptionAtBOX()
#     my_order = make_order('buy', 1)
#     app.placeOrder(orderId=app.wrapper.order_id, contract=contract, order=my_order)
#     app.reqIds(0)
#     return

def calculate_john_person_pivots(close:float, high:float, low:float):
    pp = (close + high + low) / 3
    r1 = 2 * pp - low
    r2 = pp + high - low
    r3 = r2 + high - low
    s1 = 2 * pp - high
    s2 = pp - high + low
    s3 = s2 - high + low
    return {'pp':pp, 'r1':r1, 'r2':r2, 'r3':r3, 's1':s1, 's2':s2, 's3':s3}



if __name__ == '__main__':
    app = TestApp("127.0.0.1", 7497, 999)

    # app.reqPositions()
    # time.sleep(2)
    # app.cancelPositions()
    # app.reqPositionsMulti(reqId=3, account='DU812882', modelCode='')
    # current_time = app.retrieve_time()

    current_time = app.reqCurrentTime()

    # app.reqAllOpenOrders()

    # incomplete_contract = Contract()
    # incomplete_contract.symbol='AMZN'
    # incomplete_contract.secType="OPT"
    # incomplete_contract.exchange = "SMART"
    # # incomplete_contract.primaryExchange = "SMART"
    # incomplete_contract.currency = "USD"
    # incomplete_contract.strike=1700
    # incomplete_contract.lastTradeDateOrContractMonth="201903"
    # incomplete_contract.right="C"
    #
    # app.reqContractDetails(1, incomplete_contract)

    # app.reqPositions()
    #
    # time.sleep(5)
    #
    # app.reqPositions()

    # print(time.ctime(current_time))
    # app.reqPositions()
    # app.reqAccountSummary(
    #     1,
    #     'All',
    #     'NetLiquidation'
    # )

    app.reqPnL(
        reqId=1,
        account="DU812882",
        modelCode=''
    )

    # app.reqPnLSingle(
    #     reqId=1,
    #     account="DU812882",
    #     modelCode="",
    #     conid=349258186
    # )

    # app.reqPositionsMulti(reqId=1, account='DU812882', modelCode='Core')
    # app.reqAllOpenOrders()
    # app.reqOpenOrders()
    # app.reqAccountUpdates(subscribe=True, acctCode="")

    # # queryTime = (datetime.datetime.today() - datetime.timedelta(days=180)).strftime("%Y%m%d %H:%M:%S")
    # queryTime = datetime.datetime.today().strftime("%Y%m%d %H:%M:%S")

    # contract_es = make_contract(
    #     symbol='ES',
    #     secType='FUT',
    #     exchange='GLOBEX',
    #     primaryExchange='GLOBEX',
    #     currency='USD',
    #     lastTradeDateOrContractMonth='201903'
    # )

    # app.reqMktData(
    #     reqId=1,
    #     contract=contract_es,
    #     genericTickList='221',
    #     snapshot=False,
    #     regulatorySnapshot=False,
    #     mktDataOptions=[]
    # )

    # print("Hour : " + str(datetime.datetime.today().hour))
    # hour = datetime.datetime.today().hour
    # if hour < 5:
    #     endTime = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%Y%m%d 05:00:00")
    # else:
    #     endTime = (datetime.datetime.today()).strftime("%Y%m%d 05:00:00")
    # print("Time : " + endTime)
    #
    # contract_spx = make_contract(
    #     symbol='SPX',
    #     secType='IND',
    #     exchange='CBOE',
    #     primaryExchange='CBOE',
    #     currency='USD'
    # )
    #
    # contract_amzn = make_contract(
    #     symbol='AMZN',
    #     secType='STK',
    #     exchange='SMART',
    #     primaryExchange='SMART',
    #     currency='USD'
    # )
    # order = make_order('buy', 1, 1600)
    # my_order_id = 18
    #
    # app.placeOrder(my_order_id, contract_amzn, order)
    # time.sleep(10)
    # app.cancelOrder(my_order_id)

    # app.reqHistoricalData(
    #     reqId=2,
    #     contract=contract_es,
    #     endDateTime=endTime,
    #     durationStr="720 S",
    #     barSizeSetting = "3 mins",
    #     whatToShow="TRADES",
    #     useRTH = 0,
    #     formatDate = 1,
    #     keepUpToDate = False,
    #     chartOptions = []
    # )

    #
    # app.reqHistoricalData(
    #     reqId=1,
    #     contract=contract_amzn,
    #     durationStr="720 S",
    #     barSizeSetting = "3 mins",
    #     whatToShow="TRADES",
    #     useRTH = 0,
    #     formatDate = 1,
    #     keepUpToDate = True,
    #     chartOptions = []
    # )

    # #
    # app.reqHistoricalData(
    #     reqId=2,
    #     contract=contract_amzn,
    #     endDateTime=endTime,
    #     durationStr="720 S",
    #     barSizeSetting = "3 mins",
    #     whatToShow="TRADES",
    #     useRTH = 1,
    #     formatDate = 1,
    #     keepUpToDate = False,
    #     chartOptions = []
    # )

    #
    # result = calculate_john_person_pivots(close=1674.56, high=1675.16, low=1626.01)
    # print(result['r2'])

    # contract = make_contract(
    #     symbol='SPX',
    #     secType='OPT',
    #     exchange='SMART',
    #     primaryExchange='SMART',
    #     currency='USD',
    #     lastTradeDateOrContractMonth='20190122',
    #     strike=2450,
    #     right='C',
    #     multiplier='100',
    #     tradingClass='SPXW'
    # )

    # app.reqHistoricalData(
    #     reqId = 8,
    #     contract = contract,
    #     endDateTime = "",
    #     durationStr = "180 S",
    #     barSizeSetting = "3 mins",
    #     whatToShow = "TRADES",
    #     useRTH = 0,
    #     formatDate = 1,
    #     keepUpToDate = True,
    #     chartOptions = []
    # )



    # app.reqRealTimeBars(
    #     reqId = 1,
    #     contract = contract,
    #     barSize = 0,
    #     whatToShow = 'TRADES',
    #     useRTH = False,
    #     realTimeBarsOptions = []
    # )

    # app.reqMktData(
    #     reqId=1,
    #     contract=OptionWithTradingClass(),
    #     genericTickList='221',
    #     snapshot=False,
    #     regulatorySnapshot=False,
    #     mktDataOptions=[]
    # )

    # contract3 = Contract()
    # contract3.symbol='SPX'
    # contract3.secType='IND'
    # contract3.exchange="CBOE"

    # app.reqContractDetails(1, incomplete_contract)

    # incomplete_contract = Contract()
    # incomplete_contract.symbol='ES'
    # incomplete_contract.secType="FOP"
    # incomplete_contract.exchange="GLOBEX"
    # incomplete_contract.currency = "USD"
    # incomplete_contract.lastTradeDateOrContractMonth = "20190128"
    # incomplete_contract.strike=2670
    # incomplete_contract.right="C"

    # contract_aapl = make_contract(
    #     symbol='AAPL',
    #     secType='STK',
    #     exchange='SMART',
    #     primaryExchange='SMART',
    #     currency='USD'
    # )
    #
    # contract_amzn = make_contract(
    #     symbol='AMZN',
    #     secType='STK',
    #     exchange='SMART',
    #     primaryExchange='SMART',
    #     currency='USD'
    # )

    # incomplete_contract = Contract()
    # incomplete_contract.symbol='ES'
    # incomplete_contract.secType="FOP"
    # incomplete_contract.exchange = "GLOBEX"
    # # incomplete_contract.primaryExchange = "SMART"
    # incomplete_contract.currency = "USD"
    # incomplete_contract.strike=2800
    # incomplete_contract.lastTradeDateOrContractMonth="20190329"
    # incomplete_contract.right="C"
    #

    # contract_spx = make_contract(
    #     symbol='RUT',
    #     secType='IND',
    #     exchange='CBOE',
    #     primaryExchange='CBOE',
    #     currency='USD'
    # )
    #
    # incomplete_contract = Contract()
    # incomplete_contract.symbol='NDX'
    # incomplete_contract.secType="IND"
    # incomplete_contract.currency = "USD"
    # incomplete_contract.exchange = "NASDAQ"
    #



    # spx_option_contract = Contract()
    # spx_option_contract.symbol='SPX'
    # spx_option_contract.secType='OPT'
    # spx_option_contract.exchange='SMART'
    # spx_option_contract.currency='USD'
    # spx_option_contract.right='C'
    # spx_option_contract.strike=2800
    # # spx_option_contract.lastTradeDateOrContractMonth='20181217'
    # spx_option_contract.lastTradeDateOrContractMonth='20190325'
    #
    # today_open = get_prev_day_market_close_time(datetime.now())
    # #
    # queryTime = (today_open - timedelta(days=32))
    # # queryTime = today_open
    # queryTimeStr = queryTime.strftime("%Y%m%d %H:%M:%S")
    # print(queryTime)
    # queryTime2 = (queryTime - timedelta(seconds=3600))
    # queryTime2Str = queryTime2.strftime("%Y%m%d %H:%M:%S")
    #
    # test_time = (today_open + timedelta(hours=4)).strftime("%Y%m%d %H:%M:%S")
    #
    # print('test_time : ' + test_time)
    # print('queryTimeStr : ' + queryTimeStr)
    # print('queryTime2Str : ' + queryTime2Str)

    # forex_contract = Contract()
    # forex_contract.symbol='GBP'
    # forex_contract.secType='CFD'
    # forex_contract.exchange='SMART'
    # forex_contract.currency='USD'

    # app.reqHistoricalData(
    #     reqId = 1,
    #     contract = forex_contract2(),
    #     endDateTime = '20190503 06:00:00',
    #     durationStr = "1 D",
    #     barSizeSetting = "3 mins",
    #     whatToShow = "MIDPOINT",
    #     useRTH = 0,
    #     formatDate = 1,
    #     keepUpToDate = False,
    #     chartOptions = []
    # )

    # spx_contract = make_contract(
    #         symbol='SPX',
    #         secType='OPT',
    #         exchange='SMART',
    #         primaryExchange='SMART',
    #         currency='USD',
    #         lastTradeDateOrContractMonth='20190708',
    #         strike=2955,
    #         right='C',
    #         multiplier='100'
    # )

    spx_contract = Contract()
    spx_contract.symbol = 'SPX'
    spx_contract.secType = 'OPT'
    spx_contract.exchange = 'SMART'
    spx_contract.primaryExchange='SMART'
    spx_contract.currency = 'USD'
    spx_contract.lastTradeDateOrContractMonth = '20190708'
    # spx_contract.strike = 2955
    spx_contract.right = 'C'
    spx_contract.multiplier = '100'

    incomplete_contract = Contract()
    incomplete_contract.symbol = 'AMZN'
    incomplete_contract.secType = "OPT"
    incomplete_contract.exchange = "SMART"
    incomplete_contract.currency = "USD"
    incomplete_contract.strike = 1900
    incomplete_contract.lastTradeDateOrContractMonth = "20190719"
    incomplete_contract.right = "C"

    # app.reqContractDetails(1, index_contract())
    #
    # app.reqMktData(
    #     reqId=3,
    #     contract=forex_contract(),
    #     genericTickList='221',
    #     snapshot=False,
    #     regulatorySnapshot=False,
    #     mktDataOptions=[]
    # )

    app.run()
    # app.disconnect()