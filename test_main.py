from moving_average_check import MovingAverageCheck
from ibapi.common import BarData

bar1 = BarData()
bar1.time = "2018-02-01 21:36:00"
bar1.close = 999

bar2 = BarData()
bar2.time = "2018-02-01 21:39:00"
bar2.close = 1000

bar3 = BarData()
bar3.time = "2018-02-01 21:42:00"
bar3.close = 1002

bar4 = BarData()
bar4.time = "2018-02-01 21:45:00"
bar4.close = 1005

bar_list = [bar1, bar2, bar3, bar4]

m = MovingAverageCheck(symbol="TEST_STOCK", min_low=2700, max_high=2730, pre_bars=bar_list)
