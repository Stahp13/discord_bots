from .command_interface import command_interface
from .queue_config import queue_config
import discord

class sq_set_channel:
    def __init__(self, bot):
        self.bot = bot
        self.config = queue_config(bot)
    async def run(self, message) -> None:
        split_message = message.content.split(' ')
        if len(split_message) != 3:
            await message.channel.send(content = f'{message.author.mention} "{message.content}": exactly two arguments are expected! Got: {len(split_message)-1}')
            return
        config_name = split_message[1]
        config_value = split_message[2]
        if config_name in self.config.config_keys.keys():
            self.bot.get_channel_config(message.channel)[config_name] = self.config.config_keys[config_name](config_value)
            self.bot.update_channel_config(message.channel)
        else:
            await message.channel.send(content = f'{message.author.mention} "{message.content}": "{config_name}" is not a recognized config')
    def help(self) -> discord.Embed:
        pass
    def short_help(self) -> str:
        return 'sets value of given config field for channel'
    def name(self) -> str:
        return 'sq!set_channel'
    def requires_su(self) -> bool:
        return True
    def requires_admin(self) -> bool:
        return True