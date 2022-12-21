import os
import discord
import random 
import json
from discord.ext import commands
import requests
import openai

# Get the Discord and Chat GPT tokens from the environment variables
DISCORD_BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN']
CHAT_GPT_TOKEN = os.environ['CHAT_GPT_TOKEN']
openai.api_key = CHAT_GPT_TOKEN

# Initialize the bot with the correct intents
description = 'I am a bot'
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
gmodel='text-davinci-003'

bot = commands.Bot(command_prefix='?', description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    #print(openai.Model.list())

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command()
async def ask(ctx, *, question):
    # Send the question to Chat GPT
    response = openai.Completion.create(
        model=gmodel,
        prompt=question,
        max_tokens=2048,
        temperature=0
    )

    # Get the response from Chat GPT
    answer = response['choices'][0]['text']

    # Send the response back to Discord
    await ctx.send(answer)

@bot.command()
async def persönlichkeitswechsel(ctx, *, person):
    # Send the question to Chat GPT
    gmodel=person

    # Get the response from Chat GPT
    answer = 'Ich bin nun ' + gmodel + '! Wenn das nicht klappt wechsel mich mit ?model bekommst du eine Übersicht'

    # Send the response back to Discord
    await ctx.send(answer)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

bot.run(DISCORD_BOT_TOKEN)