import discord
from discord.ext import commands
import logging
import random

logger = logging.getLogger("EricLocator")

random_not_found_messages = [
    "404 - Eric not found",
    "Oukilé Eric ?",
    "Trouves Eric et gagnes un cookie !",
    "Personne sait où est Eric ?"
]


class ModalView(discord.ui.Modal, title='Eric Locator 2000'):
    salle = discord.ui.TextInput(
        label='Salle',
        placeholder='N102 / N104A / N104B',
        required=True,
        max_length=100
    )

    async def on_submit(self, interaction: discord.Interaction, /) -> None:
        embed = discord.Embed(
            title= "Eric est dans la salle " + self.salle.value + " !",
            color=0x00FF00
        )
        embed.set_author(name="Eric Locator",
                         icon_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fs3.amazonaws.com%2Fimages.seroundtable.com%2Fgoogle-maps-icon-1580992464.png")

        async for message in interaction.channel.history():
            await message.delete()
        await interaction.response.send_message(embed=embed, view=MessageView())


class PartialMessageView(discord.ui.View):
    """
    Vue pour la position d'Eric, sans le "perdu" (pour éviter les doublons).
    """

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label='Eric est dans ma salle !',
        style=discord.ButtonStyle.red,
        custom_id='eric:in_my_room'
    )
    async def in_my_room(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Show modal
        await interaction.response.send_modal(ModalView())


class MessageView(discord.ui.View):
    """
    Vue pour la position d'Eric.
    """

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label='Eric est dans ma salle !',
        style=discord.ButtonStyle.red,
        custom_id='eric:in_my_room'
    )
    async def in_my_room(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Show modal
        await interaction.response.send_modal(ModalView())

    @discord.ui.button(
        label='Eric est perdu !',
        style=discord.ButtonStyle.green,
        custom_id='eric:lost'
    )
    async def lost(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title=random.choice(random_not_found_messages),
            color=0x00FF00
        )
        embed.set_author(name="Eric Locator",
                         icon_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fs3.amazonaws.com%2Fimages.seroundtable.com%2Fgoogle-maps-icon-1580992464.png")

        # clear channel and send message
        async for message in interaction.channel.history():
            await message.delete()
        await interaction.response.send_message(embed=embed, view=PartialMessageView())


class EricLocator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_load(self) -> None:
        """
        Lorsque le cog est chargé.
        """
        self.bot.add_view(MessageView())
        self.bot.add_view(PartialMessageView())

    @commands.hybrid_group(
        name='eric',
        description="Trouve Eric"
    )
    async def eric(self, ctx):
        """
        Gérer les rôles d'année.

        :param context:
        """
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                description="Tu dois spécifier une sous-commande !",
                color=0xE02B2B,
            )
            await ctx.send(embed=embed, ephemeral=True)

    @eric.command(
        name='summon',
        description=r"Envoyer le premier message pour trouver Eric (/!\ efface tous les messages du salon)"
    )
    @commands.has_permissions(manage_messages=True)
    async def summon(self, ctx):
        """
        Envoyer le message de position d'Eric.

        :param ctx:
        """
        embed = discord.Embed(
            title="Personne ne sait où est Eric :/",
            description="Trouve Eric et tu gagnes un cookie",
            color=0x00FF00
        )
        embed.set_author(name="Eric Locator",
                         icon_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fs3.amazonaws.com%2Fimages.seroundtable.com%2Fgoogle-maps-icon-1580992464.png")

        # clear channel and send message
        async for message in ctx.channel.history():
            await message.delete()
        await ctx.send(embed=embed, view=PartialMessageView())


async def setup(bot):
    await bot.add_cog(EricLocator(bot))
