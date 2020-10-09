from .command_interface import command_interface
from .notification_config import notification_config
import discord

class sq_notify:
    def __init__(self, bot):
        self.bot = bot
        self.config = queue_config(bot)
    async def run(self, message) -> None:
        split_message = message.content.split(' ')
        if len(split_message) != 2:
            await message.channel.send(content = f'{message.author.mention} "{message.content}": exactly one argument is expected! Got: {len(split_message)-1}')
            return
        integer_value = None
        try:
            integer_value = int(split_message[1])
        except:
            await message.channel.send(content = f'{message.author.mention} "{message.content}": Could not convert "{split_message[1]}" to integer!')
            return
        self.config.set_notification_config(message.channel, message.author, +integer_value)
        await message.channel.send(content = f'{message.author.mention}: succesfully set notify threshold to {integer_value}')
    def help(self) -> discord.Embed:
        pass
    def short_help(self) -> str:
        return 'Sets notification settings for user'
    def name(self) -> str:
        return 'sq!notify'
    def requires_su(self) -> bool:
        return False
    def requires_admin(self) -> bool:
        return False