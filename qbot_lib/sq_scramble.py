from .command_interface import command_interface
from .player_queue import player_queue
from .sq_show import sq_show
import discord
import random

class sq_scramble:
    def __init__(self, bot):
        self.bot = bot
        self.queue = player_queue(bot)
    async def run(self, message) -> None:
        queue = self.queue.get_queue(message.channel)
        shuffled_indices = [i for i in range(len(queue))]
        random.shuffle(shuffled_indices)
        half_size = int(self.queue.config.get_queue_size(message.channel)/2)
        q_values = [v for v in queue.values()]
        team_A = 'team A:'+''.join(f' {q_values[user_idx].mention}' for user_idx in shuffled_indices[:half_size])
        team_B = 'team B:'+''.join(f' {q_values[user_idx].mention}' for user_idx in shuffled_indices[half_size:half_size*2])
        await message.channel.send(content = f'{team_A}\n{team_B}')
    def help(self) -> discord.Embed:
        embed = discord.Embed(title='help', color=discord.Colour.orange())
        content = """This command is used to generate shuffled team compositions.
        """
        embed.add_field(name=f'syntax: sq!scramble', value=content, inline=False)
        return embed
    def short_help(self) -> str:
        return 'shuffles teams'
    def name(self) -> str:
        return 'sq!scramble'
    def requires_su(self) -> bool:
        return False
    def requires_admin(self) -> bool:
        return False
