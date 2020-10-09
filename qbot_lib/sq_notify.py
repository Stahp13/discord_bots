from .command_interface import command_interface
from .notification_config import notification_config
import discord

class sq_notify:
    def __init__(self, bot):
        self.bot = bot
        self.config = queue_config(bot)
    async def run(self, message) -> None:
        pass
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