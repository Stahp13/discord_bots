from .command_interface import command_interface
from .queue_config import queue_config
import discord
from datetime import datetime

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
    
    def get_last_DM_time(self, channel, member):
        return self.bot.get_channel_data(channel).setdefault('sq_notify_last_message_time', dict()).setdefault(member.id, datetime(2000, 1, 1))

    def update_last_DM_time(self, channel, member):
        self.bot.get_channel_data(channel).setdefault('sq_notify_last_message_time', dict())[member.id] = datetime.now()
        self.bot.update_channel_data(channel)

    async def notify_players(self, channel):
        notification_config = self.config.get_channel_notification_config(channel)
        current_queue = self.get_queue(channel)
        current_queue_size = len(current_queue)
        for user_id, user_config in notification_config.items():
            required_number_of_players, minimum_delay = user_config
            if user_id in current_queue:
                continue
            if current_queue_size == required_number_of_players:
                user = channel.guild.get_member(user_id)
                if user is None:
                    print(f'Warning: could not fetch user: "{user_id}"')
                    continue
                if (datetime.now() - self.get_last_DM_time(channel, user)).total_seconds() > minimum_delay * 60:
                    self.update_last_DM_time(channel, user)
                    try:
                        await user.send(f"Hey! There are {required_number_of_players} players in {channel.guild.name}/{channel.name} queue!")
                    except:
                        await message.channel.send(content = user.mention + ' Could not create a DM, make sure you have DMs enabled')

    async def add_player(self, channel, member):
        queue = self.get_queue(channel)
        if not member.id in queue:
            queue[member.id] = member
            await  self.notify_players(channel)
            await self.check_full(channel)

    async def remove_player(self, channel, member):
        self.get_queue(channel).pop(member.id, None)