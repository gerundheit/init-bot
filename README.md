# Init-Bot
Init-Bot is a simple dice roller and initiative tracker for 5th Edition D&D groups that play over Discord.

# Libraries
This program is written in Python 3 and uses [python-dotenv](https://pypi.org/project/python-dotenv/) for Discord bot token management and the [Discord API wrapper](https://discordpy.readthedocs.io/en/stable/index.html).

# Setup
1. To set up your own instance of Init-Bot, you will first need your own Discord server. Then, get signed up on the [Discord Developer Portal](https://discord.com/developers/docs/intro), where you'll set up an application and, within it, a bot. [RealPython.com](https://realpython.com/how-to-make-a-discord-bot-python/) has a guide on how to do this. Follow the instructions all the way through OAuth2 authentication to add your bot to your server as if it is a user.

2. Once you've got your bot registered and this repository downloaded locally, create a new file called .env in the repository. Inside it, paste the following text.
> \# .env

> DISCORD_TOKEN = your-token

3. Replace "your-token" with the Bot Token pasted in from your Discord Developer account. Save.

4. Run init-bot.py in your terminal shell. You should now be able to interact with the bot. See below for a list of supported commands. The bot will only be available in your server while it is running, so either keep it going in the background on your computer during game sessions, or set up a more permanent solution for serving it on a continuous basis. Presently, each local installation of the bot can only interact with one server at a time.

# Interacting with the Bot
These commands can also be viewed in Init-Bot's Discord server while it is running by posting the message "$manual" in a text channel.

- $hello : Init-Bot will say hello back.
- $roll : Command to roll any number of any type of dice, e.g. "$roll 8d6" or "$roll 1d20+4". For simple rolls of any kind, such as attack rolls or damage pools. Bonuses can be specified behind a plus mark (no spaces).
- $i : Command to add someone to Init-Bot's initiative tracker list. After the "$i", specify character name (no spaces please), initiative bonus, and whether the character gets advantage on the roll (if they do, say "adv"; if they don't, you don't need to say so). Example: "$i Fiver 5 adv" means that Fiver gets +5 to initiative rolls and has advantage; "$i Fiver 5" means she has +5 but no advantage. Enter this command once per character, per combat as its own message.
- $go : Command to have Init-Bot take all of the characters you've entered, roll their initiative for you, and put them in order. The bot will pin the post to the channel to make it easy to reference during combat.
- $add : Command to insert a new character mid-combat. Use the same arguments for names, bonuses, and advantage as you do with the $i command.
- $end : Command to end combat. Init-Bot will wipe the order clean for next time.
