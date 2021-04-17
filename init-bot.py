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

    if message.content.startswith('$manual'):
        await message.channel.send("""I'm here to help you keep track of combat initiative, and I understand the following commands:

        $hello — I'll say hello back!

        $i — Command to add someone to my initiative tracker list. After the $i, specify character name, iniative bonus, and whether they get advantage on the roll (if they do, say "adv"; if they don't, you don't need to say so.) Example: "$i Fiver adv" means that Fiver gets +5 to initiative rolls and has advantage on initiative rolls; "$i Fiver 5" means she has +5 but no initiative. Enter this command once per character, per combat.

        $roll — Command to have me take all of the characters you've entered, roll their initiative for you, and put them in order. I'll pin the post to make it easy to reference during combat.

        $new-challenger — Command to insert a new character mid-combat. I'm still learning and initiative order is a lot to remember, so you'll need to roll for the newcomer. After the $new-challenger, specify character name and what they rolled, like this: "$new-challenger Lich Queen 17". I'll update the post to match.

        $end — Command to end combat. I'll un-pin the post and wipe the order clean for next time.
        """)

client.run(TOKEN)
