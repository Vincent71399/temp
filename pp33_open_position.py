from ibapi.contract import Contract
from ibapi.order import Order


class PP33OpenPosition:
    def __init__(self, contract:Contract, order:Order):
        self.contract = contract
        self.order = order



