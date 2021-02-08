import re
from dateutil.parser import *
import datetime
from collections import OrderedDict


class Dates:
    def __init__(self):
        self.dates_list = []
        self.date_time_list = []
        self.total_days = 0
        self.message_days = 0
        self.longest_convo_messages = 0
        self.longest_convo_start = None
        self.longest_convo_end = None
        self.messages_per_hour = []
        self.messages_per_day = []

    def findall_dates(self, file_contents):
        date_pattern = r"\n[\d]{1,2}/[\d]{1,2}/[\d]{2}"
        self.dates_list = re.findall(date_pattern, file_contents)
        # to remove \n from date, using date[1:]
        self.dates_list = [date[1:] for date in self.dates_list]
        # OrderedDict.fromkeys removes duplicates while preserving order
        self.dates_list = list(OrderedDict.fromkeys(self.dates_list))

    def findall_date_time(self, file_contents):
        date_time_pattern = r"\n[\d]{1,2}/[\d]{1,2}/[\d]{2}, [\d]{2}:[\d]{2}"
        self.date_time_list = re.findall(date_time_pattern, file_contents)
        self.date_time_list = [parse(date_time[1:]) for date_time in self.date_time_list]

    def count_days(self, dates_list):
        start_date = parse(dates_list[0])
        end_date = parse(dates_list[-1])
        self.total_days = (end_date - start_date).days
        self.message_days = len(dates_list)

    def longest_conversation(self, date_time_list):
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
            if counter > self.longest_convo_messages:
                self.longest_convo_messages = counter
                self.longest_convo_end = j-1
                self.longest_convo_start = temp

    def find_peak_hour(self, date_time_list):
        messages_in_hour = {}
        for date_time in date_time_list:
            if date_time.hour not in messages_in_hour:
                messages_in_hour[date_time.hour] = 1
            else:
                messages_in_hour[date_time.hour] += 1
        self.messages_per_hour = sorted(messages_in_hour.items(), key=lambda item: item[1], reverse=True)
        self.messages_per_hour = [(datetime.time(hour[0]), hour[1]) for hour in self.messages_per_hour]

    def find_peak_day(self, date_time_list):
        messages_in_day = {}
        day_mapping = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
        for date_time in date_time_list:
            if date_time.weekday() not in messages_in_day:
                messages_in_day[date_time.weekday()] = 1
            else:
                messages_in_day[date_time.weekday()] += 1
        self.messages_per_day = sorted(messages_in_day.items(), key=lambda item: item[1], reverse=True)
        self.messages_per_day = [(day_mapping[day[0]], day[1]) for day in self.messages_per_day]

