import datetime
from datetime import timedelta


def date_adding(start_date, days):
    return string_to_date((start_date + timedelta(days=days)).strftime('%Y-%m-%d')).date()


def date_to_string(date):
    return date.strftime('%Y-%m-%d')


def string_to_date(date_in_string):
    return datetime.datetime.strptime(date_in_string, '%Y-%m-%d')
