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
description = '''I am a bot'''
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
gmodel='text-davinci-003'
gmodels=[]

bot = commands.Bot(command_prefix='?', description=description, intents=intents)

@bot.event
async def on_ready():
    # Setting `Listening ` status
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="/chat"))

    #get chatgpt models
    response = openai.Model.list()
    for ele in response["data"]:
        gmodels.append(ele["id"])

    #ready
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.hybrid_command(name='chat', description='chat with gpt')
async def chat(ctx, *, question):
    # Send the question to Chat GPT
    print(question)
    response = openai.Completion.create(
        model=gmodel,
        prompt=question,
        max_tokens=2048,
        temperature=1
    )

    # Get the response from Chat GPT
    answer = response['choices'][0]['text']

    # Send the response back to Discord
    await ctx.send(answer)

@bot.hybrid_command(name='changeme', description='change the gpt model')
async def changeme(ctx, *, model):
    # set new model
    global gmodels
    global gmodel
    if model in gmodels:
        gmodel=model
        answer = 'Ich bin nun ' + gmodel + '. Wenn das nicht klappt wechsel mich. Mit ?model bekommst du eine Übersicht'
    else:
        answer = 'Das Model ' + model + ' existiert nicht! Für eine übersicht gebe ?model ein'

    # Send the response back to Discord
    await ctx.send(answer)

@bot.hybrid_command(name='whoami', description='get the current gpt model')
async def whoami(ctx):
    global gmodel
    # Send the response back to Discord
    await ctx.send('Ich bin ' + gmodel)

@bot.hybrid_command(name='models', description='get all avaliable models')
async def models(ctx):
    # Send the response back to Discord
    await ctx.send(gmodels)

@bot.hybrid_command(name='roll', description='roll dices')
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
async def synccommands(ctx):
    #sync commands
    await bot.tree.sync()
    await ctx.send('updated')

bot.run(DISCORD_BOT_TOKEN)