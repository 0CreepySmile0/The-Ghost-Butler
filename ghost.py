import discord
from discord import app_commands
from datetime import datetime
from os import getenv
from dotenv import load_dotenv


load_dotenv()
intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
TOKEN = getenv("GHOST")
HOME = discord.Object(id=898841935937163286)
guilds = lambda: {i.id: i for i in client.guilds}
RED = 0xff0000
YELLOW = 0xffea00
GREEN = 0x30ff00


# @tree.command(
#     name="kick",
#     description="Kick someone's ass outta server"
# )
# @app_commands.checks.has_permissions(administrator=True)
# async def kick(interaction: discord.Interaction, member: discord.Member):
#     if member.id == interaction.user.id:
#         await interaction.response.send_message("You can't kick yourself, dumb", ephemeral=True)
#     else:
#         await interaction.response.\
#             send_message(f"Successfully kick {member.mention}", ephemeral=True)
#         await interaction.\
#             guild.kick(member, reason=f"You were kicked by {interaction.user.mention}")


@tree.command(
    name="avatar",
    description="Get avatar image"
)
async def avatar(interaction: discord.Interaction, member: discord.Member = None):
    if member is None:
        who = interaction.user
    else:
        who = member
    image = who.display_avatar.url
    embed = discord.Embed(
        title=f"{who.display_name}'s Avatar",
        color=who.color
    )
    embed.set_image(url=image)
    await interaction.response.send_message(embed=embed)


@tree.command(
    name="global_avatar",
    description="Get global avatar image"
)
async def global_avatar(interaction: discord.Interaction, member: discord.Member = None):
    if member is None:
        who = interaction.user
    else:
        who = member
    image = who.avatar.url
    embed = discord.Embed(
        title=f"{who.global_name}'s Avatar",
        color=who.accent_color
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
async def on_member_join(member: discord.Member):
    if member.guild.id == HOME.id:
        channel = client.get_channel(1193183104815345734)
        emoji = member.guild.get_emoji(1181521817618370562)
        message = discord.Embed(
            title="Welcome!",
            description=f"***{member.mention} ({member.name})*** ไม่ได้พบกันนานเลยนะ {emoji}",
            color=member.accent_color,
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
            color=member.color,
            timestamp=datetime.now()
        )
        message.set_image(url=member.display_avatar.url)
        await channel.send(embed=message)


@client.event
async def on_member_update(before: discord.Member, after: discord.Member):
    if after.guild.id == HOME.id:
        boost_role = after.guild.get_role(996733822500610128)
        if (boost_role in after.roles) and (boost_role not in before.roles):
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


@client.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    if before.author == client.user:
        return
    if after.guild.id == HOME.id:
        author = before.author
        embed = discord.Embed(title=f"Message edited at {after.jump_url}",
                              timestamp=datetime.now(),
                              description=f"**Message by {author.mention}**",
                              color=YELLOW)
        embed.add_field(name="Before", value=f"*Content:* {before.content}", inline=False)
        embed.add_field(name="After", value=f"*Content:* {after.content}", inline=False)
        embed.set_footer(text=f"{author.display_name} ({author.id})",
                         icon_url=author.display_avatar.url)
        message_channel = client.get_channel(1214605219770667101)
        await message_channel.send(embed=embed)


@client.event
async def on_message_delete(message: discord.Message):
    if message.author == client.user:
        return
    if message.guild.id == HOME.id:
        author = message.author
        embed = discord.Embed(title=f"Message deleted at {message.channel.mention}",
                              timestamp=datetime.now(),
                              description=f"**Message by {author.mention}**",
                              color=RED)
        embed.add_field(name="Deleted", value=f"*Content:* {message.content}", inline=False)
        embed.set_footer(text=f"{author.display_name} ({author.id})",
                         icon_url=author.display_avatar.url)
        message_channel = client.get_channel(1214605219770667101)
        await message_channel.send(embed=embed)


@client.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    if member == client.user:
        return
    if member.guild.id == HOME.id:
        message_channel = client.get_channel(1214605381393846323)
        if (before.channel is None) and (after.channel is not None):
            embed = discord.Embed(title="Joined",
                                  description=f"{member.mention} join voice channel",
                                  color=GREEN,
                                  timestamp=datetime.now())
            embed.add_field(name="Current", value=f"{after.channel.mention}", inline=False)
            embed.set_footer(text=f"{member.display_name} ({member.id})",
                             icon_url=member.display_avatar.url)
            await message_channel.send(embed=embed)
        elif (before.channel is not None) and (after.channel is None):
            embed = discord.Embed(title="Disconnected",
                                  description=f"{member.mention} leave voice channel",
                                  color=RED,
                                  timestamp=datetime.now())
            embed.add_field(name="Last channel", value=f"{before.channel.mention}", inline=False)
            embed.set_footer(text=f"{member.display_name} ({member.id})",
                             icon_url=member.display_avatar.url)
            await message_channel.send(embed=embed)
        elif (before.channel is not None) and (after.channel is not None):
            embed = discord.Embed(title="Moved",
                                  description=f"{member.mention} change voice channel",
                                  color=YELLOW,
                                  timestamp=datetime.now())
            embed.add_field(name="From", value=f"{before.channel.mention}", inline=False)
            embed.add_field(name="To", value=f"{after.channel.mention}", inline=False)
            embed.set_footer(text=f"{member.display_name} ({member.id})",
                             icon_url=member.display_avatar.url)
            await message_channel.send(embed=embed)


@client.event
async def on_ready():
    await tree.sync()
    activity = discord.Activity(type=discord.ActivityType.watching, name="How to do chores")
    await client.change_presence(activity=activity)
    print(f"Logged in as {client.user}")


client.run(TOKEN)
