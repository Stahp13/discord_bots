from .command_interface import command_interface
from .queue_config import queue_config
import discord

class sq_get_channel:
    def __init__(self, bot):
        self.bot = bot
        self.config = queue_config(bot)
    async def run(self, message) -> None:
        split_message = message.content.split(' ')
        if len(split_message) != 2:
            await message.channel.send(content = f'{message.author.mention} "{message.content}": exactly one argument is expected! Got: {len(split_message)-1}')
            return
        config_name = split_message[1]
        if config_name in self.config.config_keys.keys():
            await message.channel.send(content = f'{config_name} = "{self.bot.get_channel_config(message.channel).get(config_name, "default")}"')
        else:
            await message.channel.send(content = f'{message.author.mention} "{message.content}": "{config_name}" is not a recognized config')
    def help(self) -> discord.Embed:
        embed = discord.Embed(title='help', color=discord.Colour.orange())
        content = """example: "sq!get_channel queue_size"
        This command is used to obtain the parameters assigned to the "queue_size" and "queue_reset" attributes.
        """
        embed.add_field(name=f'syntax: sq!get_channel <attribute>', value=content, inline=False)
        return embed
    def short_help(self) -> str:
        return 'gets value of given config field for channel'
    def name(self) -> str:
        return 'sq!get_channel'
    def requires_su(self) -> bool:
        return True
    def requires_admin(self) -> bool:
        return True
