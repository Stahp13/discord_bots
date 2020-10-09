from .command_interface import command_interface
import discord

class sq_help:
    def __init__(self, bot):
        self.bot = bot
    async def run(self, message) -> None:
        split_message = message.content.split(' ')
        if len(split_message) == 1:
            await self.__help_1_arg(message)
        elif len(split_message) == 2:
            await self.__help_2_arg(message, split_message[1])
        else:
            await message.channel.send(content = f'{message.author.mention} "{message.content}": too many arguments for command sq!help!')
    async def __help_1_arg(self, message):
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
    async def __help_2_arg(self, message, command):
        sq_command = command
        if not command.startswith('sq!'):
            sq_command = 'sq!' + command
        if sq_command not in self.bot.commands:
            await message.channel.send(content = f'{message.author.mention} "{message.content}": unknown command')
        embed = self.bot.commands[sq_command].help()
        if embed is None:
            await message.channel.send(content = f'detailed help for "{command}" is not provided')
        else:
            await message.channel.send(embed=embed)
    def help(self) -> discord.Embed:
        embed = discord.Embed(title='help', color=discord.Colour.orange())
        content = """syntax: sq!help [command]
        When used without additional arguments displays list of commands.
        When "command" argument is passed displays detailed info about given command
        """
        embed.add_field(name=f'Usage:', value=content, inline=False)
        return embed
    def short_help(self) -> str:
        return 'type sq!help <command> for extra info'
    def name(self) -> str:
        return 'sq!help'
    def requires_su(self) -> bool:
        return False
    def requires_admin(self) -> bool:
        return False