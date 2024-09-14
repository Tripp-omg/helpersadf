import discord
from discord.ext import commands

class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="serverinfo", description="Get information about the server.")
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
            return
        
        embed = discord.Embed(title=f"Server Info: {guild.name}", color=discord.Color.blue())
        embed.add_field(name="Server ID", value=guild.id, inline=False)
        embed.add_field(name="Owner", value=guild.owner, inline=False)
        embed.add_field(name="Created At", value=guild.created_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
        embed.add_field(name="Members", value=guild.member_count, inline=False)
        embed.add_field(name="Channels", value=len(guild.channels), inline=False)
        embed.add_field(name="Roles", value=len(guild.roles), inline=False)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(ServerInfo(bot))
