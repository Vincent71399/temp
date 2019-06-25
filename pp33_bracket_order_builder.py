from ibapi.order import Order

from config import *


class PP33BracketOrderBuilder:
    TRAIL_STOP_PERCENTAGE = 20
    TAKE_PROFIT_PERCENTAGE = 15

    def __init__(self, parent_order_id:int, parent_order:Order):
        self.parent_order = parent_order
        self.parent_order.orderId = parent_order_id

        if parent_order.action == ORDER_ACTION_BUY:
            self.close_order_action = ORDER_ACTION_SELL
        else:
            self.close_order_action = ORDER_ACTION_BUY

        self.parent_order.transmit = False
        self.take_profit_order = self._take_profit_order_builder()
        self.stop_loss_order = self._stop_loss_order_builder()

    ####################
    # public functions #
    ####################
    def bracket_order_list(self):
        return [self.parent_order, self.take_profit_order, self.stop_loss_order]

    #####################
    # private functions #
    #####################
    def _take_profit_order_builder(self):
        take_profit = Order()
        take_profit.orderId = self.parent_order.orderId + 1
        take_profit.action = self.close_order_action
        take_profit.orderType = ORDER_TYPE_LMT
        take_profit.totalQuantity = self.parent_order.totalQuantity
        take_profit.lmtPrice = self.parent_order.lmtPrice * (100 + PP33BracketOrderBuilder.TAKE_PROFIT_PERCENTAGE) / 100
        take_profit.parentId = self.parent_order.orderId
        take_profit.transmit = False
        return take_profit

    def _stop_loss_order_builder(self):
        stop_loss = Order()
        stop_loss.orderId = self.parent_order.orderId + 2
        stop_loss.parentId = self.parent_order.orderId
        stop_loss.action = self.close_order_action
        stop_loss.orderType = ORDER_TYPE_TRAILSTOP
        stop_loss.totalQuantity = self.parent_order.totalQuantity
        stop_loss.trailingPercent = PP33BracketOrderBuilder.TRAIL_STOP_PERCENTAGE
        stop_loss.transmit = True
        return stop_loss