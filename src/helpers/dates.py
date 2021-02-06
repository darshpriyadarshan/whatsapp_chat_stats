import re
from dateutil.parser import *
from collections import OrderedDict


def findall_dates(file_contents):
    date_pattern = r"\n[\d]{1,2}/[\d]{1,2}/[\d]{2}"
    dates_list= re.findall(date_pattern, file_contents)
    return list(OrderedDict.fromkeys(dates_list))


def count_days(dates_list):
    start_date = parse(dates_list[0])
    end_date = parse(dates_list[-1])
    total_days = (end_date-start_date).days
    message_days = len(dates_list)
    return total_days-message_days, total_days
