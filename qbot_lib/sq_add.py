from .command_interface import command_interface
from .sq_show import sq_show
from .queue_config import queue_config
from .player_queue import player_queue
import discord

class sq_add:
    def __init__(self, bot):
        self.bot = bot
        self.queue = player_queue(bot)
        self.queue_display = sq_show(bot)
    async def run(self, message) -> None:
        for member in message.mentions:
            await self.queue.add_player(message.channel, member)
        await self.queue_display.run(message)
    def help(self) -> discord.Embed:
        pass
    def short_help(self) -> str:
        return 'adds mentioned players to the queue'
    def name(self) -> str:
        return 'sq!add'
    def requires_su(self) -> bool:
        return False
    def requires_admin(self) -> bool:
        return True