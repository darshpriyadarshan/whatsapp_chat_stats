import logging
import re

def find_names(file_contents):
    logging.debug("find_names::enter")
    datetime_pattern = r"\[?[\d]{1,2}/[\d]{1,2}/[\d]{2,4}, [\d]{1,2}:[\d]{2}(:[\d]{2})?( [AP]M\] )?( [ap]m)?( - )?"
    datetime_pattern_n = r"\n\[?[\d]{1,2}/[\d]{1,2}/[\d]{2,4}, [\d]{1,2}:[\d]{2}(:[\d]{2})?( [AP]M\] )?( [ap]m)?( - )?"
    f1 = ''
    f2 = ''
    f1_set = False
    #re.match checks for pattern at the beginning, if not found returns null
    if re.match(datetime_pattern, file_contents):
        logging.debug("starting pattern matched")
        for match in re.finditer(datetime_pattern_n, file_contents):
            name_starting_index = match.end()
            name_ending_index = file_contents.find(":", name_starting_index)
            if not f1_set:
                f1 = file_contents[name_starting_index:name_ending_index]
                if "Messages and calls are end-to-end encrypted" in f1 or "changed their phone number" in f1:
                    continue
                else:
                    f1_set = True
            else:
                f2 = file_contents[name_starting_index:name_ending_index]
                if "Messages and calls are end-to-end encrypted" in f2 or "changed their phone number" in f2 or f1==f2:
                    continue
                else:
                    break
    logging.debug("find_names::exit")
    return f1, f2


def names_parsed(f1, f2):
    logging.debug("names_parsed::enter")
    f1_parsed = " " + f1 + ": "
    f2_parsed = " " + f2 + ": "
    logging.debug("names_parsed::exit")
    return f1_parsed, f2_parsed

