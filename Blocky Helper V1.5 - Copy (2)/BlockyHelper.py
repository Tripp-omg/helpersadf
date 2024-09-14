import discord
from discord.ext import commands, tasks
from discord import app_commands
from roblox_api import RobloxApi
from weblog import log_to_webhook
import os
import sys
import io
from datetime import timedelta
import random



def login_to_roblox():
    global roblox_api
    roblox_api = RobloxApi(cookie=ROBLOX_COOKIE)
    roblox_api.check_authentication()
    print(f"Logged in as: {roblox_api.get_authenticated_user()}")

def reauthenticate():
    try:
        print("Attempting reauthentication...")
        login_to_roblox()
        print("Reauthentication successful.")
    except Exception as e:
        print(f"Reauthentication failed: {e}")

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.AutoShardedBot(command_prefix='/', intents=intents)

# Set up statuses
statuses = [
    {"type": discord.ActivityType.playing, "name": "Roblox"},
    {"type": discord.ActivityType.streaming, "name": "the epic fight", "url": "https://www.roblox.com/groups/33284428/The-Menacing-Foes#!/about"},
    {"type": discord.ActivityType.listening, "name": "for commands"},
    {"type": discord.ActivityType.watching, "name": "over the server"},
    {"type": discord.ActivityType.competing, "name": "against the Olympic swimmers"}
]

@tasks.loop(minutes=10)
async def change_status():
    current_status = statuses[change_status.current_loop % len(statuses)]
    activity = discord.Activity(type=current_status["type"], name=current_status["name"])
    if "url" in current_status:
        activity.url = current_status["url"]
    await bot.change_presence(activity=activity)

# Load commands from the slashcommands/user directory
async def load_extensions():
    for filename in os.listdir('./slashcommands/user'):
        if filename.endswith('.py') and not filename.startswith('__') and not filename.startswith('roblox_api'):
            try:
                await bot.load_extension(f'slashcommands.user.{filename[:-3]}')
                print(f"Loaded extension: {filename}")
            except Exception as e:
                print(f"Failed to load extension {filename}: {e}")


@bot.tree.command(name='restart', description='Restarts the bot')
async def restart(interaction: discord.Interaction):
    if interaction.user.id not in OwnerID:
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
        return

    await interaction.response.send_message("Bot is restarting...", ephemeral=True)
    log_to_webhook(f"Bot is restarting by {interaction.user}.")
    await bot.close()
    os.execv(sys.executable, ['python'] + sys.argv)
setattr(bot.tree.get_command('restart'), 'hidden', True)

@bot.tree.command(name='shutdown', description='Shuts down the bot')
async def shutdown(interaction: discord.Interaction):
    if interaction.user.id not in OwnerID:
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
        return

    await interaction.response.send_message("Bot is shutting down...", ephemeral=True)
    log_to_webhook(f"Bot is shutting down by {interaction.user}.")
    await bot.close()
setattr(bot.tree.get_command('shutdown'), 'hidden', True)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')\

    await load_extensions()
    await bot.tree.sync()  # Sync commands to Discord
    login_to_roblox()
    change_status.start()

bot.run(TOKEN)
