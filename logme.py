#!/Users/yc/opt/anaconda3/bin/python

from os import path
from sys import argv
from optparse import OptionParser
from datetime import datetime, date, time, timedelta

log_dir = "./logs"
date_format = "%Y-%m-%d"
time_format = "%H:%M:%S"
datetime_format = "{} {}".format(datetime, time_format)

parser = OptionParser()
parser.add_option("-d", "--diff-days", dest="diff_days", default=0, type="int", help="the diff between today and the day to log")
parser.add_option("-l", "--log", dest="log_message", default=None, help="log some thing")
parser.add_option('-t', "--today", dest="list_today", action="store_true", default=False, help="show logs of today")
parser.add_option("-y", "--yestoday", dest="list_yestorday", action="store_true", default=False, help="show logs of yestorday")
parser.add_option("-w", "--week", dest="list_week", action="store_true", default=False, help="show logs of this week")


class Date:
    def __init__(self, _date):
        if isinstance(_date, date):
            self._date = _date

    def minus(self, td):
        return Date(self._date - td)

    def add(self, td):
        return Date(self._date + td)

    def weekday(self):
        return self._date.weekday()

    def __str__(self):
        return self._date.strftime(date_format)

class Time:
    def __init__(self, _time):
        if isinstance(_time, time):
            self._time = _time

    def __str__(self):
        return self._time.strftime(time_format)

def get_current():
    current = datetime.now()
    date = current.date()
    time = current.time()
    return Date(date), Time(time)

def get_log_file_of_date(date: Date):
    return path.join(log_dir, str(date) + ".log")

def write_message(date: Date, time: Time, message):
    file_path = get_log_file_of_date(date)
    mode = "a" if path.exists(file_path) else "w"
    with open(file_path, mode) as f:
        f.write("{}##{}####\n".format(time, message))

def get_logs(date):
    file_path = get_log_file_of_date(date)
    if not path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        return f.readlines()

def print_line():
    print("==========" * 3)

def print_date_logs(date):
    print_line()
    print("date: {}".format(str(date)))
    logs = get_logs(date)
    print_line()
    for log in logs:
        print(log, end="")

def days_in_week_of_day(day):
    dates = [day.add(timedelta(days=i)) for i in range(0 - day.weekday(), 7 - day.weekday())]
    return dates

def print_week_logs(day):
    days = days_in_week_of_day(day)
    for day in days:
        print_date_logs(day)

def log_day_in_diff(diff):
    d, _ = get_current()
    d = d.add(timedelta(days=diff))
    return print_date_logs(d)

def log_week_with_days_in_diff(n):
    d, _ = get_current()
    d = d.add(timedelta(days=n))
    print_week_logs(d)

if __name__ == "__main__":
    (options, _) = parser.parse_args()
    log_message = options.log_message
    list_today = options.list_today
    list_yestorday = options.list_yestorday
    list_week = options.list_week
    diff_days = options.diff_days
    d, t = get_current()

    arg_string = " ".join(argv[1:])

    if not arg_string.startswith("-"):
        log_message = arg_string

    log_message = log_message.strip()

    if log_message:
        write_message(d, t, log_message)

    if list_today:
        diff_days = 0
    if list_yestorday:
        diff_days = -1

    if list_week:
        log_week_with_days_in_diff(diff_days)
    else:
        log_day_in_diff(diff_days)

