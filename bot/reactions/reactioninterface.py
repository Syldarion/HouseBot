import discord

from .reactioncontext import ReactionContext


class ReactionInterface(object):
    def __init__(self):
        self._add_reaction_handlers = {

        }

        self._remove_reaction_handlers = {

        }

    async def handle_reaction_add(self, reaction_payload: discord.RawReactionActionEvent):
        context = ReactionContext(reaction_payload)
        await self._add_reaction_handlers[context.emoji_name].handle_reaction(context)

    async def handle_reaction_remove(self, reaction_payload: discord.RawReactionActionEvent):
        context = ReactionContext(reaction_payload)
        await self._remove_reaction_handlers[context.emoji_name].handle_reaction(context)
