import os

from discord.ext import commands
import discord
import logging
import asyncio

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Main")


async def load_cogs() -> None:
    """
    The code in this function is executed whenever the bot will start.
    """
    for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                await bot.load_extension(f"cogs.{extension}")
                logger.info(f"Extension '{extension}' chargée avec succès")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                logger.error(
                    f"Une erreur est survenue pendant le chargement de l'extension {extension} : \n{exception}")


class MonumentalBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(command_prefix=commands.when_mentioned_or('roles!'), intents=intents)

    async def on_ready(self):
        logger.info('Chargement des extensions...')
        await load_cogs()
        logger.info(f'Connecté en tant que {self.user} (ID: {self.user.id})')
        logger.info("Synchronisation des commandes...")
        await bot.tree.sync()
        logger.info("Synchronisation terminée.")
        logger.info(f'------')
        await self.change_presence(status=discord.Status.online)


bot = MonumentalBot()
bot.status = discord.Status.do_not_disturb

bot.run(os.getenv("TOKEN"), log_handler=None)
