import shared
import datetime as dt
import pytest


def test_chat_filename_parts():
    # test with ms
    assert shared.chat_filename_parts("Corp_20230413_153106_651799459.txt") == (
        "Corp",
        dt.datetime(2023, 4, 13, 15, 31, 6),
    )

    # test without ms
    assert shared.chat_filename_parts("Corp_20230413_153106.txt") == (
        "Corp",
        dt.datetime(2023, 4, 13, 15, 31, 6),
    )

    # test failt withou time
    assert shared.chat_filename_parts("Corp_20230413.txt") is None


def test_game_filename_parts():
    # test with ms
    assert shared.game_filename_parts("20230413_153106_651799459.txt") == dt.datetime(
        2023, 4, 13, 15, 31, 6
    )

    # test without ms
    assert shared.game_filename_parts("20230413_153106.txt") == dt.datetime(
        2023, 4, 13, 15, 31, 6
    )

    # test failt withou time
    assert shared.game_filename_parts("20230413.txt") is None


def test_log_line_parts():
    # with username
    assert shared.log_line_parts("[ 2023.04.22 08:44:59 ] user name > message") == (
        dt.datetime(2023, 4, 22, 8, 44, 59),
        "user name",
        "message",
    )

    # without username
    assert shared.log_line_parts("[ 2023.04.22 08:44:59 ] message") == (
        dt.datetime(2023, 4, 22, 8, 44, 59),
        None,
        "message",
    )


def test_proper_removal_of_control_characters():
    # nothing
    assert shared.remove_control_characters("test") == "test"
    # newline
    assert shared.remove_control_characters("test\ntest") == "testtest"
    # null
    assert shared.remove_control_characters("test\0test") == "testtest"
