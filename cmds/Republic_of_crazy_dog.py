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


class Republic_of_crazy_dog(CE):

    def __init__(self,bot:commands.Bot):
        self.guild_id = 890892967991189534
        self.channel_id = 911276047331389530
        
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} 已載入")
        
        
        
    @app_commands.command(name= "update_member")
    async def update_member(self,i: discord.Interaction):
        channel = i.guild.get_channel(self.channel_id)
        get_member = i.guild.member_count
        channel_name = "目前成員:"+str(get_member)
        await channel.edit(name=channel_name)
        await i.response.send_message(f"已修改目前成員")
        
    # @app_commands.command(name = "minecraft")
    # async def getip(self,i:discord.Interaction):
    #     if(i.user.id==449950100861747200):
    #         ip = requests.get('https://api.ipify.org').text
    #         await i.response.send_message(ip)
    #     else:
    #         await i.response.send_message(f"你不是擁有者")
    
    
    
async def setup(bot):
    await bot.add_cog(Republic_of_crazy_dog(bot))