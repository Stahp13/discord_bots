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
        queue_size = self.config.get_queue_size(message.channel)
        embed = discord.Embed(title=f'Queue {len(current_queue)}/{queue_size}', color=discord.Colour.orange())
        content=''
        if len(current_queue) == 0:
            embed.add_field(name='Players:', value='Queue is empty')
        else:
            user_ids = [user_id for user_id in current_queue.keys()]
            embed_content = ''.join(f'{idx+1}. {user.mention}\n' for idx, user in enumerate([current_queue[user_id] for user_id in user_ids[:queue_size]]))
            embed.add_field(name='Players:', value=embed_content)
            if len(current_queue) > queue_size:
                embed_content = ''.join(f'{idx+1}. {user.mention}\n' for idx, user in enumerate([current_queue[user_id] for user_id in user_ids[queue_size:]]))
                embed.add_field(name='Waitlist:', value=embed_content)
        await self.bot.temporary_message(message.channel, content = content, embed=embed)
    def help(self) -> discord.Embed:
        embed = discord.Embed(title='help', color=discord.Colour.orange())
        content = """This command is used to display the queue.
        """
        embed.add_field(name=f'syntax: sq!show', value=content, inline=False)
        return embed
    def short_help(self) -> str:
        return 'display queue'
    def name(self) -> str:
        return 'sq!show'
    def requires_su(self) -> bool:
        return False
    def requires_admin(self) -> bool:
        return False
