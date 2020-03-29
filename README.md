# Viber_message_extractor
Viber no longer provides an option to download your chat message history. It uses sqlite3 database to save all it's data so you just need to locate the database file and the script does the rest for you.

### dependencies:
python3 and sqlite3 need to be installed

### usage:
`python3 extract_chats.py [-h] database_file [chats_directory]`

#### positional arguments:

##### database_file   
A path to a database file used by Viber. On Linux located in : ~/.ViberPC/[your_phone_number]/viber.db
##### hats_directory
Path to a directory where chat history files will be saved. If the directory does not exist, it wil be created automatically.

#### optional arguments:

##### -h, --help
show this help message and exit
