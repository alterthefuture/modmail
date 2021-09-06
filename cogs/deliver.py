from discord.ext import commands
import discord
from helper import *
from pymongo import MongoClient
import json

with open("config.json") as f:
 config = json.load(f)

category_id = config.get("category_id")
server_id = config.get("server_id")
mongo_url = config.get("mongo_url")

cluster = MongoClient(mongo_url)
db = cluster["main"]
collection = db["users"]
server_collection = db["servers"]

class deliver_message(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.guild:
            return

        if message.author == self.bot.user:
            return
        
        if message.author.id in server_collection.find_one({"_id": int(server_id)})["blacklisted_users"]:
            return

        try:
            category = self.bot.get_channel(int(category_id))

            data = collection.find_one({"_id": message.author.id})

            if not data:
                try:
                    collection.insert_one({"_id": message.author.id, "modmail_channel": "None"})
                    channel = await category.create_text_channel(f"{message.author.id}", permission_synced=True)
                    await channel.send(embed=create_embed(f"{message.author}: **{message.content}**"))

                    collection.update_one({"_id": message.author.id}, {"$set": {"modmail_channel": channel.id}})
                except Exception as error:
                    print(error)
            else:
                try:
                    channel = self.bot.get_channel(data["modmail_channel"])
                    await channel.send(embed=create_embed(f"{message.author}: **{message.content}**"))
                except Exception as error:
                    print(error)

        except Exception as error:
            print(error)

def setup(bot):
    bot.add_cog(deliver_message(bot))