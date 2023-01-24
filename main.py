import os

from discord.ext import commands
import discord

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

a2id = 1067545025010999397


class EnglishRolesView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='1', style=discord.ButtonStyle.green, custom_id='persistent_view:1')
    async def one(self, interaction: discord.Interaction, button: discord.ui.Button):
        await addEnglishRoles(1, interaction)

    @discord.ui.button(label='2', style=discord.ButtonStyle.grey, custom_id='persistent_view:2')
    async def two(self, interaction: discord.Interaction, button: discord.ui.Button):
        await addEnglishRoles(2, interaction)

    @discord.ui.button(label='3', style=discord.ButtonStyle.blurple, custom_id='persistent_view:3')
    async def three(self, interaction: discord.Interaction, button: discord.ui.Button):
        await addEnglishRoles(3, interaction)

    @discord.ui.button(label='4', style=discord.ButtonStyle.red, custom_id='persistent_view:4')
    async def four(self, interaction: discord.Interaction, button: discord.ui.Button):
        await addEnglishRoles(4, interaction)

    @discord.ui.button(label='5', style=discord.ButtonStyle.green, custom_id='persistent_view:5')
    async def five(self, interaction: discord.Interaction, button: discord.ui.Button):
        await addEnglishRoles(5, interaction)

    @discord.ui.button(label='6', style=discord.ButtonStyle.blurple, custom_id='persistent_view:6')
    async def six(self, interaction: discord.Interaction, button: discord.ui.Button):
        await addEnglishRoles(6, interaction)


async def addEnglishRoles(role_number: int, interaction: discord.Interaction):
    if discord.utils.get(interaction.guild.roles, id=english_roles_ids[role_number - 1]) not in interaction.user.roles:
        await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, id=english_roles_ids[role_number]),
                                         reason="English")
        await interaction.response.send_message("Top ! C'est noté !", ephemeral=True)
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
    async def role_select(self, select: discord.ui.RoleSelect, interaction: discord.Interaction):
        await addPrositRoles(select.values[0], interaction)


async def addPrositRoles(role_number: int, interaction: discord.Interaction):
    if role_number in groupe1:
        await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, id=groupe1id),
                                         reason="Prosit")
    elif role_number in groupe2:
        await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, id=groupe2id),
                                         reason="Prosit")

    if discord.utils.get(interaction.guild.roles, id=prosit_roles_ids[role_number - 1]) not in interaction.user.roles:
        await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, id=prosit_roles_ids[role_number]),
                                         reason="Prosit")
        await interaction.response.send_message("Top ! C'est noté !", ephemeral=True)
    else:
        await interaction.response.send_message("Tu as déjà ce rôle !", ephemeral=True)


class YearView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='A1', style=discord.ButtonStyle.green, custom_id='persistent_view:green')
    async def a1(self, interaction: discord.Interaction, button: discord.ui.Button):
        if discord.utils.get(interaction.guild.roles, id=1067545025010999397) in interaction.user.roles:
            await interaction.user.remove_roles(discord.utils.get(interaction.guild.roles, id=1067545025010999397),
                                                reason="A1")
            await interaction.response.send_message("Top ! C'est noté, choisis ton groupe d'anglais et ton groupe "
                                                    "prosit !", ephemeral=True)
        await interaction.response.send_message("Top ! C'est noté, choisis ton groupe d'anglais et ton groupe prosit !",
                                                ephemeral=True)

    @discord.ui.button(label='A2', style=discord.ButtonStyle.red, custom_id='persistent_view:red')
    async def a2(self, interaction: discord.Interaction, button: discord.ui.Button):
        if discord.utils.get(interaction.guild.roles, id=1067545025010999397) not in interaction.user.roles:
            await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, id=1067545025010999397),
                                             reason="A2")
            await interaction.response.send_message("Top ! C'est noté !", ephemeral=True)
        await interaction.response.send_message("C'est tout bon, tu as déjà le rôle !", ephemeral=True)


class PersistentViewBot(commands.Bot):
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

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')


bot = PersistentViewBot()


@bot.command()
@commands.is_owner()
async def english(ctx: commands.Context):
    """Starts a persistent view."""
    # In order for a persistent view to be listened to, it needs to be sent to an actual message.
    # Call this method once just to store it somewhere.
    # In a more complicated program you might fetch the message_id from a database for use later.
    # However this is outside of the scope of this simple example.
    if ctx.author.id == 284017092246765589:
        await ctx.send(file=discord.File("english.png"), view=EnglishRolesView())


@bot.command()
async def prosit(ctx: commands.Context):
    """Starts a persistent view."""
    # In order for a persistent view to be listened to, it needs to be sent to an actual message.
    # Call this method once just to store it somewhere.
    # In a more complicated program you might fetch the message_id from a database for use later.
    # However this is outside of the scope of this simple example.
    if ctx.author.id == 284017092246765589:
        await ctx.send(file=discord.File("prosit.png"), view=PrositGroupView())


@bot.command()
async def year(ctx: commands.Context):
    """Starts a persistent view."""
    # In order for a persistent view to be listened to, it needs to be sent to an actual message.
    # Call this method once just to store it somewhere.
    # In a more complicated program you might fetch the message_id from a database for use later.
    # However this is outside of the scope of this simple example.
    if ctx.author.id == 284017092246765589:
        await ctx.send(file=discord.File("year.png"), view=YearView())


#bot.run(os.getenv("TOKEN"))
bot.run("MTA2NzU1MTY5ODc5NDU3ODAwMA.GH9KFY.IMu_o8TIk2G4X1fhqjCCV-nQHIIYAq3PyjAKi8")