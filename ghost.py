import discord
from discord import app_commands
from datetime import datetime
from os import getenv
from dotenv import load_dotenv
import typing


load_dotenv()
intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
TOKEN = getenv("TOKEN")
GUILD = discord.Object(id=898841935937163286)


@tree.command(
    name="avatar",
    description="Get your avatar image",
    guild=GUILD
)
async def avatar(interaction: discord.Interaction, member: typing.Optional[discord.Member]=None):
    if member is None:
        who = interaction.user
    else:
        who = member
    image = who.display_avatar.url
    embed = discord.Embed(
        title=f"{who.display_name}'s Avatar",
        color=discord.Color.random()
    )
    embed.set_image(url=image)
    await interaction.response.send_message(embed=embed)


@client.event
async def on_ready():

    await tree.sync(guild=GUILD)
    print(f"Logged in as {client.user}")


@client.event
async def on_member_join(member):
    if member.guild == GUILD:
        channel = client.get_channel(1193183104815345734)
        message = discord.Embed(
            title="Welcome",
            description=f"***{member.mention} ({member.name})*** ไม่ได้พบกันนานเลยนะ =)",
            color=discord.Color.random(),
            timestamp=datetime.now(),
        )
        message.set_image(url=member.display_avatar.url)
        await channel.send(embed=message)


@client.event
async def on_member_remove(member):
    if member.guild == GUILD:
        channel = client.get_channel(898847240460845077)
        message = discord.Embed(
            title="Goodbye",
            description=f"April showers bring may flowers ***{member.mention} ({member.name})***",
            color=discord.Color.random(),
            timestamp=datetime.now(),
        )
        message.set_image(url=member.display_avatar.url)
        await channel.send(embed=message)


@client.event
async def on_message(message):
    if message.channel.id == 1212011324033470566:
        admin_id = [812919079278608415, 759707563704057877]
        server = client.get_guild(898841935937163286)
        role_id = [1181437334638567484, 1108179331076861953, 1181623448259268669,
                   1181441664255004775]
        role = [discord.utils.get(server.roles, id=i) for i in role_id]
        if message.author == client.user:
            return None
        if message.content == ".":
            await message.author.add_roles(*role)
            await message.delete(delay=2.0)
        if message.author.id not in admin_id:
            await message.delete(delay=2.0)


client.run(TOKEN)
