# bot.py
import os

import discord
from dotenv import load_dotenv
from calcs import d20

#Tokens are stored in .env.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

#Confirms in shell that bot is connected to the server
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

initiative_entries = {}

#Prompts that will cause Init-Bot to respond to text messages in channels.
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    #Add a character to those getting their initiatives rolled
    if message.content.startswith('$i'):
        await message.channel.send('I understand you\'re opening combat.')

    #Rolls initiative for all characters entered, creates a new dictionary of chracters and roll values, and posts/pins post
    if message.content.startswith('$roll'):
        await message.channel.send('Here\'s the part where I roll initiative.')

    #Allows users to insert late-coming characters in the middle of combat, either with a pre-specified iniaitive roll, or rolling for them.
    #if message.content.startswith('$new-challenger'):
        #await.message.channel.send('Gotcha, inserting a new guy!')

    #Clears the initiative order in the program and unpins the previous message for a fresh start
    if message.content.startswith('$end'):
        await message.channel.send('I understand combat has ended.')

client.run(TOKEN)
