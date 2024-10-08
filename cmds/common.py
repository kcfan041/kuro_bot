import discord
from discord import app_commands
from discord.ext import commands
from discord import Webhook
from core.classes import CE
import subprocess
import requests
import aiohttp
import asyncio
import time
import json
import sys
import os

class common(CE):
    with open('./setting/world_config.json','r',encoding='utf8') as jfile:
        world_config = json.load(jfile)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} 已載入")

    @commands.command()
    async def sync(self,ctx: commands.Context):
        fmt = await ctx.bot.tree.sync()
        await ctx.send(f"{len(fmt)}")
        
    @app_commands.command(name= "restart_bot")
    async def restart_bot(self,i: discord.Interaction):
        with open('./setting/setting.json','r',encoding='utf8') as jfile:
            setting = json.load(jfile)
        await i.response.defer()
        if i.user.id == setting["owner"]:
            message = await i.followup.send("執行重啟中..",ephemeral=False)
            if "response" not in setting["last_ready_time"]:
                setting["last_ready_time"]["response"] = {}
            setting["last_ready_time"]["response"]["message_id"] = message.id
            setting["last_ready_time"]["response"]["channel_id"] = i.channel.id
            setting["last_ready_time"]["response"]["need_response"] = 1
            with open('./setting/setting.json', 'w', encoding='utf8') as jfile:
                json.dump(setting, jfile, indent=4)
            subprocess.Popen([r"C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp\\kmaid.bat"])
            await self.bot.close()
            sys.exit()
        else:
            await i.response.send_message("你不是擁有者..")
            
    @app_commands.command(name= "help",description="show all commands")
    async def help(self,i: discord.Interaction):
        embed = discord.Embed(title="命令列表")

        for cog_name, cog in self.bot.cogs.items():
            for command in cog.get_app_commands():
                if command.description == "…":
                    text = "無"
                else:
                    text = command.description
                embed.add_field(name=command.name, value=f" 來自 {cog_name}\n 敘述 {text}", inline=False)
        await i.response.send_message(embed=embed)
        
    @app_commands.command(name= "set_owner")
    async def set_owner(self,i: discord.Interaction):
        with open('./setting/setting.json','r',encoding='utf8') as jfile:
            setting = json.load(jfile)

        setting["owner"] = i.user.id
        
        with open('./setting/setting.json','w',encoding='utf8') as jfile:
            json.dump(setting,jfile,indent=4)

    # @app_commands.command(name= "delete") #無用
    # async def delete(self,i: discord.Interaction):
    #     with open('./setting/webhook_url.json','r',encoding='utf8') as jfile:
    #         webhook_url = json.load(jfile)
    #     with open('./setting/world.json','r',encoding='utf8') as jfile:
    #         world = json.load(jfile)
    #     with open('./setting/world_config.json','r',encoding='utf8') as jfile:
    #         world_config = json.load(jfile)

    #     await i.response.send_message(f'正在刪除')

    #     for w in webhook_url:
    #         webhook = await i.guild.webhooks()
    #         for x in webhook:
    #             if str(w) == str(x.url):
    #                 async with aiohttp.ClientSession() as session:
    #                     webhook = Webhook.from_url(w, session=session)
    #                     await webhook.delete(reason="restart")
    #                     del webhook_url[str(i.guild.id)]

    #     #刪除頻道
    #     for g in world:
    #         if str(g) == str(i.guild_id):
    #             for w in world[str(i.guild_id)]["world"]:
    #                 for x in world[str(i.guild_id)]["world"][w]:
    #                     for y in world[str(i.guild_id)]["world"][w][x]:
    #                         ID = world[str(i.guild_id)]["world"][w][x][y]
    #                         try:
    #                             channel = self.bot.get_channel(ID)
    #                             await channel.delete()
    #                         except:
    #                             pass
        
    #     del world[str(i.guild_id)]
    #     del webhook_url[str(i.guild.id)]

    #     with open('./setting/webhook_url.json','w',encoding='utf8') as jfile:
    #         json.dump(webhook_url,jfile,indent=4)
    #     with open('./setting/world.json','w',encoding='utf8') as jfile:
    #         json.dump(world,jfile,indent=4)
    #     await i.edit_original_response(content=f'刪除完成')

    @app_commands.command(name = "clear")
    @app_commands.describe(num="你想要刪除的行數")
    async def clear(self,i: discord.Integration,num:int):
        await i.response.send_message(f"即將刪除{num}則訊息",ephemeral=True)
        await i.channel.purge(limit=num)
        await i.edit_original_response(content=f'已刪除{num}則訊息')
        await asyncio.sleep(2)
        await i.delete_original_response()

    # @app_commands.command(name = "webhook_test") #無用
    # @app_commands.describe(text="text")
    # async def webhook_test(self,i: discord.Interaction,text:str):
    #     with open('./setting/webhook_url.json','r',encoding='utf8') as jfile:
    #         webhook_url = json.load(jfile)

    #     print(i.response.is_done())

    #     async with aiohttp.ClientSession() as session:
    #         webhook = Webhook.from_url(webhook_url[str(i.guild.id)], session=session)
    #         await webhook.send(content=text,username="test_bot")

    # @app_commands.command(name = "add_twitchstreamer") #無用
    # @app_commands.describe(twitch_id="twitch_id")
    # async def add_twitchstreamer(self,i: discord.Integration,twitch_id:str):
    #     with open('./setting/twitch_id.json','r',encoding='utf8') as jfile:
    #         tid = json.load(jfile)
    #     tid[str(twitch_id)] = twitch_id
    #     with open('./setting/twitch_id.json','w',encoding='utf8') as jfile:
    #         json.dump(tid,jfile,indent=4)
    #     await i.response.send_message(f"已添加{twitch_id}進列表",ephemeral=True)

    @app_commands.command(name = "getip")
    async def getip(self,i:discord.Interaction):
        if True:
        # if(i.user.id==449950100861747200):
            ip = requests.get('https://api.ipify.org').text
            await i.response.send_message(ip)
        else:
            await i.response.send_message(f"你不是擁有者")

    

async def setup(bot):
    await bot.add_cog(common(bot))