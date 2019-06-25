from ibapi.order import Order

from placeorder.config import app, ORDER_ACTION_BUY, ORDER_ACTION_SELL, ORDER_TYPE_TRAILSTOP, ORDER_TYPE_MKT, \
    ORDER_TYPE_LMT
from placeorder.common.add_order_condition import time_condition
from placeorder.common.time_util import get_today_market_close_time
from placeorder.normalize_price import normalize

from datetime import datetime, timedelta


class PP33BracketOrderBuilder:
    def __init__(self, parent_order:Order, symbol, take_profit_order: Order = None, stop_loss_order: Order = None, quit_before_close_order: Order = None):
        self.parent_order = parent_order
        self.symbol = symbol

        if parent_order.action == ORDER_ACTION_BUY:
            self.close_order_action = ORDER_ACTION_SELL
        else:
            self.close_order_action = ORDER_ACTION_BUY

        self.parent_order.transmit = False
        self.parent_order.sweepToFill = True
        self.take_profit_order = self._take_profit_order_builder(take_profit_order)
        self.stop_loss_order = self._stop_loss_order_builder(stop_loss_order)
        self.quit_before_close_order = self._quit_before_market_close_order_builder(quit_before_close_order)

    ####################
    # public functions #
    ####################
    def bracket_order_list(self):
        return [self.take_profit_order, self.stop_loss_order, self.quit_before_close_order]

    #####################
    # private functions #
    #####################
    def _take_profit_order_builder(self, order: Order):
        if order is None:
            take_profit = Order()
        else:
            take_profit = order
        take_profit.action = self.close_order_action
        take_profit.orderType = ORDER_TYPE_LMT
        take_profit.totalQuantity = self.parent_order.totalQuantity
        take_profit.lmtPrice = self.parent_order.lmtPrice * (100 + app.config.PP33_LIMITS[self.symbol]['take_profit']) / 100
        take_profit.lmtPrice = normalize(self.symbol, take_profit.lmtPrice)
        take_profit.parentId = self.parent_order.orderId
        take_profit.transmit = False
        return take_profit

    def _stop_loss_order_builder(self, order: Order):
        if order is None:
            stop_loss = Order()
        else:
            stop_loss = order
        stop_loss.action = self.close_order_action
        stop_loss.orderType = ORDER_TYPE_TRAILSTOP
        stop_loss.totalQuantity = self.parent_order.totalQuantity
        stop_loss.trailingPercent = app.config.PP33_LIMITS[self.symbol]['stop_loss']
        stop_loss.parentId = self.parent_order.orderId
        stop_loss.transmit = False
        return stop_loss

    def _quit_before_market_close_order_builder(self, order: Order):
        if order is None:
            quit_before_close = Order()
        else:
            quit_before_close = order
        quit_before_close.action = self.close_order_action
        quit_before_close.orderType = ORDER_TYPE_MKT
        quit_before_close.totalQuantity = self.parent_order.totalQuantity
        quit_before_close.parentId = self.parent_order.orderId

        today_mkt_close_time = get_today_market_close_time(datetime.today())
        cancel_time = today_mkt_close_time - timedelta(minutes=30)
        cancel_time_str = cancel_time.strftime("%Y%m%d %H:%M:%S")
        quit_before_close.conditions.append(time_condition(is_more=True, time=cancel_time_str))
        quit_before_close.transmit = True
        return quit_before_close
