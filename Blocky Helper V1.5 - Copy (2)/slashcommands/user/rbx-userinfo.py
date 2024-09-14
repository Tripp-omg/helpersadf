import discord
from discord.ext import commands
from discord import app_commands
from roblox_api import RobloxApi


class RbxUserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='rbx-userinfo', description='Fetches Roblox user info')
    async def userinfo(self, interaction: discord.Interaction, username: str = None, userid: str = None):
        try:
            if not username and not userid:
                await interaction.response.send_message("Please provide either a username or user ID.", ephemeral=True)
                return

            if username:
                user_id = roblox_api.get_user_id_by_username(username)
            else:
                user_id = userid

            user_info = roblox_api.get_user_info(user_id)
            if user_info:
                embed = discord.Embed(title=f"User Info for {user_info.get('name')}", color=discord.Color.blue())
                embed.add_field(name="Username", value=user_info.get('name'), inline=False)
                embed.add_field(name="Display Name", value=user_info.get('displayName'), inline=False)
                embed.add_field(name="ID", value=user_info.get('id'), inline=False)
                embed.add_field(name="Description", value=user_info.get('description', 'No description available'), inline=False)
                embed.add_field(name="Created", value=user_info.get('created'), inline=False)
                embed.add_field(name="Banned?", value="Yes" if user_info.get('isBanned') else "No")
                embed.add_field(name="Verified", value="Yes" if user_info.get("hasVerifiedBadge") else "No")
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message("Failed to retrieve user info.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(RbxUserInfo(bot))