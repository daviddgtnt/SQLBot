import discord
from discord.ext import commands

class help(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Help command loaded')

    @commands.command()
    async def help(self, ctx):

        helpembed = discord.Embed(
            colour = discord.Colour.blue(),
            title = 'Command List:',
            description = '#help | Show this message\n#tables | See all the tables.\n#entries <table> | See all the entries in a table.\n#create <name> | Creates a table\n#insert <table> <value> | Inserts a value into the table.\n#delete <table> <value> | Deletes anytihng in the table with the value.\n#drop <table> | Drops a table'
        )
        helpembed.set_footer(text='SQLBot by DavidDGTNT')
        await ctx.send(embed=helpembed)

def setup(client):
    client.add_cog(help(client))