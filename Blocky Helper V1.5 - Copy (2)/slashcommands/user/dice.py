import discord
from discord.ext import commands
import random

class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="dice", description="Roll a die with a specified number of sides.")
    @discord.app_commands.describe(sides="The number of sides on the die")
    async def dice(self, interaction: discord.Interaction, sides: int = 6):
        if sides <= 0:
            await interaction.response.send_message("The number of sides must be greater than 0.")
            return

        roll = random.randint(1, sides)
        await interaction.response.send_message(f"You rolled a {roll} on a {sides}-sided die.")

async def setup(bot: commands.Bot):
    await bot.add_cog(Dice(bot))
