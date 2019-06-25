from datetime import datetime, timedelta

import pandas_market_calendars as mcal
import pandas as pd
import pytz

nyse = mcal.get_calendar('NYSE')
start = (datetime.now() - timedelta(days=30)).astimezone(tz=pytz.utc)
end = (datetime.now() + timedelta(days=30)).astimezone(tz=pytz.utc)
cached_schedule = nyse.schedule(start_date=start.strftime('%Y-%m-%d'), end_date=end.strftime('%Y-%m-%d'))


def widen_cached_schedule(new_start, new_end):
    global start, end, cached_schedule
    if new_start < start or new_end > end:
        start = new_start if new_start < start else start
        end = new_end if new_end > end else end
        cached_schedule = nyse.schedule(start_date=start.strftime('%Y-%m-%d'), end_date=end.strftime('%Y-%m-%d'))


def get_prev_day_market_close_time(current_time):
    current_time_utc = current_time.astimezone(tz=pytz.utc)

    schedule = get_market_schedule(current_time_utc)

    prev_day_close = None
    for close_time in schedule['market_close']:
        if close_time < current_time_utc.replace(tzinfo=pytz.utc):
            prev_day_close = close_time
        else:
            break

    return datetime.fromtimestamp(prev_day_close.value / 1000000000)


def get_today_market_close_time(current_time):
    current_time_utc = current_time.astimezone(tz=pytz.utc)

    schedule = get_market_schedule(current_time_utc)

    today_close = None
    for close_time in schedule['market_close']:
        if close_time > current_time_utc.replace(tzinfo=pytz.utc):
            today_close = close_time
            break

    return datetime.fromtimestamp(today_close.value / 1000000000)


def get_today_market_open_time(current_time):
    current_time_utc = current_time.astimezone(tz=pytz.utc)

    schedule = get_market_schedule(current_time_utc)

    today_open = None
    for row in schedule.itertuples():
        if row.market_close > current_time_utc.replace(tzinfo=pytz.utc):
            today_open = row.market_open
            break

    return datetime.fromtimestamp(today_open.value / 1000000000)


def is_market_open(current_time):
    current_time_utc = current_time.astimezone(tz=pytz.utc)
    schedule = get_market_schedule(current_time_utc)
    result = nyse.open_at_time(schedule, pd.Timestamp(current_time_utc.timestamp(), unit='s', tz=pytz.utc))
    return result


def get_market_schedule(current_time_utc):
    start_date = (current_time_utc - timedelta(days=10))
    end_date = (current_time_utc + timedelta(days=10))
    widen_cached_schedule(start_date, end_date)
    schedule = cached_schedule[start_date.strftime('%Y-%m-%d'): end_date.strftime('%Y-%m-%d')]
    return schedule
