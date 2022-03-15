import json
import discord
import re
from bot.commands.commandinterface import CommandInterface
from bot.reactions.reactioninterface import ReactionInterface
import utils.path_utils as PathUtils


class DiscordClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super(DiscordClient, self).__init__(*args, **kwargs)

        self.command_interface = CommandInterface()
        self.reaction_interface = ReactionInterface()

        # Bot Settings
        self.command_prefix = ""

        self.load_bot_settings()

    async def on_ready(self):
        pass

    async def on_message(self, message: discord.message):
        if message.author.id == self.user.id:
            return

        # We need to use regex because the mention string can have a few different
        # characters depending on how the user was mentioned
        if not re.match(f"^<@.?{self.user.id}>", message.content):
            return

        # Strip bot mention from the message
        message.content = re.sub(f"^<@.?{self.user.id}>", "", message.content).strip()

        await self.command_interface.handle_command_message(message)

    async def on_raw_reaction_add(self, reaction_payload: discord.RawReactionActionEvent):
        if reaction_payload.user_id == self.user.id:
            return

        # await self.reaction_interface.handle_reaction_add(reaction_payload)

    async def on_raw_reaction_remove(self, reaction_payload: discord.RawReactionActionEvent):
        if reaction_payload.user_id == self.user.id:
            return

        # await self.reaction_interface.handle_reaction_remove(reaction_payload)

    def get_username_by_id(self, user_id):
        user = self.get_user(int(user_id))
        if not user:
            return "Unknown User"
        else:
            return user.name

    def load_bot_settings(self):
        settings_path = PathUtils.get_user_data_file_path("bot_settings.json")
        with open(settings_path, "r") as f:
            try:
                settings_data = json.load(f)
            except:
                settings_data = {}
        self.command_prefix = settings_data.get("prefix", "$")

    def save_bot_settings(self):
        settings_path = PathUtils.get_user_data_file_path("bot_settings.json")
        settings_data = {
            "prefix": self.command_prefix
        }
        with open(settings_path, "w") as f:
            json.dump(settings_data, f)
