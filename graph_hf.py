import sqlite3
import sys
import matplotlib

from extract_chats import get_chat_messages

CHAT_ID = 6


def main():
    conn = sqlite3.connect(sys.argv[1])
    messages = get_chat_messages(conn, CHAT_ID)


if __name__ == '__main__':
    main()
