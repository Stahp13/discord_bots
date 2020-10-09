from .command_interface import command_interface
from .player_queue import player_queue
from .sq_show import sq_show
import discord

class sq_join:
    def __init__(self, bot):
        self.bot = bot
        self.queue = player_queue(bot)
        self.queue_display = sq_show(bot)
    async def run(self, message) -> None:
        await self.queue.add_player(message.channel, message.author)
        await self.queue_display.run(message)
    def help(self) -> discord.Embed:
        pass
    def short_help(self) -> str:
        return 'Adds message author to the queue'
    def name(self) -> str:
        return 'sq!join'
    def requires_su(self) -> bool:
        return False
    def requires_admin(self) -> bool:
        return False