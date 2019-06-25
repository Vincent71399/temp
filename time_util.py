from datetime import datetime, timedelta

import pandas_market_calendars as mcal
import pandas as pd
import pytz

nyse = mcal.get_calendar('NYSE')


def get_prev_day_market_close_time(current_time):
    current_time_utc = current_time.astimezone(tz=pytz.utc)

    start_date = (current_time_utc - timedelta(days=10)).strftime('%Y-%m-%d')
    end_date = current_time_utc.strftime('%Y-%m-%d')
    schedule = nyse.schedule(start_date=start_date, end_date=end_date)

    prev_day_close = None
    for close_time in schedule['market_close']:
        if close_time < current_time_utc.replace(tzinfo=pytz.utc):
            prev_day_close = close_time
        else:
            break

    return datetime.fromtimestamp(prev_day_close.value/1000000000)


def get_today_market_close_time(current_time):
    current_time_utc = current_time.astimezone(tz=pytz.utc)

    start_date = current_time_utc.strftime('%Y-%m-%d')
    end_date = (current_time_utc + timedelta(days=10)).strftime('%Y-%m-%d')
    schedule = nyse.schedule(start_date=start_date, end_date=end_date)

    today_close = None
    for close_time in schedule['market_close']:
        if close_time > current_time_utc.replace(tzinfo=pytz.utc):
            today_close = close_time
            break

    return datetime.fromtimestamp(today_close.value/1000000000)


def get_today_market_open_time(current_time):
    current_time_utc = current_time.astimezone(tz=pytz.utc)

    start_date = current_time_utc.strftime('%Y-%m-%d')
    end_date = (current_time_utc + timedelta(days=10)).strftime('%Y-%m-%d')
    schedule = nyse.schedule(start_date=start_date, end_date=end_date)

    today_open = None
    for row in schedule.itertuples():
        if row.market_close > current_time_utc.replace(tzinfo=pytz.utc):
            today_open = row.market_open
            break

    return datetime.fromtimestamp(today_open.value/1000000000)


def is_market_open(current_time):
    current_time_utc = current_time.astimezone(tz=pytz.utc)
    start_date = (current_time_utc - timedelta(days=10)).strftime('%Y-%m-%d')
    end_date = (current_time_utc + timedelta(days=10)).strftime('%Y-%m-%d')
    schedule = nyse.schedule(start_date=start_date, end_date=end_date)
    result = nyse.open_at_time(schedule, pd.Timestamp(current_time_utc.timestamp(), unit='s', tz=pytz.utc))
    return result



