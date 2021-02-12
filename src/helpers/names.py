import logging


def find_names(file_contents):
    logging.debug("find_names::enter")
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
    logging.debug("find_names::exit")
    return f1, f2


def names_parsed(f1, f2):
    logging.debug("names_parsed::enter")
    f1_parsed = " - " + f1 + ": "
    f2_parsed = " - " + f2 + ": "
    logging.debug("names_parsed::exit")
    return f1_parsed, f2_parsed

