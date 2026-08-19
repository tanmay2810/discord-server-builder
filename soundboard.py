"""
Soundboard Manager — Play sound effects in voice channels
Supports MP3, WAV, and OGG formats
Requires discord.py voice support (install: pip install discord.py[voice])
"""

import os
import discord
from pathlib import Path
from discord.ext import commands
from config import load_server_config

CONFIG = load_server_config(None)

# Sound effects library
SOUNDBOARD_DIR = "soundboard"


class SoundboardManager:
    """Manage soundboard audio effects"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.current_audio = {}  # Track playing audio per voice channel
    
    def get_sounds(self) -> dict:
        """Get all available sound files organized by category"""
        sounds = {}
        
        if not Path(SOUNDBOARD_DIR).exists():
            return sounds
        
        for category_folder in Path(SOUNDBOARD_DIR).iterdir():
            if category_folder.is_dir():
                category = category_folder.name
                sounds[category] = []
                
                for sound_file in category_folder.glob("*"):
                    if sound_file.suffix.lower() in [".mp3", ".wav", ".ogg"]:
                        sounds[category].append(sound_file.name)
        
        return sounds
    
    async def play_sound(self, interaction: discord.Interaction, sound_name: str):
        """Play a sound in the user's current voice channel"""
        
        # Check if user is in voice channel
        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.response.send_message("❌ You must be in a voice channel!", ephemeral=True)
            return
        
        voice_channel = interaction.user.voice.channel
        
        # Find the sound file
        sound_path = None
        for category_folder in Path(SOUNDBOARD_DIR).iterdir():
            if category_folder.is_dir():
                potential_path = category_folder / sound_name
                if potential_path.exists():
                    sound_path = potential_path
                    break
        
        if not sound_path:
            await interaction.response.send_message(f"❌ Sound '{sound_name}' not found!", ephemeral=True)
            return
        
        try:
            await interaction.response.defer()
            
            # Connect to voice channel
            voice_client = await voice_channel.connect()
            
            # Play audio
            audio_source = discord.FFmpegPCMAudio(str(sound_path))
            voice_client.play(audio_source)
            
            await interaction.followup.send(f"🔊 Playing: **{sound_name}**")
            
        except Exception as e:
            await interaction.followup.send(f"❌ Error playing sound: {str(e)}")
    
    async def stop_sound(self, guild: discord.Guild):
        """Stop current audio in guild voice channels"""
        for voice_client in self.bot.voice_clients:
            if voice_client.guild == guild and voice_client.is_playing():
                voice_client.stop()


def register_soundboard_commands(bot: commands.Bot):
    """Register soundboard slash commands"""
    
    soundboard = SoundboardManager(bot)
    
    @bot.tree.command(name="sounds", description="List all available soundboard effects")
    async def list_sounds(interaction: discord.Interaction):
        """Show available sound effects"""
        sounds = soundboard.get_sounds()
        
        if not sounds:
            await interaction.response.send_message("❌ No sounds available. Create a `soundboard/` folder with sound files.", ephemeral=True)
            return
        
        embed = discord.Embed(title="🎵 Soundboard Effects", color=discord.Color.blue())
        
        for category, sound_list in sounds.items():
            embed.add_field(name=category, value="\n".join(f"`{s}`" for s in sound_list), inline=False)
        
        await interaction.response.send_message(embed=embed)
    
    @bot.tree.command(name="play", description="Play a sound effect (use /sounds to see list)")
    @discord.app_commands.describe(sound="The sound effect to play")
    async def play_sound_command(interaction: discord.Interaction, sound: str):
        """Play a specific sound effect"""
        await soundboard.play_sound(interaction, sound)
    
    @bot.tree.command(name="stop_audio", description="Stop current audio playback")
    async def stop_audio_command(interaction: discord.Interaction):
        """Stop all audio in the guild"""
        await soundboard.stop_sound(interaction.guild)
        await interaction.response.send_message("⏹️ Audio stopped")
