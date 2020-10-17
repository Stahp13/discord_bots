from .command_interface import command_interface
from .sq_show import sq_show
from .player_queue import player_queue
import discord

class sq_empty:
    def __init__(self, bot):
        self.bot = bot
        self.queue = player_queue(bot)
        self.queue_display = sq_show(bot)
    async def run(self, message) -> None:
        self.queue.get_queue(message.channel).clear()
        await self.queue_display.run(message)
    def help(self) -> discord.Embed:
        embed = discord.Embed(title='help', color=discord.Colour.orange())
        content = """This command is used to remove all users from the queue. This command requires queue bot elevated privileges.
        """
        embed.add_field(name=f'syntax: sq!empty', value=content, inline=False)
        return embed
    def short_help(self) -> str:
        return 'removes all players from queue'
    def name(self) -> str:
        return 'sq!empty'
    def requires_su(self) -> bool:
        return False
    def requires_admin(self) -> bool:
        return True
