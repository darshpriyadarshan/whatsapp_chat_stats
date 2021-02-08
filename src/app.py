from helpers.dates import Dates
from friend import Friend
from helpers import names, generic
import traceback
from flask import Flask
from flask import render_template
app = Flask(__name__)


class Main:
    def __init__(self):
        self.file_path = None
        self.file_contents = None

    def prepare_stats(self, friend1, friend2, date_object):
        try:
            friend1.name, friend2.name = names.find_names(self.file_contents)
            print("Friend1 is {}".format(friend1.name))
            print("Friend2 is {}".format(friend2.name))

            friend1.parsed_name, friend2.parsed_name = names.names_parsed(
                friend1.name, friend2.name)

            friend1.find_message_count(self.file_contents)
            friend2.find_message_count(self.file_contents)
            print("Number of messages sent by {} is {}".format(
                friend1.name, friend1.message_count))
            print("Number of messages sent by {} is {}".format(
                friend2.name, friend2.message_count))

            friend1.prepare_messages_list(self.file_contents)
            friend2.prepare_messages_list(self.file_contents)

            friend1.find_word_frequency()
            friend2.find_word_frequency()
            print("Number of media sent by {} is {}".format(
                friend1.name, friend1.media_shared))
            print("Number of media sent by {} is {}".format(
                friend2.name, friend2.media_shared))
            print("Number of words sent by {} is {}".format(
                friend1.name, friend1.word_count))
            print("Number of words sent by {} is {}".format(
                friend2.name, friend2.word_count))

            friend1.find_frequently_used_words()
            friend2.find_frequently_used_words()
            print("We are considering words with 3 or more letters for frequently used words, words are not case "
                  "sensitive")
            print("Frequently used words sent by {} are {}".format(
                friend1.name, friend1.frequently_used_words))
            print("Frequently used words sent by {} are {}".format(
                friend2.name, friend2.frequently_used_words))

            date_object.findall_dates(self.file_contents)
            date_object.findall_date_time(self.file_contents)
            date_object.longest_conversation(date_object.date_time_list)
            date_object.count_days(date_object.dates_list)
            friend1.messages_per_day = round(
                friend1.message_count / date_object.total_days, 2)
            friend2.messages_per_day = round(
                friend2.message_count / date_object.total_days, 2)

            print("Number of days without any message is {} from a total of {}".format(
                date_object.total_days - date_object.message_days, date_object.total_days))
            print("Messages per day by {} is {}".format(
                friend1.name, friend1.messages_per_day))
            print("Messages per day by {} is {}".format(
                friend2.name, friend2.messages_per_day))
            print(
                "Total length of all messages put together by {} is {}".format(friend1.name, friend1.total_messages_length))
            print(
                "Total length of all messages put together by {} is {}".format(friend2.name, friend2.total_messages_length))
            print("Longest Message by {} is {} \nLength is {}".format(friend1.name, friend1.longest_message,
                                                                      friend1.longest_message_length))
            print("Longest Message by {} is {} \nLength is {}".format(friend2.name, friend2.longest_message,
                                                                      friend2.longest_message_length))
            print("For finding the longest conversation, we have considered a maximum time gap of 10 minutes between "
                  "adjacent messages")
            print("Longest conversation has {} messages, started at {}, ended at {}".format(
                date_object.longest_convo_messages, date_object.date_time_list[
                    date_object.longest_convo_start],
                date_object.date_time_list[date_object.longest_convo_end]))
            print("Average length of each message by {} is {}".format(
                friend1.name, friend1.average_message_length))
            print("Average length of each message by {} is {}".format(
                friend2.name, friend2.average_message_length))
            print("Average number of words per message by {} is {}".format(
                friend1.name, friend1.average_words_per_message))
            print("Average number of words per message by {} is {}".format(
                friend2.name, friend2.average_words_per_message))

            friend1.find_frequently_used_emojis()
            friend2.find_frequently_used_emojis()
            # print("Frequently used emojis by {} are {}".format(friend1.name, friend1.frequently_used_emojis))
            # print("Frequently used emojis by {} are {}".format(friend2.name, friend2.frequently_used_emojis))
            print("Frequently used emojis by {} with description {}".format(
                friend1.name, friend1.emojis_with_description))
            print("Frequently used emojis by {} with description {}".format(
                friend2.name, friend2.emojis_with_description))

            date_object.find_peak_hour(date_object.date_time_list)
            percent_of_total_messages_hour = round(
                (date_object.messages_per_hour[0][1] / (friend1.message_count + friend2.message_count)) * 100, 2)
            print("Most number of messages were sent at during {} hour of the day. "
                  "Total messages at this hour are {} which is {}% of total messages".format(
                      date_object.messages_per_hour[0][0], date_object.messages_per_hour[0][1], percent_of_total_messages_hour))

            date_object.find_peak_day(date_object.date_time_list)
            percent_of_total_messages_day = round(
                (date_object.messages_per_day[0][1] / (friend1.message_count + friend2.message_count)) * 100, 2)
            print("Most number of messages were sent on {}. "
                  "Total messages on this day are {} which is {}% of total messages".format(
                      date_object.messages_per_day[0][0], date_object.messages_per_day[0][1], percent_of_total_messages_day))

        except Exception:
            print(traceback.format_exc())

    def main(self):
        try:
            self.file_path = "../sample.txt"
            self.file_contents = generic.read_file(self.file_path)
            #print(file_contents)
            friend1 = Friend()
            friend2 = Friend()
            date_object = Dates()
            self.prepare_stats(friend1, friend2, date_object)
        except Exception:
            print(traceback.format_exc())


@app.route("/")
def home():
    try:
        main_obj = Main()
        main_obj.file_path = "../sample.txt"
        main_obj.file_contents = generic.read_file(main_obj.file_path)
        #print(file_contents)
        friend1 = Friend()
        friend2 = Friend()
        date_object = Dates()
        main_obj.prepare_stats(friend1, friend2, date_object)
    except Exception:
        print(traceback.format_exc())
    finally:
        return render_template("basic.html", friend1=friend1, friend2=friend2, date_object=date_object)

