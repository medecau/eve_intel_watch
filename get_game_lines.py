import pathlib
import shared
import re


# example:
# (kind) log message
message_pattern = re.compile(r"^\((?P<kind>[^\)]+)\) (?P<message>.+)$")

logs = pathlib.Path("data/logs")

gamelogs = logs / "Gamelogs"

sorted_files = sorted(
    gamelogs.glob("*.txt"), key=lambda f: shared.game_filename_parts(f.name)
)


def emit_game_files():
    gamelogs = logs / "Gamelogs"

    sorted_files = sorted(
        gamelogs.glob("*.txt"), key=lambda f: shared.game_filename_parts(f.name)
    )

    return sorted_files


def emit_game_lines():
    for file in emit_game_files():
        with open(file, "r") as f:
            for line in f:
                line_parts = shared.log_line_parts(line)
                if line_parts:
                    time, _, message = line_parts
                    kind, message = message_pattern.match(message).groups()

                    yield time, kind, message


def emit_location():
    # Undock message example:
    # Undocking from Jita IV - Moon 4 - Caldari Navy Assembly Plant to Jita solar system.
    # Jump message example:
    # Jumping from Jita to Perimeter
    undock_pattern = re.compile(r"Undocking from (?P<from>.+) to (?P<to>.+)")
    jump_pattern = re.compile(r"Jumping from (?P<from>.+) to (?P<to>.+)")

    for time, kind, message in emit_game_lines():
        if match := undock_pattern.match(message):
            yield time, match.group("from"), match.group("to")
        elif match := jump_pattern.match(message):
            yield time, match.group("from"), match.group("to")


def last_location():
    for time, from_, to_ in emit_location():
        pass
    return to_
