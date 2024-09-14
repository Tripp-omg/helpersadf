import discord
from discord.ext import commands

class MemberCount(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="membercount", description="Displays the total number of members, humans, and bots")
    async def membercount(self, interaction: discord.Interaction):
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
            return
        
        total_members = guild.member_count
        human_count = sum(1 for member in guild.members if not member.bot)
        bot_count = sum(1 for member in guild.members if member.bot)
        embed = discord.Embed(title="Member Count", color=discord.Color.blue())
        embed.add_field(name="Total Members:", value=total_members, inline=False)
        embed.add_field(name="Total Humans:", value=human_count, inline=False)
        embed.add_field(name="Total Bots:", value=bot_count, inline=False)
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(MemberCount(bot))
