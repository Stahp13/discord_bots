from .command_interface import command_interface
from .queue_config import queue_config
import discord

class sq_notify:
    def __init__(self, bot):
        self.bot = bot
        self.config = queue_config(bot)
        self.ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
    async def run(self, message) -> None:
        split_message = message.content.split(' ')
        if len(split_message) == 2:
            if(split_message[1] == 'stop'):
                self.config.set_notification_config(message.channel, message.author, 0, 0)
                await message.channel.send(content = f'{message.author.mention} Queue Bot will not send you notifications in DM')
                return
            else:
                await message.channel.send(content = f'{message.author.mention} Unknown command or to few arguments, type sq!help notify for details')
                return
        if len(split_message) != 3:
            await message.channel.send(content = f'{message.author.mention} "{message.content}": one or two argument are expected! Got: {len(split_message)-1}')
            return
        
        number_of_players = None
        minimum_delay = None
        try:
            number_of_players = int(split_message[1])
        except:
            await message.channel.send(content = f'{message.author.mention} "{message.content}": Could not convert "{split_message[1]}" to integer!')
            return
        try:
            minimum_delay = int(split_message[2])
        except:
            await message.channel.send(content = f'{message.author.mention} "{message.content}": Could not convert "{split_message[2]}" to integer!')
            return
        
        self.config.set_notification_config(message.channel, message.author, number_of_players, minimum_delay)
        content = ''
        if number_of_players <= 0 or number_of_players > self.config.get_queue_size(message.channel):
            content = f'{message.author.mention} Queue Bot will not send you notifications in DM'
        else:
            content = f'{message.author.mention}: Queue Bot will now notify you via private message whenever the following conditions are satisfied:\n'
            content += f'1) {self.ordinal(number_of_players)} players are in the queue\n'
            content += f'2) Queue Bot has not sent you a notification from this channel in past {minimum_delay} minute(s)\n'
            content += f'3) You are not in the queue'
        await message.channel.send(content = content)
    def help(self) -> discord.Embed:
        embed = discord.Embed(title='help', color=discord.Colour.orange())
        content = """example: "sq!notify 7 60" or "sq!notify 0 0"
        This command expects the arguments of the queue size you wish to be notified of followed by the time threshold you wish to be notified (i.e. enter 240 if you only want to receive messages every four hours). To disable notifications, enter "0" for both arguments.
        This command is used to subscribe to the queue bot private message feature that will DM users who wish to receive notifications when the queue reaches the desired number of users. Direct messages must be enabled by the user for the server the bot is hosted on.
        """
        embed.add_field(name=f'syntax: sq!notify <queue_size> <interval_minutes>', value=content, inline=False)
        return embed
    def short_help(self) -> str:
        return 'notifies players when the queue reaches selected capacity'
    def name(self) -> str:
        return 'sq!notify'
    def requires_su(self) -> bool:
        return False
    def requires_admin(self) -> bool:
        return False
