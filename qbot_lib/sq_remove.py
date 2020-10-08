from .command_interface import command_interface
import discord

class sq_remove:
    def __init__(self, bot):
        self.bot = bot
    async def run(self, message) -> None:
        current_queue = self.bot.get_queue(message.channel)
        for member in message.mentions:
            current_queue.pop(member.id, None)
        await self.bot.queue_show(message.channel)
    def help(self) -> discord.Embed:
        pass
    def short_help(self) -> str:
        return 'adds mentioned players to the queue'
    def name(self) -> str:
        return 'sq!remove'
    def requires_su(self) -> bool:
        return True