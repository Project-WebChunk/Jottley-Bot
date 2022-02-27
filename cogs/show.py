import discord
from discord.ext import commands
from main import database
from bs4 import BeautifulSoup as bs

class Show(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def show(self, ctx, bookID=None, chapterID=None, snippetID=None):
        userID = ctx.author.id
        user = database.getUser(userID)
        if not user:
            await ctx.send("You are not logged in")
        else:
            if bookID is None:
                books = []
                for book in user['books']:
                    books.append(database.getBook(book, userID))
                embed = discord.Embed(title=f"{user['username']}'s books", description="All of your books", color=0x00ff00)
                for book in books:
                    embed.add_field(name=book['name'], value=f"Book ID: {book['_id']}\nChapter Count: {len(book['chapters'])} \nBook Index: {user['books'].index(book['_id'])}", inline=False)
                await ctx.send(embed=embed)
            
            elif chapterID is None:
                book = database.getBook(bookID, userID)
                if book:
                    chapters = []
                    embed = discord.Embed(title=f"{book['name']}'s chapters", description=f"All chapters inside {book['name']}", color=0x00ff00)
                    for chapter in book['chapters'].values():
                        embed.add_field(name=chapter['name'], value=f"Chapter ID: {chapter['_id']}\nSnippet Count: {len(chapter['snippets'])} \nChapter Index: {book['chapterOrder'].index(chapter['_id'])}", inline=False)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("Invalid book ID")
                
            elif snippetID is None:
                chapter = database.getBook(bookID, userID)
                if chapter:
                    chapter = chapter['chapters']
                    if chapterID in chapter.keys():
                        chapter = chapter[chapterID]
                        embed = discord.Embed(title=f"{chapter['name']}'s snippets", description=f"All snippets inside {chapter['name']}", color=0x00ff00)
                        for snip in chapter['snippets'].values():
                            embed.add_field(name=snip['name'], value=f"Snippet ID: {snip['_id']}\nSnippet Index: {chapter['snippetOrder'].index(snip['_id'])}", inline=False)
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send("Invalid chapter ID")
                else:
                    await ctx.send("Invalid book ID")
            
            else:
                book = database.getBook(bookID, userID)
                if book:
                    chapters = book['chapters']
                    if chapterID in chapters.keys():
                        chapter = chapters[chapterID]
                        if snippetID in chapter['snippets'].keys():
                            snippet = chapter['snippets'][snippetID]
                            code = bs(snippet['content'], 'html.parser').prettify()
                            embed = discord.Embed(title=f"{snippet['name']}", description=f"```html\n{code}```", color=0x00ff00)
                            await ctx.send(embed=embed)
                        else:
                            await ctx.send("Invalid snippet ID")
                    else:
                        await ctx.send("Invalid chapter ID")
                else:
                    await ctx.send("Invalid book ID")
                    
        
def setup(client):
    client.add_cog(Show(client))