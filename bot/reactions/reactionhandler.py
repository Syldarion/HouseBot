import abc


class ReactionHandler(abc.ABC):
    def __init__(self, name, unicode):
        self.name = name
        self.unicode = unicode

    @abc.abstractmethod
    async def handle_reaction(self, reaction_context):
        pass
