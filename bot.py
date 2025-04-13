from keep_alive import keep_alive
import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import re
import asyncio
import logging
import sys
from flask import Flask
from threading import Thread

load_dotenv()

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

GUILD_ID = 1278677581209796618
TICKET_CHANNEL_PREFIX = "ticket-"
ROLE_NAME = "UNION CITIZEN"
REMOVE_ROLE_NAME = "Undocumented"

@tasks.loop(minutes=1)
async def check_bot_status():
    logging.info("Checking bot status...")

@bot.event
async def on_ready():
    print(f"{bot.user} 로그인 완료")
    check_bot_status.start()

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if not message.channel.name.startswith(TICKET_CHANNEL_PREFIX):
        return

    try:
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
    except Exception as e:
        logging.error(f"Error processing message: {e}")
    
    await bot.process_commands(message)

async def restart_bot():
    logging.info("Bot is restarting...")
    os.execv(sys.executable, ['python'] + sys.argv)

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()

keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))
