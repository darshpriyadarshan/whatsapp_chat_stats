import re
from dateutil.parser import *
import datetime
from collections import OrderedDict


def findall_dates(file_contents):
    date_pattern = r"\n[\d]{1,2}/[\d]{1,2}/[\d]{2}"
    dates_list = re.findall(date_pattern, file_contents)
    # to remove \n from date, using date[1:]
    dates_list_formatted = [date[1:] for date in dates_list]
    # OrderedDict.fromkeys removes duplicates while preserving order
    return list(OrderedDict.fromkeys(dates_list_formatted))


def findall_date_time(file_contents):
    date_time_pattern = r"\n[\d]{1,2}/[\d]{1,2}/[\d]{2}, [\d]{2}:[\d]{2}"
    date_time_list = re.findall(date_time_pattern, file_contents)
    date_time_list_formatted = [date_time[1:] for date_time in date_time_list]
    return date_time_list_formatted, list(OrderedDict.fromkeys(date_time_list_formatted))


def count_days(dates_list):
    start_date = parse(dates_list[0])
    end_date = parse(dates_list[-1])
    total_days = (end_date - start_date).days
    message_days = len(dates_list)
    return total_days - message_days, total_days


def parse_date_time_list(date_time_list):
    parsed_list = [parse(date_time) for date_time in date_time_list]
    return parsed_list


def longest_conversation(date_time_list):
    messages_number = 0
    i = -1
    j = 0
    while j < len(date_time_list):
        i += 1
        j = i+1
        counter = 0
        if (date_time_list[j] - date_time_list[i]).seconds < 600:
            temp = i
        else:
            continue
        while j < len(date_time_list) and (date_time_list[j] - date_time_list[i]).seconds < 600:
            counter += 1
            i += 1
            j += 1
        if counter > messages_number:
            messages_number = counter
            end_time_index = j-1
            start_time_index = temp
    return messages_number, start_time_index, end_time_index


def find_peak_hour(date_time_list):
    messages_in_hour = {}
    for date_time in date_time_list:
        if date_time.hour not in messages_in_hour:
            messages_in_hour[date_time.hour] = 1
        else:
            messages_in_hour[date_time.hour] += 1
    messages_in_hour_list = sorted(messages_in_hour.items(), key=lambda item: item[1], reverse=True)
    # print(messages_in_hour_list)
    peak_hour = datetime.time(messages_in_hour_list[0][0])
    return peak_hour, messages_in_hour_list[0][1]


def find_peak_day(date_time_list):
    messages_in_day = {}
    day_mapping = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    for date_time in date_time_list:
        if date_time.weekday() not in messages_in_day:
            messages_in_day[date_time.weekday()] = 1
        else:
            messages_in_day[date_time.weekday()] += 1
    messages_in_day_list = sorted(messages_in_day.items(), key=lambda item: item[1], reverse=True)
    # print(messages_in_day_list)
    peak_day = day_mapping[messages_in_day_list[0][0]]
    return peak_day, messages_in_day_list[0][1]

