from .command_interface import command_interface
import discord

class sq_empty:
    def __init__(self, bot):
        self.bot = bot
    async def run(self, message) -> None:
        self.bot.get_queue(message.channel).clear()
        await self.bot.queue_show(message.channel)
    def help(self) -> discord.Embed:
        pass
    def short_help(self) -> str:
        return 'Removes all players from the queue'
    def name(self) -> str:
        return 'sq!empty'
    def requires_su(self) -> bool:
        return True