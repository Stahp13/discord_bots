from .command_interface import command_interface
import discord

class sq_join:
    def __init__(self, bot):
        self.bot = bot
    async def run(self, message) -> None:
        channel = message.channel
        self.bot.get_queue(channel)[message.author.id] = message.author
        current_queue = self.bot.get_queue(channel)
        await self.bot.check_full(channel)
        await self.bot.queue_show(channel)
    def help(self) -> discord.Embed:
        pass
    def short_help(self) -> str:
        return 'Adds message author to the queue'
    def name(self) -> str:
        return 'sq!join'
    def requires_su(self) -> bool:
        return False