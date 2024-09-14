import discord
from discord.ext import commands
from roblox_api import RobloxApi


class GroupInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="groupinfo", description="Get information about a Roblox group.")
    @discord.app_commands.describe(group_id="The ID of the group to get information about")
    async def groupinfo(self, interaction: discord.Interaction, group_id: int):
        try:
            group_info = roblox_api.get_group_info(group_id)

            # Extract data from group_info
            name = group_info.get('name', 'N/A')
            description = group_info.get('description', 'N/A')
            owner = group_info.get('owner', {})
            shout = group_info.get('shout', {})
            member_count = group_info.get('memberCount', 'N/A')
            has_verified_badge = group_info.get('hasVerifiedBadge', 'N/A')

            # Format owner details
            owner_name = owner.get('displayName', 'N/A')
            owner_username = owner.get('username', 'N/A')

            # Format shout details
            shout_body = shout.get('body', 'N/A')
            shout_poster = shout.get('poster', {})
            shout_poster_name = shout_poster.get('displayName', 'N/A')
            shout_poster_username = shout_poster.get('username', 'N/A')
            shout_created = shout.get('created', 'N/A')

            embed = discord.Embed(title=f"Group Info: {name}", color=discord.Color.orange())
            embed.add_field(name="Group ID", value=group_id, inline=False)
            embed.add_field(name="Description", value=description, inline=False)
            embed.add_field(name="Owner", value=f"{owner_name} ({owner_username})", inline=False)
            embed.add_field(name="Shout", value=f"{shout_body} - Posted by {shout_poster_name} ({shout_poster_username}) on {shout_created}", inline=False)
            embed.add_field(name="Members", value=member_count, inline=False)
            embed.add_field(name="Verified Badge", value=has_verified_badge, inline=False)
            # Thumbnail URL can be included if available in the data

            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"Error fetching group info: {e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(GroupInfo(bot))
