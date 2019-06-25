class PP33ExitStrategy(object):

    DEATH_CROSS = -1
    GOLD_CROSS = 1
    NOTHING_HAPPEN = 0

    TAKE_PROFIT_FACTOR = 0.05

    def __init__(self,
                 enter_price:float,
                 go_long:bool,
                 pp33_bound_line_price:float,
                 pp33_mid_line_price:float,
                 john_person1_price:float,
                 john_person2_price:float,
                 john_person3_price:float):
        self.enter_price = enter_price
        self.go_long = go_long
        self.pp33_bound_line_price = pp33_bound_line_price
        self.pp33_mid_line_price = pp33_mid_line_price
        self.john_person1_price = john_person1_price
        self.john_person2_price = john_person2_price
        self.john_person3_price = john_person3_price

    def feed_underlying_price(self, underlying_price:float, moving_average_signal:int):
        if self.hit_john_person_line(underlying_price) or self.hit_stop_loss_line(underlying_price) or self.cross_signal(moving_average_signal):
            return True
        return False

    def feed_option_price(self, option_price:float, minutes_to_market_close:int):
        if self.take_profit(option_price, minutes_to_market_close):
            return True
        return False

    def take_profit(self, option_price:float, minutes_to_market_close:int):
        take_profit_factor = PP33ExitStrategy.TAKE_PROFIT_FACTOR
        if minutes_to_market_close < 120:
            take_profit_factor = take_profit_factor * minutes_to_market_close / 120
            print("Take_profit_factor : " + str(take_profit_factor))
        if option_price >= (self.enter_price * (1 + take_profit_factor)):
            return True
        else:
            return False

    def hit_john_person_line(self, underlying_price):
        if self.go_long:
            if self.john_person1_price > self.pp33_bound_line_price:
                if self.john_person1_price - self.pp33_bound_line_price > self.pp33_bound_line_price - self.pp33_mid_line_price:
                    if underlying_price >= self.john_person1_price:
                        return True
                else:
                    if underlying_price >= self.john_person2_price:
                        return True
            elif self.john_person1_price <= self.pp33_bound_line_price < self.john_person2_price:
                if self.john_person2_price - self.pp33_bound_line_price > self.pp33_bound_line_price - self.pp33_mid_line_price:
                    if underlying_price >= self.john_person2_price:
                        return True
                else:
                    if underlying_price >= self.john_person3_price:
                        return True
            elif self.john_person2_price <= self.pp33_bound_line_price < self.john_person3_price:
                if self.john_person3_price - self.pp33_bound_line_price > self.pp33_bound_line_price - self.pp33_mid_line_price:
                    if underlying_price >= self.john_person3_price:
                        return True
        else:
            if self.john_person1_price < self.pp33_bound_line_price:
                if self.pp33_bound_line_price - self.john_person1_price > self.pp33_mid_line_price - self.pp33_bound_line_price:
                    if underlying_price <= self.john_person1_price:
                        return True
                else:
                    if underlying_price <= self.john_person2_price:
                        return True
            elif self.john_person1_price >= self.pp33_bound_line_price > self.john_person2_price:
                if self.pp33_bound_line_price - self.john_person2_price > self.pp33_mid_line_price - self.pp33_bound_line_price:
                    if underlying_price <= self.john_person2_price:
                        return True
                else:
                    if underlying_price <= self.john_person3_price:
                        return True
            elif self.john_person2_price >= self.pp33_bound_line_price > self.john_person3_price:
                if self.pp33_bound_line_price - self.john_person3_price > self.pp33_mid_line_price - self.pp33_bound_line_price:
                    if underlying_price <= self.john_person3_price:
                        return True
        return False

    def hit_stop_loss_line(self, underlying_price):
        if self.go_long and underlying_price <= self.pp33_mid_line_price:
            return True
        elif self.go_long == False and underlying_price >= self.pp33_mid_line_price:
            return True
        return False

    def cross_signal(self, moving_average_signal):
        if moving_average_signal == PP33ExitStrategy.DEATH_CROSS and self.go_long:
            return True
        elif moving_average_signal == PP33ExitStrategy.GOLD_CROSS and self.go_long == False:
            return True
        return False



