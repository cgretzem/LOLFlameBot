import os
import discord
from dotenv import load_dotenv
from league import main
from Tts import getSpeech, delSpeech
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
client = discord.Client()

bot = commands.Bot(command_prefix = "#")

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

@bot.command(name = 'GamerTime')
async def runProg(ctx):
    channel = ctx.author.voice.channel
    if ctx.message.author == bot.user:
        return
    run = True
    while run:
        event = main()
        if event == 'League Game over! Type #GamerTime to restart the bot.' or event == 'Could not connect to game':
            run = False
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        name = getSpeech(event)
        try:
            vc = await channel.connect()
        except TimeoutError as err:
            print(err)
            vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio(name))
        helper(ctx)
            
        await ctx.send(event)##
        await ctx.voice_client.disconnect()
        delSpeech(name)

def helper(ctx):
    run = True
    while run:
        if not ctx.voice_client.is_playing():
            return

@bot.command()
async def stop(ctx):
    """Stops and disconnects the bot from voice"""
    await ctx.voice_client.disconnect()

@bot.event
async def on_ready():
    print('Connected to server')

bot.run(TOKEN)

