# Tidal Force Robotics
# 2021, Email Blaster
# MIT License


import discord

from discord.ext import commands


class InfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send("Welcome {0.mention}.".format(member))

    @commands.Cog.listener()
    async def on_ready(self):
        status_channel = self.bot.get_channel(int("590312300695650305"))

        await status_channel.send(
            f"Email Blaster version {self.bot.version} just restarted."
        )

    @commands.command()
    async def version(self, ctx, *, member: discord.Member = None):
        await ctx.send(f"I am running version {self.bot.version}.")

    # This wont work till discord 2.0
    # @commands.command()
    # async def thread(self, ctx, *args, member: discord.Member = None):
    #     """Makes a thread for you"""

    #     thread_name = ' '.join(args)

    #     await ctx.send(f'Making a "{thread_name}" thread for you')


def setup(bot):
    bot.add_cog(InfoCog(bot))
