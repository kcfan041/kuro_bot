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
        print("Republic of crazy dog serves 已載入")
        
        
        
    @app_commands.command(name= "update_member")
    async def update_member(self,i: discord.Interaction):
        channel = i.guild.get_channel(self.channel_id)
        get_member = i.guild.member_count
        channel_name = "目前成員:"+str(get_member)
        await channel.edit(name=channel_name)
        await i.response.send_message(f"已修改目前成員")
    
    
    
async def setup(bot):
    await bot.add_cog(Republic_of_crazy_dog(bot))