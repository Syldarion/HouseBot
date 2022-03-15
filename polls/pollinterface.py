import discord

from bot.embeds.pollembed import PollEmbed
from bot.embeds.pollresultsembed import PollResultsEmbed
from polls.consts import POLL_OPTION_EMOJIS
from database.databaseinterface import DatabaseInterface


class PollInterface(object):
    def __init__(self):
        pass

    @classmethod
    async def create_poll(cls, channel, creator, title, options):
        options_tuples = []

        for i in range(len(options)):
            options_tuples.append((POLL_OPTION_EMOJIS[i], options[i]))

        poll_id = DatabaseInterface.instance().add_poll(title, creator.id, options_tuples)
        if not poll_id:
            await channel.send("Failed to create poll")
            return

        poll_embed = await PollEmbed(poll_id, title, creator, options).build_embed()
        poll_msg = await channel.send(embed=poll_embed)

        DatabaseInterface.instance().assign_poll_message_id(poll_id, poll_msg.id)

        for i in range(len(options)):
            await poll_msg.add_reaction(POLL_OPTION_EMOJIS[i])

    @classmethod
    async def close_poll(cls, channel, requestor, poll_id):
        requestor_id = requestor.id
        poll_data = DatabaseInterface.instance().get_poll_by_id(poll_id)

        if not poll_data:
            await channel.send(f"Could not find poll with ID {poll_id}.")
            return

        poll_open = poll_data["open"]

        if not poll_open:
            await channel.send(f"Poll is already closed.")
            return

        poll_creator = poll_data["creator_id"]

        if poll_creator != requestor_id:
            await channel.send("You cannot close a poll you did not open.")
            return

        DatabaseInterface.instance().close_poll(poll_id)
        poll_options = DatabaseInterface.instance().get_poll_options(poll_id)

        message_obj = None
        try:
            message_obj = await channel.fetch_message(poll_data["message_id"])
        except discord.NotFound:
            await channel.send(f"Could not find poll {poll_id} in this channel.")

        message_reactions = message_obj.reactions
        option_counts = []

        for option in poll_options:
            for reaction in message_reactions:
                # reaction.emoji could be a str or Emoji object
                if isinstance(reaction.emoji, str):
                    emoji_name = reaction.emoji
                else:
                    emoji_name = reaction.emoji.name

                if option[0] == emoji_name:
                    # Subtract 1 from reaction.count to remove the bot's reaction
                    option_counts.append((option[0], option[1], reaction.count - 1))
                    break

        option_counts.sort(key=lambda x: x[2], reverse=True)

        results_embed = await PollResultsEmbed(poll_id, poll_data["title"], option_counts).build_embed()
        await channel.send(embed=results_embed)
