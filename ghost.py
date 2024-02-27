import discord
from discord.ext import commands
from datetime import datetime
from os import getenv
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.all()
client = commands.Bot(command_prefix=".", intents=intents)
TOKEN = getenv("TOKEN")


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_member_join(member):
    channel = client.get_channel(1193183104815345734)
    message = discord.Embed(
        title="Welcome",
        description=f"***{member.name}*** ไม่ได้พบกันนานเลยนะ =)",
        color=discord.Color.random(),
        timestamp=datetime.now(),
    )
    await channel.send(embed=message)


@client.event
async def on_member_remove(member):
    channel = client.get_channel(898847240460845077)
    message = discord.Embed(
        title="Goodbye",
        description=f"April showers bring may flowers ***{member.name}***",
        color=discord.Color.random(),
        timestamp=datetime.now(),
    )
    await channel.send(embed=message)


@client.event
async def on_message(message):
    admin_id = [812919079278608415, 759707563704057877]
    server = client.get_guild(898841935937163286)
    role_id = [1181437334638567484, 1108179331076861953, 1181623448259268669, 1181441664255004775]
    role = [discord.utils.get(server.roles, id=i) for i in role_id]
    if message.author == client.user:
        return None
    if message.channel.id == 1212011324033470566:
        if message.content == ".":
            await message.author.add_roles(*role)
    if message.author.id not in admin_id:
        await message.delete(delay=2.0)


client.run(TOKEN)
