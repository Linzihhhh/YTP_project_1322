import discord
from discord.ext import commands
from discord import app_commands, Interaction
from discord import VoiceClient, VoiceChannel
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
        if voice_client is None:
            return
        if voice_client.is_playing():
            voice_client.pause()
        await voice_client.move_to(channel)
        if voice_client.is_paused():
            voice_client.resume()

    async def _leave(self, guild: Guild):
        voice_client: VoiceClient = guild.voice_client
        if voice_client is not None:
            await voice_client.disconnect()

    async def _play(self, channel: VoiceChannel, source: discord.FFmpegPCMAudio):
        """
        Retrieve a playable source and play it
        """
        await self._join(channel)
        voice_client: VoiceClient = channel.guild.voice_client
        if voice_client.is_playing() or voice_client.is_paused():
            return
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

    @app_commands.command(name="join", description="owo")
    async def join(self, interacion: Interaction):
        await self._join(interacion.user.voice.channel)
        await interacion.response.send_message("hello", ephemeral=True)

    @app_commands.command(name="summon", description="oao")
    async def summon(self, interacion: Interaction):
        await self._summon(interacion.user.voice.channel)
        await interacion.response.send_message("summon", ephemeral=True)

    @app_commands.command(name="leave", description="ouo")
    async def leave(self, interacion: Interaction):
        await self._leave(interacion.guild)
        await interacion.response.send_message("byebye", ephemeral=True)

    @app_commands.command(name="play", description="Play the song or playlist you want")
    async def play(self, interaction: Interaction, qstring: str):
        await self._play(interaction.user.voice.channel, discord.FFmpegPCMAudio(qstring))
        await interaction.response.send_message("Succeed to play the music")

    @app_commands.command(name="pause", description="Pause the current playing audio")
    async def pause(self, interaction: Interaction):
        await self._pause(interaction.guild)
        await interaction.response.send_message("Succeed to pause the current playing music")

    @app_commands.command(name="resume", description="Resume the current paused audio")
    async def resume(self, interaction: Interaction):
        await self._resume(interaction.guild)
        await interaction.response.send_message("Succeed to resume the current paused music")

    @app_commands.command(name="skip", description="Skip the current playing audio")
    async def skip(self, interaction: Interaction):
        await self._skip(interaction.guild)
        await interaction.response.send_message("Succeed to pause the current playing music")