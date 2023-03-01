from discord.ext import commands
import discord
import logging

prosit_roles_ids = [
    1067546371831373894,  # 1
    1067546493847879690,  # 2
    1067546513108119593,  # 3
    1067546549296578560,  # 4
    1067546567105589358,  # 5
    1067546583975075851,  # 6
    1067546602216099942,  # 7
    1067546620314521670,  # 8
    1067546637909622804,  # 9
    1067546745782927401,  # 10
    1067546767186464899,  # 11
    1067546782910922872,  # 12
    1067546799667167333,  # 13
    1067546817467777144  # 14
]

groupe1 = [1, 2, 3, 4]
groupe2 = [5, 6, 7, 8]
groupe3 = [9, 10, 11, 12, 13, 14]
groupe1id = 1067546097045745835
groupe2id = 1067546168067903519
groupe3id = 1072828558352842814

logger = logging.getLogger("Prosit")


class View(discord.ui.View):
    """
    Vue pour la sélection du groupe prosit.
    """

    def __init__(self):
        super().__init__(timeout=None)

    options = [
        discord.SelectOption(label='1'),
        discord.SelectOption(label='2'),
        discord.SelectOption(label='3'),
        discord.SelectOption(label='4'),
        discord.SelectOption(label='5'),
        discord.SelectOption(label='6'),
        discord.SelectOption(label='7'),
        discord.SelectOption(label='8'),
        discord.SelectOption(label='9'),
        discord.SelectOption(label='10'),
        discord.SelectOption(label='11'),
        discord.SelectOption(label='12'),
        discord.SelectOption(label='13'),
        discord.SelectOption(label='14')
    ]

    @discord.ui.select(placeholder="Choisis ton groupe prosit !", options=options, custom_id='prosit_group_select')
    async def role_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        logger.info("Rôle Équipe " + select.values[0] + " demandé par " + interaction.user.name)
        await add_prosit_roles(int(select.values[0]), interaction)


async def add_prosit_roles(role_number: int, interaction: discord.Interaction):
    if discord.utils.get(interaction.guild.roles, id=prosit_roles_ids[role_number - 1]) not in interaction.user.roles:
        await interaction.response.send_message("C'est noté !\n*Patiente un instant que les roles soient ajoutés par "
                                                "Discord*", ephemeral=True)
        for role in prosit_roles_ids:
            if discord.utils.get(interaction.guild.roles, id=role) in interaction.user.roles:
                logger.debug("Rôle " + discord.utils.get(interaction.guild.roles, id=role).name +
                             " retiré à " + interaction.user.name)
                await interaction.user.remove_roles(discord.utils.get(interaction.guild.roles, id=role))
            else:
                logger.debug("Rôle " + discord.utils.get(interaction.guild.roles, id=role).name +
                             " n'a pas été retiré " + interaction.user.name)

        if discord.utils.get(interaction.guild.roles, id=groupe1id) in interaction.user.roles:
            await interaction.user.remove_roles(discord.utils.get(interaction.guild.roles, id=groupe1id))
            logger.debug("Rôle " + discord.utils.get(interaction.guild.roles, id=groupe1id).name +
                         " retiré à " + interaction.user.name)
        elif discord.utils.get(interaction.guild.roles, id=groupe2id) in interaction.user.roles:
            logger.debug("Rôle " + discord.utils.get(interaction.guild.roles, id=groupe2id).name +
                         " retiré à " + interaction.user.name)
            await interaction.user.remove_roles(discord.utils.get(interaction.guild.roles, id=groupe2id))
        elif discord.utils.get(interaction.guild.roles, id=groupe3id) in interaction.user.roles:
            logger.debug("Rôle " + discord.utils.get(interaction.guild.roles, id=groupe3id).name +
                         " retiré à " + interaction.user.name)
            await interaction.user.remove_roles(discord.utils.get(interaction.guild.roles, id=groupe3id))

        if role_number in groupe1:
            logger.info("Rôle " +
                        discord.utils.get(interaction.guild.roles, id=groupe1id).name +
                        " ajouté à " + interaction.user.name)
            await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, id=groupe1id))
        elif role_number in groupe2:
            logger.info("Rôle " +
                        discord.utils.get(interaction.guild.roles, id=groupe2id).name +
                        " ajouté à " + interaction.user.name)
            await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, id=groupe2id))

        elif role_number in groupe3:
            logger.info("Rôle " +
                        discord.utils.get(interaction.guild.roles, id=groupe3id).name +
                        " ajouté à " + interaction.user.name)
            await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, id=groupe3id))

        logger.info("Rôle " +
                    discord.utils.get(interaction.guild.roles, id=prosit_roles_ids[role_number - 1]).name +
                    " ajouté à " + interaction.user.name)
        await interaction.user.add_roles(
            discord.utils.get(interaction.guild.roles, id=prosit_roles_ids[role_number - 1]),
        )
    else:
        await interaction.response.send_message("Tu as déjà ce rôle !", ephemeral=True)


class Prosit(commands.Cog):
    """
    Gérer les rôles de prosit.
    """

    def __init__(self, bot):
        self.bot = bot

    def cog_load(self) -> None:
        """
        Lorsque le cog est chargé.
        """
        self.bot.add_view(View())

    @commands.hybrid_group(
        name="prosit",
        description="Gérer les rôles de prosit.",
    )
    async def prosit(self, context: commands.Context) -> None:
        """
        Gérer les rôles de prosit.

        :param context:
        """
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="Tu dois spécifier une sous-commande !",
                color=0xE02B2B,
            )
            await context.send(embed=embed, ephemeral=True)

    @prosit.command(name="summon", description="Envoyer le message de choix des rôles de prosit.")
    @commands.has_permissions(manage_messages=True)
    async def summon(self, ctx: commands.Context):
        """
        Envoyer le message de choix des rôles de prosit.

        :param ctx:
        """
        await ctx.send(file=discord.File("medias/prosit.png"), view=View())
        if ctx.interaction is None:
            await ctx.message.delete()

    @prosit.command(name="reset", description="Réinitialiser les rôles de prosit de tous les membres.")
    @commands.has_permissions(manage_roles=True)
    async def reset(self, ctx: commands.Context):
        """
        Supprimer tous les rôles de prosit.

        :param ctx:
        """
        member_count = ctx.guild.member_count
        embed = discord.Embed(
            title="Suppression des rôles de prosit en cours...",
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
            for role in prosit_roles_ids, groupe1id, groupe2id, groupe3id:
                if discord.utils.get(ctx.guild.roles, id=role) in member.roles:
                    await member.remove_roles(discord.utils.get(ctx.guild.roles, id=role))
                    logger.info("Rôle " + discord.utils.get(ctx.guild.roles, id=role).name +
                                " retiré à " + member.name)
            treated_members += 1
            embed.description = f"{treated_members} / {member_count} membres traités (Actuel: {member.name})."
            await message.edit(embed=embed)
            logger.debug("Traitement de " + member.name + " terminé.")


async def setup(bot):
    await bot.add_cog(Prosit(bot))
