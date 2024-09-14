import discord
from discord.ext import commands

class RoleInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="roleinfo", description="Get information about a role.")
    @discord.app_commands.describe(role="The role to get information about")
    async def roleinfo(self, interaction: discord.Interaction, role: discord.Role = None):
        role = role or discord.utils.get(interaction.guild.roles, id=interaction.user.top_role.id)
        
        embed = discord.Embed(title=f"Role Info: {role.name}", color=role.color)
        embed.add_field(name="Role ID", value=role.id, inline=False)
        embed.add_field(name="Role Color", value=str(role.color), inline=False)
        embed.add_field(name="Created At", value=role.created_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
        embed.add_field(name="Position", value=role.position, inline=False)
        embed.add_field(name="Mentionable", value=role.mentionable, inline=False)
        embed.add_field(name="Members with Role", value=len(role.members), inline=False)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(RoleInfo(bot))
