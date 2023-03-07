import discord
from discord.ext import commands
from discord import app_commands, Interaction
from discord import VoiceClient, VoiceChannel, StageChannel, VoiceState
from discord import Guild

from datetime import datetime

class PlayerBase:
    def __init__(self):
        pass

    async def _join(self, channel: VoiceChannel):
        voice_client: VoiceClient = channel.guild.voice_client
        if voice_client is None:
            await channel.connect()

    async def _summon(self, channel: VoiceChannel):
        voice_client: VoiceClient = channel.guild.voice_client
        self._join(channel)
        if voice_client.is_playing():
            voice_client.pause()
        await voice_client.move_to(channel)
        if voice_client.is_paused():
            voice_client.resume()

    async def _leave(self, guild: Guild):
        voice_client: VoiceClient = guild.voice_client
        if voice_client is not None:
            await voice_client.disconnect()

    async def _play_source(self, channel: VoiceChannel, source: discord.FFmpegPCMAudio):
        """
        Retrieve a playable source and play it
        """
        await self._join(channel)
        voice_client: VoiceClient = channel.guild.voice_client
        voice_client.play(source)
        
    async def _pause(self, guild: Guild):
        voice_client: VoiceClient = guild.voice_client
        if voice_client is not None and voice_client.is_playing():
            voice_client.pause()

    async def _resume(self, guild: Guild):
        voice_client: VoiceClient = guild.voice_client
        if voice_client is not None and voice_client.is_paused():
            voice_client.resume()

    async def _skip(self, guild: Guild):
        voice_client: VoiceClient = guild.voice_client
        if voice_client is not None:
            voice_client.stop()

class PlayerBaseCog(PlayerBase, commands.Cog):
    def __init__(self):
        super().__init__()
    

    async def _connectable_channel(self, interaction: Interaction) -> bool:
        if not isinstance(interaction.user.voice.channel, discord.channel.VocalGuildChannel):
            await interaction.response.send_message("Please enter a voice channel first", ephemeral=True)
            return False
        return True
    
    async def sent_embed(self, interaction: Interaction, color:discord.Colour, title:str):
        embed = discord.Embed(
            title=title,
            color=color,
            timestamp=datetime.now()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.Cog.listener(name="on_voice_state_update")
    async def on_no_audiences(self, member: discord.Member, before: VoiceState, after: VoiceState):
        voice_client: VoiceClient = member.guild.voice_client
        if voice_client is None:
            return
        if len(voice_client.channel.members) == 0:
            self._pause()

    @app_commands.command(name="join", description="加入使用者所在頻道")
    async def join(self, interaction: Interaction):
        if interaction.user.voice is None:
            await self.sent_embed(interaction,0xde1f1f,"無法找到語音頻道!")
            return
        await self._join(interaction.user.voice.channel)
        await self.sent_embed(interaction,0x23fa4a,f"已加入{interaction.user.voice.channel.name}")

    @app_commands.command(name="summon", description="切換至使用者所在頻道")
    async def summon(self, interaction: Interaction):
        if interaction.guild.voice_client is None:
            await self.sent_embed(interaction,0xde1f1f,"尚未加入語音頻道!")
            return
        if interaction.user.voice is None:
            await self.sent_embed(interaction,0xde1f1f,"無法找到語音頻道!")
            return
        await self._summon(interaction.user.voice.channel)
        await self.sent_embed(interaction,0x23fa4a,f"已切換至{interaction.user.voice.channel.name}")

    @app_commands.command(name="leave", description="退出頻道")
    async def leave(self, interaction: Interaction):
        await self._leave(interaction.guild)
        await self.sent_embed(interaction,0x23fa4a,f"已退出頻道")

    @app_commands.command(name="pause", description="暫停音樂")
    async def pause(self, interaction: Interaction):
        voice_client: VoiceClient = interaction.guild.voice_client
        if voice_client is None:
            await self.sent_embed(interaction,0xde1f1f,"尚未加入語音頻道!")
            return
        if voice_client.is_playing():
            await self._pause(interaction.guild)
        await self.sent_embed(interaction,0x23fa4a,f"已暫停音樂!")


    @app_commands.command(name="resume", description="繼續播放音樂")
    async def resume(self, interaction: Interaction):
        voice_client: VoiceClient = interaction.guild.voice_client
        if voice_client is None:
            await self.sent_embed(interaction,0xde1f1f,"尚未加入語音頻道!")
            return
        if voice_client.is_paused():
            await self._resume(interaction.guild)
        await self.sent_embed(interaction,0x23fa4a,f"音樂已繼續播放!")


    @app_commands.command(name="skip", description="跳過音樂")
    async def skip(self, interaction: Interaction):
        voice_client: VoiceClient = interaction.guild.voice_client
        if voice_client is None:
            await self.sent_embed(interaction,0xde1f1f,"尚未加入語音頻道!")
            return
        if voice_client.is_playing() or voice_client.is_paused():
            await self._skip(interaction.guild)
            await self.sent_embed(interaction,0x23fa4a,f"已跳過音樂!")
            return
        await self.sent_embed(interaction,0xde1f1f,"無播放中音樂!")

