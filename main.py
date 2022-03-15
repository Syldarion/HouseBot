import os
import argparse
from bot.discordclient import DiscordClient
from database.databaseinterface import DatabaseInterface


def get_program_args():
    parser = argparse.ArgumentParser(description="Run your HouseBot")

    parser.add_argument("--setuponly", dest="setup_only", action="store_true", help="Run the bot setup and exit")

    return parser.parse_args()


def run():
    args = get_program_args()

    DatabaseInterface.instance().setup_database()

    if args.setup_only:
        return

    DiscordClient().run(os.environ["BOT_TOKEN"])


if __name__ == '__main__':
    run()
