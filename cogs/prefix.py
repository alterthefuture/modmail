from discord.ext import commands
from pymongo import MongoClient
from helper import *
import json

with open("config.json") as f:
 config = json.load(f)

mongo_url = config.get("mongo_url")

cluster = MongoClient(mongo_url)
db = cluster["main"]
collection = db["servers"]

cluster = MongoClient(mongo_url)

class change_prefix(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, new_prefix):
        try:
            collection.update_one({"_id": ctx.guild.id}, {"$set": {"prefix": new_prefix}})
            await ctx.send(embed=create_embed(f"Successfully changed guild prefix to `{new_prefix}`"))
        except:
            await ctx.send(embed=error_embed("Failed to change prefix."))

def setup(bot):
    bot.add_cog(change_prefix(bot))
