import os
import sqlite3
import csv
import argparse


# if chat name exists, use it, if not, join all contact names in the chat
def get_chat_file_name(conn, chat_id, chat_name):
    if(chat_name):
        return chat_name + ".csv"

    chat_name = ""
    result = conn.execute("SELECT Contact.name FROM Contact JOIN ChatRelation USING (ContactID) WHERE ChatID = ?;", (chat_id,))
    for row in result:
        if(row[0] is not None):
            chat_name += row[0]
        else:
            chat_name += "None"
        chat_name += "-"
    chat_name = chat_name[:-1].replace(" ", "_")  # strip last '-' and replace spaces
    return chat_name + ".csv"


# returns list of messages where each message
# is a following tuple: (timestamp, name_of_sender, message_text)
def get_chat_messages(conn, chat_id):
    result = conn.execute(
 """SELECT datetime(TimeStamp/1000+3600, 'unixepoch'), (SELECT Contact.name FROM (Events JOIN Contact USING (ContactID)) N WHERE M.ContactID = N.ContactID), Body\
    FROM (Messages join Events USING (EventID)) M\
    WHERE ChatID = ? AND Messages.Type = 1\
    ORDER BY TimeStamp;""", (chat_id,))
    messages = []
    for row in result:
        messages.append(row)
    return messages


# prints messages to a file in the csv format
def print_chat_to_file(conn, chat_id, chat_name, chats_directory):
    file_name = get_chat_file_name(conn, chat_id, chat_name)
    messages = get_chat_messages(conn, chat_id)

    with open(chats_directory + file_name, "w", newline="", encoding="utf-8") as file:
        csvwriter = csv.writer(file)
        for message in messages:
            csvwriter.writerow(message)

    print("Created:", chats_directory + file_name + ",", "messages:", len(messages))


def create_conn(file_name):
    return sqlite3.connect(file_name)


# chat_info := (chat_id, chat_name)
def get_chat_infos(conn):
    result = conn.execute("SELECT ChatID, name FROM ChatInfo;")
    chat_infos = []
    for row in result:
        chat_infos.append(row)
    return chat_infos


def get_arguments():
    parser = argparse.ArgumentParser(description="Extracts chat messages from Viber")
    parser.add_argument("database_file", help="A path to a database file used by Viber. \
                        On Linux located in : ~/.ViberPC/[your_phone_number]/viber.db")
    parser.add_argument("chats_directory", default="chats", nargs='?', help="Path to a directory where chat \
                        history files will be saved. If the directory does not exist, it wil be created automatically.")
    return parser.parse_args()


def main():
    arguments = get_arguments()
    conn = create_conn(arguments.database_file)

    if not os.path.exists(arguments.chats_directory):
        os.makedirs(arguments.chats_directory, exist_ok=True)

    chat_infos = get_chat_infos(conn)
    for chat_id, chat_name in chat_infos:
        print_chat_to_file(conn, chat_id, chat_name, arguments.chats_directory + "/")


if __name__ == "__main__":
    main()
