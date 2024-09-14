import discord
from discord.ext import commands
blacklisted_words = ["https://", "@everyone", "@here", "discord.gg/"]
class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="say", description="Make the bot say something.")
    @discord.app_commands.describe(message="The message for the bot to say")
    async def say(self, interaction: discord.Interaction, message: str):
        if any(word in message for word in blacklisted_words):
            await interaction.response.send_message("Your message contains blacklisted content.", ephemeral=True)
            return
        await interaction.response.send_message(message)

async def setup(bot: commands.Bot):
    await bot.add_cog(Say(bot))
