# Tidal Force Robotics
# 2021, Email Blaster
# MIT License


import os
import sys
import sqlite3
import logging

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
        self.version = str(os.environ.get('GIT_COMMIT'))  # Currently running version
        # Find out if we're running in debug mode, or not.
        self.debug = str(os.environ.get("DEBUG")).lower() in ('true', '1', 't')

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
        self.bot.run(self.bot.config['token'])

    def get_config(self):
        '''Returns the config or halts loading till a config is found'''

        database_file_location = '/app/config/blaster.db'

        try:
            database = self.initalize_database(database_file_location)

            return database
        except sqlite3.OperationalError as e:
            logging.error(e)
            logging.warn('Bot detected it was running locally! or there was an error finding a db.')
            logging.info('Attempting an alternative configuration')

            database_file_location = '/tmp/mailblaster/blaster.db'

    def initalize_database(self, db_file_loc):
        # Connects to the blaster database
        database = KeyValueTable(db_file_loc)

        # Settings to run through when configuring hardcoded/default settings
        env_settings = ['token',
                        'alertsrole',
                        'alertschannel',
                        'email',
                        'emailpassword',
                        'emailserver']

        for setting in env_settings:
            value = str(os.environ.get(setting.upper()))  # Get the content of that setting

            # Check if its populated
            if value != 'None':
                logging.debug(f'Found manual var {setting} set to {value}.')
                if value != database[setting]:
                    logging.info(f'User configured value {value} for entry {setting} differs from saved setting, {database[setting]}, updating.')  # noqa: E501
                    database[setting] = value  # Update manually configured value
                    database.commit()

        logging.info('Database and config loaded and up to date!')
        database.commit()
        return database
