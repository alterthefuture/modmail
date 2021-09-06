from discord.ext import commands
from pymongo import MongoClient
import discord
import json

with open("config.json") as f:
 config = json.load(f)

mongo_url = config.get("mongo_url")

cluster = MongoClient(mongo_url)
db = cluster["main"]
collection = db["servers"]

class help(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        get_data = collection.find_one({"_id": ctx.guild.id})
        prefix = get_data["prefix"]

        embed=discord.Embed(title="ModMail Commands",description="Commands with () are optional || Commands with [] are required.")
        embed.add_field(name="Prefix", value=f"Description: Changes server prefix\nUsage: `{prefix}prefix [prefix]`", inline=False)
        embed.add_field(name="Close", value=f"Description: Closes modmail channel\nUsage: `{prefix}close`", inline=False)
        embed.add_field(name="Blacklist", value=f"Description: Blacklist mentioned user\nUsage: `{prefix}blacklist [@member]`", inline=False)
        embed.add_field(name="Unblacklist", value=f"Description: Unblacklist mentioned user\nUsage: `{prefix}unblacklist [@member]`", inline=False)
        embed.add_field(name="Blacklisted", value=f"Description: Shows all blacklisted members\nUsage: `{prefix}blacklisted`", inline=False)
        embed.set_footer(text="Made by Scriptz#0001")
        embed.set_thumbnail(url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(help(bot))