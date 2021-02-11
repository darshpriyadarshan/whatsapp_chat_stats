import re
import emoji
import regex
import logging


class Friend:
    def __init__(self):
        self.name = None
        self.parsed_name = None
        self.message_count = 0
        self.messages_list = []
        self.word_count = 0
        self.word_frequency_dict = {}
        self.media_shared = 0
        self.frequently_used_words = None
        self.messages_per_day = 0
        self.total_messages_length = 0
        self.longest_message = None
        self.longest_message_length = 0
        self.average_message_length = 0
        self.average_words_per_message = 0
        self.emoji_dict = {}
        self.frequently_used_emojis = None
        self.emojis_with_description = []

    def find_message_count(self, file_contents):
        logging.debug("find_message_count::enter")
        self.message_count = file_contents.count(self.parsed_name)
        logging.debug("find_message_count::exit")

    def prepare_messages_list(self, file_contents):
        logging.debug("prepare_messages_list::enter")
        date_pattern = '[\d]{1,2}/[\d]{1,2}/[\d]{2}'
        message_pattern = self.parsed_name + '(.*)\n' + date_pattern
        self.messages_list = re.findall(message_pattern, file_contents)
        logging.debug("prepare_messages_list::exit")

    def find_word_frequency(self):
        logging.debug("find_word_frequency::enter")
        for message in self.messages_list:
            self.total_messages_length += len(message)
            word = regex.findall(r'\X', message)
            for an_emoji in word:
                if any(char in emoji.UNICODE_EMOJI['en'] for char in an_emoji):
                    if '\u200d' in an_emoji and ord(an_emoji[-1]) != 65039:
                        an_emoji += chr(65039)
                    if an_emoji not in self.emoji_dict:
                        self.emoji_dict[an_emoji] = 1
                    else:
                        self.emoji_dict[an_emoji] += 1
            if len(message) > self.longest_message_length and not ('https' in message or 'http' in message or 'magnet:?' in message):
                self.longest_message_length = len(message)
                self.longest_message = message
            for word in message.split(" "):
                self.word_count += 1
                if len(word) > 2:
                    if word.lower() not in self.word_frequency_dict:
                        self.word_frequency_dict[word.lower()] = 1
                    else:
                        self.word_frequency_dict[word.lower()] += 1

        self.word_frequency_dict.pop('omitted>', 0)
        self.media_shared = self.word_frequency_dict.pop('<media', 0)
        self.word_count = self.word_count - 2 * self.media_shared
        self.average_message_length = round(self.total_messages_length/self.message_count, 2)
        self.average_words_per_message = round(self.word_count/self.message_count, 2)
        logging.debug("find_word_frequency::exit")

    def find_frequently_used_words(self):
        logging.debug("find_frequently_used_words::enter")
        number_of_words = 20
        self.frequently_used_words = sorted(self.word_frequency_dict.items(),
                                            key=lambda item: item[1],
                                            reverse=True)[:number_of_words]
        logging.debug("find_frequently_used_words::exit")

    def find_frequently_used_emojis(self):
        logging.debug("find_frequently_used_emojis::enter")
        number_of_emojis = 10
        self.frequently_used_emojis = sorted(self.emoji_dict.items(), key=lambda item: item[1], reverse=True)[0:]
        for an_emoji in self.frequently_used_emojis:
            if an_emoji[0] in emoji.UNICODE_EMOJI['en'].keys():
                self.emojis_with_description.append([an_emoji, emoji.UNICODE_EMOJI['en'][an_emoji[0]][1:-1]])
        self.emojis_with_description = self.emojis_with_description[0:number_of_emojis]
        logging.debug("find_frequently_used_emojis::exit")
