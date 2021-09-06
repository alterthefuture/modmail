from helper import *
from discord.ext import commands
import discord
from pymongo import MongoClient
import datetime
import json

with open("config.json") as f:
 config = json.load(f)
 
mongo_url = config.get("mongo_url")

cluster = MongoClient(mongo_url)
db = cluster["main"]
collection = db["servers"]

class blacklist_user(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def blacklist(self, ctx, member:discord.Member):
        try:
            collection.update_one({"_id": ctx.guild.id}, {"$push": {"blacklisted_users": member.id}})
            return await ctx.send(embed=create_embed(f"{member.mention} Has been blacklisted in this server."))
        except:
            return await ctx.send(embed=error_embed("Failed to blacklist mentioned user."))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unblacklist(self, ctx, member:discord.Member):
        try:
            collection.update_one({"_id": ctx.guild.id}, {"$pull": {"blacklisted_users": member.id}})
            return await ctx.send(embed=create_embed(f"{member.mention} Has been unblacklisted in this server."))
        except:
            return await ctx.send(embed=error_embed("Failed to unblacklist mentioned user."))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def blacklisted(self, ctx):
        data = collection.find_one({"_id": ctx.guild.id})["blacklisted_users"]
        embed=discord.Embed(title=f"{ctx.guild.name} Blacklist",description="**__Blacklisted Users__**\n",timestamp=datetime.datetime.utcnow(),color=discord.Color.blurple())
        for i in data:
            embed.description += f'**{self.bot.get_user(i)}** - {i}\n'
        embed.set_thumbnail(url=ctx.guild.icon_url)

        await ctx.send(embed=embed)
            
def setup(bot):
    bot.add_cog(blacklist_user(bot))