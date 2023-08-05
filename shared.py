import re
import datetime as dt
import unicodedata

# parse file name to get channel, date, time, ms groups
# example:
# - Corp_20230413_153106_651799459.txt
# - Corp_20230413_153106.txt
# <channel>_<date>_<time>_<ms>.txt
# <channel>_<date>_<time>.txt
chat_filename_pattern = re.compile(
    r"^(?P<channel>.+)_(?P<datetime>\d{8}_\d{6})(_(?P<ms>\d+))?.txt$"
)


def chat_filename_parts(filename):
    """Returns a tuple of (channel, and datetime) if the filename matches the pattern, otherwise None"""
    match = chat_filename_pattern.match(filename)
    if match:
        channel = match.group("channel")
        datetime = dt.datetime.strptime(match.group("datetime"), "%Y%m%d_%H%M%S")

        return channel, datetime


# parse file name to get date, time, and optionaly ms groups
# example:
# - 20230413_153106_651799459.txt
# - 20230413_153106.txt

game_filename_pattern = re.compile(r"^(?P<datetime>\d{8}_\d{6})(_(?P<ms>\d+))?.txt$")


def game_filename_parts(filename):
    """Returns a tuple of (datetime) if the filename matches the pattern, otherwise None"""
    match = game_filename_pattern.match(filename)
    if match:
        datetime = dt.datetime.strptime(match.group("datetime"), "%Y%m%d_%H%M%S")

        return datetime


# parse log line, the username is optional
# example:
# - [ 2023.04.22 08:44:59 ] user name > message
# - [ 2023.04.22 08:44:59 ] log message
log_line_pattern = re.compile(
    r"^\[ (?P<datetime>\d{4}.\d{2}.\d{2} \d{2}:\d{2}:\d{2}) \](?: ?(?P<user>.+?) >)? (?P<message>.+)$"
)


def log_line_parts(line):
    """Returns a tuple of (datetime, user, message) if the line matches the pattern, otherwise None"""
    match = log_line_pattern.match(line)
    if match:
        datetime = dt.datetime.strptime(match.group("datetime"), "%Y.%m.%d %H:%M:%S")
        user = match.group("user")
        message = match.group("message")

        return datetime, user, message


def remove_control_characters(s):
    """Remove control characters from string"""
    return "".join(ch for ch in s if unicodedata.category(ch)[0] != "C")
