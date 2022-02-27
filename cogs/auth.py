import discord
from discord.ext import commands

class Authentication:
    def __init__(self, client):
        slef.client = client
    
    @commands.command()
    async def register(self, ctx):
        userID = ctx.author.id
        ctx.send(f'{userID}')