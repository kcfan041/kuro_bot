import discord
from dotenv import load_dotenv
from discord.ext import commands
import asyncio
import json
import os

load_dotenv()   
TOKEN = os.getenv("TOKEN")
application_id = os.getenv("application_id")
bot = commands.Bot(command_prefix=".",intents=discord.Intents.all(),application_id=application_id)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("啟動成功")

async def load():
    for file in os.listdir('./cmds'):
        if file.endswith('.py'):
            await bot.load_extension(f'cmds.{file[:-3]}')

async def main():
    await load()
    await bot.start(TOKEN)

asyncio.run(main())

