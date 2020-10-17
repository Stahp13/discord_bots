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
        embed = discord.Embed(title='help', color=discord.Colour.orange())
        content = """example: "sq!add @JohnDoe @JaneDoe"
        This command is used to add a user to the queue. This command accepts multiple arguments. This command requires queue bot elevated privileges.
        """
        embed.add_field(name=f'syntax: sq!add <user>', value=content, inline=False)
        return embed
    def short_help(self) -> str:
        return 'adds mentioned players to the queue'
    def name(self) -> str:
        return 'sq!add'
    def requires_su(self) -> bool:
        return False
    def requires_admin(self) -> bool:
        return True
