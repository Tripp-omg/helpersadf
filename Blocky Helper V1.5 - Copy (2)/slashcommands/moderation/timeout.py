import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta
from discord.utils import utcnow

class Timeout(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='timeout', description='Timeout a user for a specified duration')
    @app_commands.describe(member='The member to timeout', duration='Duration in minutes', reason='Reason for the timeout')
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, duration: int, reason: str = None):
        if not interaction.user.guild_permissions.moderate_members:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        if member == interaction.user:
            await interaction.response.send_message("You cannot timeout yourself.", ephemeral=True)
            return

        if duration <= 0:
            await interaction.response.send_message("The timeout duration must be greater than 0.", ephemeral=True)
            return

        try:
            timeout_until = utcnow() + timedelta(minutes=duration)
            await member.timeout(timeout_until, reason=reason)
            await interaction.response.send_message(f"Successfully timed out {member.mention} for {duration} minutes.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Failed to timeout {member.mention}. Error: {e}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Timeout(bot))
