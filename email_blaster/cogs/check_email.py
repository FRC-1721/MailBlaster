import logging

from discord.ext import tasks, commands


class CheckEmailCog(commands.Cog):
    def __init__(self, bot):
        pass

    def cog_unload(self):
        # Unloads the cog. (stops whatever its doing)
        self.check_email.cancel()

        # Docs on connection/error handling here
        # https://discordpy.readthedocs.io/en/latest/ext/tasks/

    @tasks.loop(minutes=5)
    async def check_email(self):
        logging.debug("Checking for new emails.")


def setup(bot):
    bot.add_cog(CheckEmailCog(bot))
