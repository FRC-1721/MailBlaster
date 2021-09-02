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


class EmailBlaster(object):

    def __init__(self):
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
        self.config.read('/app/email-blaster/email_blaster/config.ini')
        logging.debug(f"Read in config, contents={self.config.sections()}")  # Debug Message.

        # TODO: These may be redundant.
        self.email = self.config['mail']['email']
        self.email_password = self.config['mail']['emailPassword']
        self.email_server = self.config['mail']['emailServer']

        # Scheduled tasks.
        if self.debug:
            # Check for emails more quickly if we're in debug mode.
            schedule.every(20).to(50).seconds.do(self.get_new_emails)
        else:
            # Check for emails every 10 to 15 minutes in normal mode.
            schedule.every(10).to(15).minutes.do(self.get_new_emails)

        # TODO: Remove in favor of callbacks, or something.
        self.email_list = []

    def run(self):
        logging.info(f"using version {self.version}")

        # Login with credentials
        self.mail = imaplib.IMAP4_SSL(self.email_server)
        self.mail.login(self.email, self.email_password)

        # Select mailbox
        self.mail.select('inbox')

        while True:
            schedule.run_pending()
            time.sleep(1)

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
