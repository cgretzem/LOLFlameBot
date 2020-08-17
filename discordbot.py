import discord, asyncio
from discord.ext import commands
from discord.ext.commands import Bot
import LOL_processor as processor
import leaguepkg
from leaguepkg import active
from leaguepkg.active import RequestError
from Tts import getSpeech, delSpeech

Token = 'NzI0NDAxMTA5NjE1MTE2MzAw.XxFIuQ.2SdIm74Ab9q1jaXXng1HIjrjn8o'
runLeague = True

bot = commands.Bot(command_prefix = "#")

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)




async def textToSpeech(ctx, arg):
    
    channel = ctx.author.voice.channel
    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(channel)
        vc = ctx.voice_client
    else:
        vc = await channel.connect()
    if arg is not None:
        for event in arg:
            if event is not None:
                await ctx.send(event)
                name = getSpeech(event)
                await checkPlaying(vc)
                if vc.is_playing() ==False:
                    vc.play(discord.FFmpegPCMAudio(name))# after = delSpeech(name))
                while vc.is_playing():
                    pass
                delSpeech(name)
        


async def checkPlaying(voice_client):
    while True:
        if voice_client.is_playing():
            await asyncio.sleep(1)
        return

@bot.command()
async def disconnect(ctx):
    try:
        await ctx.voice_client.disconnect()
    except:
        pass
    run = False
    if run:
        pass
run = True

@bot.command()
async def league(ctx):

    await ctx.send('Starting league service')
    while run:
        try:
            response = await processor.send()
            
            try:
                
                await textToSpeech(ctx, response)
            except:
                await asyncio.sleep(3)
                await textToSpeech(ctx, response)
            if response == "Game is done!":
                    await asyncio.sleep(2)
            
        except RequestError:
            pass
        
@bot.command()
async def pogchamp(ctx):
    channel = ctx.author.voice.channel
    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(channel)
        vc = ctx.voice_client
    else:
        vc = await channel.connect()
        pog = getSpeech('pog champ')
        await checkPlaying(vc)
        if vc.is_playing() ==False:
            vc.play(discord.FFmpegPCMAudio(pog))# after = delSpeech(name))
    

@bot.event
async def on_ready():
    print('Connected to server')

bot.run(Token)