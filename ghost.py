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
HOME = discord.Object(id=898841935937163286)
guilds = lambda: {i.id: i for i in client.guilds}


@tree.command(
    name="avatar",
    description="Get avatar image"
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


@tree.command(
    name="ping",
    description="Show bot latency"
)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong: **{client.latency:.2f} ms**")


@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user}")


@client.event
async def on_member_join(member: discord.Member):
    if member.guild.id == HOME.id:
        channel = client.get_channel(1193183104815345734)
        emoji = member.guild.get_emoji(1181521817618370562)
        message = discord.Embed(
            title="Welcome!",
            description=f"***{member.mention} ({member.name})*** ไม่ได้พบกันนานเลยนะ {emoji}",
            color=discord.Color.random(),
            timestamp=datetime.now()
        )
        message.set_image(url=member.display_avatar.url)
        await channel.send(embed=message)


@client.event
async def on_member_remove(member: discord.Member):
    if member.guild.id == HOME.id:
        channel = client.get_channel(898847240460845077)
        emoji = member.guild.get_emoji(1181847726216986664)
        message = discord.Embed(
            title="Goodbye~",
            description=f"April showers bring may flowers ***{member.mention} ({member.name})*** "
                        f"{emoji}",
            color=discord.Color.random(),
            timestamp=datetime.now()
        )
        message.set_image(url=member.display_avatar.url)
        await channel.send(embed=message)


@client.event
async def on_member_update(before: discord.Member, after: discord.Member):
    if after.guild.id == HOME.id:
        if after.guild.get_role(996733822500610128) in after.roles:
            channel = after.guild.system_channel
            emoji = after.guild.get_emoji(1108248544101539911)
            emoji2 = after.guild.get_emoji(1181847701726441502)
            embed = discord.Embed(
                title="Thank you!",
                description=f"""***{after.mention} ({after.name})***
ขอบคุณสำหรับการซัพพอร์ต หวังว่าเราจะได้มีโอกาสตอบแทนคุณ...{emoji2}{emoji}""",
                color=0xff00d8,
                timestamp=datetime.now()
            )
            embed.set_image(url=after.display_avatar.url)
            await channel.send(embed=embed)


@client.event
async def on_message(message: discord.Message):
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
