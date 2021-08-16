# Tidal Force robotics
# 2021, Email Blaster
# MIT License


import os
import sys
import logging
import email
import imaplib

# Setup logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

class EmailBlaster(object):

    def __init__(self):
        self.version = os.environ.get('GIT_COMMIT') # Currently running version
        
        self.email = 'concordroboticsalert1721@gmail.com'
        self.email_password = ''
        self.email_server = 'imap.gmail.com'

        # Login with credentials
        self.mail = imaplib.IMAP4_SSL(self.email_server)
        self.mail.login(self.email, self.email_password)

        # Select mailbox
        self.mail.select('inbox')

    def run(self):
        logging.info(f"using version {self.version}")

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
