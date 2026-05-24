import discord
from discord.ext import commands
from datetime import datetime, timedelta, timezone
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    try:
        await bot.tree.sync()
        print("Slash commands synced")
    except Exception as e:
        print("Sync error:", e)

    print(f"Logged in as {bot.user}")

@bot.tree.command(name="unban-24h", description="Unban users banned in last 24h")
async def unban_24h(interaction: discord.Interaction):

    # 🔥 THIS FIXES “did not respond”
    await interaction.response.defer()

    if not interaction.user.guild_permissions.administrator:
        return await interaction.followup.send("No permission")

    guild = interaction.guild
    cutoff = datetime.now(timezone.utc) - timedelta(days=1)

    targets = set()

    async for entry in guild.audit_logs(limit=2000, action=discord.AuditLogAction.ban):
        if entry.created_at >= cutoff and entry.target:
            targets.add(entry.target.id)

    await interaction.followup.send(f"Found {len(targets)} users. Unbanning...")

    count = 0

    for uid in targets:
        try:
            user = await bot.fetch_user(uid)
            await guild.unban(user)
            count += 1
        except:
            pass

    await interaction.followup.send(f"Done. Unbanned {count}")

bot.run(TOKEN)
