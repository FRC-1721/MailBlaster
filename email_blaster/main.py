# Tidal Force Robotics
# 2021, Email Blaster
# MIT License


import os
import sys
import sqlite3
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

        config_file_location = '/config/config.ini'
        database_file_location = '/config/blaster.db'

        try:
            database = self.initalize_database(config_file_location, database_file_location)

            return database
        except sqlite3.OperationalError:
            logging.warn('Bot detected it was running locally! or there was an error finding a db.')
            logging.info('Attempting an alternative configuration')

            config_file_location = '/tmp/mailblaster/config.ini'
            database_file_location = '/tmp/mailblaster/blaster.db'

    def initalize_database(self, cfg_file_loc, db_file_loc):
        # Connects to the blaster database
        database = KeyValueTable(db_file_loc)
        # Connect to the config.ini
        config = configparser.ConfigParser()

        # Check if static config.ini exists
        if os.path.isfile(cfg_file_loc):
            logging.info(f'File found at {cfg_file_loc}, attempting to load')

            config.read(cfg_file_loc)
        else:
            try:
                logging.warning('Config file not found! Copying default in.')
                copyfile('/app/resources/config.ini', cfg_file_loc)
            except PermissionError:
                logging.error('Unable to copy file! Permission error! This is not fixed yet!')

        _config = {}
        # Convert the static config to a dict without sections
        for section in config.sections():
            for pair in config.items(section):
                key = pair[0]
                value = pair[1]
                _config[key] = value  # Funky stuff

        config = _config
        logging.info('Converted config.ini to a dict.')

        # Once the config is loaded, and the db we can compare them
        # Compare
        try:
            assert database['token'] == config['token']
        except AssertionError:
            # Assertion error if what we asserted is not true.
            logging.info('Static database and configuration database differ! Updating database.')

            # Mirror the config over.
            for key in config:
                database[key] = config[key]

            logging.info('Converted ini to database, continuing to load the bot.')
            database.commit()
            return database
        except KeyError:
            # Key error if token straight up does not exist
            logging.warning('Database was detected to be empty!" \
                "Copying in defaults from config.ini.')

            # Mirror the config over.
            for key in config:
                database[key] = config[key]

            logging.warning('Default database has been coppied." \
                "Its possible only default values are set, check config.ini.')
            database.commit()
            return database

        logging.info('Database and config loaded and up to date!')
        database.commit()
        return database
