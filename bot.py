import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import re

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

GUILD_ID = 1278677581209796618
TICKET_CHANNEL_PREFIX = "ticket-"
ROLE_NAME = "UNION CITIZEN"
REMOVE_ROLE_NAME = "Undocumented"

@bot.event
async def on_ready():
    print(f"{bot.user} 로그인 완료")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if not message.channel.name.startswith(TICKET_CHANNEL_PREFIX):
        return

    name_match = re.search(r"^이름\s*[:：]\s*(.+)$", message.content, re.MULTILINE)
    family_match = re.search(r"^가문\s*[:：]\s*(.+)$", message.content, re.MULTILINE)

    if name_match and family_match:
        name = name_match.group(1).strip()
        family = family_match.group(1).strip()
        nickname = f"자유시민 {name} {family}"

        guild = bot.get_guild(GUILD_ID)
        member = guild.get_member(message.author.id)

        add_role = discord.utils.get(guild.roles, name=ROLE_NAME)
        remove_role = discord.utils.get(guild.roles, name=REMOVE_ROLE_NAME)

        if add_role:
            await member.add_roles(add_role)
        if remove_role:
            await member.remove_roles(remove_role)

        await member.edit(nick=nickname)
        await message.channel.delete()

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))

