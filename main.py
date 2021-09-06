from discord.ext import commands
from pymongo import MongoClient
from helper import *
import discord
import os
import json

with open("config.json") as f:
 config = json.load(f)

token = config.get("token")
mongo_url = config.get("mongo_url")
bot_activity = config.get("bot_activity")

cluster = MongoClient(mongo_url)
db = cluster["main"]
collection = db["servers"]

def get_prefix(client, message):
	extras = collection.find_one({"_id": message.guild.id})
	prefixes = extras["prefix"]
	return commands.when_mentioned_or(*prefixes)(client,message)

intents=discord.Intents.all()

bot = commands.Bot(command_prefix=get_prefix,intents=intents,case_insensitive=True,owner_id=798325945463078952)
bot.remove_command(name='help')

@bot.event
async def on_connect():
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name=bot_activity))

@bot.event
async def on_ready():
    print("> Bot is online!")
    print("> Attempting to add server(s) that are not in the database to the database.\n")

    guilds = bot.guilds
    dbguilds = []
    for item in collection.find():
      dbguilds.append(item["_id"])
    for guild in guilds:
      if guild.id not in dbguilds:
        collection.insert_one({"_id": guild.id, "prefix": "?", "blacklisted_users": []})
        print(f"> {guild.id} Has been added to database.")

    print("\n> Finished adding servers to database. Bot is ready to go!")

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name=f"My DMS!"))

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith(f"<@!{bot.user.id}>") and len(message.content) == len(f"<@!{bot.user.id}>"):
      get_data = collection.find_one({"_id": message.guild.id})
      prefix = get_data["prefix"]

      await message.channel.send(embed=create_embed(f"My prefix for this server is `{prefix}`"))

    await bot.process_commands(message)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(token)
