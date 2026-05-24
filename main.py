import discord
from discord.ext import commands
from datetime import datetime, timedelta, timezone
import os

TOKEN = os.getenv("TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

intents = discord.Intents.default()
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Bot ready")

@bot.tree.command(name="unban-24h", description="Unban users banned in last 24h")
async def unban_24h(interaction: discord.Interaction):

    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("No permission", ephemeral=True)

    await interaction.response.send_message("Starting unban process... (this may take a bit)")

    guild = interaction.guild
    cutoff = datetime.now(timezone.utc) - timedelta(days=1)

    targets = set()

    async for entry in guild.audit_logs(limit=2000, action=discord.AuditLogAction.ban):
        if entry.created_at >= cutoff and entry.target:
            targets.add(entry.target.id)

    count = 0

    for uid in targets:
        try:
            user = await interaction.client.fetch_user(uid)
            await guild.unban(user)
            count += 1
        except:
            pass

    await interaction.followup.send(f"Done. Unbanned {count}")
