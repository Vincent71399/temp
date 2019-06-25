from moving_average_check import MovingAverageCheck
from ibapi.common import BarData

bar1 = BarData()
bar1.date = "2018-02-01 21:36:00"
bar1.close = 999

bar2 = BarData()
bar2.date = "2018-02-01 21:39:00"
bar2.close = 1000

bar3 = BarData()
bar3.date = "2018-02-01 21:42:00"
bar3.close = 1002

bar4 = BarData()
bar4.date = "2018-02-01 21:45:00"
bar4.close = 1003

bar5 = BarData()
bar5.date = "2018-02-01 21:48:00"
bar5.close = 1006

bar6 = BarData()
bar6.date = "2018-02-01 21:51:00"
bar6.close = 1008

bar_list = [bar1, bar2, bar3, bar4, bar5, bar6]

m = MovingAverageCheck(symbol="TEST_STOCK", min_low=2700, max_high=2730, pre_bars=bar_list)

# print("Long MA")
# for item in m.ma_long:
#     print(item[0] + " : " + str(item[1]))
#
# print("Short MA")
# for item in m.ma_short:
#     print(item[0] + " : " + str(item[1]))

bar_test = BarData()
bar_test.date = "2018-02-01 21:54:00"
bar_test.close = 1022

m.feed(bar_test)
print("Long MA")
for item in m.ma_long:
    print(item[0] + " : " + str(item[1]))

print("Short MA")
for item in m.ma_short:
    print(item[0] + " : " + str(item[1]))

bar_test.close = 1060
m.feed(bar_test)
print("Long MA")
for item in m.ma_long:
    print(item[0] + " : " + str(item[1]))

print("Short MA")
for item in m.ma_short:
    print(item[0] + " : " + str(item[1]))

print("Trend : " + str(m.latest_trend))

bar_feed_1 = BarData()
bar_feed_1.date = "2018-02-01 21:57:00"
bar_feed_1.close = 1014
m.feed(bar_feed_1)

print("Trend : " + str(m.latest_trend))

bar_feed_2 = BarData()
bar_feed_2.date = "2018-02-01 22:00:00"
bar_feed_2.close = 1010
m.feed(bar_feed_2)

print("Trend : " + str(m.latest_trend))

bar_feed_3 = BarData()
bar_feed_3.date = "2018-02-01 22:03:00"
bar_feed_3.close = 1005
m.feed(bar_feed_3)

print("Trend : " + str(m.latest_trend))

bar_feed_4 = BarData()
bar_feed_4.date = "2018-02-01 22:03:00"
bar_feed_4.close = 1005
m.feed(bar_feed_4)

print("Trend : " + str(m.latest_trend))

bar_feed_5 = BarData()
bar_feed_5.date = "2018-02-01 22:06:00"
bar_feed_5.close = 999
m.feed(bar_feed_5)

bar_feed_6 = BarData()
bar_feed_6.date = "2018-02-01 22:09:00"
bar_feed_6.close = 990
m.feed(bar_feed_6)

print("Trend : " + str(m.latest_trend))