import discord
from discord.ext import commands

class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="userinfo", description="Get information about a user.")
    @discord.app_commands.describe(user="The user to get information about")
    async def userinfo(self, interaction: discord.Interaction, user: discord.User = None):
        user = user or interaction.user
        embed = discord.Embed(title=f"User Info: {user}", color=discord.Color.green())
        embed.add_field(name="User ID", value=user.id, inline=False)
        embed.add_field(name="Joined At", value=user.joined_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
        embed.add_field(name="Created At", value=user.created_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
        embed.add_field(name="Top Role", value=user.top_role.name, inline=False)
        embed.set_thumbnail(url=user.avatar_url)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(UserInfo(bot))
