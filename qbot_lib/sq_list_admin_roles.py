from .command_interface import command_interface
import discord

class sq_list_admin_roles:
    def __init__(self, bot):
        self.bot = bot
    async def run(self, message) -> None:
        guild = message.channel.guild
        embed = discord.Embed(title=f'Admin roles', color=discord.Colour.orange())
        su_roles = self.bot.get_admin_roles(guild)
        if len(su_roles) == 0:
            await message.channel.send(content='There are currently no roles with admin permissions')
        else:
            embed_content = ''.join(su_roles)
            embed.add_field(name='Names:', value=embed_content)
            await message.channel.send(content='', embed=embed)

    def help(self) -> discord.Embed:
        embed = discord.Embed(title='help', color=discord.Colour.orange())
        content = """This command is used to display the roles that have access to queue bot admin features.
        """
        embed.add_field(name=f'syntax: sq!list_admin_roles', value=content, inline=False)
        return embed
    def short_help(self) -> str:
        return 'list roles that have elevated privileges'
    def name(self) -> str:
        return 'sq!list_admin_roles'
    def requires_su(self) -> bool:
        return True
    def requires_admin(self) -> bool:
        return True
