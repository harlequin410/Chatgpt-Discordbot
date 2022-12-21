import os
import discord
from discord.ext import commands
import requests

# Get the Discord and Chat GPT tokens from the environment variables
DISCORD_BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN']
CHAT_GPT_TOKEN = os.environ['CHAT_GPT_TOKEN']

bot = commands.Bot(command_prefix='!', token=DISCORD_BOT_TOKEN)

@bot.command()
async def ask(ctx, *, question):
    # Send the question to Chat GPT
    response = requests.post('https://api.openai.com/v1/chatgpt/', 
                             headers={'Authorization': 'Bearer ' + CHAT_GPT_TOKEN,
                                      'Content-Type': 'application/json'},
                             json={'prompt': question, 'max_tokens': 1024}).json()

    # Get the response from Chat GPT
    answer = response['choices'][0]['text']

    # Send the response back to Discord
    await ctx.send(answer)

bot.run()