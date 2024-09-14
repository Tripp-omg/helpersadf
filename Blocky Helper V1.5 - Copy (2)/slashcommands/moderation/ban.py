import discord
from discord.ext import commands
from discord import app_commands

class ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='ban', description='Ban a user from the server')
    @app_commands.describe(member='The member to ban', reason='Reason for the ban')
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        if member == interaction.user:
            await interaction.response.send_message("You cannot ban yourself.", ephemeral=True)
            return

        try:
            await member.ban(reason=reason)
            await interaction.response.send_message(f"Successfully banned {member.mention}.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Failed to ban {member.mention}. Error: {e}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(ban(bot))
