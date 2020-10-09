from .command_interface import command_interface
import discord

class sq_help:
    def __init__(self, bot):
        self.bot = bot
    async def run(self, message) -> None:
        author = message.author
        embed = discord.Embed(title='help', color=discord.Colour.orange())
        content = '\n'.join([f'{command.name()}: ' + command.short_help() for command in self.bot.commands.values() if not command.requires_su() and not command.requires_admin()])
        embed.add_field(name=f'Command list:', value=content, inline=False)
        if self.bot.member_is_admin(author):
            content = '\n'.join([f'{command.name()}: ' + command.short_help() for command in self.bot.commands.values() if not command.requires_su() and command.requires_admin()])
            embed.add_field(name=f'Admin command list:', value=content, inline=False)
        if self.bot.member_is_su(author):
            content = '\n'.join([f'{command.name()}: ' + command.short_help() for command in self.bot.commands.values() if command.requires_su()])
            embed.add_field(name=f'Super user command list:', value=content, inline=False)
        await message.channel.send(embed=embed)
    def help(self) -> discord.Embed:
        pass
    def short_help(self) -> str:
        return 'displays this message'
    def name(self) -> str:
        return 'sq!help'
    def requires_su(self) -> bool:
        return False
    def requires_admin(self) -> bool:
        return False