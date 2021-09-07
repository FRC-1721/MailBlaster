# Tidal Force Robotics
# 2021, Email Blaster
# MIT License


import os
import sys
import logging
import configparser
from shutil import copyfile

from discord.ext import commands
from email_blaster.keyValueTable import KeyValueTable


class EmailBlaster(object):

    def __init__(self):
        # Create our discord bot
        self.bot = commands.Bot(command_prefix='.')

        # Append our workdir to the path (for importing modules)
        self.workdir = '/app/email_blaster/'
        sys.path.append(self.workdir)

        # Get the build commit that the code was built with.
        self.version = os.environ.get('GIT_COMMIT')  # Currently running version
        # Find out if we're running in debug mode, or not.
        self.debug = not os.getenv("DEBUG", 'False').lower() in ('true', '1', 't')

        # Setup logging.
        if self.debug:
            logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
            logging.debug("Running in debug mode.")
        else:
            logging.basicConfig(stream=sys.stderr, level=logging.INFO)
            logging.info("Running in prod mode.")

        # Append some extra information to our discord bot
        self.bot.config = self.get_config()  # Package config with bot
        self.bot.version = self.version  # Package version with bot

        for filename in os.listdir(self.workdir + 'cogs'):
            logging.info(f"Found file {filename}, loading as extension.")
            if filename.endswith('.py'):
                self.bot.load_extension(f'cogs.{filename[:-3]}')

    def run(self):
        logging.info(f"using version {self.version}")

        # Run the discord bot using our token.
        self.bot.run(self.bot.config['discord']['token'])

    def get_config(self):
        '''Returns the config or halts loading till a config is found'''

        config_file_location = '/config/config.ini'
        database_file_location = '/config/blaster.db'

        # Connects to the blaster database
        database = KeyValueTable(database_file_location)
        # Connect to the config.ini
        config = configparser.ConfigParser()

        # Check if static config.ini exists
        if os.path.isfile(config_file_location):
            logging.info(f'File found at {config_file_location}, attempting to load')

            config.read(config_file_location)
        else:
            try:
                logging.warning('Config file not found! Copying default in.')
                copyfile('/app/resources/config.ini', config_file_location)
            except PermissionError:
                logging.error('Unable to copy file! Permission error! This is not fixed yet!')

        # Once the config is loaded, and the db we can compare them
        # Compare
        assert database['token'] == config['discord']['Token']

        return None
