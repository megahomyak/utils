import discord
from discord.ext import commands
import asyncio

states = {}

intents = discord.Intents.default()
intents.guild_reactions = True
client = commands.Bot(command_prefix="", intents=intents, self_bot=True)


CANDY_DERP = "<:CandyDerp:1050542180411904082>"
PHI_LETS_GO = "<:PhiLetsGo:1052801687066263582>"
POPGOES_2 = "<:popgoes2:1023025784169967676>"
PHI_CRY = "<:PhiCry:1016190512241328241>"
PHI_HYPE = "<:PhiHype:1016190502351147038>"
POPGOES_LEFT_HEAD = "<:popgoesLeftHead:1023025793695236140>"
POPGOES_RIGHT_TAIL = "<:popgoesRightTail:1023025800171245579>"
POPGOES_HORI = "<:popgoesHori:1023025791644225597>"


@client.event
async def on_ready():
    print("Starting!")


@client.event
async def on_reaction_remove(reaction: discord.Reaction, _user):
    await on_reaction_modification(reaction, -1)


@client.event
async def on_reaction_add(reaction: discord.Reaction, _user):
    await on_reaction_modification(reaction, 1)


async def on_reaction_modification(reaction: discord.Reaction, bias: int):
    async with asyncio.Lock():
        try:
            index = states[reaction.message.id]
        except KeyError:
            return
        if str(reaction.emoji) == CANDY_DERP:
            index -= bias
        elif str(reaction.emoji) == PHI_LETS_GO:
            index += bias
        else:
            return
        if index == -1:
            new_message_text = f":trophy:{CANDY_DERP} Candy won! {POPGOES_2}{PHI_CRY}"
            del states[reaction.message.id]
        elif index == 11:
            new_message_text = f"{CANDY_DERP}{POPGOES_2} Phisnom won! {PHI_HYPE}:Trophy:"
            del states[reaction.message.id]
        else:
            new_message_text = make_output(index)
            states[reaction.message.id] = index
        await reaction.message.edit(content=new_message_text)


def make_output(left_side_index):
    return "React with the emoji you want to win:\n\n:trophy:" + POPGOES_2 * left_side_index + CANDY_DERP + POPGOES_LEFT_HEAD + POPGOES_HORI * 5 + POPGOES_RIGHT_TAIL + PHI_LETS_GO + POPGOES_2 * (10 - left_side_index) + ":trophy:"


states = {}


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user and message.content == "/weaslopull":
        states[message.id] = 5
        await message.edit(content=make_output(5))


client.run(open("personal_discord_token.txt").read().strip(), bot=False)
