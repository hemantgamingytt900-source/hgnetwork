import discord
from discord.ext import commands
import re
from datetime import timedelta

TOKEN = "YOUR_BOT_TOKEN_HERE"

OWNER_IDS = {1372939423297179790}

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

# ================= DATA =================
bad_words = {
    "sala",
    "teri gand"
}

allowed_ips_for_all = {
    "play.hgnetwork.fun",
    "25565"
}

spam_count = {}
spam_limit = 10
spam_time = 5  # seconds

setup_channel = None

# ================= EVENTS =================
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# ================= TIMEOUT FUNCTION =================
async def timeout_user(member, message, reason):
    try:
        await message.delete()
        await member.timeout(timedelta(minutes=1), reason=reason)

        for owner_id in OWNER_IDS:
            owner = await bot.fetch_user(owner_id)
            await owner.send(
                f"⚠ **User Timed Out**\n"
                f"User: {member}\n"
                f"Reason: {reason}\n"
                f"Server: {message.guild.name}"
            )
    except Exception as e:
        print(f"Error timing out user: {e}")

# ================= OWNER CHECK =================
def is_owner(ctx):
    return ctx.author.id in OWNER_IDS

# ================= MESSAGE FILTER =================
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()
    member = message.author

    # -------- SPAM CHECK --------
    user_id = member.id
    spam_count.setdefault(user_id, [])
    spam_count[user_id].append(message.created_at)

    spam_count[user_id] = [
        t for t in spam_count[user_id]
        if (message.created_at - t).total_seconds() <= spam_time
    ]

    if len(spam_count[user_id]) >= spam_limit:
        await timeout_user(member, message, "Spam detected")
        spam_count[user_id].clear()
        return

    # -------- LINK CHECK --------
    if re.search(r"https?://|www\.", content):
        await timeout_user(member, message, "Link not allowed")
        return

    # -------- IP CHECK --------
    ip_shared = any(ip in content for ip in allowed_ips_for_all)

    # Only timeout if IP is not allowed
    if not ip_shared and re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", content):
        await timeout_user(member, message, "IP sharing not allowed")
        return

    # -------- BAD WORD CHECK --------
    for word in bad_words:
        if word in content:
            await timeout_user(member, message, "Bad word used")
            return

    await bot.process_commands(message)

# ================= COMMANDS =================
@bot.command()
async def add_bad_words(ctx, *, word):
    if not is_owner(ctx):
        return
    bad_words.add(word.lower())
    await ctx.send(f"✅ Bad word added: `{word}`")

@bot.command()
async def addowner(ctx, user: discord.User):
    if not is_owner(ctx):
        return
    OWNER_IDS.add(user.id)
    await ctx.send(f"👑 New owner added: {user}")

@bot.command()
async def setup_pus(ctx, channel: discord.TextChannel):
    if not is_owner(ctx):
        return

    global setup_channel
    setup_channel = channel.id

    await ctx.send(f"⚙ Setup completed in {channel.mention}")

    for owner_id in OWNER_IDS:
        owner = await bot.fetch_user(owner_id)
        await owner.send(
            f"✅ Setup done\n"
            f"Channel: {channel.name}\n"
            f"Server: {ctx.guild.name}"
        )

# ================= RUN =================
bot.run(TOKEN)

