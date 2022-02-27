import discord
import os
from discord.ext import commands
import config
import jishaku
from databases import Database

database = Database(config.MONGO_URI)
client = commands.Bot(command_prefix='!')
client.load_extension("jishaku")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        
client.run(config.TOKEN)