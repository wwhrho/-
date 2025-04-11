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
AUTH_CHANNEL_CATEGORY_ID = 1287381448810037258
ROLE_NAME = "UNION CITIZEN"
REMOVE_ROLE_NAME = "Undocumented"

@bot.event
async def on_ready():
    print(f"{bot.user} 로그인 완료")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    print(f"메시지 수신: {message.content}")

    if not message.channel.name.startswith(TICKET_CHANNEL_PREFIX):
        print("채널 이름이 ticket-으로 시작하지 않음")
        return

    if message.channel.category_id != AUTH_CHANNEL_CATEGORY_ID:
        print("카테고리 ID 불일치")
        return

    name_match = re.search(r"이름\s*[:：]\s*(.+)", message.content)
    family_match = re.search(r"가문\s*[:：]\s*(.+)", message.content)

    if not name_match:
        print("이름 못 찾음")
    if not family_match:
        print("가문 못 찾음")

    if name_match and family_match:
        name = name_match.group(1).strip()
        family = family_match.group(1).strip()
        nickname = f"자유시민 {name} {family}"
        print(f"닉네임 설정 시도: {nickname}")

        guild = bot.get_guild(GUILD_ID)
        member = guild.get_member(message.author.id)

        add_role = discord.utils.get(guild.roles, name=ROLE_NAME)
        remove_role = discord.utils.get(guild.roles, name=REMOVE_ROLE_NAME)

        if add_role:
            await member.add_roles(add_role)
            print(f"{ROLE_NAME} 역할 부여")
        if remove_role:
            await member.remove_roles(remove_role)
            print(f"{REMOVE_ROLE_NAME} 역할 제거")

        await member.edit(nick=nickname)
        print(f"닉네임 변경 완료: {nickname}")

        await message.channel.delete()
        print("채널 삭제 완료")

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
