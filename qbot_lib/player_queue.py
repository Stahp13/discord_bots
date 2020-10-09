from .command_interface import command_interface
from .queue_config import queue_config
import discord

class player_queue:
    def __init__(self, bot):
        self.bot = bot
        self.config = queue_config(bot)

    def get_queue(self, channel):
        return self.bot.get_channel_temp_data(channel).setdefault('queue', dict())
    
    async def check_full(self, channel):
        current_queue = self.get_queue(channel)
        if len(current_queue) == self.config.get_queue_size(channel):
            content = 'players:'+''.join(f' {user.mention}' for _, user in current_queue.items())
            embed = discord.Embed(title=f'Queue has filled up!', color=discord.Colour.orange())
            await channel.send(content = content, embed = embed)
            if self.config.get_queue_reset(channel):
                current_queue.clear()

    async def add_player(self, channel, member):
        self.get_queue(channel)[member.id] = member
        await self.check_full(channel)

    async def remove_player(self, channel, member):
        self.get_queue(channel).pop(member.id, None)