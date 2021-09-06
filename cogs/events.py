from discord.ext import commands
from pymongo import MongoClient
import json

with open("config.json") as f:
 config = json.load(f)
 
mongo_url = config.get("mongo_url")

cluster = MongoClient(mongo_url)
db = cluster["main"]
collection = db["servers"]

class events(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        try:
            collection.insert_one({"_id": guild.id, "prefix": "?", "blacklisted_users": []})
            print(f"> {guild.name} Has been added to database.")
        except Exception as error:
            print(error)

    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
        try:
            collection.delete_one({"_id": guild.id})
            print(f"> {guild.name} Has been removed from database.")
        except Exception as error:
            print(error)

def setup(bot):
    bot.add_cog(events(bot))
