from .command_interface import command_interface
import discord

class sq_remove_admin_role:
    def __init__(self, bot):
        self.bot = bot
    async def run(self, message) -> None:
        split_message = message.content.split(' ')
        if len(split_message) != 2:
            await message.channel.send(content = f'{message.author.mention} "{message.content}": exactly one argument is expected! Got: {len(split_message)-1}')
        role = split_message[1]
        guild = message.channel.guild
        su_roles = self.bot.get_admin_roles(guild)
        if role in su_roles:
            su_roles.remove(role)
            self.bot.update_guild_config(guild)
            await message.channel.send(content = f'{message.author.mention} "{message.content}": "{role}" removed from administrators group!')
        else:
            await message.channel.send(content = f'{message.author.mention} "{message.content}": "{role}" is not in admin roles!')
    def help(self) -> discord.Embed:
        embed = discord.Embed(title='help', color=discord.Colour.orange())
        content = """example: "sq!remove_admin_role Mods"
        This command is used to revoke Queue Bot admin permissions from a role/rank within the Discord server. Discord server administrators by default have super user permissions.
        """
        embed.add_field(name=f'syntax: sq!remove_admin_role <role>', value=content, inline=False)
        return embed
    def short_help(self) -> str:
        return 'revoke elevated privileges'
    def name(self) -> str:
        return 'sq!remove_admin_role'
    def requires_su(self) -> bool:
        return True
    def requires_admin(self) -> bool:
        return True
