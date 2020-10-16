import sys
import discord
import os
from discord_bot import discord_bot
from qbot_lib.sq_help import sq_help
from qbot_lib.sq_show import sq_show
from qbot_lib.sq_join import sq_join
from qbot_lib.sq_leave import sq_leave
from qbot_lib.sq_add import sq_add
from qbot_lib.sq_remove import sq_remove
from qbot_lib.sq_empty import sq_empty
from qbot_lib.sq_add_admin_role import sq_add_admin_role
from qbot_lib.sq_remove_admin_role import sq_remove_admin_role
from qbot_lib.sq_list_admin_roles import sq_list_admin_roles
from qbot_lib.sq_set_channel import sq_set_channel
from qbot_lib.sq_get_channel import sq_get_channel
from qbot_lib.sq_scramble import sq_scramble
from qbot_lib.sq_notify import sq_notify
#from qbot_lib.sq_notify import 
#from qbot_lib.sq_help import Sq_add

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
            'sq!show':sq_show(self),
            'sq!join':sq_join(self),
            'sq!leave':sq_leave(self),
            'sq!add':sq_add(self),
            'sq!remove':sq_remove(self),
            'sq!empty':sq_empty(self),
            'sq!add_admin_role':sq_add_admin_role(self),
            'sq!remove_admin_role':sq_remove_admin_role(self),
            'sq!list_admin_roles':sq_list_admin_roles(self),
            'sq!set_channel':sq_set_channel(self),
            'sq!get_channel':sq_get_channel(self),
            'sq!scramble':sq_scramble(self),
            'sq!notify':sq_notify(self)
        }

    def get_admin_roles(self, guild):
        return self.get_guild_config(guild).setdefault('admin_roles', [])

    def member_is_su(self, member):
        return member.guild_permissions == discord.Permissions.all()
    
    def member_is_admin(self, member):
        if self.member_is_su(member):
            return True
        for role in member.roles:
            if role.name in self.get_admin_roles(member.guild):
                return True
        return False

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
            if (command.requires_su() and not self.member_is_su(message.author)) or (command.requires_admin() and not self.member_is_admin(message.author)):
                await message.channel.send(content = f'{message.author.mention} "{message.content}": User does not have permissions to do that!')
                return
            await command.run(message)
            return

        elif message_lowercase == "sq!quit" and self.member_is_su(message.author):
            await self.close()
        elif message_lowercase.startswith('sq!'):
            await message.channel.send(content = f'{message.author.mention} "{message.content}": Unknown command, type sq!help for help')
            

client = q_bot()
client.run(TOKEN)