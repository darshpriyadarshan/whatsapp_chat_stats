import re
from dateutil.parser import *
from collections import OrderedDict


def findall_dates(file_contents):
    date_pattern = r"\n[\d]{1,2}/[\d]{1,2}/[\d]{2}"
    dates_list = re.findall(date_pattern, file_contents)
    # to remove \n from date, using date[1:]
    dates_list_formatted = [date[1:] for date in dates_list]
    # OrderedDict.fromkeys removes duplicates while preserving order
    return list(OrderedDict.fromkeys(dates_list_formatted))


def findall_datetime(file_contents):
    datetime_pattern = r"\n[\d]{1,2}/[\d]{1,2}/[\d]{2}, [\d]{2}:[\d]{2}"
    datetime_list = re.findall(datetime_pattern, file_contents)
    datetime_list_formatted = [datetime[1:] for datetime in datetime_list]
    return datetime_list_formatted, list(OrderedDict.fromkeys(datetime_list_formatted))


def count_days(dates_list):
    start_date = parse(dates_list[0])
    end_date = parse(dates_list[-1])
    total_days = (end_date - start_date).days
    message_days = len(dates_list)
    return total_days - message_days, total_days


def parse_datetime_list(datetime_list):
    parsed_list = [parse(datetime) for datetime in datetime_list]
    return parsed_list


def longest_conversation(datetime_list):
    messages_number = 0
    i = -1
    j = 0
    while j < len(datetime_list):
        i += 1
        j = i+1
        counter = 0
        if (datetime_list[j] - datetime_list[i]).seconds < 600:
            temp = i
        else:
            continue
        while j < len(datetime_list) and (datetime_list[j] - datetime_list[i]).seconds < 600:
            counter += 1
            i += 1
            j += 1
        if counter > messages_number:
            messages_number = counter
            end_time_index = j-1
            start_time_index = temp
    return messages_number, start_time_index, end_time_index
