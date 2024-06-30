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


class FKBLM(CE):

    def __init__(self,bot:commands.Bot):
        self.temporary_channels = []
        self.temporary_categories = []

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} 已載入")

    @commands.Cog.listener()
    async def on_guild_channel_create(self,channel):
        with open('./setting/channel_role.json','r',encoding='utf8') as jfile:
            role_data = json.load(jfile)
        if channel.guild.id == int(1120396807906791576):
            if str(channel.type) == "voice" and channel.name == "討論":
                channelname = str(channel.category.name) + str(channel.name)
                role_data[str(channel.id)] = (await channel.guild.create_role(name = channelname)).id
                print(f"新增身份組{channelname},原因：on_guild_channel_create")
            elif str(channel.type) == "category":
                pass
            else:
                role_data[str(channel.id)] = (await channel.guild.create_role(name = channel.name)).id
                print(f"新增身份組{channel.name},原因：on_guild_channel_create")
            with open('./setting/channel_role.json','w',encoding='utf8') as jfile:
                json.dump(role_data,jfile,indent=4)
            if(str(channel.type)=="text"):
                await channel.set_permissions(channel.guild.roles[0],view_channel=False)
                await channel.set_permissions(channel.guild.get_role(role_data[str(channel.id)]),view_channel=True)
                print(f"修改頻道{channel.name} {channel.id}至身分組特定")

    @commands.Cog.listener()
    async def on_guild_channel_delete(self,channel):
        with open('./setting/channel_role.json','r',encoding='utf8') as jfile:
            role_data = json.load(jfile)
        if channel.guild.id == int(1120396807906791576):
            if str(channel.id) in role_data:
                await (channel.guild.get_role(role_data[str(channel.id)])).delete()
                print(f"移除身份組{channel.name},原因：on_guild_channel_delete")
                del role_data[str(channel.id)]
                with open('./setting/channel_role.json','w',encoding='utf8') as jfile:
                    json.dump(role_data,jfile,indent=4) 

    #學習重點
    @commands.Cog.listener()
    async def on_voice_state_update(self,member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        possible_channel_name = f"{member.nick}'s area"
        
        if str(member.nick) == "None":
            if str(member.global_name) == "None":
                pn = f"{member.name}發呆"
            else:
                pn = f"{member.global_name}發呆"
        else:
            pn = f"{member.nick}發呆" 
                
            
        if after.channel:
            if after.channel.name == "發呆":
                temp_channel = await after.channel.clone(name=pn)
                await member.move_to(temp_channel)
                self.temporary_channels.append(temp_channel.id)
            # if after.channel.name == 'teams':
            #     temporary_category = await after.channel.guild.create_category(name=possible_channel_name)
            #     await temporary_category.create_text_channel(name="text")
            #     temp_channel = await temporary_category.create_voice_channel(name="voice")
            #     await member.move_to(temp_channel)
            #     temporary_categories.append(temp_channel.id)


        if before.channel:
            if before.channel.id in self.temporary_channels:
                if len(before.channel.members) == 0:
                    await before.channel.delete()
            if before.channel.id in self.temporary_categories:
                if len(before.channel.members) == 0:
                    for channel in before.channel.category.channels:
                        await channel.delete()
                    await before.channel.category.delete()

    @commands.Cog.listener()
    async def on_message(self,m):
        key = ["hi","Hi"]
        if str(m.content) in key and m.author != bot.user:
            await m.channel.send("hi")

        await bot.process_commands(m)
    
    @app_commands.command(name = "add_project")
    @app_commands.describe(project_name="你想要的專案名稱",channel_name="你想要主頻道的名稱",user="請的@方式添加")
    async def add_project(self,i: discord.Integration,project_name:str,channel_name:str,user:str):
        userlist=user.split()
        category=await i.guild.create_category_channel(name=project_name)
        asyncio.sleep(1)
        text=await i.guild.create_text_channel(name=channel_name,category=category)
        asyncio.sleep(1)
        voice=await i.guild.create_voice_channel(name=f"討論",category=category)
        c=0
        while c<(len(userlist))*2:
            with open('./setting/channel_role.json','r',encoding='utf8') as jfile:
                role_data = json.load(jfile)
            c=0
            await asyncio.sleep(1)
            for rid in role_data:
                if str(text.id)==rid:
                    for x in userlist:
                        u=i.guild.get_member(int(x[2:-1]))
                        r=i.guild.get_role(role_data[rid])
                        ok=0
                        for ur in u.roles:
                            if ur.id==r.id:
                                ok=1
                                c+=1
                        if ok==0:
                            await u.add_roles(r)
                            print(f"已將{u}新增至{r}身份組中")
                if str(voice.id)==rid:
                    for x in userlist:
                        u=i.guild.get_member(int(x[2:-1]))
                        r=i.guild.get_role(role_data[rid])
                        ok=0
                        for ur in u.roles:
                            if ur.id==r.id:
                                ok=1
                                c+=1
                        if ok==0:
                            await u.add_roles(r)
                            print(f"已將{u}新增至{r}身份組中")
        await voice.set_permissions(voice.guild.roles[0],view_channel=False)
        await voice.set_permissions(voice.guild.get_role(role_data[str(voice.id)]),view_channel=True)
        print("執行完畢")

    # @app_commands.command(name = "end_project")
async def setup(bot):
    await bot.add_cog(FKBLM(bot))