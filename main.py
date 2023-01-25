import os

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

groupe1 = [0, 1, 2, 3, 4, 5, 6, 7, 8]
groupe2 = [9, 10, 11, 12, 13, 14]
groupe1id = 1067546097045745835
groupe2id = 1067546168067903519

a1id = 1067743463174582343
a2id = 1067545025010999397

suggestion_channel_id = 0000000000000000000

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class EnglishRolesView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='1', style=discord.ButtonStyle.green, custom_id='english:1')
    async def one(self, interaction: discord.Interaction, button: discord.ui.Button):
        logging.info("Anglais - Rôle Groupe 1 demandé par " + interaction.user.name)
        await addEnglishRoles(1, interaction)

    @discord.ui.button(label='2', style=discord.ButtonStyle.grey, custom_id='english:2')
    async def two(self, interaction: discord.Interaction, button: discord.ui.Button):
        logging.info("Anglais - Rôle Groupe 2 demandé par " + interaction.user.name)
        await addEnglishRoles(2, interaction)

    @discord.ui.button(label='3', style=discord.ButtonStyle.blurple, custom_id='english:3')
    async def three(self, interaction: discord.Interaction, button: discord.ui.Button):
        logging.info("Anglais - Rôle Groupe 3 demandé par " + interaction.user.name)
        await addEnglishRoles(3, interaction)

    @discord.ui.button(label='4', style=discord.ButtonStyle.red, custom_id='english:4')
    async def four(self, interaction: discord.Interaction, button: discord.ui.Button):
        logging.info("Anglais - Rôle Groupe 4 demandé par " + interaction.user.name)
        await addEnglishRoles(4, interaction)

    @discord.ui.button(label='5', style=discord.ButtonStyle.green, custom_id='english:5')
    async def five(self, interaction: discord.Interaction, button: discord.ui.Button):
        logging.info("Anglais - Rôle Groupe 5 demandé par " + interaction.user.name)
        await addEnglishRoles(5, interaction)

    @discord.ui.button(label='6', style=discord.ButtonStyle.blurple, custom_id='english:6')
    async def six(self, interaction: discord.Interaction, button: discord.ui.Button):
        logging.info("Anglais - Rôle Groupe 6 demandé par " + interaction.user.name)
        await addEnglishRoles(6, interaction)


async def addEnglishRoles(role_number: int, interaction: discord.Interaction):
    if discord.utils.get(interaction.guild.roles, id=english_roles_ids[role_number - 1]) not in interaction.user.roles:
        await interaction.response.send_message("Top ! C'est noté !", ephemeral=True)

        for role in english_roles_ids:
            if discord.utils.get(interaction.guild.roles, id=role) in interaction.user.roles:
                logging.debug("Anglais - Rôle " + discord.utils.get(interaction.guild.roles, id=role).name +
                              " retiré à " + interaction.user.name)
                await interaction.user.remove_roles(discord.utils.get(interaction.guild.roles, id=role))
            else:
                logging.debug("Anglais - Rôle " + discord.utils.get(interaction.guild.roles, id=role).name +
                              " n'a pas été retiré " + interaction.user.name)

        await interaction.user.add_roles(
            discord.utils.get(interaction.guild.roles, id=english_roles_ids[role_number - 1]),
            reason="English")
        logging.info("Anglais - Rôle " +
                     discord.utils.get(interaction.guild.roles, id=english_roles_ids[role_number - 1]).name +
                     " ajouté à " + interaction.user.name)
    else:
        await interaction.response.send_message("Tu as déjà ce rôle !", ephemeral=True)


class PrositGroupView(discord.ui.View):
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
        logging.info("Prosit - Rôle Équipe " + select.values[0] + " demandé par " + interaction.user.name)
        await addPrositRoles(int(select.values[0]), interaction)


async def addPrositRoles(role_number: int, interaction: discord.Interaction):
    if discord.utils.get(interaction.guild.roles, id=prosit_roles_ids[role_number - 1]) not in interaction.user.roles:
        await interaction.response.send_message("C'est noté !\n*Patientes un instant que les roles soient ajoutés par "
                                                "Discord*", ephemeral=True)
        for role in prosit_roles_ids:
            if discord.utils.get(interaction.guild.roles, id=role) in interaction.user.roles:
                logging.debug("Prosit - Rôle " + discord.utils.get(interaction.guild.roles, id=role).name +
                              " retiré à " + interaction.user.name)
                await interaction.user.remove_roles(discord.utils.get(interaction.guild.roles, id=role))
            else:
                logging.debug("Prosit - Rôle " + discord.utils.get(interaction.guild.roles, id=role).name +
                              " n'a pas été retiré " + interaction.user.name)

        if discord.utils.get(interaction.guild.roles, id=groupe1id) in interaction.user.roles:
            await interaction.user.remove_roles(discord.utils.get(interaction.guild.roles, id=groupe1id))
            logging.debug("Prosit - Rôle " + discord.utils.get(interaction.guild.roles, id=groupe1id).name +
                          " retiré à " + interaction.user.name)
        elif discord.utils.get(interaction.guild.roles, id=groupe2id) in interaction.user.roles:
            logging.debug("Prosit - Rôle " + discord.utils.get(interaction.guild.roles, id=groupe2id).name +
                          " retiré à " + interaction.user.name)
            await interaction.user.remove_roles(discord.utils.get(interaction.guild.roles, id=groupe2id))

        if role_number in groupe1:
            logging.info("Prosit - Rôle " +
                         discord.utils.get(interaction.guild.roles, id=groupe1id).name +
                         " ajouté à " + interaction.user.name)
            await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, id=groupe1id),
                                             reason="Prosit")
        elif role_number in groupe2:
            logging.info("Prosit - Rôle " +
                         discord.utils.get(interaction.guild.roles, id=groupe2id).name +
                         " ajouté à " + interaction.user.name)
            await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, id=groupe2id),
                                             reason="Prosit")

        logging.info("Prosit - Rôle " +
                     discord.utils.get(interaction.guild.roles, id=prosit_roles_ids[role_number - 1]).name +
                     " ajouté à " + interaction.user.name)
        await interaction.user.add_roles(
            discord.utils.get(interaction.guild.roles, id=prosit_roles_ids[role_number - 1]),
            reason="Prosit")
    else:
        await interaction.response.send_message("Tu as déjà ce rôle !", ephemeral=True)


class YearView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='A1', style=discord.ButtonStyle.green, custom_id='year:1')
    async def a1(self, interaction: discord.Interaction, button: discord.ui.Button):
        logging.info("Année - Rôle A1 demandé par " + interaction.user.name)
        if discord.utils.get(interaction.guild.roles, id=a2id) in interaction.user.roles:
            logging.debug("Année - Rôle " + discord.utils.get(interaction.guild.roles, id=a2id).name +
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
        logging.info("Année - Rôle " + discord.utils.get(interaction.guild.roles, id=a1id).name +
                     " ajouté à " + interaction.user.name)

    @discord.ui.button(label='A2', style=discord.ButtonStyle.red, custom_id='year:2')
    async def a2(self, interaction: discord.Interaction, button: discord.ui.Button):
        logging.info("Année - Rôle A2 demandé par " + interaction.user.name)
        if discord.utils.get(interaction.guild.roles, id=a2id) not in interaction.user.roles:
            await interaction.response.send_message("Top ! C'est noté !\n*Patientes un instant le temps que Discord "
                                                    "t'ajoutes le role*", ephemeral=True)

            for role in english_roles_ids:
                if discord.utils.get(interaction.guild.roles, id=role) in interaction.user.roles:
                    logging.debug("Année - Rôle " + discord.utils.get(interaction.guild.roles, id=role).name +
                                  " retiré à " + interaction.user.name)
                    await interaction.user.remove_roles(discord.utils.get(interaction.guild.roles, id=role))
            for role in prosit_roles_ids:
                if discord.utils.get(interaction.guild.roles, id=role) in interaction.user.roles:
                    logging.debug("Année - Rôle " + discord.utils.get(interaction.guild.roles, id=role).name +
                                  " retiré à " + interaction.user.name)
                    await interaction.user.remove_roles(discord.utils.get(interaction.guild.roles, id=role))

            if discord.utils.get(interaction.guild.roles, id=groupe1id) in interaction.user.roles:
                logging.debug("Année - Rôle " + discord.utils.get(interaction.guild.roles, id=groupe1id).name +
                              " retiré à " + interaction.user.name)
                await interaction.user.remove_roles(discord.utils.get(interaction.guild.roles, id=groupe1id))

            if discord.utils.get(interaction.guild.roles, id=groupe2id) in interaction.user.roles:
                logging.debug("Année - Rôle " + discord.utils.get(interaction.guild.roles, id=groupe2id).name +
                              " retiré à " + interaction.user.name)
                await interaction.user.remove_roles(discord.utils.get(interaction.guild.roles, id=groupe2id))
            await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, id=a2id),
                                             reason="A2")
            logging.info("Année - Rôle " +
                         discord.utils.get(interaction.guild.roles, id=a2id).name +
                         " ajouté à " + interaction.user.name)
        else:
            await interaction.response.send_message("C'est tout bon, tu as déjà le rôle !", ephemeral=True)


class MonumentalBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix=commands.when_mentioned_or('roles!'), intents=intents)

    async def setup_hook(self) -> None:
        # Register the persistent view for listening here.
        # Note that this does not send the view to any message.
        # In order to do this you need to first send a message with the View, which is shown below.
        # If you have the message_id you can also pass it as a keyword argument, but for this example
        # we don't have one.
        self.add_view(EnglishRolesView())
        self.add_view(PrositGroupView())
        self.add_view(YearView())

    async def on_message(self, message: discord.Message) -> None:
        if message.channel.id == suggestion_channel_id:
            await message.add_reaction("✅")
            await message.add_reaction("❌")
            await message.create_thread(name="Suggestion de " + message.author.name, auto_archive_duration=60)
        await self.process_commands(message)

    async def on_ready(self):
        logging.info(f'Connecté en tant que {self.user} (ID: {self.user.id})')


bot = MonumentalBot()


@bot.command()
@commands.has_permissions(manage_messages=True)
async def english(ctx: commands.Context):
    """Starts a persistent view."""
    # In order for a persistent view to be listened to, it needs to be sent to an actual message.
    # Call this method once just to store it somewhere.
    # In a more complicated program you might fetch the message_id from a database for use later.
    # However this is outside of the scope of this simple example.
    await ctx.send(file=discord.File("english.png"), view=EnglishRolesView())
    await ctx.message.delete()


@bot.command()
@commands.has_permissions(manage_messages=True)
async def prosit(ctx: commands.Context):
    """Starts a persistent view."""
    # In order for a persistent view to be listened to, it needs to be sent to an actual message.
    # Call this method once just to store it somewhere.
    # In a more complicated program you might fetch the message_id from a database for use later.
    # However this is outside of the scope of this simple example.
    await ctx.send(file=discord.File("prosit.png"), view=PrositGroupView())
    await ctx.message.delete()


@bot.command()
@commands.has_permissions(manage_messages=True)
async def year(ctx: commands.Context):
    """Starts a persistent view."""
    # In order for a persistent view to be listened to, it needs to be sent to an actual message.
    # Call this method once just to store it somewhere.
    # In a more complicated program you might fetch the message_id from a database for use later.
    # However this is outside of the scope of this simple example.
    # si l'auteur a les permissions d'administrateur
    await ctx.send(file=discord.File("year.png"), view=YearView())
    await ctx.message.delete()


bot.run(os.getenv("TOKEN"), log_handler=None)
