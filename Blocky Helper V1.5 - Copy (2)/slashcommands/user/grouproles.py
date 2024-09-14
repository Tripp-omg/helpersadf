import discord
from discord.ext import commands
from roblox_api import RobloxApi
import io



class GroupRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="grouproles", description="Lists all roles in a Roblox group")
    async def grouproles(self, interaction: discord.Interaction, group_id: int):
        try:
            # Fetch the roles for the given group ID
            roles_response = roblox_api.get_group_roles(group_id)
            
            if isinstance(roles_response, dict) and 'roles' in roles_response:
                roles = roles_response['roles']
                role_list = ""
                if roles:
                    for role in roles:
                        role_rank = role.get('rank', 'N/A')
                        role_name = role.get('name', 'N/A')
                        role_description = role.get('description', 'No description available')
                        role_list += f"Role ID: {role_rank}\nRole Name: {role_name}\nDescription: {role_description}\n\n"

                    # Handle long lists
                    if len(role_list) > 1000:
                        with io.BytesIO(role_list.encode('utf-8')) as file:
                            file.seek(0)
                            await interaction.response.send_message(
                                content="Role list is too long to display in a single message. Here's a file:",
                                file=discord.File(file, "roles.txt")
                            )
                    else:
                        # Fetch group info for the embed
                        group_info = roblox_api.get_group_info(group_id)
                        embed = discord.Embed(title=f"Group Roles for {group_info.get('name')}", color=discord.Color.yellow())
                        embed.add_field(name="Group roles:", value=role_list, inline=False)
                        await interaction.response.send_message(embed=embed)
                else:
                    await interaction.response.send_message("No roles found for this group.")
            else:
                await interaction.response.send_message("Failed to retrieve roles or roles are in an unexpected format.")
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(GroupRoles(bot))
