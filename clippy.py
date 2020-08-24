import sys
import discord
import json
import os
from discord_bot import discord_bot

__location__ = os.path.dirname(os.path.abspath(__file__))
__data_path__ = os.path.join(__location__, 'data', 'Clippy')

if len(sys.argv) == 1:
    print('Too few arguments for QBot, missing discord bot token!')
elif len(sys.argv) > 2:
    print('Too many command line arguments, required just one: discord bot token!')

TOKEN = sys.argv[1]

class Clippy(discord_bot):
    def __init__(self):
        discord_bot.__init__(self, __data_path__)
        
    def get_clip(self, channel):
        return self.get_channel_config(channel.guild.id, channel.id).get('clipped_message', '')

    def set_clip(self, channel, clipped_message):
        self.get_channel_config(channel.guild.id, channel.id)['clipped_message'] = clipped_message
        self.update_channel_config(channel)

    async def clip(self, channel):
        my_message = self.get_clip(channel)
        if my_message != '':
            await self.temporary_message(channel, my_message)

    async def on_message(self, message):
        if message.author == self.user:
            return
        self.global_lock.acquire()
        message_lowercase = message.content.lower()

        if(message_lowercase.startswith('!clip ')):
            if message.author.permissions_in(message.channel).kick_members:
                self.set_clip(message.channel, message.content[6:])
                await self.clip(message.channel)
            else:
                await message.channel.send(content = f'{message.author.mention} "{message.content}": You don\'t have permissions to execute that command', embed = None)
                await self.clip(message.channel)
        elif message_lowercase == "!clip_stop" or message_lowercase == "!clipstop":
            self.set_clip(message.channel, '')
        elif message_lowercase == "!clip_quit":
            await self.close()
        else:
            await self.clip(message.channel)
        self.global_lock.release()
            

client = Clippy()
client.run(TOKEN)