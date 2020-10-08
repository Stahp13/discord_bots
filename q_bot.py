import sys
import discord
import os
from discord_bot import discord_bot
from qbot_lib.sq_help import sq_help
from qbot_lib.sq_join import sq_join
from qbot_lib.sq_leave import sq_leave
from qbot_lib.sq_add import sq_add
from qbot_lib.sq_remove import sq_remove
from qbot_lib.sq_empty import sq_empty
#from qbot_lib.sq_notify import 
#from qbot_lib.sq_help import Sq_add

queue_size = 8

__location__ = os.path.dirname(os.path.abspath(__file__))
__data_path__ = os.path.join(__location__, 'data', 'QBot')

if len(sys.argv) == 1:
    print('Too few arguments for QBot, missing discord bot token!')
elif len(sys.argv) > 2:
    print('Too many command line arguments, required just one: discord bot token!')

TOKEN = sys.argv[1]

class q_bot(discord_bot):
    def __init__(self):
        discord_bot.__init__(self, __data_path__)
        self.commands = {
            'sq!help':sq_help(self),
            'sq!join':sq_join(self),
            'sq!leave':sq_leave(self),
            'sq!add':sq_add(self),
            'sq!remove':sq_remove(self),
            'sq!empty':sq_empty(self)
        }

    def get_su_roles(self, guild):
        return self.get_guild_config(guild).setdefault('su_roles', [])

    def add_su_role(self, guild, role):
        su_roles = self.get_su_roles(guild)
        if not role in su_roles:
            su_roles.append(role)
            self.update_guild_config(guild)

    def member_is_su(self, member):
        pass
        #return member.roles in
    
    def get_queue(self, channel):
        return self.get_channel_temp_data(channel).setdefault('queue', dict())

    def help_embed(self):
        embed = discord.Embed(title='help', color=discord.Colour.orange())
        content = """sq!join:   joins queue
                     sq!leave:  leave queue
                     sq!show:   shows players in queue, aliases: sq!list, sq!view
                     sq!remove: removes mentioned players from the queue"""
        embed.add_field(name=f'commands:', value=content, inline=False)
        return embed
    
    async def queue_show(self, channel):
        current_queue = self.get_queue(channel)
        embed = discord.Embed(title=f'Queue {len(current_queue)}/{queue_size}', color=discord.Colour.orange())
        content=''
        if len(current_queue) == 0:
            embed.add_field(name='players:', value='Queue is empty')
        else:
            embed_content = ''.join(f'{idx+1}. {user[1].mention}\n' for idx, user in enumerate(current_queue.items()))
            embed.add_field(name='players:', value=embed_content)
        await self.temporary_message(channel, content = content, embed=embed)
    
    async def check_full(self, channel):
        current_queue = self.get_queue(channel)
        if len(current_queue) == queue_size:
            content = 'players:'+''.join(f' {user.mention}' for _, user in current_queue.items())
            embed = discord.Embed(title=f'Queue has filled up!', color=discord.Colour.orange())
            await channel.send(content = content, embed = embed)
            current_queue.clear()

    async def on_message(self, message):
        if message.author == self.user:
            return
        channel = message.channel
        message_lowercase = message.content.lower()

        if not message_lowercase.startswith('sq!'):
            return

        command_str = message_lowercase.split(' ')[0]
        command = self.commands.get(command_str, None)
        if command is not None:
            await command.run(message)
            return

        elif message_lowercase == "sq!quit":
            await self.close()
        elif message_lowercase == 'sq!show' or message_lowercase == 'sq!list' or message_lowercase == 'sq!view':
            self.get_queue(channel)
            await self.queue_show(message.channel)
        elif message_lowercase.startswith('sq!'):
            await message.channel.send(content = f'{message.author.mention} "{message.content}": Unknown command, type sq!help for help')
            

client = q_bot()
client.run(TOKEN)