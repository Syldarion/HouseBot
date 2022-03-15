from .customembed import CustomEmbed
from utils.colorgen import get_random_hue


class PollResultsEmbed(CustomEmbed):
    def __init__(self, poll_id, poll_title, results):
        super(PollResultsEmbed, self).__init__()
        self.poll_id = poll_id
        self.poll_title = poll_title
        self.results = results

    async def build_embed(self):
        self.title = f"'{self.poll_title}' results"
        self.description = "\n".join([f"{opt[0]} {opt[1]} [{opt[2]} vote(s)]" for opt in self.results])
        self.color = get_random_hue()
        self.footer_text = f"Poll ID [{self.poll_id}]"

        return await super(PollResultsEmbed, self).build_embed()
