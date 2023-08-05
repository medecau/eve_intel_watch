import datetime as dt
from itertools import groupby, chain
import pathlib
import shared

logs = pathlib.Path("data/logs")

chatlogs = logs / "Chatlogs"

# group by channel
# sort by date


def list_channels():
    channels = {shared.chat_filename_parts(f.name)[0] for f in chatlogs.glob("*.txt")}
    return sorted(channels)


def channel_files(channel):
    return sorted(
        chatlogs.glob(f"{channel}*.txt"),
        key=lambda f: shared.chat_filename_parts(f.name),
    )


def process_line(line):
    line = shared.remove_control_characters(line).strip()
    if not line:
        return None
    line_parts = shared.log_line_parts(line)
    if line_parts:
        time, user, message = line_parts
        if dt.datetime.utcnow() - time < dt.timedelta(hours=2):
            return time, user, message


def channel_lines(channel):
    for file in channel_files(channel):
        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            yield from (
                processed for line in f if (processed := process_line(line)) is not None
            )


for channel in list_channels():
    if "intel" not in channel.lower():
        continue

    for time, user, message in channel_lines(channel):
        print(f"{time} {user}@{channel}: {message}")
