# Tidal Force Robotics
# 2021, Email Blaster
# MIT License


import logging
import imaplib
import email

from discord.ext import tasks, commands


class CheckEmailCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Start checking for emails.
        self.check_email.start()

    def cog_unload(self):
        # Unloads the cog. (stops whatever its doing)
        self.check_email.cancel()

        # Docs on connection/error handling here
        # https://discordpy.readthedocs.io/en/latest/ext/tasks/

    @tasks.loop(minutes=3)
    async def check_email(self):
        alert_chennel_id = self.bot.config['alertschannel']
        alert_chanel = self.bot.get_channel(int(alert_chennel_id))

        logging.debug(f"Checking for new emails, sending info to {alert_chennel_id}")

        email_content = self.get_new_emails()

        if len(email_content) > 0:
            payload = f"""
@everyone

{email_content}

Email Blaster version {self.bot.version}"""

            await alert_chanel.send(payload)
        else:
            logging.debug('Nothing to send.')

    @check_email.before_loop
    async def before_email(self):
        # Wait till the bot is ready
        logging.info('Email Checking Cog is loaded and ready, waiting for bot to start..')
        await self.bot.wait_until_ready()

        # Start the imap connector
        self.email_address = self.bot.config['email']
        self.email_password = self.bot.config['emailpassword']
        self.email_server = self.bot.config['emailserver']

        # Setup a connection to the imap mailserver
        self.mail = imaplib.IMAP4_SSL(self.email_server)
        self.mail.login(self.email_address, self.email_password)

    def get_new_emails(self):
        """
        Check for new unread emails and add them to a postlist to sort through.
        """

        # Select mailbox
        self.mail.select('inbox')

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
                    logging.info(f'From: {mail_from}')
                    logging.info(f'Subject: {mail_subject}')
                    logging.info(f'Content: {mail_content}')

                    return mail_content
        return ""  # Return empty string otherwise

    @check_email.error
    async def exception_catching_callback(self, e):
        logging.error(f'caught error: {e}')
        quit()


def setup(bot):
    bot.add_cog(CheckEmailCog(bot))
