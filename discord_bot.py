import sys
import discord
import threading
import pickle
import json
import os
from pathlib import Path

def create_dict():
    return dict()

class discord_bot(discord.Client):
    def __init__(self, data_directory):
        discord.Client.__init__(self)
        # serializable data
        self.guilds_data = dict()
        # locks
        self.guild_locks = dict()
        self.channel_locks = dict()
        self.global_lock = threading.RLock()    
        # defaults
        self.data_directory = data_directory
        self.default_guild_config = create_dict
        self.default_guild_data = create_dict
        self.default_channel_config = create_dict
        self.default_channel_data = create_dict
    
    def __get_guild(self, guild_id):
        with self.global_lock:
            return self.guilds_data.setdefault(guild_id, dict())

    def get_guild_config_by_id(self, guild_id):
        with self.global_lock:
            return self.__get_guild(guild_id).setdefault("config", self.default_guild_config())

    def get_guild_config(self, guild):
        return self.get_guild_config_by_id(guild.id)

    def get_guild_data_by_id(self, guild_id):
        with self.global_lock:
            return self.__get_guild(guild_id).setdefault("data", self.default_guild_data())

    def get_guild_data(self, guild):
        return self.get_guild_data_by_id(guild.id)

    def get_guild_temp_data_by_id(self, guild_id):
        with self.global_lock:
            return self.__get_guild(guild_id).setdefault("temp_data", dict())

    def get_guild_temp_data(self, guild):
        return self.get_guild_temp_data_by_id(guild.id)

    def get_guild_config_file(self, guild_id):
        return os.path.join(self.data_directory, "guilds", str(guild_id), "config.json")

    def get_guild_data_file(self, guild_id):
        return os.path.join(self.data_directory, "guilds", str(guild_id), "data.p")

    def update_guild_config(self, guild):
        guild_config = self.get_guild_config(guild)
        guild_config_file = self.get_guild_config_file(guild.id)
        Path(os.path.dirname(guild_config_file)).mkdir(parents=True, exist_ok=True)
        with open(guild_config_file, 'w') as f:
            f.write(json.dumps(guild_config))

    def update_guild_data(self, guild_id):
        guild_data = self.get_guild_data(guild_id)
        guild_data_file = self.get_guild_data_file(guild_id)
        Path(os.path.dirname(guild_data_file)).mkdir(parents=True, exist_ok=True)
        pickle.dump(guild_data, open(guild_data_file, "wb"))

    def get_guild_lock(self, guild_id):
        with self.global_lock:
            return self.guild_locks.setdefault(guild_id, threading.RLock())

    def __get_channel(self, guild_id, channel_id):
        with self.global_lock:
            return self.__get_guild(guild_id).setdefault("channels", dict()).setdefault(channel_id, dict())

    def get_channel_config_by_id(self, guild_id, channel_id):
        with self.global_lock:
            return self.__get_channel(guild_id, channel_id).setdefault("config", self.default_channel_config())
    
    def get_channel_config(self, channel):
        return self.get_channel_config_by_id(channel.guild.id, channel.id)

    def get_channel_data_by_id(self, guild_id, channel_id):
        with self.global_lock:
            return self.__get_channel(guild_id, channel_id).setdefault("data", self.default_channel_data())

    def get_channel_data(self, channel):
        return self.get_channel_data_by_id(channel.guild.id, channel.id)

    def get_channel_temp_data_by_id(self, guild_id, channel_id):
        with self.global_lock:
            return self.__get_channel(guild_id, channel_id).setdefault("temp_data", dict())

    def get_channel_temp_data(self, channel):
        return self.get_channel_temp_data_by_id(channel.guild.id, channel.id)

    def update_channel_config(self, channel):
        channel_config = self.get_channel_config(channel)
        channel_config_file = self.get_channel_config_file(channel.guild.id, channel.id)
        Path(os.path.dirname(channel_config_file)).mkdir(parents=True, exist_ok=True)
        with open(channel_config_file, 'w') as f:
            f.write(json.dumps(channel_config))

    def update_channel_data(self, channel):
        channel_data = self.get_channel_data_by_id(channel.guild.id, channel.id)
        channel_data_file = self.get_channel_data_file(channel.guild.id, channel.id)
        Path(os.path.dirname(channel_data_file)).mkdir(parents=True, exist_ok=True)
        pickle.dump(channel_data, open(channel_data_file, "wb"))

    def get_channel_config_file(self, guild_id, channel_id):
        return os.path.join(self.data_directory, "guilds", str(guild_id), "channels", str(channel_id), "config.json")

    def get_channel_data_file(self, guild_id, channel_id):
        return os.path.join(self.data_directory, "guilds", str(guild_id), "channels", str(channel_id), "data.p")

    def get_channel_lock(self, guild_id, channel_id):
        with self.global_lock:
            return self.channel_locks.setdefault(guild_id, dict()).setdefault(channel_id, threading.RLock())

    async def temporary_message(self, channel, content = None, embed = None):
        lock = None
        with self.global_lock:
            lock = self.get_channel_lock(channel.guild.id, channel.id)
        with lock:
            temp_channel_data = self.get_channel_temp_data_by_id(channel.guild.id, channel.id)
            channel_data = self.get_channel_data_by_id(channel.guild.id, channel.id)
            last_message = temp_channel_data.get('temporary_message', None)
            if last_message is None:
                last_message_id = channel_data.get('temporary_message', None)
                if last_message_id is not None:
                    try:
                        last_message = await self.get_guild(channel.guild.id).get_channel(channel.id).fetch_message(last_message_id)
                    except:
                        print("Warning: could not fetch saved temporary_message: ", sys.exc_info()[0])
            if last_message is not None:
                try:
                    await last_message.delete()
                except:
                    print("Warning: couldn't delete temporary message: ", sys.exc_info()[0])
            temp_channel_data['temporary_message'] = await channel.send(content = content, embed = embed)
            channel_data['temporary_message'] = temp_channel_data['temporary_message'].id
            print(channel_data)
            self.update_channel_data(channel)

    @staticmethod
    def try_load_json(file_path, default_return):
        if not os.path.isfile(file_path):
            Path(os.path.dirname(file_path)).mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w') as f:
                f.write(json.dumps({}))
        try:
            with open(file_path) as json_file:
                data = json.load(json_file)
                return data
        except:
            print(f'Warning: Failed to read json file "{file_path}": ', sys.exc_info()[0])
        return default_return

    @staticmethod
    def try_load_pickle(file_path, default_return):
        if not os.path.isfile(file_path):
            pickle.dump({}, open(file_path, "wb"))
        try:
            return pickle.load(open(file_path, "rb"))
        except:
            print(f'Warning: Failed to read pickle file "{file_path}": ', sys.exc_info()[0])
        return default_return

    async def on_ready(self):
        with self.global_lock:
            print(f'{self.user} has connected to Discord!')
            guilds_path = os.path.join(self.data_directory, "guilds")
            Path(guilds_path).mkdir(parents=True, exist_ok=True)
            for guild_id_str in os.listdir(guilds_path):
                guild_id = 0
                try:
                    guild_id = int(guild_id_str)
                except:
                    print(f"Warning: Invalid guid id, id must be an int: {guid_id_str}")
                    continue
                guild_directory = os.path.join(self.data_directory, "guilds", guild_id_str)
                self.get_guild_config_by_id(guild_id)
                self.guilds_data.setdefault(guild_id, {})['config'] = self.try_load_json(os.path.join(guild_directory, "config.json"), self.default_guild_config())
                self.get_guild_data_by_id(guild_id)
                self.guilds_data.setdefault(guild_id, {})['data'] = self.try_load_pickle(os.path.join(guild_directory, "data.p"), self.default_guild_data())
                channels_path = os.path.join(self.data_directory, "guilds")
                Path(channels_path).mkdir(parents=True, exist_ok=True)
                for channel_id_str in os.listdir(os.path.join(guild_directory, "channels")):
                    channel_id = 0
                    try:
                        channel_id = int(channel_id_str)
                    except:
                        print(f"Warning: Invalid channel id, id must be an int: {channel_id_str}")
                        continue
                    channel_directory = os.path.join(guild_directory, "channels", channel_id_str)
                    self.get_channel_config_by_id(guild_id, channel_id)
                    print(self.guilds_data[guild_id]['channels'])
                    self.guilds_data[guild_id]['channels'][channel_id]['config'] = self.try_load_json(os.path.join(channel_directory, "config.json"), self.default_channel_config())
                    self.get_channel_data_by_id(guild_id, channel_id)
                    self.guilds_data[guild_id]['channels'][channel_id]['data'] = self.try_load_pickle(os.path.join(channel_directory, "data.p"), self.default_channel_data())
