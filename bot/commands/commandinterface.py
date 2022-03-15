import discord
import shlex
from .standalonecommands import RollCommand
from .pollcommands import poll_command_group


class CommandInterface(object):
    def __init__(self):
        roll_command = RollCommand()

        self.command_handlers = {
            roll_command.name: roll_command,
            poll_command_group.name: poll_command_group
        }

    async def handle_command_message(self, message: discord.Message) -> bool:
        command_parts = shlex.split(message.content)

        if not command_parts:
            return

        handler_name = command_parts[0]

        if handler_name in self.command_handlers:
            await self.command_handlers[handler_name].handle_command(command_parts[1:], message)
