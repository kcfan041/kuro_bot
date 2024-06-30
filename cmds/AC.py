import discord
from discord import app_commands
from discord.ext import commands
from discord import Webhook
from core.classes import CE
import requests
import aiohttp
import asyncio
import time
import json
import os

class AC(CE):
    with open('./setting/setting.json','r',encoding='utf8') as jfile:
        setting = json.load(jfile)
    with open('./setting/world_config.json','r',encoding='utf8') as jfile:
        world_config = json.load(jfile)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} 已載入")

    
    @app_commands.command(name= "test")
    async def test(self,i: discord.Interaction):
        # await i.response.send_message(await i.guild.integrations().account)
        ttest = await i.guild.integrations()
        print(ttest)
        print(ttest.account)
        print(1)
        pass

    @app_commands.command(name = "restart")
    async def restart(self,i: discord.Interaction):
        with open('./setting/webhook_url.json','r',encoding='utf8') as jfile:
            webhook_url = json.load(jfile)
        with open('./setting/world.json','r',encoding='utf8') as jfile:
            world = json.load(jfile)
        with open('./setting/world_config.json','r',encoding='utf8') as jfile:
            world_config = json.load(jfile)

        await i.response.send_message(f'正在重新設置')
        
        for w in webhook_url:
            webhook = await i.guild.webhooks()
            for x in webhook:
                if str(w) == str(x.url):
                    async with aiohttp.ClientSession() as session:
                        webhook = Webhook.from_url(w, session=session)
                        await webhook.delete(reason="restart")
                        del webhook_url[str(i.guild.id)]

        #刪除頻道
        for g in world:
            if str(g) == str(i.guild_id):
                for w in world[str(i.guild_id)]["world"]:
                    for x in world[str(i.guild_id)]["world"][w]:
                        for y in world[str(i.guild_id)]["world"][w][x]:
                            ID = world[str(i.guild_id)]["world"][w][x][y]
                            try:
                                channel = self.bot.get_channel(ID)
                                await channel.delete()
                            except:
                                pass
        
        world[str(i.guild_id)]={}
        world[str(i.guild_id)]["world"] = world_config

        #新增頻道
        for w in world_config:
            text = f"{i.guild.name}_{w}"
            category = await i.guild.create_category_channel(name=text)
            world[str(i.guild_id)]["world"][w]["category"][text]=category.id
            world_config = world_config[w]
            for x in world_config:
                if x == "channel":
                    for y in world_config[x]:
                        channel = await i.guild.create_text_channel(name=y,category=category)
                        world[str(i.guild_id)]["world"][w][x][y]=channel.id
                if x == "voicechannel":
                    for y in world_config[x]:
                        channel = await i.guild.create_voice_channel(name=y,category=category)
                        world[str(i.guild_id)]["world"][w][x][y]=channel.id

        webhook = await i.guild.get_channel(world[str(i.guild_id)]["world"]["start_world"]["channel"]["start"]).create_webhook(name="NPC")
        webhook_url[str(i.guild.id)] = str(webhook.url)
        
        with open('./setting/webhook_url.json','w',encoding='utf8') as jfile:
            json.dump(webhook_url,jfile,indent=4)
        with open('./setting/world.json','w',encoding='utf8') as jfile:
            json.dump(world,jfile,indent=4)
        await i.edit_original_response(content=f'設定已重置')

    @app_commands.command(name = "add_ac_new_player")
    @app_commands.describe(name = "請輸入角色名稱")
    async def new_player(self,i: discord.Interaction,name:str):
        with open('character/new_player.json','r',encoding='utf8') as jfile:
            player = json.load(jfile)
        user = i.user.id
        player["name"] = name
        player["starttime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        with open(f'character/player/{user}.json','w',encoding='utf8') as jfile:
            json.dump(player,jfile,indent=4)
        await i.response.send_message(f"已新增角色：{name}")

    @app_commands.command(name = "add_ac_new_npc")
    @app_commands.describe(name = "請輸入角色名稱")
    async def new_NPC(self,i: discord.Interaction,name:str):
        with open('character/new_player.json','r',encoding='utf8') as jfile:
            player = json.load(jfile)
        user = i.user.id
        player["name"] = name
        player["starttime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        with open(f'character/npc/{name}.json','w',encoding='utf8') as jfile:
            json.dump(player,jfile,indent=4)
        await i.response.send_message(f"已新增NPC：{name}")

    # @app_commands.command(name = "")


async def setup(bot):
    await bot.add_cog(AC(bot))