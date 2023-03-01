from discord.ext import commands
import discord
import logging

english_roles_ids = [
    1067546201332928543,  # 1
    1067546253090619402,  # 2
    1067546292303171655,  # 3
    1067546315074060358,  # 4
    1067546333021491260,  # 5
    1067548245863186472  # 6
]

logger = logging.getLogger("Anglais")


class View(discord.ui.View):
    """
    Vue pour la sélection du groupe d'anglais.
    """

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='1', style=discord.ButtonStyle.green, custom_id='english:1')
    async def one(self, interaction: discord.Interaction, button: discord.ui.Button):
        logger.info("Rôle Groupe 1 demandé par " + interaction.user.name)
        await add_role(1, interaction)

    @discord.ui.button(label='2', style=discord.ButtonStyle.grey, custom_id='english:2')
    async def two(self, interaction: discord.Interaction, button: discord.ui.Button):
        logger.info("Rôle Groupe 2 demandé par " + interaction.user.name)
        await add_role(2, interaction)

    @discord.ui.button(label='3', style=discord.ButtonStyle.blurple, custom_id='english:3')
    async def three(self, interaction: discord.Interaction, button: discord.ui.Button):
        logger.info("Rôle Groupe 3 demandé par " + interaction.user.name)
        await add_role(3, interaction)

    @discord.ui.button(label='4', style=discord.ButtonStyle.red, custom_id='english:4')
    async def four(self, interaction: discord.Interaction, button: discord.ui.Button):
        logger.info("Rôle Groupe 4 demandé par " + interaction.user.name)
        await add_role(4, interaction)

    @discord.ui.button(label='5', style=discord.ButtonStyle.green, custom_id='english:5')
    async def five(self, interaction: discord.Interaction, button: discord.ui.Button):
        logger.info("Rôle Groupe 5 demandé par " + interaction.user.name)
        await add_role(5, interaction)

    @discord.ui.button(label='6', style=discord.ButtonStyle.blurple, custom_id='english:6')
    async def six(self, interaction: discord.Interaction, button: discord.ui.Button):
        logger.info("Rôle Groupe 6 demandé par " + interaction.user.name)
        await add_role(6, interaction)


async def add_role(role_number: int, interaction: discord.Interaction):
    """
    Ajouter un rôle d'anglais.

    :param role_number:
    :param interaction:
    """
    if discord.utils.get(interaction.guild.roles,
                         id=english_roles_ids[role_number - 1]) not in interaction.user.roles:
        await interaction.response.send_message("Top ! C'est noté !", ephemeral=True)

        for role in english_roles_ids:
            if discord.utils.get(interaction.guild.roles, id=role) in interaction.user.roles:
                await interaction.user.remove_roles(discord.utils.get(interaction.guild.roles, id=role))
                logger.debug("Rôle " + discord.utils.get(interaction.guild.roles, id=role).name +
                             " retiré à " + interaction.user.name)
            else:
                logger.debug("Rôle " + discord.utils.get(interaction.guild.roles, id=role).name +
                             " n'a pas été retiré " + interaction.user.name)

        await interaction.user.add_roles(
            discord.utils.get(interaction.guild.roles, id=english_roles_ids[role_number - 1])
        )
        logger.info("Rôle " +
                    discord.utils.get(interaction.guild.roles, id=english_roles_ids[role_number - 1]).name +
                    " ajouté à " + interaction.user.name)
    else:
        await interaction.response.send_message("Tu as déjà ce rôle !", ephemeral=True)


class English(commands.Cog):
    """
    Gérer les rôles d'anglais.
    """

    def __init__(self, bot):
        self.bot = bot

    def cog_load(self) -> None:
        """
        Lorsque le cog est chargé.
        """
        self.bot.add_view(View())

    @commands.hybrid_group(
        name="english",
        description="Gérer les rôles d'anglais.",
    )
    async def english(self, context: commands.Context) -> None:
        """
        Gérer les rôles d'anglais.

        :param context:
        """
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="Tu dois spécifier une sous-commande !",
                color=0xE02B2B,
            )
            await context.send(embed=embed, ephemeral=True)

    @english.command(name="summon", description="Envoyer le message de choix des rôles d'anglais.")
    @commands.has_permissions(manage_messages=True)
    async def summon(self, ctx: commands.Context):
        """
        Envoyer le message de choix des rôles d'anglais.

        :param ctx:
        """
        await ctx.send(file=discord.File("medias/english.png"), view=View())
        if ctx.interaction is None:
            await ctx.message.delete()

    @english.command(name="reset", description="Réinitialiser les rôles d'anglais de tous les membres.")
    @commands.has_permissions(manage_roles=True)
    async def reset(self, ctx: commands.Context):
        """
        Supprimer tous les rôles d'anglais.

        :param ctx:
        """
        member_count = ctx.guild.member_count
        embed = discord.Embed(
            title="Suppression des rôles d'anglais en cours...",
            description=f"0 / {member_count} membres traités (Actuel: ...).",
            color=0xE02B2B,
        )
        message = await ctx.send(
            embed=embed,
            ephemeral=True
        )
        logger.info("Suppression des rôles d'anglais demandée par " + ctx.author.name)

        treated_members = 0
        for member in ctx.guild.members:
            logger.debug("Traitement de " + member.name)
            for role in english_roles_ids:
                if discord.utils.get(ctx.guild.roles, id=role) in member.roles:
                    await member.remove_roles(discord.utils.get(ctx.guild.roles, id=role))
                    logging.info("Rôle " + discord.utils.get(ctx.guild.roles, id=role).name +
                                 " retiré à " + member.name)
            treated_members += 1
            embed.description = f"{treated_members} / {member_count} membres traités (Actuel: {member.name})."
            await message.edit(embed=embed)
            logger.debug("Traitement de " + member.name + " terminé")


async def setup(bot):
    await bot.add_cog(English(bot))
