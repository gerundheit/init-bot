# bot.py
import os

import discord
from dotenv import load_dotenv
from random import randint

#Tokens are stored in .env.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
initiative_entries = []
rolled_initiative_values = []

#Basic die roller
def d20():
    return randint(1, 20)

#Confirms in shell that bot is connected to the server
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

#Prompts that will cause Init-Bot to respond to text messages in channels.
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    #Add a character to those getting their initiatives rolled by appending their name and other arguments to the initiative list as a tuple.
    if message.content.startswith('$i'):
        command = str(message.content).split()
        try:
            initiative_entries.append((command[1], command[2], command[3]))
        except:
            initiative_entries.append((command[1], command[2]))
        await message.channel.send('Added {} to combat.'.format(command[1]))
        await message.channel.send(initiative_entries)

    #Rolls initiative for all characters entered, creates a new dictionary of characters and roll values, and posts/pins post
    if message.content.startswith('$roll'):
        await message.channel.send('Here\'s the part where I roll initiative.')
        for entry in initiative_entries:
            rolled_value = int(roll) + entry[1]
        #This is currently raising TypeError: 'int' object is not subscriptable
            rolled_initiative_values.append(rolled_value)
        rolled_initiative_values.sort(key=lambda a: a[1], reverse=True)
        await message.channel.send(rolled_initiative_values)

    #Allows users to insert late-coming characters in the middle of combat, either with a pre-specified iniaitive roll, or rolling for them. [Note: rolling for them not yet implemented.]
    #if message.content.startswith('$new-challenger'):
        #await.message.channel.send('Gotcha, inserting a new guy!')

    #Clears the initiative order from the list variable and unpins the previous message for a fresh start
    if message.content.startswith('$end'):
        await message.channel.send('I understand combat has ended.')

    if message.content.startswith('$manual'):
        await message.channel.send("""I'm here to help you keep track of combat initiative, and I understand the following commands:

        $hello — I'll say hello back!

        $i — Command to add someone to my initiative tracker list. After the $i, specify character name, initiative bonus, and whether they get advantage on the roll (if they do, say "adv"; if they don't, you don't need to say so.) Example: "$i Fiver adv" means that Fiver gets +5 to initiative rolls and has advantage on initiative rolls; "$i Fiver 5" means she has +5 but no advantage. Enter this command once per character, per combat.

        $roll — Command to have me take all of the characters you've entered, roll their initiative for you, and put them in order. I'll pin the post to make it easy to reference during combat.

        $new-challenger — Command to insert a new character mid-combat. I'm still learning and initiative order is a lot to remember, so you'll need to roll for the newcomer. After the $new-challenger, specify character name and what they rolled, like this: "$new-challenger Lich Queen 17". I'll update the post to match.

        $end — Command to end combat. I'll un-pin the post and wipe the order clean for next time.
        """)

client.run(TOKEN)
