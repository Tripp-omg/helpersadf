import discord
from discord.ext import commands
from discord import app_commands

class kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name='kick', description='Kick a user from the server')
    @app_commands.describe(member='The member to kick', reason='Reason for the kick')
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        if not interaction.user.guild_permissions.kick_members:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        if member == interaction.user:
            await interaction.response.send_message("You cannot kick yourself.", ephemeral=True)
            return

        try:
            await member.kick(reason=reason)
            await interaction.response.send_message(f"Successfully kicked {member.mention}.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Failed to kick {member.mention}. Error: {e}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(kick(bot))