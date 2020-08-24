import sys
import discord
import os
from discord_bot import discord_bot

queue_size = 8

__location__ = os.path.dirname(os.path.abspath(__file__))
__data_path__ = os.path.join(__location__, 'data', 'QBot')

if len(sys.argv) == 1:
    print('Too few arguments for QBot, missing discord bot token!')
elif len(sys.argv) > 2:
    print('Too many command line arguments, required just one: discord bot token!')

TOKEN = sys.argv[1]

class QBot(discord_bot):
    def __init__(self):
        discord_bot.__init__(self, __data_path__)
    
    def get_queue(self, channel):
        return self.get_channel_data(channel.guild.id, channel.id).setdefault('queue', dict())

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

    async def queue_logic(self, channel):
        current_queue = self.get_queue(channel)
        await self.check_full(channel)
        await self.queue_show(channel)
        
            
    def queue_remove(self, channel, author, mentions):
        current_queue = self.get_queue(channel)
        if author.permissions_in(channel).kick_members:
            for member in mentions:
                current_queue.pop(member.id, None)

    async def queue_add(self, channel, author, mentions):
        current_queue = self.get_queue(channel)
        if author.permissions_in(channel).kick_members:
            for member in mentions:
                current_queue[member.id] = member
                await self.check_full(channel)
    
    async def on_message(self, message):
        if message.author == self.user:
            return
        channel = message.channel
        message_lowercase = message.content.lower()

        if message_lowercase == 'sq!help':
            await message.channel.send(embed=self.help_embed())
        elif message_lowercase == "sq!quit":
            await self.close()
        elif message_lowercase == 'sq!join':
            self.get_queue(channel)[message.author.id] = message.author
            await self.queue_logic(message.channel)
        elif message_lowercase == 'sq!leave':
            self.get_queue(channel).pop(message.author.id, None)
            await self.queue_logic(message.channel)
        elif message_lowercase == 'sq!show' or message_lowercase == 'sq!list' or message_lowercase == 'sq!view':
            self.get_queue(channel)
            await self.queue_show(message.channel)
        elif message_lowercase == 'sq!empty':
            if message.author.permissions_in(message.channel).kick_members:
                self.get_queue(channel).clear()
                await self.queue_show(message.channel)
            else:
                await self.temporary_message(message.channel, f'{message.author.mention} "{message.content}": You don\'t have permissions to execute that command')
        elif message_lowercase.startswith('sq!remove'):
            if message.author.permissions_in(message.channel).kick_members:
                self.queue_remove(message.channel, message.author, message.mentions)
                await self.queue_show(message.channel)
            else:
                await self.temporary_message(message.channel, f'{message.author.mention} "{message.content}": You don\'t have permissions to execute that command')
        elif message_lowercase.startswith('sq!add'):
            if message.author.permissions_in(message.channel).kick_members:
                await self.queue_add(message.channel, message.author, message.mentions)
                await self.queue_show(message.channel)
            else:
                await self.temporary_message(message.channel, f'{message.author.mention} "{message.content}": You don\'t have permissions to execute that command')
        elif message_lowercase.startswith('sq!'):
            await self.temporary_message(message.channel, f'{message.author.mention} "{message.content}": Unknown command, type sq!help for help')
            

client = QBot()
client.run(TOKEN)