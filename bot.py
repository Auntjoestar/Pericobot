import discord
from discord.ext import commands
from random import choice, randint
import os
import asyncio
import threading

# Replace this with your bot's token
TOKEN = os.getenv("API_KEY")

# Create an instance of a bot with command support
intents = discord.Intents.default()
intents.message_content = True  # Enable reading message content
intents.members = True  # Enable access to members
intents.voice_states = True  # Enable access to voice state updates
bot = commands.Bot(command_prefix='!', intents=intents)

def shuffle(arr):
    for i in range(len(arr) - 1, 0, -1):
        j = randint(0, i)
        arr[i], arr[j] = arr[j], arr[i]

def send_message(ctx, message):
    asyncio.run_coroutine_threadsafe(ctx.send(message), bot.loop)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def retador(ctx):
    # Get the voice channel
    channel = ctx.author.voice.channel

    if channel:
        members = channel.members
        if len(members) >= 2:
            shuffle(members)
            retador = choice(members)
            retado = choice([member for member in members if member != retador])
            retador = retador.mention
            retado = retado.mention
            response = f"El retador es {retador}\nEl retado es {retado}"
            await ctx.send(response)
        else:
            await ctx.send('No hay suficientes miembros en el canal de voz.')
    else:
        await ctx.send('No se encontró el canal de voz especificado.')

@bot.command()
async def noCoito(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voiceClient = await channel.connect()
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        SOUND = os.path.join(BASE_DIR, 'no-coito.mp3')

        if os.path.exists(SOUND):
            thread = threading.Thread(target=send_message, args=(ctx, f'No coito en {channel}, puta'))
            thread.start()
            voiceClient.play(discord.FFmpegPCMAudio(SOUND))
            voiceClient.source = discord.PCMVolumeTransformer(voiceClient.source)
            voiceClient.source.volume = 0.5
            while voiceClient.is_playing():
                await asyncio.sleep(1)
            await voiceClient.disconnect()
    else:
        await ctx.send('Debes estar en un canal de voz, bobita!')

@bot.command()
async def dlst(ctx, user: discord.Member):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voiceClient = await channel.connect()
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        SOUND = os.path.join(BASE_DIR, 'daleLoquitaSosTuani.opus')

        if os.path.exists(SOUND):
            user = user.mention
            thread = threading.Thread(target=send_message, args=(ctx, f'Dale {user}, sos tuani'))
            thread.start()
            voiceClient.play(discord.FFmpegPCMAudio(SOUND))
            voiceClient.source = discord.PCMVolumeTransformer(voiceClient.source)
            voiceClient.source.volume = 0.5
            while voiceClient.is_playing():
                await asyncio.sleep(1)
            await voiceClient.disconnect()
    else:
        await ctx.send('Debes estar en un canal de voz, bobita!')

# Run the bot
bot.run(TOKEN)


