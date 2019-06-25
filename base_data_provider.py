import asyncio

from ibapi.contract import Contract, ContractDetails
from ibapi.client import EClient
from ibapi.order_state import OrderState
from ibapi.wrapper import EWrapper, OrderId, iswrapper, TickerId, TickType, TickAttrib, BarData
from ibapi.order import Order

from threading import Thread


class BaseDataProvider(EWrapper, EClient):
    def __init__(self, ipaddress, portid, clientid):
        super().__init__()
        EClient.__init__(self, wrapper=self)
        self.order_id = None
        self.req_id = 0
        self.account = ''

        self.account_summary_handlers = {}
        self.account_summary_end_handlers = {}
        self.contract_details_handlers = {}
        self.contract_details_end_handlers = {}
        self.current_time_handler = None
        self.historical_data_handlers = {}
        self.historical_data_end_handlers = {}
        self.historical_data_update_handlers = {}
        self.position_handler = None
        self.position_end_handler = None
        self.open_order_handler = None
        self.open_order_end_handler = None
        self.order_status_handlers = {}
        self.tick_option_computation_handlers = {}
        self.tick_price_handlers = {}
        self.tick_size_handlers = {}
        self.pnl_handlers = {}

        self.connection_ready = False
        self.connect(ipaddress, portid, clientid)
        self.accountSummarySubscribed = False

        thread = Thread(target=self.run)
        thread.start()
        setattr(self, "_thread", thread)

    async def wait_for_connection(self):
        from timeit import default_timer as timer
        start = timer()
        while not self.connection_ready:
            end = timer()
            if end - start > 2:
                print('wait for next valid ID timed out.')
                self.reqIds(1)
                start = end
            await asyncio.sleep(0.01)

    def next_req_id(self):
        self.req_id += 1
        return self.req_id

    def next_order_id(self):
        if self.order_id:
            self.order_id += 1
        return self.order_id

    ##########################
    # eclient functions with callback
    ##########################
    def req_account_summary_with_callback(self, attribute, callback_account_summary=None, callback_account_summary_end=None):
        if self.accountSummarySubscribed:
            return
        req_id = self.next_req_id()
        if callback_account_summary:
            self.account_summary_handlers[req_id] = callback_account_summary
        if callback_account_summary_end:
            self.account_summary_end_handlers[req_id] = callback_account_summary_end
        self.reqAccountSummary(req_id, 'All', attribute)
        self.accountSummarySubscribed = True
        return req_id

    def req_contract_details_with_callback(self, contract, callback_contract_details=None, callback_contract_details_end=None):
        req_id = self.next_req_id()
        if callback_contract_details:
            self.contract_details_handlers[req_id] = callback_contract_details
        if callback_contract_details_end:
            self.contract_details_end_handlers[req_id] = callback_contract_details_end
        self.reqContractDetails(req_id, contract)
        return req_id

    def req_current_time_with_callback(self, callback_current_time=None):
        if callback_current_time:
            self.current_time_handler = callback_current_time
        self.reqCurrentTime()

    def req_historical_data_with_callback(self, contract, end_date_time, duration_str
                                          , bar_size_setting, use_rth=1, keep_up_to_date=False,
                                          callback_historical_data=None, callback_historical_data_end=None
                                          , callback_historical_data_update=None):
        req_id = self.next_req_id()
        if callback_historical_data:
            self.historical_data_handlers[req_id] = callback_historical_data
        if callback_historical_data_end:
            self.historical_data_end_handlers[req_id] = callback_historical_data_end
        if callback_historical_data_update:
            self.historical_data_update_handlers[req_id] = callback_historical_data_update
        self.reqHistoricalData(req_id, contract, endDateTime=end_date_time, durationStr=duration_str,
                               barSizeSetting=bar_size_setting,
                               whatToShow="TRADES", useRTH=use_rth, formatDate=1, keepUpToDate=keep_up_to_date,
                               chartOptions=[])
        return req_id

    def req_mkt_data_with_callback(self, contract,
                    generic_tick_list, snapshot = False, regulatory_snapshot = False,
                    mkt_data_options = [], callback_tick_option_computation=None,
                    callback_tick_price=None, callback_tick_size=None):
        req_id = self.next_req_id()
        if callback_tick_option_computation:
            self.tick_option_computation_handlers[req_id] = callback_tick_option_computation
        if callback_tick_price:
            self.tick_price_handlers[req_id] = callback_tick_price
        if callback_tick_size:
            self.tick_size_handlers[req_id] = callback_tick_size
        self.reqMktData(reqId=req_id, contract=contract, genericTickList=generic_tick_list, snapshot=snapshot,
                        regulatorySnapshot=regulatory_snapshot, mktDataOptions=mkt_data_options)
        return req_id

    def place_order_with_callback(self, contract: Contract, order: Order,
                                  callback_order_status=None, callback_open_order=None, callback_open_order_end=None):
        order_id = self.next_order_id()
        if callback_order_status:
            self.order_status_handlers[order_id] = callback_order_status
        self.placeOrder(order_id, contract, order)
        print(
            "Order#{6} placed. {0} {1} {2} {3} Qty:{4} LmtPrice:{5}".format(order.action, contract.symbol,
                                                                                        str(contract.strike),
                                                                                        contract.right, str(order.totalQuantity),
                                                                                        str(order.lmtPrice),
                                                                                        str(order_id)))
        return order_id

    def cancel_order_with_callback(self, order_id:int, callback_order_status=None):
        if callback_order_status:
            self.order_status_handlers[order_id] = callback_order_status
        self.cancelOrder(order_id)
        print("Cancel Order : " + str(order_id))
        return True

    def req_pnl_with_callback(self, callback_pnl=None):
        req_id = self.next_req_id()
        self.reqPnL(req_id, self.account, '')
        if callback_pnl:
            self.pnl_handlers[req_id] = callback_pnl
        return req_id

    def req_position_with_callback(self, callback_position=None, callback_position_end=None):
        if callback_position:
            self.position_handler = callback_position
        if callback_position_end:
            self.position_end_handler = callback_position_end
        self.reqPositions()
        return True

    def req_open_orders_with_callback(self, callback_open_order=None, callback_open_order_end=None):
        if callback_open_order:
            self.open_order_handler = callback_open_order
        if callback_open_order_end:
            self.open_order_end_handler = callback_open_order_end
        self.reqAllOpenOrders()
        return True

    #############################
    # override ewrapper functions
    #############################
    @iswrapper
    def accountSummary(self, reqId: int, account: str, tag: str, value: str,
                       currency: str):
        super().accountSummary(reqId, account, tag, value, currency)
        handler = self.account_summary_handlers.get(reqId)
        if handler:
            handler(reqId, account, tag, value, currency)

    @iswrapper
    def accountSummaryEnd(self, reqId: int):
        super().accountSummaryEnd(reqId)
        handler = self.account_summary_end_handlers.get(reqId)
        if handler:
            handler(reqId)

    @iswrapper
    def contractDetails(self, reqId:int, contractDetails:ContractDetails):
        super().contractDetails(reqId, contractDetails)
        handler = self.contract_details_handlers.get(reqId)
        if handler:
            handler(reqId, contractDetails)

    @iswrapper
    def contractDetailsEnd(self, reqId:int):
        super().contractDetailsEnd(reqId)
        handler = self.contract_details_end_handlers.get(reqId)
        if handler:
            handler(reqId)

    @iswrapper
    def currentTime(self, time_from_server):
        super().currentTime(time_from_server)
        handler = self.current_time_handler
        if handler:
            handler(time_from_server)

    @iswrapper
    def historicalData(self, reqId: int, bar: BarData):
        handler = self.historical_data_handlers.get(reqId)
        if handler:
            handler(reqId, bar)

    @iswrapper
    def historicalDataEnd(self, reqId: int, start: str, end: str):
        handler = self.historical_data_end_handlers.get(reqId)
        if handler:
            handler(reqId, start, end)

    @iswrapper
    def historicalDataUpdate(self, reqId: int, bar: BarData):
        handler = self.historical_data_update_handlers.get(reqId)
        if handler:
            handler(reqId, bar)

    @iswrapper
    def nextValidId(self, order_id: int):
        super().nextValidId(order_id)
        self.order_id = order_id - 1
        self.connection_ready = True
        print("next valid id is " + str(order_id))

    @iswrapper
    def openOrder(self, orderId:OrderId, contract:Contract, order:Order,
                  orderState:OrderState):
        super().openOrder(orderId, contract, order, orderState)
        handler = self.open_order_handler
        if handler:
            handler(orderId, contract, order, orderState)

    @iswrapper
    def openOrderEnd(self):
        super().openOrderEnd()
        handler = self.open_order_end_handler
        if handler:
            handler()

    @iswrapper
    def orderStatus(self, orderId: OrderId, status: str, filled: float,
                    remaining: float, avgFillPrice: float, permId: int,
                    parentId: int, lastFillPrice: float, clientId: int,
                    whyHeld: str, mktCapPrice: float):
        super().orderStatus(orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)
        handler = self.order_status_handlers.get(orderId)
        if handler:
            handler(orderId, status, remaining, avgFillPrice)

    @iswrapper
    def position(self, account: str, contract: Contract, position: float,
                 avgCost: float):
        super().position(account, contract, position, avgCost)
        handler = self.position_handler
        if handler:
            handler(account, contract, position, avgCost)

    @iswrapper
    def positionEnd(self):
        super().positionEnd()
        handler = self.position_end_handler
        if handler:
            handler()

    @iswrapper
    def tickOptionComputation(self, reqId: TickerId, tickType: TickType,
                              impliedVol: float, delta: float, optPrice: float, pvDividend: float,
                              gamma: float, vega: float, theta: float, undPrice: float):
        super().tickOptionComputation(reqId, tickType, impliedVol, delta, optPrice, pvDividend, gamma, vega, theta, undPrice)
        handler = self.tick_option_computation_handlers.get(reqId)
        if handler:
            handler(reqId, tickType, impliedVol, delta,
                    optPrice, pvDividend, gamma, vega, theta, undPrice)

    @iswrapper
    def tickPrice(self, reqId: TickerId, tickType: TickType, price: float,
                  attrib: TickAttrib):
        handler = self.tick_price_handlers.get(reqId)
        if handler:
            handler(price)

    @iswrapper
    def tickSize(self, reqId: TickerId, tickType: TickType, size: int):
        """Market data tick size callback. Handles all size-related ticks."""
        super().tickSize(reqId, tickType, size)
        handler = self.tick_size_handlers.get(reqId)
        if handler:
            handler(reqId, tickType, size)

    @iswrapper
    def updatePortfolio(self, contract: Contract, position: float,
                        marketPrice: float, marketValue: float,
                        averageCost: float, unrealizedPNL: float,
                        realizedPNL: float, accountName: str):
        super().updatePortfolio(contract, position, marketPrice, marketValue,
                                averageCost, unrealizedPNL, realizedPNL, accountName)
        print("UpdatePortfolio.", "Symbol:", contract.symbol, "SecType:", contract.secType, "Exchange:",
              contract.exchange, "Position:", position, "MarketPrice:", marketPrice,
              "MarketValue:", marketValue, "AverageCost:", averageCost,
              "UnrealizedPNL:", unrealizedPNL, "RealizedPNL:", realizedPNL,
              "AccountName:", accountName)

    @iswrapper
    def managedAccounts(self, accountsList:str):
        """Receives a comma-separated string with the managed account ids."""
        self.account = accountsList.split(',')[0]

    @iswrapper
    def pnl(self, reqId: int, dailyPnL: float, unrealizedPnL: float, realizedPnL: float):
        handler = self.pnl_handlers.get(reqId)
        if handler:
            handler(reqId, dailyPnL, unrealizedPnL, realizedPnL)
