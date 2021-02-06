import sqlite3
import discord
import os
from discord.ext import commands, tasks

client = commands.Bot(command_prefix = '#')
client.remove_command('help')

@client.event
async def on_ready():
    print('Bot started.')
    await client.change_presence(activity=discord.Game('Where the tables never end!'))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in all required arguments.')
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Unknown command. Use .help for a list of commands')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have the required permissions to run this command.')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {client.latency * 1000}ms')

def owner(ctx):
    return ctx.author.id == 317394276189208576

@client.command()
@commands.check(owner)
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

@client.command()
@commands.check(owner)
async def shutdown(ctx):
    exit()

@client.command()
@commands.check(owner)
async def status(ctx, *, txt):
    await client.change_presence(activity=discord.Game(txt))

@client.command()
@commands.check(owner)
async def log(ctx, *, txt):
    print(txt)

@client.command()
@commands.check(owner)
async def say(ctx, *, txt):
    await ctx.channel.purge(limit=1)
    await ctx.send(txt)

@client.command()
async def tables(ctx):
    await ctx.send('Tables:')

    conn = sqlite3.connect('sqlbot.db')

    c = conn.cursor()

    for row in c.execute("SELECT name FROM sqlite_master WHERE type = 'table'"):
        await ctx.send(row)

    conn.close()

@client.command()
async def create(ctx, name):
    await ctx.send('Created table!')
    
    conn = sqlite3.connect('sqlbot.db')

    c = conn.cursor()

    query = f"CREATE TABLE IF NOT EXISTS {name} (text text)"

    c.execute(query)

    conn.commit()

    conn.close()

@client.command()
async def drop(ctx, name):
    await ctx.send('Dropped table!')

    conn = sqlite3.connect('sqlbot.db')

    c = conn.cursor()

    query = f"DROP TABLE IF EXISTS {name}"

    c.execute(query)

    conn.commit()

    conn.close()

@client.command()
async def entries(ctx, table):
    await ctx.send('Entries:')

    conn = sqlite3.connect('sqlbot.db')

    c = conn.cursor()
    
    query = f"SELECT * FROM {table}"

    for row in c.execute(query):
        await ctx.send(row)

    conn.commit()

    conn.close()

@client.command()
async def insert(ctx, table, *, txt):
    await ctx.send('Inserted text!')

    conn = sqlite3.connect('sqlbot.db')

    c = conn.cursor()

    query = f"INSERT INTO {table} VALUES ('{txt}')"

    c.execute(query)
    
    conn.commit()

    conn.close()

@client.command()
async def delete(ctx, table, *, txt):
    await ctx.send(f'Deleted any entries in {table} where the text attribute is {txt}!')

    conn = sqlite3.connect('sqlbot.db')
    
    c = conn.cursor()

    query = f"DELETE FROM {table} WHERE text = '{txt}'"

    c.execute(query)

    conn.commit()

    conn.close()
@client.command()
@commands.check(owner)
async def query(ctx, *, query):
    await ctx.send(query+" sent!")
    
    conn = sqlite3.connect('sqlbot.db')

    c = conn.cursor()

    c.execute(query)
    
    conn.commit()

    conn.close()

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run('ODA3MzE5ODM0Njg1NDcyODA4.YB2RLw.vwQ-pzfbFgqlCDmHkAjUgAHHkbM')
