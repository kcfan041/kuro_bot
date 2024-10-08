import discord
from discord.ui import Button, View
from discord import app_commands
from discord.ext import commands
from core.classes import CE
import asyncio
import yt_dlp
import time
import json
import os


class music(CE):

    def __init__(self,bot:commands.Bot):
        self.queue = []
        self.bot = bot
        
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} 已載入")
        
        
    @app_commands.command(name= "play_music")
    async def play_music(self,i: discord.Interaction,url: str):
        voice_channel = i.user.voice.channel if i.user.voice else None
        if not voice_channel:
            return await i.response.send_message("找不到你存在的頻道..")
        if not i.guild.voice_client:
            await voice_channel.connect()
        await i.response.defer()
        ydl_opts = {
        'extract_flat': True,
        'ignoreerrors': True,
        'quiet': True,
        'playlistend': 50
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            if 'list=' in url:
                # print(1)
                info = ydl.extract_info(url=url, download=False)
                if 'entries' not in info:
                    info = ydl.extract_info(url=f"ytsearch:{info['url']}", download=False)
            else:
                info = ydl.extract_info(url=f"ytsearch:{url}", download=False)
            if 'entries' in info:
                await i.followup.send(content="處理下載中")
                # print(2)
                print(len(info['entries']))
                for entry in info['entries']:
                    # print(3)
                    if entry is None or 'id' not in entry:
                        print("無效影片，跳過")
                        continue
                    # print(3.5)
                    self.queue.append((entry['url'], entry['title']))
                    # print(4)
                    await i.followup.send(f'以新增至清單中: **{entry["title"]}**')
                    if not i.guild.voice_client.is_playing():
                        await self.play_next(i)
            
        if not i.guild.voice_client.is_playing():
            await self.play_next(i)
        
    async def play_next(self,interaction: discord.Interaction):
        if self.queue:
            url, title = self.queue.pop(0)
            FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
            }
            try:
                audio_url = await self.get_audio_url(url)
            except Exception as e:
                print(f"Error extracting audio: {e}")
            try:
                source = discord.FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS)
            except Exception as e:
                print(f"Error extracting audio: {e}")
            try:
                interaction.guild.voice_client.play(source, after=lambda _: self.bot.loop.create_task(self.play_next(interaction)))
            except Exception as e:
                print(f"Error extracting audio: {e}")
            view = MusicControlView()
            await interaction.followup.send(f"Now playing **{title}**", view=view)
        elif not interaction.guild.voice_client.is_playing():
            await asyncio.sleep(30)
            await interaction.guild.voice_client.disconnect()
            
    
    @app_commands.command(name= "skip_music")
    async def skip_music(self,i: discord.Interaction):
        if i.guild.voice_client and i.guild.voice_client.is_playing():
            i.guild.voice_client.stop()
        await i.response.send_message("音樂已跳過", ephemeral=True)
            
    async def get_audio_url(self,video_url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            
            # 檢查是否是播放列表，如果是則只取第一個條目
            if 'entries' in info_dict:
                info_dict = info_dict['entries'][0]

            # 提取最佳音頻格式的URL
            audio_url = info_dict.get('url', None)
            return audio_url
        
        
        
    @app_commands.command(name= "skip_all_music")
    async def skip_all_music(self,i: discord.Interaction):
        await i.response.send_message("正在清除歌單..")
        self.queue = []
        if i.guild.voice_client and i.guild.voice_client.is_playing():
            i.guild.voice_client.stop()
        await i.edit_original_response(content="清除完成")
        await asyncio.sleep(5)
        await i.guild.voice_client.disconnect()
        pass
    
class MusicControlView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.music_cog = music

    @discord.ui.button(emoji="⏯️")
    async def pause_button(self, interaction: discord.Interaction, button: Button):
        vc = interaction.guild.voice_client
        if vc and vc.is_playing():
            vc.pause()
            await interaction.response.send_message("音樂已暫停", ephemeral=True)
        elif vc and not vc.is_playing():
            vc.resume()
            await interaction.response.send_message("音樂已繼續播放", ephemeral=True)

    @discord.ui.button(emoji="⏭️")
    async def skip_button(self, interaction: discord.Interaction, button: Button):
        vc = interaction.guild.voice_client
        if vc and vc.is_playing():
            vc.stop()
            await interaction.response.send_message("音樂已跳過", ephemeral=True)
      
    
async def setup(bot):
    await bot.add_cog(music(bot))