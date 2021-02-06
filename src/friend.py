import re
import math


class Friend:
    def __init__(self):
        self.name = None
        self.parsed_name = None
        self.message_count = None
        self.messages_list = None
        self.word_count = 0
        self.word_frequency_dict = {}
        self.media_shared = None
        self.frequently_used_words = None
        self.messages_per_day = 0
        self.total_messages_length = 0
        self.longest_message = None
        self.longest_message_length = 0
        self.average_message_length = 0
        self.average_words_per_message = 0

    def find_message_count(self, file_contents):
        self.message_count = file_contents.count(self.parsed_name)

    def prepare_messages_list(self, file_contents):
        date_pattern = '[\d]{1,2}/[\d]{1,2}/[\d]{2}'
        message_pattern = self.parsed_name + '(.*)\n' + date_pattern
        self.messages_list = re.findall(message_pattern, file_contents)

    def find_word_frequency(self):
        for message in self.messages_list:
            self.total_messages_length += len(message)
            if len(message) > self.longest_message_length and not (message.startswith('https') or
                                                                   (message.startswith('magnet:?'))):
                self.longest_message_length = len(message)
                self.longest_message = message
            for word in message.split(" "):
                self.word_count += 1
                if word not in self.word_frequency_dict:
                    self.word_frequency_dict[word] = 1
                else:
                    self.word_frequency_dict[word] += 1
        self.word_frequency_dict = dict(sorted(self.word_frequency_dict.items(),
                                               key=lambda item: item[1],
                                               reverse=True))
        self.word_frequency_dict.pop('omitted>', 0)
        self.media_shared = self.word_frequency_dict.pop('<Media', 0)
        self.word_count = self.word_count - 2 * self.media_shared
        self.average_message_length = math.ceil(self.total_messages_length/self.message_count)
        self.average_words_per_message = math.ceil(self.word_count/self.message_count)

    def find_frequently_used_words(self):
        number_of_words = 10
        self.frequently_used_words = sorted(self.word_frequency_dict.items(),
                                            key=lambda item: item[1],
                                            reverse=True)[:number_of_words]


