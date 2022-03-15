import discord
from .command import Command, CommandArg, JoinStringAction, CommandExecuteError
from .commandgroup import CommandGroup
from polls.pollinterface import PollInterface


poll_command_group = CommandGroup("poll")


class PollCreateCommand(Command):
    def __init__(self):
        super(PollCreateCommand, self).__init__("create",
                                                description_text="Create a new poll")

        title_arg = CommandArg(names=["title"],
                               help="Poll title",
                               type=str)
        single_choice_arg = CommandArg(names=["-singlechoice", "-sc"],
                                       dest="single",
                                       help="Set a poll to only allow one choice",
                                       action="store_true")
        poll_options_arg = CommandArg(names=["options"],
                                      help="Poll options",
                                      nargs="*",
                                      action="extend")

        self.add_arg(title_arg)
        self.add_arg(single_choice_arg)
        self.add_arg(poll_options_arg)

        self.add_example("@HouseBot poll create \"My poll\" \"Option A\" \"Option B\"")
        self.add_example("@HouseBot poll create -singlechoice \"My poll\" \"Option A\" \"Option B\"")

    async def execute(self, message: discord.Message, args):
        await PollInterface.create_poll(message.channel, message.author, args.title, args.options)


class PollCloseCommand(Command):
    def __init__(self):
        super(PollCloseCommand, self).__init__("close",
                                               description_text="Close an open poll")

        poll_id_arg = CommandArg(names=["poll_id"],
                                 help="Poll ID",
                                 type=int)

        self.add_arg(poll_id_arg)

        self.add_example("@HouseBot poll close 15")

    async def execute(self, message: discord.Message, args):
        await PollInterface.close_poll(message.channel, message.author, args.poll_id)


poll_command_group.add_command(PollCreateCommand())
poll_command_group.add_command(PollCloseCommand())
