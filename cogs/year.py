from discord.ext import commands
from cogs.english import english_roles_ids
from cogs.prosit import prosit_roles_ids, groupe1id, groupe2id, groupe3id
import discord
import logging

a1id = 1067743463174582343
a2id = 1067545025010999397

logger = logging.getLogger('Année')


class View(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='A1', style=discord.ButtonStyle.green, custom_id='year:1')
    async def a1(self, interaction: discord.Interaction, button: discord.ui.Button):
        logger.info("Rôle A1 demandé par " + interaction.user.name)
        if discord.utils.get(interaction.guild.roles, id=a2id) in interaction.user.roles:
            logger.debug("Rôle " + discord.utils.get(interaction.guild.roles, id=a2id).name +
                         " retiré à " + interaction.user.name)
            await interaction.response.send_message("Top ! C'est noté, choisis ton groupe d'anglais et ton groupe "
                                                    "prosit !", ephemeral=True)
            await interaction.user.remove_roles(discord.utils.get(interaction.guild.roles, id=a2id),
                                                reason="A1")
        else:
            await interaction.response.send_message("Top ! C'est noté, choisis ton groupe d'anglais et ton groupe "
                                                    "prosit !", ephemeral=True)
        await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, id=a1id),
                                         reason="A1")
        logger.info("Rôle " + discord.utils.get(interaction.guild.roles, id=a1id).name +
                    " ajouté à " + interaction.user.name)

    @discord.ui.button(label='A2', style=discord.ButtonStyle.red, custom_id='year:2')
    async def a2(self, interaction: discord.Interaction, button: discord.ui.Button):
        logger.info("Rôle A2 demandé par " + interaction.user.name)
        if discord.utils.get(interaction.guild.roles, id=a2id) not in interaction.user.roles:
            await interaction.response.send_message("Top ! C'est noté !\n*Patiente un instant le temps que Discord "
                                                    "t'ajoutes le role*", ephemeral=True)

            for role in english_roles_ids, prosit_roles_ids, groupe1id, groupe2id, groupe3id:
                if discord.utils.get(interaction.guild.roles, id=role) in interaction.user.roles:
                    logger.debug("Rôle " + discord.utils.get(interaction.guild.roles, id=role).name +
                                 " retiré à " + interaction.user.name)
                    await interaction.user.remove_roles(discord.utils.get(interaction.guild.roles, id=role))

        else:
            await interaction.response.send_message("C'est tout bon, tu as déjà le rôle !", ephemeral=True)


class Year(commands.Cog):
    """
    Gérer les rôles d'année.
    """

    def __init__(self, bot):
        self.bot = bot

    def cog_load(self) -> None:
        """
        Lorsque le cog est chargé.
        """
        self.bot.add_view(View())

    @commands.hybrid_group(
        name="year",
        description="Gérer les rôles d'année.",
    )
    async def year(self, context: commands.Context) -> None:
        """
        Gérer les rôles d'année.

        :param context:
        """
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="Tu dois spécifier une sous-commande !",
                color=0xE02B2B,
            )
            await context.send(embed=embed, ephemeral=True)

    @year.command(name="summon", description="Envoyer le message de choix des rôles d'année.")
    @commands.has_permissions(manage_messages=True)
    async def summon(self, ctx: commands.Context):
        """
        Envoyer le message de choix des rôles de prosit.

        :param ctx:
        """
        await ctx.send(file=discord.File("medias/prosit.png"), view=View())
        if ctx.interaction is None:
            await ctx.message.delete()

    @year.command(name="reset", description="Réinitialiser les rôles d'année de tous les membres.")
    @commands.has_permissions(manage_roles=True)
    async def reset(self, ctx: commands.Context):
        """
        Supprimer tous les rôles de prosit.

        :param ctx:
        """
        member_count = ctx.guild.member_count
        embed = discord.Embed(
            title="Suppression des rôles d'année en cours...",
            description=f"0 / {member_count} membres traités (Actuel: ...).",
            color=0xE02B2B,
        )
        message = await ctx.send(
            embed=embed,
            ephemeral=True
        )
        logger.info("Suppression des rôles de prosit demandée par " + ctx.author.name)

        treated_members = 0
        for member in ctx.guild.members:
            logger.debug("Traitement de " + member.name)
            for role in a1id, a2id:
                if discord.utils.get(ctx.guild.roles, id=role) in member.roles:
                    await member.remove_roles(discord.utils.get(ctx.guild.roles, id=role))
                    logger.info("Rôle " + discord.utils.get(ctx.guild.roles, id=role).name +
                                " retiré à " + member.name)
            treated_members += 1
            embed.description = f"{treated_members} / {member_count} membres traités (Actuel: {member.name})."
            await message.edit(embed=embed)
            logger.debug("Traitement de " + member.name + " terminé.")


async def setup(bot):
    await bot.add_cog(Year(bot))
