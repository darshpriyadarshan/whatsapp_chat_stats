import traceback
import math

from helpers import dates, names, generic
from friend import Friend


def main():
    try:
        file_path = "../sample.txt"
        file_contents = generic.read_file(file_path)
        #print(file_contents)
        friend1 = Friend()
        friend2 = Friend()

        friend1.name, friend2.name = names.find_names(file_contents)
        print("Friend1 is {}".format(friend1.name))
        print("Friend2 is {}".format(friend2.name))

        friend1.parsed_name, friend2.parsed_name = names.names_parsed(friend1.name,friend2.name)

        friend1.find_message_count(file_contents)
        friend2.find_message_count(file_contents)
        print("Number of messages sent by {} is {}".format(friend1.name, friend1.message_count))
        print("Number of messages sent by {} is {}".format(friend2.name, friend2.message_count))

        friend1.prepare_messages_list(file_contents)
        friend2.prepare_messages_list(file_contents)

        friend1.find_word_frequency()
        friend2.find_word_frequency()
        print("Number of media sent by {} is {}".format(friend1.name, friend1.media_shared))
        print("Number of media sent by {} is {}".format(friend2.name, friend2.media_shared))
        print("Number of words sent by {} is {}".format(friend1.name, friend1.word_count))
        print("Number of words sent by {} is {}".format(friend2.name, friend2.word_count))

        friend1.find_frequently_used_words()
        friend2.find_frequently_used_words()
        print("We are considering words with 3 or more letters for frequently used words, words are not case sensitive")
        print("Frequently used words sent by {} are {}".format(friend1.name, friend1.frequently_used_words))
        print("Frequently used words sent by {} are {}".format(friend2.name, friend2.frequently_used_words))

        dates_list = dates.findall_dates(file_contents)
        datetime_list, datetime_list_unique = dates.findall_datetime(file_contents)
        datetime_list = dates.parse_datetime_list(datetime_list)
        messages_count, start_time_index, end_time_index = dates.longest_conversation(datetime_list)
        no_message_days, total_days = dates.count_days(dates_list)
        friend1.messages_per_day = math.ceil(friend1.message_count/total_days)
        friend2.messages_per_day = math.ceil(friend2.message_count/total_days)

        print("Number of days without any message is {} from a total of {}".format(no_message_days, total_days))
        print("Messages per day by {} is {}".format(friend1.name, friend1.messages_per_day))
        print("Messages per day by {} is {}".format(friend2.name, friend2.messages_per_day))
        print("Total length of all messages put together by {} is {}".format(friend1.name,
                                                                             friend1.total_messages_length))
        print("Total length of all messages put together by {} is {}".format(friend2.name,
                                                                             friend2.total_messages_length))
        print("Longest Message by {} is {} \nLength is {}".format(friend1.name, friend1.longest_message,
                                                                  friend1.longest_message_length))
        print("Longest Message by {} is {} \nLength is {}".format(friend2.name, friend2.longest_message,
                                                                  friend2.longest_message_length))
        print("For finding the longest conversation, we have considered a maximum time gap of 10 minutes between "
              "adjacent messages")
        print("Longest conversation has {} messages, started at {}, ended at {}".format(messages_count,
                                                                                        datetime_list[start_time_index],
                                                                                        datetime_list[end_time_index]))
        print("Average length of each message by {} is {}".format(friend1.name, friend1.average_message_length))
        print("Average length of each message by {} is {}".format(friend2.name, friend2.average_message_length))
        print("Average number of words per message by {} is {}".format(friend1.name, friend1.average_words_per_message))
        print("Average number of words per message by {} is {}".format(friend2.name, friend2.average_words_per_message))

    except Exception:
        print(traceback.format_exc())


if __name__ == "__main__":
    main()
