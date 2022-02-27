import discord
from discord.ext import commands
from main import database

class Authentication(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def register(self, ctx, key):
        userID = ctx.author.id
        # await ctx.send(f'{userID}')
        res = database.registerUser(userID, key)
        if res[0]:
            embed = discord.Embed(title="Success", description=f'Account `{res[1]["username"]}` has been assigned to {ctx.author.mention}', color=0x00ff00)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Error", description="Invalid key", color=0xff0000)
            await ctx.send(embed=embed)
    
    @commands.command()
    async def logout(self, ctx):
        userID = ctx.author.id
        res = database.logout(userID)
        if res:
            embed = discord.Embed(title="Success", description=f'Account `{res["username"]}` has been logged out', color=0x00ff00)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Error", description="You are not logged in", color=0xff0000)
            await ctx.send(embed=embed)
        
def setup(client):
    client.add_cog(Authentication(client))