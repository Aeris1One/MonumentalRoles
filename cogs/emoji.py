import discord
from discord.ext import commands
import os

import logging

logger = logging.getLogger("Emoji")


class Emoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # when an emoji is deleted, if there's a jpg with its name in /emojis, recreate it
    @commands.Cog.listener()
    async def on_audit_log_entry(self, entry: discord.AuditLogEntry):
        if entry.action == discord.AuditLogAction.emoji_delete:
            logger.info(f"Emoji {entry.target.name} supprimé par {entry.user.name}.")
            if os.path.isfile(f"/emojis/{entry.target.name}.jpg"):
                logger.info(f"Re-création de l'emoji {entry.target.name}")
                await self.bot.get_guild(entry.guild.id).create_custom_emoji(name=entry.target.name, image=open(
                    f"emojis/{entry.target.name}.jpg", "rb").read())

    # on load, add all emojis in /emojis to all guilds
    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for file in os.listdir(f"/emojis"):
                if file.endswith(".jpg"):
                    emoji_name = file[:-4]
                    if not discord.utils.get(guild.emojis, name=emoji_name):
                        logger.info(f"Ajout de l'emoji {emoji_name} dans le serveur {guild.name}")
                        await guild.create_custom_emoji(name=emoji_name,
                                                        image=open(f"/emojis/{emoji_name}.jpg", "rb").read())


async def setup(bot):
    await bot.add_cog(Emoji(bot))
