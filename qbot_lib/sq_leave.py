from .command_interface import command_interface
from .player_queue import player_queue
from .sq_show import sq_show
import discord

class sq_leave:
    def __init__(self, bot):
        self.bot = bot
        self.queue = player_queue(bot)
        self.queue_display = sq_show(bot)
    async def run(self, message) -> None:
        await self.queue.remove_player(message.channel, message.author)
        await self.queue_display.run(message)
    def help(self) -> discord.Embed:
        embed = discord.Embed(title='help', color=discord.Colour.orange())
        content = """This command is used by users to leave the queue.
        """
        embed.add_field(name=f'syntax: sq!leave', value=content, inline=False)
        return embed
    def short_help(self) -> str:
        return 'Removes message author from the queue'
    def name(self) -> str:
        return 'sq!leave'
    def requires_su(self) -> bool:
        return False
    def requires_admin(self) -> bool:
        return False
