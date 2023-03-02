import discord
from discord.ext import commands
from discord import app_commands, Interaction
from discord import VoiceClient, VoiceChannel, StageChannel, VoiceState
from discord import Guild

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

    @commands.Cog.listener(name="on_voice_state_update")
    async def on_no_audiences(self, member: discord.Member, before: VoiceState, after: VoiceState):
        voice_client: VoiceClient = member.guild.voice_client
        if len(voice_client.channel.members) == 0:
            self._pause()

    @app_commands.command(name="join", description="owo")
    async def join(self, interaction: Interaction):
        if not await self._connectable_channel(interaction):
            return
        await self._join(interaction.user.voice.channel)
        await interaction.response.send_message("hello", ephemeral=True)

    @app_commands.command(name="summon", description="oao")
    async def summon(self, interaction: Interaction):
        if not self._connectable_channel(interaction):
            return
        await self._summon(interaction.user.voice.channel)
        await interaction.response.send_message("summon", ephemeral=True)

    @app_commands.command(name="leave", description="ouo")
    async def leave(self, interaction: Interaction):
        await self._leave(interaction.guild)
        await interaction.response.send_message("byebye", ephemeral=True)

    @app_commands.command(name="pause", description="Pause the current playing audio")
    async def pause(self, interaction: Interaction):
        voice_client: VoiceClient = interaction.guild.voice_client
        if voice_client is not None and voice_client.is_playing():
            await self._pause(interaction.guild)
            await interaction.response.send_message("Succeed to pause the current playing music")

    @app_commands.command(name="resume", description="Resume the current paused audio")
    async def resume(self, interaction: Interaction):
        voice_client: VoiceClient = interaction.guild.voice_client
        if voice_client is not None and voice_client.is_paused():
            await self._resume(interaction.guild)
            await interaction.response.send_message("Succeed to resume the current paused music")

    @app_commands.command(name="skip", description="Skip the current playing audio")
    async def skip(self, interaction: Interaction):
        voice_client: VoiceClient = interaction.guild.voice_client
        if voice_client is not None and (voice_client.is_playing() or voice_client.is_paused()):
            await self._skip(interaction.guild)
            await interaction.response.send_message("Succeed to skip the current playing music")