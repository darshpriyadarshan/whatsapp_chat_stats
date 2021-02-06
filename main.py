import re
import traceback
import datetime
import math
from dateutil.parser import *
from collections import OrderedDict


def find_names(file_contents):
    name_starting_index = file_contents.find(" - ") + 3
    name_ending_index = file_contents.find(":", name_starting_index)
    f1 = file_contents[name_starting_index:name_ending_index]
    name_starting_index = file_contents.find(" - ", name_ending_index) + 3
    name_ending_index = file_contents.find(":", name_starting_index)
    while True:
        f2 = file_contents[name_starting_index:name_ending_index]
        if f2 != f1:
            break
        else:
            name_starting_index = file_contents.find(" - ", name_ending_index) + 3
            name_ending_index = file_contents.find(":", name_starting_index)
    print("friend1 is {}".format(f1))
    print("friend2 is {}".format(f2))
    return f1, f2


def names_parsed(f1,f2):
    f1_parsed = " - " + f1 + ": "
    f2_parsed = " - " + f2 + ": "
    return f1_parsed,f2_parsed


def message_count(file_contents, f1_parsed, f2_parsed):
    f1_message_count = file_contents.count(f1_parsed)
    f2_message_count = file_contents.count(f2_parsed)
    print("Number of messages sent by friend1 is {}".format(f1_message_count))
    print("Number of messages sent by friend2 is {}".format(f2_message_count))
    return f1_message_count, f2_message_count


def prepare_messages_list(file_contents, f1_parsed, f2_parsed):
    s = f1_parsed + '(.*)\n[\d]{1,2}/[\d]{1,2}/[\d]{2}'
    messages_list1 = re.findall(s, file_contents)
    s = f2_parsed + '(.*)\n[\d]{1,2}/[\d]{1,2}/[\d]{2}'
    messages_list2 = re.findall(s, file_contents)
    return messages_list1,messages_list2


def find_word_frequency(messages_list):
    word_count = 0
    word_frequency_dict = {}
    for message in messages_list:
        for word in message.split(" "):
            word_count += 1
            if word not in word_frequency_dict:
                word_frequency_dict[word] = 1
            else:
                word_frequency_dict[word] += 1
    word_frequency_dict = dict(sorted(word_frequency_dict.items(), key=lambda item: item[1], reverse=True))
    word_frequency_dict.pop('omitted>', 0)
    media_shared = word_frequency_dict.pop('<Media', 0)
    word_count = word_count - 2*media_shared
    return word_count, word_frequency_dict, media_shared


def top_words(word_frequency_dict):
    return sorted(word_frequency_dict.items(), key=lambda item: item[1], reverse=True)[:10]


def findall_dates(file_contents):
    dates_list= re.findall(r"\n[\d]{1,2}/[\d]{1,2}/[\d]{2}", file_contents)
    return list(OrderedDict.fromkeys(dates_list))


def count_days(dates_list):
    start_date = parse(dates_list[0])
    end_date = parse(dates_list[-1])
    total_days = (end_date-start_date).days
    message_days = len(dates_list)
    print("Number of days without any message is {} from a total of {}".format(total_days-message_days, total_days))
    return total_days-message_days, total_days


def main():
    try:
        file = open("sample.txt", encoding="utf8", mode="r")
        file_contents = file.read()
        # print(file_contents)
        friend1, friend2 = find_names(file_contents)
        f1_parsed_name,f2_parsed_name = names_parsed(friend1,friend2)
        friend1_message_count, friend2_message_count = message_count(file_contents, f1_parsed_name, f2_parsed_name)
        messages_list1, messages_list2 = prepare_messages_list(file_contents,f1_parsed_name, f2_parsed_name)
        word_count1, word_frequency_dict1, media_shared_by_f1 = find_word_frequency(messages_list1)
        word_count2, word_frequency_dict2, media_shared_by_f2 = find_word_frequency(messages_list2)
        print("Number of media sent by {} is {}".format(friend1, media_shared_by_f1))
        print("Number of media sent by {} is {}".format(friend2, media_shared_by_f2))
        print("Number of words sent by {} is {}".format(friend1, word_count1))
        print("Number of words sent by {} is {}".format(friend2, word_count2))
        top_words_f1 = top_words(word_frequency_dict1)
        top_words_f2 = top_words(word_frequency_dict2)
        print("Top words sent by {} is {}".format(friend1, top_words_f1))
        print("Top words sent by {} is {}".format(friend2, top_words_f2))
        dates_list = findall_dates(file_contents)
        no_message_days, total_days = count_days(dates_list)
        messages_per_day_f1 = math.ceil(friend1_message_count/total_days)
        messages_per_day_f2 = math.ceil(friend2_message_count/total_days)
        print("Messages per day by {} is {}".format(friend1, messages_per_day_f1))
        print("Messages per day by {} is {}".format(friend2, messages_per_day_f2))

    except Exception:
        print(traceback.format_exc())


if __name__ == "__main__":
    main()