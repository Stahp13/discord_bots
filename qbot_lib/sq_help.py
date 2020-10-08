from .command_interface import command_interface
import discord

class sq_help:
    def __init__(self, bot):
        self.bot = bot
    async def run(self, message) -> None:
        embed = discord.Embed(title='help', color=discord.Colour.orange())
        content = u'' + '\n'.join([f'{command.name()}: ' + command.short_help() for command in self.bot.commands.values() if not command.requires_su()])
        content = content.replace(' ', '\u0020')
        embed.add_field(name=f'Command list:', value=content, inline=False)
        await message.channel.send(embed=embed)
    def help(self) -> discord.Embed:
        pass
    def short_help(self) -> str:
        return 'displays this message'
    def name(self) -> str:
        return 'sq!help'
    def requires_su(self) -> bool:
        return False