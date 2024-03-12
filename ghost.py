import os
import discord
from discord import app_commands
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()
intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
TOKEN = os.getenv("GHOST")
HOME = discord.Object(898841935937163286)
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
#

@tree.command(
    name="รับยศ",
    description="ใช้คำสั่งนี้รับยศ Member เพื่อจะได้เห็นห้องอื่นๆเพิ่มเติม",
    guild=client.get_guild(898841935937163286)
)
async def get_roles(interaction: discord.Interaction):
    if interaction.channel.id == 1212011324033470566:
        role_id = [1181437334638567484, 1108179331076861953, 1181623448259268669,
                   1181441664255004775]
        server = client.get_guild(898841935937163286)
        roles = [discord.utils.get(server.roles, id=i) for i in role_id]
        emoji = client.get_emoji(1181847879174856834)
        embed = discord.Embed(
            title="Successfully add roles!",
            description=f"เราได้เพิ่มยศ {roles[1].mention} ให้คุณแล้ว, สำรวจดิสของเราได้เลยนะ {emoji}",
            color=interaction.user.accent_color
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        await interaction.user.add_roles(*roles)
    else:
        channel = client.get_channel(1212011324033470566)
        emoji = client.get_emoji(1181847802612027413)
        embed = discord.Embed(
            title="Invalid channel",
            description=f"ใช้คำสั่งนี้ได้แค่ที่ห้อง {channel.mention} เท่านั้นน้า {emoji}",
            color=interaction.user.accent_color
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


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
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    if message.guild.id == HOME.id:
        if message.is_system():
            if message.type == discord.MessageType.premium_guild_subscription:
                channel = client.get_channel(1181486685477941290)
                emoji = message.guild.get_emoji(1108248544101539911)
                emoji2 = message.guild.get_emoji(1181847701726441502)
                embed = discord.Embed(
                    title="Thank you!",
                    description=f"""***{message.author.mention} ({message.author.name})***
                ขอบคุณสำหรับการซัพพอร์ต หวังว่าเราจะได้มีโอกาสตอบแทนคุณ...{emoji2}{emoji}""",
                    color=0xff00d8,
                    timestamp=datetime.now()
                )
                embed.set_image(url=message.author.display_avatar.url)
                await channel.send(embed=embed)


@client.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    if before.author == client.user:
        return
    if before.content == after.content:
        return
    if before.guild.id == HOME.id:
        files = []
        author = before.author
        embed = discord.Embed(title=f"Message edited at {after.jump_url}",
                              timestamp=datetime.now(),
                              description=f"**Message by {author.mention}**",
                              color=YELLOW)
        if len(before.content) >= 1024:
            name = "before.txt"
            with open(name, "w") as f:
                f.write(before.content)
            file = os.path.join(name)
            files.append(discord.File(fp=file))
            before_content = "***In before.txt on top***"
        else:
            before_content = before.content
        if len(after.content) >= 1024:
            name = "after.txt"
            with open(name, "w") as f:
                f.write(after.content)
            file = os.path.join(name)
            files.append(discord.File(fp=file))
            after_content = "***In after.txt on top***"
        else:
            after_content = after.content
        embed.add_field(name="Before:", value=before_content, inline=False)
        embed.add_field(name="After:", value=after_content, inline=False)
        embed.set_footer(text=f"{author.display_name} ({author.id})",
                         icon_url=author.display_avatar.url)
        message_channel = client.get_channel(1214605219770667101)
        await message_channel.send(embed=embed, files=files)
        for i in files:
            os.remove(i.filename)


@client.event
async def on_message_delete(message: discord.Message):
    if message.is_system():
        return
    if message.author == client.user:
        return
    if message.guild.id == HOME.id:
        author = message.author
        files = []
        message_channel = client.get_channel(1214605219770667101)
        embed = discord.Embed(title=f"Message deleted at {message.channel.mention}",
                              timestamp=datetime.now(),
                              description=f"**Message by {author.mention}**",
                              color=RED)
        if len(message.content) >= 1024:
            name = "text.txt"
            with open(name, "w") as f:
                f.write(message.content)
            file = os.path.join(name)
            files.append(discord.File(fp=file))
            content = "***In text.txt on top***"
        else:
            content = message.content
        if message.attachments:
            for i in message.attachments:
                await i.save(i.filename)
                file = os.path.join(i.filename)
                files.append(discord.File(fp=file))
        embed.add_field(name="Content:", value=content, inline=False)
        embed.set_footer(text=f"{author.display_name} ({author.id})",
                         icon_url=author.display_avatar.url)
        await message_channel.send(embed=embed, files=files)
        for i in files:
            os.remove(i.filename)


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
        elif before.channel != after.channel:
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
