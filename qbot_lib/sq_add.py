from .command_interface import command_interface
import discord

class sq_add:
    def __init__(self, bot):
        self.bot = bot
    async def run(self, message) -> None:
        channel = message.channel
        current_queue = self.bot.get_queue(channel)
        for member in message.mentions:
            current_queue[member.id] = member
            await self.bot.check_full(channel)
        await self.bot.queue_show(channel)
    def help(self) -> discord.Embed:
        pass
    def short_help(self) -> str:
        return 'adds mentioned players to the queue'
    def name(self) -> str:
        return 'sq!add'
    def requires_su(self) -> bool:
        return True