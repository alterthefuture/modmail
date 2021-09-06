import discord
import random

def create_embed(text):
    embed=discord.Embed(description=text,color=discord.Color.blurple())

    return embed

def error_embed(text):
    embed=discord.Embed(description=text,color=discord.Color.red())

    return embed
