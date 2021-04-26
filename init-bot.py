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
def dice_roller(x):
    return randint(1, x)

#Confirms in shell that bot is connected to the server
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

#Prompts that will cause Init-Bot to respond to text messages in channels.
@client.event
async def on_message(message):
    #Pins message to channel if it's an initiative order posting
    if message.author == client.user and ':' in message.content:
        await message.pin()

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$thanks'):
        await message.channel.send('You\'re welcome!')

    #Add a character to those getting their initiatives rolled by appending their name and other arguments to the initiative list as a tuple.
    if message.content.startswith('$i'):
        command = str(message.content).split()
        bonus = int(command[2])
        try:
            initiative_entries.append((command[1], bonus, command[3]))
        except:
            initiative_entries.append((command[1], bonus))
        await message.channel.send('Added {} to combat.'.format(command[1]))
        #await message.channel.send(initiative_entries)

    #Rolls initiative for all characters entered, creates a new dictionary of characters and roll values, and posts/pins post
    if message.content.startswith('$go'):
        await message.channel.send('Rolling initiative...')
        for entry in initiative_entries:
            if 'adv' in entry[2:]: #Rolls with advantage
                roll_1, roll_2 = dice_roller(20), dice_roller(20)
                print('{name} rolled {one} and {two}.'.format(name=entry[0], one=roll_1, two=roll_2))
                if roll_1 >= roll_2:
                    rolled_value = roll_1 + entry[1]
                else:
                    rolled_value = roll_2 + entry[1]
                rolled_initiative_values.append((entry[0], rolled_value))
            else: #Rolls normally
                rolled_value = dice_roller(20) + entry[1]
                rolled_initiative_values.append((entry[0], rolled_value))
        rolled_initiative_values.sort(key=lambda a: a[1], reverse=True)
        output = ['{}: {}'.format(result[0], result[1]) for result in rolled_initiative_values]
        output = '\n'.join(output)
        await message.channel.send(output)

#Rolls an additional character into the initiative order mid-combat
    if message.content.startswith('$add'):
        command = str(message.content).split()
        name, bonus = command[1], int(command[2])
        if 'adv' in command[2:]: #Rolls with advantage
            roll_1, roll_2 = dice_roller(20), dice_roller(20)
            print('{name} rolled {one} and {two}.'.format(name=name, one=roll_1, two=roll_2))
            if roll_1 >= roll_2:
                rolled_value = roll_1 + bonus
            else:
                rolled_value = roll_2 + bonus
            rolled_initiative_values.append((name, rolled_value))
        else: #Rolls normally
            rolled_value = dice_roller(20) + bonus
            rolled_initiative_values.append((name, rolled_value))
        rolled_initiative_values.sort(key=lambda a: a[1], reverse=True)
        output = ['{}: {}'.format(result[0], result[1]) for result in rolled_initiative_values]
        output = '\n'.join(output)
        await message.channel.send(output)

#Removes a character from the initiative order, pre-rolling or mid-combat
    if message.content.startswith('$del'):
        command = str(message.content).split()
        name = command[1]
        for tup in initiative_entries: #Deletes from the pre-roll initiative roster
            if name in str(tup):
                initiative_entries.remove(tup)
        for tup in rolled_initiative_values: #Deletes from the rolled initiative order variable
            if name in str(tup):
                rolled_initiative_values.remove(tup)
        await message.channel.send('Removed {} from combat.'.format(name))
        if rolled_initiative_values != []:  #Re-sends the updated initiative order to the text channel if combat has already started
            rolled_initiative_values.sort(key=lambda a: a[1], reverse=True)
            output = ['{}: {}'.format(result[0], result[1]) for result in rolled_initiative_values]
            output = '\n'.join(output)
            await message.channel.send(output)

#Clears the initiative order from the list variable and unpins the previous message for a fresh start
    if message.content.startswith('$end'):
        await message.channel.send('Combat has ended. Clearing the board.')
        del rolled_initiative_values[0:]
        del initiative_entries[0:]

#Misc dice rolls
    if message.content.startswith('$roll'):
        command = str(message.content).split()
        if '+' in message.content:
            roll_bonus = command[1].split('+')
            dice_command = roll_bonus[0].split('d')
            roll_bonus = int(roll_bonus[-1])
        else:
            roll_bonus = 0
            dice_command = command[1].split('d')
        number_of_dice = int(dice_command[0])
        number_of_sides = int(dice_command[1])
        results_list = []
        rolls_sum = 0
        for number in range(0, number_of_dice):
            result = dice_roller(number_of_sides)
            results_list.append(result)
        for i in results_list:
            rolls_sum = rolls_sum + i
        rolls_sum = rolls_sum + roll_bonus
        await message.channel.send('That\'s {} ({}+{}).'.format(rolls_sum, results_list, roll_bonus))

#Displays help text/manual in the text channel.
    if message.content.startswith('$manual'):
        await message.channel.send("""I'm here to roll dice and to help you keep track of combat initiative, and I understand the following commands:

        $hello : I'll say hello back!

        $roll : Command to roll any number of any type of dice, e.g. "$roll 8d6" or "$roll 1d20+4". For simple rolls of any kind, such as attack rolls or damage pools. Bonuses can be specified behind a plus mark (no spaces).

        $i : Command to add someone to my initiative tracker list. After the $i, specify character name (no spaces please), initiative bonus, and whether they get advantage on the roll (if they do, say "adv"; if they don't, you don't need to say so). Example: "$i Fiver 5 adv" means that Fiver gets +5 to initiative rolls and has advantage; "$i Fiver 5" means she has +5 but no advantage. Enter this command once per character, per combat.

        $go : Command to have me take all of the characters you've entered, roll their initiative for you, and put them in order. I'll pin the post to make it easy to reference during combat.

        $add : Command to insert a new character mid-combat. Use the same arguments for names, bonuses, and advantage as you do with the $i command.

        $del : Command to delete a character from the initiative order. This works before or after combat begins (AKA before or after the $go command). Just specify character name, e.g. "$del Fiver".

        $end : Command to end combat. I'll wipe the order clean for next time, but you need to un-pin the old post, please.
        """)

client.run(TOKEN)
