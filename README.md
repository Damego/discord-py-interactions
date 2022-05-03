<div align="center">
    <a href="https://pypi.org/project/discord-py-interactions/">
        <img src=".github/banner_transparent.png" alt="discord-py-interactions" height="128">
    </a>
    <h2>Your ultimate Discord interactions library for <a href="https://github.com/Rapptz/discord.py">discord.py</a>.</h2>
</div>

<div align="center">
        <a href="https://app.codacy.com/gh/eunwoo1104/discord-py-slash-command?utm_source=github.com&utm_medium=referral&utm_content=eunwoo1104/discord-py-slash-command&utm_campaign=Badge_Grade_Settings">
            <img src="https://api.codacy.com/project/badge/Grade/224bdbe58f8f43f28a093a33a7546456" alt="Codacy Badge">
        </a>
        <a href="https://discord.gg/KkgMBVuEkx">
            <img alt="Discord" src="https://img.shields.io/discord/789032594456576001">
        </a>
</div>

<p align="center">
    <a href="#about">About</a> |
    <a href="#installation">Installation</a> |
    <a href="#examples">Examples</a> |
    <a href="https://discord.gg/KkgMBVuEkx">Discord</a> |
    <a href="https://pypi.org/project/discord-py-interactions/">PyPI</a>
</p>

# About
## What happend with original library?
Original library has become a separate wrapper for discord API and got version 4. Its not more extension for `discord.py`
But there are people who want to continue using v3 with `discord.py`
## What is discord-py-interactions?
`discord-py-interactions` is, in the simplest terms, a library extension that builds off of the currently existing
discord.py API wrapper. While we do use our own basic class code for our own library, a large majority of
this library uses discord.py base events in order to make contextualization of interactions relatively easy
for us.

### When did this begin?
In mid-December of 2020, Discord released the very first type of components, **slash commands.** These were
relatively primitive at the time of their debut, however, over time they slowly came to grew more complex
and mutable. This library was created 2 days after the release of slash commands to Discord, and ever since
has been actively growing.

## What do we currently support?
At this time, we are able to provide you an non-exhaustive list (because Discord are actively
creating more interactions at this time) of all components integrated as interactions:

* Slash Commands
* Buttons, Selects, Modals

# Installation
We recommend using pip in order to install our library. You are able to do this by typing the following line below:

`pip uninstall discord-py-interactions`
`pip install git+https://github.com/Damego/discord-py-interactions.git`

# Examples
## Slash Commands
This example shows a very quick and simplistic solution to implementing a slash command.

```py
from discord import Client, Intents, Embed
from discord_slash import SlashCommand, SlashContext

bot = Client(intents=Intents.default())
slash = SlashCommand(bot)

@slash.slash(name="test")
async def test(ctx: SlashContext):
    embed = Embed(title="Embed Test")
    await ctx.send(embed=embed)

bot.run("discord_token")
```

### Cogs
This example serves as an alternative method for using slash commands in a cog instead.

```py
# bot.py
from discord import Intents
from discord.ext.commands import Bot
from discord_slash import SlashCommand

# Note that command_prefix is a required but essentially unused paramater.
# Setting help_command=False ensures that discord.py does not create a !help command.
# Enabling self_bot ensures that the bot does not try and parse messages that start with "!".
bot = Bot(command_prefix="!", self_bot=True, help_command=False, intents=Intents.default())
slash = SlashCommand(bot)

bot.load_extension("cog")
bot.run("discord_token")

# cog.py
from discord import Embed
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext

class Slash(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @cog_ext.cog_slash(name="test")
    async def _test(self, ctx: SlashContext):
        embed = Embed(title="Embed Test")
        await ctx.send(embed=embed)

def setup(bot: Bot):
    bot.add_cog(Slash(bot))
```

## Buttons
This basic example shows how to easily integrate buttons into your commands. Buttons are not limited to
slash commands and may be used in regular discord.py commands as well.

```py
from discord_slash.component import Button, ButtonStyle

buttons = [
    Button(style=ButtonStyle.green, label="A green button"),
    Button(style=ButtonStyle.blue, label="A blue button")
]

await ctx.send(components=[buttons])
```

### Advanced
For more advanced use, please refer to our official documentation on [buttons here.](https://discord-py-interactions.readthedocs.io/en/latest/components.html#responding-to-interactions)

## Selects
This basic example shows how to add selects into our bot. Selects offer the same accessibility as buttons do
in premise of limitations.

```py
from discord_slash.component import Select, SelectOption

select = Select(
    options=[
        SelectOption(label="Lab Coat", value="coat", emoji="🥼"),
        SelectOption(label="Test Tube", value="tube", emoji="🧪"),
        SelectOption(label="Petri Dish", value="dish", emoji="🧫")
    ],
    placeholder="Choose your option",
    min_values=1, # the minimum number of options a user must select
    max_values=2 # the maximum number of options a user can select
)

await ctx.send(components=[action_row])
```

### Advanced
For more advanced use, please refer to our official documentation on [selects here.](https://discord-py-interactions.readthedocs.io/en/latest/components.html#what-about-selects-dropdowns)

## Context Menus
This basic example shows how to add a message context menu.

```py
from discord_slash.context import MenuContext
from discord_slash.model import ContextMenuType

@slash.context_menu(target=ContextMenuType.MESSAGE,
                    name="commandname",
                    guild_ids=[789032594456576001])
async def commandname(ctx: MenuContext):
    await ctx.send(
        content=f"Responded! The content of the message targeted: {ctx.target_message.content}",
        hidden=True
    )
```

### Advanced
For more advanced use, please refer to our official documentation on [context menus here.](https://discord-py-interactions.readthedocs.io/en/latest/gettingstarted.html#adding-context-menus)

--------

- The discord-interactions library is based off of API gateway events. If you are looking for a library webserver-based, please consider:
    - [dispike](https://github.com/ms7m/dispike)
    - [discord-interactions-python](https://github.com/discord/discord-interactions-python)
- If you are looking for a similar library for other languages, please refer to here:
    - [discord-api-docs Community Resources: Interactions](https://discord.com/developers/docs/topics/community-resources#interactions)
