from datetime import datetime, timedelta, date
import json
from workalendar.america.brazil import BrazilDistritoFederal
import pandas as pd
from collections import namedtuple


class DateTimeUtils(object):
    pattern_usa = "%Y-%m-%d"
    pattern_usa_full = "%Y-%m-%d %H:%M:%S"
    pattern_brazil = "%d-%m-%Y"
    pattern_brazil_full = "%d-%m-%Y %H:%M:%S"
    pattern_name_file = "%Y_%m_%d_%H_%M_%S"
    pattern_time = "%H:%M:%S"
    br_df_calendar = BrazilDistritoFederal()
    datetime_default = datetime(1, 1, 1, 1, 1, 1)
    year_default = 1998

    @staticmethod
    def convert_str_datetime(date: str, pattern: str):
        if pd.isnull(date):
            return DateTimeUtils.datetime_default
        if "T" in date:
            return datetime.strptime(date.split("T")[0], pattern)
        else:
            return datetime.strptime(date, pattern)

    @staticmethod
    def convert_str_time(time: str, pattern: str):
        if pd.isnull(time):
            return DateTimeUtils.datetime_default
        else:
            time = "0001-01-01 " + time
            return DateTimeUtils.convert_str_datetime(
                time, DateTimeUtils.pattern_usa_full
            )

    @staticmethod
    def convert_datetime_str(date: datetime, pattern: str):
        return date.strftime(pattern)

    @staticmethod
    def diff_days(start: datetime, end: datetime, work_days: bool):
        if start.date() == end.date():
            return 1
        elif work_days:
            return DateTimeUtils.br_df_calendar.get_working_days_delta(start, end, True)
        else:
            return (end - start).days + 1

    @staticmethod
    def interval(hour: int, interval: int = 24):
        period = (hour - 1) // interval
        start = period * interval
        end = start + interval
        return "Between " + str(start) + " and " + str(end) + " days"

    @staticmethod
    def check_limit(value: int, limit: int):
        check = ""
        if value <= limit:
            check = "In "
        else:
            check = "Above "
        return check + str(limit) + " days"

    @staticmethod
    def quarter(date: datetime):
        return pd.Timestamp(year=date.year, month=date.month, day=date.day).quarter

    @staticmethod
    def no_work_days(start: datetime, end: datetime):
        day = 0
        while start.date() != end.date():
            if not DateTimeUtils.br_df_calendar.is_working_day(start):
                day = day + 1
            start = start + timedelta(days=1)
        return day

    @staticmethod
    def diff_hours(start: datetime, end: datetime, work_days: bool):
        date = namedtuple("Data", "years months days hours minutes seconds")
        if end == DateTimeUtils.datetime_default:
            date.years = DateTimeUtils.year_default
            return date
        else:
            diff = end - start
            td = diff - timedelta(days=DateTimeUtils.no_work_days(start, end))
            date.seconds = int(td.total_seconds())
            date.years = date.seconds // (12 * 30 * 24 * 60 * 60)
            date.seconds %= 12 * 30 * 24 * 60 * 60
            date.months = date.seconds // (30 * 24 * 60 * 60)
            date.seconds %= 30 * 24 * 60 * 60
            date.days = date.seconds // (24 * 60 * 60)
            date.seconds %= 24 * 60 * 60
            date.hours = date.seconds // (60 * 60)
            date.seconds %= 60 * 60
            date.minutes = date.seconds // 60
            date.seconds %= 60
            return date


class JsonUtils(object):
    @staticmethod
    def __json_default(obj):
        if isinstance(obj, date):
            return DateTimeUtils.convert_datetime_str(
                obj, DateTimeUtils.pattern_usa_full
            )
        else:
            return obj.__dict__

    @staticmethod
    def convert_json(value):
        return (
            json.dumps(
                value, default=JsonUtils.__json_default, indent=4, ensure_ascii=False
            )
            .encode("utf8")
            .decode()
        )
