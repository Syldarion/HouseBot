from .customembed import CustomEmbed, CustomEmbedField
from utils.colorgen import discord_color_hsv, get_random_hue
from polls.consts import POLL_OPTION_EMOJIS


class PollEmbed(CustomEmbed):
    def __init__(self, poll_id, poll_title, poll_creator, options_list):
        super(PollEmbed, self).__init__()
        self.poll_id = poll_id
        self.poll_title = poll_title
        self.poll_creator = poll_creator
        self.poll_options = options_list

    async def build_embed(self):
        self.title = self.poll_title
        self.author_text = self.poll_creator.name
        self.author_icon_url = self.poll_creator.avatar_url
        self.description = self.build_poll_description()
        self.color = get_random_hue()
        self.footer_text = f"Poll ID [{self.poll_id}]"

        return await super(PollEmbed, self).build_embed()

    def build_poll_description(self):
        description_str = ""
        for i in range(len(self.poll_options)):
            description_str += f"{POLL_OPTION_EMOJIS[i]} {self.poll_options[i]}\n"
        return description_str
