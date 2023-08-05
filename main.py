import get_game_lines
import get_channel_lines


def main():
    last_location = get_game_lines.last_location()
    print(f"Last location: {last_location}")

    for channel in get_channel_lines.list_channels():
        if "intel" not in channel.lower():
            print(f"Skipping {channel} (not intel channel)")
            continue

        for time, user, message in get_channel_lines.channel_lines(channel):
            if last_location.lower() in message.lower():
                print(f"{time} {user}@{channel}: {message}")

            else:
                print(".")


main()
