import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="help", description="Lists all commands available to the public")
    async def help(self, interaction: discord.Interaction):
        commands = self.bot.tree.get_commands()
        embed = discord.Embed(title="Help", color=discord.Color.purple())
        for command in commands:
            if getattr(command, 'hidden', False):
                continue
            embed.add_field(
                name=f"/{command.name}",
                value=command.description or "No description available",
                inline=False
            )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))
