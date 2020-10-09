import discord

class command_interface:
    async def run(self, message) -> None:
        pass
    def help(self) -> discord.Embed:
        pass
    def short_help(self) -> str:
        pass
    def name(self) -> str:
        pass
    def requires_su(self) -> bool:
        pass
    def requires_admin(self) -> bool:
        pass