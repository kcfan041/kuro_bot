import discord
from dotenv import load_dotenv
from discord.ext import commands
import asyncio
import datetime
import json
import os

load_dotenv()   
TOKEN = os.getenv("TOKEN")
application_id = os.getenv("application_id")
bot = commands.Bot(command_prefix=".",intents=discord.Intents.all(),application_id=application_id)

@bot.event
async def on_ready():
    print("更新指令")
    await bot.tree.sync()
    print("更新指令完成")
    print("更新時間")
    await update_last_ready_time()
    print("更新時間完成")
    print("更新簡介")
    text = "kuro v0.1.4"
    print(text)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=text))
    print("更新簡介完成")
    print("啟動成功")
    
async def update_last_ready_time():
    now = datetime.datetime.now()
    time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    print(time_str)
    with open('./setting/setting.json', 'r', encoding='utf8') as jfile:
        setting = json.load(jfile)
    if "last_ready_time" not in setting:
        setting["last_ready_time"] = {}
        setting["last_ready_time"]["time"] = time_str
    else:
        if "response" in setting["last_ready_time"]:
            if setting["last_ready_time"]["response"]["need_response"] == 1:
                channel = bot.get_channel(setting["last_ready_time"]["response"]["channel_id"])
                message = await channel.fetch_message(setting["last_ready_time"]["response"]["message_id"])
                await message.edit(content="kuro已成功重啟")
                setting["last_ready_time"]["response"]["need_response"] = 0
    with open('./setting/setting.json', 'w', encoding='utf8') as jfile:
        json.dump(setting, jfile, indent=4)
    
async def load():
    for file in os.listdir('./cmds'):
        if file.endswith('.py'):
            await bot.load_extension(f'cmds.{file[:-3]}')

async def main():
    await load()
    await bot.start(TOKEN)

asyncio.run(main())

