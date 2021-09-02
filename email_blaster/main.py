# Tidal Force robotics
# 2021, Email Blaster
# MIT License


import os
import sys
import logging
import email
import imaplib
import schedule
import time
import configparser

from email_blaster.cogs import check_email
from importlib.util import resolve_name

from discord.ext import commands


class EmailBlaster(object):

    def __init__(self):
        # Create our discord bot
        self.bot = commands.Bot(command_prefix='.')

        # Append our workdir to the path (for importing modules)
        self.workdir = '/app/email_blaster'
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

        # Create a config object.
        self.config = configparser.ConfigParser()

        # Read in our configuration.
        logging.debug(f"Looking for config in {os.listdir(os.getcwd())}")  # Debug message.
        self.config.read(self.workdir + '/config.ini')
        logging.debug(f"Read in config, contents={self.config.sections()}")  # Debug Message.

        # TODO: These may be redundant.
        self.email = self.config['mail']['email']
        self.email_password = self.config['mail']['emailPassword']
        self.email_server = self.config['mail']['emailServer']

        # TODO: Remove in favor of callbacks, or something.
        self.email_list = []

        for filename in os.listdir(self.workdir + '/cogs'):
            logging.debug(f"Found file {filename}, loading as extension.")
            if filename.endswith('.py'):
                self.bot.load_extension(f'cogs.{filename[:-3]}')
        #self.bot.load_extension("cogs.check_email")


    def run(self):
        logging.info(f"using version {self.version}")

        # Login with credentials
        #self.mail = imaplib.IMAP4_SSL(self.email_server)
        #self.mail.login(self.email, self.email_password)

        # Select mailbox
        #self.mail.select('inbox')

        # Run the discord bot using our token.
        self.bot.run(self.config['discord']['token'])

    def get_new_emails(self):
        """
        Check for new unread emails and add them to a postlist to sort through.
        """

        logging.debug("Checking for new emails.")
        # From here https://humberto.io/blog/sending-and-receiving-emails-with-python/
        status, data = self.mail.search(None, "(UNSEEN)")

        mail_ids = []

        for block in data:
            mail_ids += block.split()

        # Fetch the mail using each ID
        for i in mail_ids:
            status, data = self.mail.fetch(i, '(RFC822)')
            for response_part in data:
                if isinstance(response_part, tuple):
                    message = email.message_from_bytes(response_part[1])
                    mail_from = message['from']
                    mail_subject = message['subject']
                    if message.is_multipart():
                        mail_content = ''

                        # on multipart we have the text message and
                        # another things like annex, and html version
                        # of the message, in that case we loop through
                        # the email payload
                        for part in message.get_payload():
                            # if the content type is text/plain
                            # we extract it
                            if part.get_content_type() == 'text/plain':
                                mail_content += part.get_payload()
                    else:
                        # if the message isn't multipart, just extract it
                        mail_content = message.get_payload()

                    # and then let's show its result
                    print(f'From: {mail_from}')
                    print(f'Subject: {mail_subject}')
                    print(f'Content: {mail_content}')
