import traceback
import math

from helpers import dates, names, generic
from friend import Friend


def main():
    try:
        file_path = "../sample.txt"
        file_contents = generic.read_file(file_path)

        friend1 = Friend()
        friend2 = Friend()

        friend1.name, friend2.name = names.find_names(file_contents)
        friend1.parsed_name, friend2.parsed_name = names.names_parsed(friend1.name,friend2.name)

        friend1.find_message_count(file_contents)
        friend2.find_message_count(file_contents)

        friend1.prepare_messages_list(file_contents)
        friend2.prepare_messages_list(file_contents)

        friend1.find_word_frequency()
        friend2.find_word_frequency()

        friend1.find_top_words()
        friend2.find_top_words()

        dates_list = dates.findall_dates(file_contents)
        no_message_days, total_days = dates.count_days(dates_list)
        friend1.messages_per_day = math.ceil(friend1.message_count/total_days)
        friend2.messages_per_day = math.ceil(friend2.message_count/total_days)

        print("Number of messages sent by {} is {}".format(friend1.name, friend1.message_count))
        print("Number of messages sent by {} is {}".format(friend2.name, friend2.message_count))
        print("Number of media sent by {} is {}".format(friend1.name, friend1.media_shared))
        print("Number of media sent by {} is {}".format(friend2.name, friend2.media_shared))
        print("Number of words sent by {} is {}".format(friend1.name, friend1.word_count))
        print("Number of words sent by {} is {}".format(friend2.name, friend2.word_count))
        print("Top words sent by {} is {}".format(friend1.name, friend1.top_words))
        print("Top words sent by {} is {}".format(friend1.name, friend2.top_words))
        print("Number of days without any message is {} from a total of {}".format(no_message_days, total_days))
        print("Messages per day by {} is {}".format(friend1.name, friend1.messages_per_day))
        print("Messages per day by {} is {}".format(friend2.name, friend2.messages_per_day))

    except Exception:
        print(traceback.format_exc())


if __name__ == "__main__":
    main()
