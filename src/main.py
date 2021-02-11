import traceback
from helpers import names
import logging


class Main:
    def __init__(self):
        self.file_contents = None
        self.peak_hour_percent = 0
        self.peak_day_percent = 0

    def prepare_stats(self, friend1, friend2, date_object):
        try:
            logging.debug("prepare_stats::enter")
            friend1.name, friend2.name = names.find_names(self.file_contents)
            logging.debug("Friend1 is %s Friend2 is %s", friend1.name, friend2.name)

            friend1.parsed_name, friend2.parsed_name = names.names_parsed(friend1.name, friend2.name)

            friend1.find_message_count(self.file_contents)
            friend2.find_message_count(self.file_contents)

            friend1.prepare_messages_list(self.file_contents)
            friend2.prepare_messages_list(self.file_contents)

            friend1.find_word_frequency()
            friend2.find_word_frequency()

            friend1.find_frequently_used_words()
            friend2.find_frequently_used_words()

            date_object.findall_dates(self.file_contents)
            date_object.findall_date_time(self.file_contents)
            date_object.longest_conversation(date_object.date_time_list)
            date_object.count_days(date_object.dates_list)
            friend1.messages_per_day = round(friend1.message_count / date_object.total_days, 2)
            friend2.messages_per_day = round(friend2.message_count / date_object.total_days, 2)

            friend1.find_frequently_used_emojis()
            friend2.find_frequently_used_emojis()

            date_object.find_peak_hour(date_object.date_time_list)
            self.peak_hour_percent = round((date_object.messages_per_hour[0][1] / (friend1.message_count + 
                                                                                   friend2.message_count)) * 100, 2)

            date_object.find_peak_day(date_object.date_time_list)
            self.peak_day_percent = round((date_object.messages_per_day[0][1] / (friend1.message_count + 
                                                                                 friend2.message_count)) * 100, 2)

            logging.debug("prepare_stats::exit")
        except Exception as e:
            logging.exception("Exception in prepare_stats")
