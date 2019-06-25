from datetime import timedelta

class AppConfig:
    #########################
    # backtest #
    #########################
    IS_BACKTESTING = False
    ENABLE_CLOSE_NEXT_OTM = True
    ENABLE_ACCURATE_TIME_CALCULATION = False
    ENABLE_ACCURATE_TIME_CALCULATION_24 = True
    PASS_PERIOD_CHECKER = 8
    TRAIL_STOP_LOSS_PERCENTAGE = 10

    PASS_TIMER_CHECKER = timedelta(minutes=2)

    #########################
    # bar crossover #
    #########################
    CHECK_TREND_OVERSHOT_USD = 2

    #########################
    # pp33 #
    #########################
    TREND_INDEX = "SPX"
    TREND_CHECK = True
    PP33_LIMITS = {
        'AMZN': {
            'take_profit': 15,
            'stop_loss': 20
        },
        'BA': {
            'take_profit': 15,
            'stop_loss': 20
        },
        'GOOGL': {
            'take_profit': 15,
            'stop_loss': 20
        },
        'NFLX': {
            'take_profit': 20,
            'stop_loss': 20
        },
        'SPX': {
            'take_profit': 10,
            'stop_loss': 15
        }
    }


class App:
    def __init__(self, config):
        self.config = config


app_config = AppConfig()
app = App(app_config)

############################
# ib api constant
############################
SECURITY_TYPE_INDEX = 'IND'
SECURITY_TYPE_STOCK = 'STK'
SECURITY_TYPE_FUTURE = 'FUT'
SECURITY_TYPE_OPTION = 'OPT'
SECURITY_TYPE_FUTURE_OPTION = 'FOP'

ORDER_ACTION_BUY = 'buy'
ORDER_ACTION_SELL = 'sell'
OPTION_RIGHT_CALL = 'C'
OPTION_RIGHT_PUT = 'P'

ORDER_TYPE_LMT = 'LMT'
ORDER_TYPE_STP = 'STP'
ORDER_TYPE_TRAILSTOP = 'TRAIL'
ORDER_TYPE_MKT = 'MKT'

ADAPTIVE_URGENT = "Urgent"
ADAPTIVE_NORMAL = "Normal"
ADAPTIVE_PATIENT = "Patient"

BAR_SIZE_1_S = '1 sec'
BAR_SIZE_5_S = '5 secs'
BAR_SIZE_15_S = '15 secs'
BAR_SIZE_30_S = '30 secs'
BAR_SIZE_1_M = '1 min'
BAR_SIZE_2_M = '2 mins'
BAR_SIZE_3_M = '3 mins'
BAR_SIZE_5_M = '5 mins'
BAR_SIZE_15_M = '15 mins'
BAR_SIZE_30_M = '30 mins'
BAR_SIZE_1_H = '1 hour'
BAR_SIZE_1_D = '1 day'

WHAT_TO_SHOW_TRADES = 'TRADES'

DURATION_STRING_S = ' S'
DURATION_STRING_D = ' D'

################################
# other constants #
################################
DECISION_LONG = 'long'
DECISION_SHORT = 'short'

WAIT_FILLING_SECONDS = 60
WAIT_ADJUST_SECONDS = 60
ADJUST_TIME = 5

DIRECT_ENTER_PRICE_DIFFERENCE = 0.05

#########################
# flags #
#########################
ENABLE_MKT_ORDER = False
DB_CONNECTED = True
ENABLE_MKT_TREND_CHECK_BACKTEST = True
