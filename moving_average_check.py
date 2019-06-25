class MovingAverageCheck(object):
    SHORT_MA_LENGTH = 2
    LONG_MA_LENGTH = 4
    PERCENTAGE_DELTA = 0.001
    INIT_CHECK_RANGE = 5
    UP_TREND = 1
    DOWN_TREND = -1
    TWO_WAY_TREND = 0

    def __init__(self, symbol: str, min_low: float, max_high: float, pre_bars: list):
        self.symbol = symbol
        self.min_low = min_low
        self.max_high = max_high
        self.mid_point = (max_high + min_low) / 2.
        self.stored_bars = pre_bars
        self.ma_short = []
        self.ma_long = []

        # trend cross related
        self.latest_trend = 0

        self.__init_ma()

    ###
    #public methods
    ###
    def feed(self, bar):
        last_bar = self.stored_bars[len(self.stored_bars) - 1]
        if last_bar.date == bar.date:
            self.stored_bars[len(self.stored_bars) - 1] = bar
            self.update_last_ma()
            self.__update_trend()
            print("Update last bar")
        else:
            self.stored_bars.append(bar)
            self.append_last_ma()
            self.__update_trend()
            print("Append last bar")

    ###
    #private methods
    ###
    def __init_ma(self):
        list_length = len(self.stored_bars)
        if list_length >= MovingAverageCheck.LONG_MA_LENGTH:
            print("Enough")
            for i in range(0, list_length - MovingAverageCheck.LONG_MA_LENGTH + 1):
                sub_list_long = self.stored_bars[i:MovingAverageCheck.LONG_MA_LENGTH + i]
                sub_list_short = sub_list_long[MovingAverageCheck.SHORT_MA_LENGTH: MovingAverageCheck.LONG_MA_LENGTH]
                sub_list_last_bar = sub_list_long[len(sub_list_long) - 1]
                average_long = self.__calculate_avg(sub_list_long)
                average_short = self.__calculate_avg(sub_list_short)
                self.ma_long.append([sub_list_last_bar.date, average_long])
                self.ma_short.append([sub_list_last_bar.date, average_short])
            self.__update_trend()
        else:
            print("Not Enough")

    def append_last_ma(self):
        stored_bar_length = len(self.stored_bars)
        sub_list_long = self.stored_bars[stored_bar_length - MovingAverageCheck.LONG_MA_LENGTH: stored_bar_length]
        sub_list_short = sub_list_long[MovingAverageCheck.SHORT_MA_LENGTH: MovingAverageCheck.LONG_MA_LENGTH]
        sub_list_last_bar = sub_list_long[len(sub_list_long) - 1]
        average_long = self.__calculate_avg(sub_list_long)
        average_short = self.__calculate_avg(sub_list_short)
        self.ma_long.append([sub_list_last_bar.date, average_long])
        self.ma_short.append([sub_list_last_bar.date, average_short])

    def update_last_ma(self):
        stored_bar_length = len(self.stored_bars)
        sub_list_long = self.stored_bars[stored_bar_length - MovingAverageCheck.LONG_MA_LENGTH: stored_bar_length]
        sub_list_short = sub_list_long[MovingAverageCheck.SHORT_MA_LENGTH: MovingAverageCheck.LONG_MA_LENGTH]
        sub_list_last_bar = sub_list_long[len(sub_list_long) - 1]
        average_long = self.__calculate_avg(sub_list_long)
        average_short = self.__calculate_avg(sub_list_short)
        self.ma_long[len(self.ma_long) - 1] = [sub_list_last_bar.date, average_long]
        self.ma_short[len(self.ma_short) - 1] = [sub_list_last_bar.date, average_short]

    def __calculate_avg(self, bar_list):
        sum = 0
        length = len(bar_list)
        for bar in bar_list:
            sum += bar.close
        return sum / length

    def __update_trend(self):
        last_index_ma = len(self.ma_long) - 1
        last_index_bar = len(self.stored_bars) - 1
        trend_judge = 0
        for i in range(0, MovingAverageCheck.INIT_CHECK_RANGE):
            index_ma = last_index_ma - i
            index_bar = last_index_bar - i
            if index_ma >=0 and index_bar >=0:
                if self.ma_long[index_ma][1] < self.ma_short[index_ma][1] < self.stored_bars[index_bar].close:
                    trend_judge +=1
                elif self.ma_long[index_ma][1] > self.ma_short[index_ma][1] > self.stored_bars[index_bar].close:
                    trend_judge -=1

            if index_ma > 0:
                if self.ma_short[index_ma][1] >= self.ma_short[index_ma - 1][1] * (1 + MovingAverageCheck.PERCENTAGE_DELTA):
                    trend_judge +=1
                elif self.ma_short[index_ma][1] <= self.ma_short[index_ma - 1][1] * (1 - MovingAverageCheck.PERCENTAGE_DELTA):
                    trend_judge -=1

            if index_bar >=0:
                if self.stored_bars[index_bar].close >= self.stored_bars[index_bar-1].close * (1 + MovingAverageCheck.PERCENTAGE_DELTA):
                    trend_judge +=1
                elif self.stored_bars[index_bar].close <= self.stored_bars[index_bar-1].close * (1 - MovingAverageCheck.PERCENTAGE_DELTA):
                    trend_judge -=1

        print("Trend Judge : " + str(trend_judge))
        if trend_judge >= 10:
            self.latest_trend = MovingAverageCheck.UP_TREND
        elif trend_judge <= -10:
            self.latest_trend = MovingAverageCheck.DOWN_TREND
        else:
            self.latest_trend = MovingAverageCheck.TWO_WAY_TREND
