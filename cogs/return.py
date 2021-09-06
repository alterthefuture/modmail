from helper import *
from discord.ext import commands
from pymongo import MongoClient
import json

with open("config.json") as f:
 config = json.load(f)
 
mongo_url = config.get("mongo_url")

cluster = MongoClient(mongo_url)
db = cluster["main"]
collection = db["users"]

class return_message(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self,message):
        if not message.guild:
            return

        if message.author == self.bot.user:
            return

        data = collection.find_one({"_id": int(message.channel.name)})

        if not data:
            return
        else:
            try:
                member = message.guild.get_member(int(message.channel.name))
                if message.content == "?close":
                    await member.send(embed=create_embed("An admin has closed your modmail."))
                    collection.delete_one({"_id": int(message.channel.name)})
                    await message.channel.delete()
                else:
                    await member.send(embed=create_embed(f"{message.author}: **{message.content}**"))
            except Exception as error:
                print(error)

def setup(bot):
    bot.add_cog(return_message(bot))