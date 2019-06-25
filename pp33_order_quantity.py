import math


class PP33OrderQuantity(object):
    BET_FACTOR = 0.02

    def __init__(self,
                 net_liquidation:float,
                 go_long:bool,
                 pp33_bound_line_price:float,
                 pp33_mid_line_price:float,
                 implied_volatility:float):

        self.net_liquidation = net_liquidation
        self.go_long = go_long
        self.pp33_bound_line_price = pp33_bound_line_price
        self.pp33_mid_line_price = pp33_mid_line_price
        self.implied_volatility = implied_volatility

    def get_quantity(self):
        max_loss = self.net_liquidation * PP33OrderQuantity.BET_FACTOR
        if self.go_long:
            expect_loss_per_quantity = (self.pp33_bound_line_price - self.pp33_mid_line_price) * self.implied_volatility * 100
        else:
            expect_loss_per_quantity = (self.pp33_mid_line_price - self.pp33_bound_line_price) * self.implied_volatility * 100
        quantity = max_loss / expect_loss_per_quantity
        return math.floor(quantity)
