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

TOKEN = 'MTI2OTAwNjkzMjE5NTQwOTk0Mg.GV7kg8.Rm7tYQ9eFxTuWN8EDYZME5HYWcKAVk_DBtv87Q'
ROBLOX_COOKIE = '_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_690D3B9AD1F12B7839E65B9D667977DDFF1329E8BFABE30EB657B9D8186F2F295501A41B906E97A97C800F5132EEE501B850311CA632658C84C0F5C670E25FBE83B3593193C1EEE5C6F40CB84F2F3C87EE605A46A63F9DE12CBFB7AFDCC7B91A91575E4BA0D92E8A066BF51B05260BF41C0CD0E2722AA0B5FEB56D0C42312D232A7FE2BEBDDD63A6DAC5D747FE0B6BD9F98817EFB67199E8B97A2786FDBC4951A0DEC367623DBF4AF3DC10DE84B710FBF3DC94CB37B1B16DD65BA2C1E6DFDF162AA9AED39B6904305C6CE4B8E6D6F818FD74144FE32567DDE07C1C392A5FF6202586540E84459E9C781452A99443C0C887CE3B8AFDA7CC48E7D7CD2DAFFA142F05AD92626EB652BD0500A6DAD11DE674E041AC8C1642660780FF66852DB525E8D2E1CCBB1E92AC317A977511007A6A8384C3C1CB5CC7D43356DC398582CBD498320A3A946D05A09D94873DD061485362A213A73252A3EE8D280E33B31F2531B4D0A7C897BBC81D663C1AE9850EA49DE87A3545C99C4B65CF0ECEA2E9FE3EDB8F103943831F9EF01180BA67F00A31475713A398BACBD91F445D3106835E824FF666C5E5E42A35D9CB8F7885E1C27591CEAEEE754C3921483EB416CAC750D6A2C42A91664771AE40A3AFDE7F78649831DB7429AABE259668EA6AEE9AFBB42143AE16AC07CCAC7BDB219EFAF9D385A83904204380B56EB4D790DE778E81A4D120D11AAE3B96C020A5230F6CE49AF50F95C2236343EF6DC56C4F86E46C343C0D3B4DAC8B2472B320DB748F9CC517921302D3DEBAC344B4AA024A632FA9A0082574563B080DCB5EFE15AB1122F00EFCDB9C4A392E7F0B25A9D8D0B6EEBEC2EAF1A95B2920732311399A79B5F66BA09CD0BC198F591D5A3D62BA5BA767FEA521D24FC6B830AB05445D43012BC20A88570E73FA7C074C147619EF75F8882C6EB2C0729D6B56B8C48E0632D95B20768F8B188BE5C8129A3DA13CE2B690FB47FC5764255A282979ABAE6C83F015781F7A73DF872E7C4A842E9F5DB676F5A8D6BAB3FAD6D39D77F281DEE758B906FE56A40F77B046F15E8827'
GROUP_ID = '34726890'
blacklisted_words = ["https://", "@everyone", "@here", "discord.gg/"]
OwnerID = [1145012840533610556]

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
