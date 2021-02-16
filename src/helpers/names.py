import logging
import re

def find_names(file_contents):
    logging.debug("find_names::enter")
    date_pattern_iphone = r"\[[\d]{1,2}/[\d]{1,2}/[\d]{2,4}"
    date_pattern_android = r"[\d]{1,2}/[\d]{1,2}/[\d]{2,4}"
    f1 = ''
    f2 = ''
    os = ''
    if re.match(date_pattern_android, file_contents):
        logging.debug("android pattern")
        os = 'android'
        name_starting_index = file_contents.find(" - ") + 3
        name_ending_index = file_contents.find(":", name_starting_index)
        f1 = file_contents[name_starting_index:name_ending_index]
        while "Messages and calls are end-to-end encrypted" in f1 or "changed their phone number" in f1:
            name_starting_index = file_contents.find(" - ", name_starting_index) + 3
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
    elif re.match(date_pattern_iphone, file_contents):
        logging.debug("iphone pattern")
        os = 'ios'
        name_starting_index = file_contents.find("] ") + 2
        name_ending_index = file_contents.find(":", name_starting_index)
        f1 = file_contents[name_starting_index:name_ending_index]
        while "Messages and calls are end-to-end encrypted" in f1 or "changed their phone number" in f1:
            name_starting_index = file_contents.find(
                "] ", name_starting_index) + 2
            name_ending_index = file_contents.find(":", name_starting_index)
            f1 = file_contents[name_starting_index:name_ending_index]
        name_starting_index = file_contents.find("] ", name_ending_index) + 2
        name_ending_index = file_contents.find(":", name_starting_index)
        while True:
            f2 = file_contents[name_starting_index:name_ending_index]
            if f2 != f1:
                break
            else:
                name_starting_index = file_contents.find(
                    "] ", name_ending_index) + 2
                name_ending_index = file_contents.find(
                    ":", name_starting_index)


    logging.debug("find_names::exit")
    return f1, f2, os


def names_parsed(f1, f2):
    logging.debug("names_parsed::enter")
    f1_parsed = " " + f1 + ": "
    f2_parsed = " " + f2 + ": "
    logging.debug("names_parsed::exit")
    return f1_parsed, f2_parsed

