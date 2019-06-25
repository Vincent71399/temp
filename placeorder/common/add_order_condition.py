from ibapi import order_condition
from ibapi.order import Order
from ibapi.tag_value import TagValue


def fill_adaptive_params(baseOrder: Order, priority: str):
    baseOrder.algoStrategy = "Adaptive"
    baseOrder.algoParams = []
    baseOrder.algoParams.append(TagValue("adaptivePriority", priority))


def price_condition(trigger_method: int, con_id: int, exchange: str, price: float, is_more: bool, is_conjunction: bool = True):
    priceCondition = order_condition.Create(order_condition.OrderCondition.Price)
    priceCondition.conId = con_id
    priceCondition.exchange = exchange
    priceCondition.isMore = is_more
    priceCondition.triggerMethod = trigger_method
    priceCondition.price = price
    priceCondition.isConjunctionConnection = is_conjunction
    return priceCondition


def time_condition(is_more: bool, time: str, is_conjunction: bool = True):
    time_condition = order_condition.Create(order_condition.OrderCondition.Time)
    time_condition.isMore = is_more
    time_condition.time = time
    time_condition.isConjunctionConnection = is_conjunction
    return time_condition


def one_cancels_all(oca_orders, oca_group):
    for o in oca_orders:
        o.ocaGroup = oca_group
        o.ocaType = 2
    return oca_orders


