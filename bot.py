import discord
from discord.ext import commands
import pymongo
import re
import random
import datetime
import time

mongo_client = pymongo.MongoClient("Your MongoDB")
db = mongo_client["nword_counter"]
collection = db["counter"]

intents = discord.Intents.all()
intents.typing = False
intents.presences = False
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    loggedmsg()


@bot.command()
async def nwords(ctx):
    total_nwords = collection.find_one({"_id": "total"})
    count = total_nwords["count"] if total_nwords else 0

    embed = discord.Embed(title="N-Words Counter", description=f"Total N-Words: {count}", color=0x000000)

    user_counts = collection.aggregate([
        {"$match": {"_id": {"$ne": "total"}}},
        {"$group": {"_id": "$_id", "count": {"$sum": "$count"}}}
    ])

    sorted_user_counts = sorted(user_counts, key=lambda x: x["count"], reverse=True)

    user_count_text = ""
    for user_count in sorted_user_counts:
        user_id = str(user_count["_id"])
        user = await bot.fetch_user(user_id)
        username = user.name if user else "Unknown User"
        count = user_count["count"]

        user_count_text += f"{username}: {count}\n"

    embed.add_field(name="Users", value=user_count_text, inline=False)

    embed.set_footer(text="Developed by Cryzis")

    await ctx.send(embed=embed)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.lower()

    matches = re.findall(r"nigger", content)
    if matches:
        user_id = str(message.author.id)

        collection.update_one({"_id": user_id}, {"$inc": {"count": len(matches)}}, upsert=True)

        collection.update_one({"_id": "total"}, {"$inc": {"count": len(matches)}}, upsert=True)

        responses = [f"HE SAID THE IT {message.author.mention}", f"THE FUNNY WORD {message.author.mention}", f"AYYY {message.author.mention} SAID THE NIGGER WORD"]
        response = random.choice(responses)
        await message.channel.send(response)

    await bot.process_commands(message)

start_time = time.time()

@bot.command()
async def status(ctx):
    try:
        mongo_client.server_info()
        mongo_status = ":green_circle: Connected"
    except Exception:
        mongo_status = ":red_circle: Disconnected"

    current_time = time.time()
    uptime = int(current_time - start_time)
    uptime_str = str(datetime.timedelta(seconds=uptime))

    bot_ping = round(bot.latency * 1000)

    embed = discord.Embed(title="Bot Status", color=discord.Color.blue())
    embed.add_field(name="MongoDB", value=mongo_status, inline=False)
    embed.add_field(name="Bot Uptime", value=uptime_str, inline=False)
    embed.add_field(name="Bot Ping", value=f"{bot_ping}ms", inline=False)

    await ctx.send(embed=embed)
def loggedmsg():
    text = '''
 ______     ______     __  __     ______     __     ______    
/\  ___\   /\  == \   /\ \_\ \   /\___  \   /\ \   /\  ___\   
\ \ \____  \ \  __<   \ \____ \  \/_/  /__  \ \ \  \ \___  \  
 \ \_____\  \ \_\ \_\  \/\_____\   /\_____\  \ \_\  \/\_____\ 
  \/_____/   \/_/ /_/   \/_____/   \/_____/   \/_/   \/_____/ 
'''
    print(text)
    time.sleep(1)
    print('--------------------------------------------------------------')
    print('               developed by Cryzis - cryzis.uk')
    
    
    
bot.run('TOKEN')
