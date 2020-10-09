from .command_interface import command_interface
from .queue_config import queue_config
from .player_queue import player_queue
import discord

class sq_show:
    def __init__(self, bot):
        self.bot = bot
        self.queue = player_queue(bot)
        self.config = queue_config(bot)
    async def run(self, message) -> None:
        current_queue = self.queue.get_queue(message.channel)
        embed = discord.Embed(title=f'Queue {len(current_queue)}/{self.config.get_queue_size(message.channel)}', color=discord.Colour.orange())
        content=''
        if len(current_queue) == 0:
            embed.add_field(name='players:', value='Queue is empty')
        else:
            embed_content = ''.join(f'{idx+1}. {user[1].mention}\n' for idx, user in enumerate(current_queue.items()))
            embed.add_field(name='players:', value=embed_content)
        await self.bot.temporary_message(message.channel, content = content, embed=embed)
    def help(self) -> discord.Embed:
        pass
    def short_help(self) -> str:
        return 'shows current queue'
    def name(self) -> str:
        return 'sq!show'
    def requires_su(self) -> bool:
        return False
    def requires_admin(self) -> bool:
        return False