import discord
from discord.ext import commands
import random

class Coinflip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="coinflip", description="Flip a coin.")
    async def coinflip(self, interaction: discord.Interaction):
        result = random.choice(["Heads", "Tails"])
        await interaction.response.send_message(f"The coin landed on {result}.")

async def setup(bot: commands.Bot):
    await bot.add_cog(Coinflip(bot))
