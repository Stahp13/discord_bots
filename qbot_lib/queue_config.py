import discord

class queue_config:
    def __init__(self, bot):
        self.bot = bot
        self.config_keys = {'queue_size':int, 'queue_reset':int}
    def get_channel_notification_config(self, channel):
        return self.bot.get_channel_data(channel).setdefault('sq_notify', dict())
    def get_notification_config(self, channel, member):
        return self.bot.get_channel_data(channel).setdefault('sq_notify', dict()).setdefault(member.id, (-1, 30))
    def set_notification_config(self, channel, member, minimum_users, minimum_delay):
        self.bot.get_channel_data(channel).setdefault('sq_notify', dict())[member.id] = (minimum_users, minimum_delay)
        self.bot.update_channel_data(channel)
    def get_queue_size(self, channel):
        return int(self.bot.get_channel_config(channel).setdefault('queue_size', '8'))
    def set_queue_size(self, channel, value):
        self.bot.get_channel_config(channel)['queue_size'] = str(value)
    def get_queue_reset(self, channel):
        return bool(int(self.bot.get_channel_config(channel).setdefault('queue_reset', 1)))
    def set_queue_reset(self, channel, value):
        self.bot.get_channel_config(channel)['queue_size'] = str(int(value))