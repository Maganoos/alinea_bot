import discord
import requests
import random
import os
import re
import io
from dotenv import load_dotenv
from base64 import b64decode
import datetime

# Load environment variables
load_dotenv(dotenv_path="/DATA/Documents/alinea_bot/meow.env")
encoded_token = os.getenv("DISCORD_BOT_TOKEN")

if encoded_token:
    TOKEN = b64decode(encoded_token).decode()
else:
    print("Error: DISCORD_BOT_TOKEN is not set in the environment variables.")

CHANNEL_ID = 782651599926984704
COMMAND_PREFIX = ["--", "!"]

client = discord.Client()

# Dictionary to store AFK users
afk_users = {}

# Function to fetch online players from the Minecraft server
def get_online_players():
    url = "https://api.mcsrvstat.us/3/play.alinea.gg"
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        responseData = response.json()

        if responseData.get("online"):
            players_list = responseData.get("players", {}).get("list", [])
            player_count = responseData.get("players", {}).get("online", 0)
            return players_list, player_count
        else:
            print("Server is offline or no data available.")
            return None, 0
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None, 0

def format_player_names(players):
    if not isinstance(players, list):
        print("Invalid players data:", players)
        return []

    player_names = [player['name'] for player in players if isinstance(player, dict) and 'name' in player]
    player_names.extend(["DanTDM", "CaptainSparklez"])  # Add fixed names
    player_names.sort()
    return player_names

def safe_eval(expression):
    """Safely evaluate an expression using a limited eval."""
    allowed_names = {
        'sum': sum,
    }
    
    try:
        # Only allow numbers, operators, and certain functions
        result = eval(expression, {"__builtins__": None}, allowed_names)
        return result
    except (NameError, SyntaxError, TypeError, ZeroDivisionError) as e:
        print(f"Error evaluating expression: {e}")
        return None

# Preload sound files
correct_sound_url = "https://www.myinstants.com/media/sounds/correct.mp3"
incorrect_sound_url = "https://www.myinstants.com/media/sounds/extremely-loud-incorrect-buzzer_0cDaG20.mp3"

correct_sound = requests.get(correct_sound_url).content
incorrect_sound = requests.get(incorrect_sound_url).content

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # Check if the message is in the correct channel
    if message.channel.id != CHANNEL_ID:
        return

    # Command handling
    for prefix in COMMAND_PREFIX:
        if message.content.startswith(prefix):
            command_body = message.content[len(prefix):].strip()  # Get the command body
            # AFK Handling
            if command_body == "afk":
                await message.channel.send(f"There are currently {len(afk_users)} AFK: {', '.join(sorted(afk_users.keys()))}")
                return
            
            # Online Handling
            elif command_body == "online":
                players, player_count = get_online_players()
                if players is not None:
                    player_names = format_player_names(players)
                    await message.channel.send(f"There are {player_count} people online: {', '.join(player_names)}")
                else:
                    await message.channel.send("The server is currently offline or no players are online.")
                return

            # Math Handling
            elif command_body.startswith("math "):
                equation = command_body[len("math "):]

                # Limit the input to 10 characters
                if len(equation) > 10:
                    await message.channel.send("Jump. <:mgc:1206606541206069300>")
                    return

                equation = equation.replace('x', '*')  # Change 'x' to '*'
                
                # Ensure only valid characters are included in the equation
                equation = re.sub(r'[^0-9+\-*/().% ]', '', equation)
                
                # Special case: "Whats 9 plus 10?"
                if equation in ["9+10", "10+9"]:
                    await message.channel.send(f"`{equation}` is equal to `21`.")
                    return

                # Check for forbidden '**' operator
                if '**' in equation:
                    await message.channel.send("Error: '**' operator is not allowed.")
                    return

                # Evaluate the equation safely
                result = safe_eval(equation)
                if result is not None:
                    await message.channel.send(f"`{equation}` is equal to `{result}`.")
                else:
                    await message.channel.send("Error: Invalid equation.")
                return  # Exit after handling the command

            # Handle percentage commands dynamically for any "how" command
            elif command_body.startswith("how"):
                # Extract the base command and input text after it
                parts = command_body.split(" ", 1)
                cmd = parts[0]  # The command itself, e.g., "howgay", "howdumb"
                input_text = parts[1].strip() if len(parts) > 1 else ""

                # Use the part of the command after "how" as the base response
                base_response = cmd[3:]

                # Handle special cases for certain users
                if cmd == "howgay" and input_text.lower() in ["tobi", "tobiasde", "tobias", "<@795312567299080212>", "alvor", "donkey", "<@453261648342548480>", "jeremy", "jerelax"]:
                    percentage = 150
                elif cmd == "howskibidi" and input_text.lower() in ["binero", "jeroen", "<@297056581860851712>"]:
                    percentage = 200
                elif cmd == "howbi" and input_text.lower() in ["magnus", "maganoos", "<@885157323880935474>", "dub", "dublelolo_ornot", "<@914727951701012560>", "toben", "mia", "x_m1axq", "isla", "<@1080131668289003580>"]:
                    percentage = 100
                elif cmd == "howskibidi" and input_text.lower() in ["jeremy", "jerelax", "<@453261648342548480>", "aartizz", "arti", "<@897329902863384577>"]:
                    percentage = -100
                elif cmd == "howuncool" and input_text.lower() in ["aartizz", "arti", "<@897329902863384577>"]:
                    percentage = 200
                elif cmd == "howginger" and input_text.lower() in ["mia", "x_m1axq", "isla", "<@1080131668289003580>"]:
                    percentage = 200
                elif cmd == "howlonely" and input_text.lower() in ["mrfunny", "funny", "<@582106808735498240>"]:
                    percentage = 690
                elif cmd == "howsexy" and input_text.lower() not in ["aartizz", "arti", "<@897329902863384577>"]:
                    percentage = 420
                elif cmd in ["howawful","howbad","howdreadful","howmiserable","howterrible","howhorrible","howappalling","howatrocious","howghastly","howhideous","hownasty","howunpleasant","howrevolting","howdisgusting","howgrim","howdire","howabysmal","howhorrendous","howpathetic","howpitiful","howvile","howloathsome","howwretched","howdetestable","howpoor","howshit","howstinky","howghetto"] and input_text.lower() == "southside":
                    percentage = 690
                elif input_text.lower() in ["tobi", "tobiasde", "tobias", "<@795312567299080212>"]:
                    percentage = random.randint(75, 100)
                else:
                    # Generate a random percentage for all other cases
                    percentage = random.randint(0, 100)
                # Send the response message
                await message.channel.send(f"{input_text} is {percentage}% {base_response}!")
                return

            #Charisma Check
            elif command_body.startswith("charismacheck"):
                percentage = random.randint(0, 100)
                await message.channel.send(f"You have {percentage}% Charisma today.")
                return
            
            # Love checker
            elif command_body.startswith("lovechecker"):
                parts = command_body.split(" ", 1)
                cmd = parts[0]
                input_text = parts[1].strip() if len(parts) > 1 else ""
                if len(input_text) > 20:
                    await message.channel.send("Jump. <:mgc:1206606541206069300>")
                    return
                
                if input_text.lower() in ["tobias and noiko", "noiko and tobias", "alvor and donkey", "donkey and alvor", "mike and toasted", "toasted and mike", "dub and mellie", "mellie and dub"]:
                    percentage = 200
                else:
                    percentage = random.randint(0, 100)
                await message.channel.send(f"{input_text} are {percentage}% in love <3")
                return
            
            # stupid useless command
            elif command_body.startswith("eval"):
                parts = command_body.split(" ", 1)
                cmd = parts[0]
                input_text = parts[1].strip() if len(parts) > 1 else ""
                
                if len(input_text) > 10:
                    await message.channel.send("Jump. <:mgc:1206606541206069300>")
                    return
                
                result = re.sub(r'[^0-9]', '', input_text)
                await message.channel.send(f"`{input_text}` is equal to `{result}`")
                
            #skibidi afk list
            elif command_body.startswith("afk"):
                await message.channel.send(f"There are currently {len(afk_users)} AFK: {', '.join(sorted(afk_users.keys()))}")
                
                
    # Check for "incorrect buzzer"
    if "incorrect buzzer" in message.content.lower():
        await message.channel.send(file=discord.File(io.BytesIO(incorrect_sound), filename="incorrect.mp3"))
        return 
    # Check for "correct buzzer"
    elif "correct buzzer" in message.content.lower():
        await message.channel.send(file=discord.File(io.BytesIO(correct_sound), filename="correct.mp3"))
        return
    
    # Check for Meow
    elif "meow" in message.content.lower():
        await message.channel.send("That's me! <:dragon_head:1021517949737119856>")
        
    # Check for Kawaii shit
    elif any(meow in message.content.lower() for meow in ["uwu", "owo", "qwq"]):
        await message.channel.send("OwO?")

    # Check for AFK status (text trigger)
    if message.content.lower().startswith("afk") and message.author.display_name.lower() not in afk_users:
        # Mark user as AFK
        afk_users[message.author.display_name.lower()] = datetime.datetime.now().timestamp()
        timestamp = int(afk_users[message.author.display_name.lower()])
        await message.channel.send(f"{message.author.display_name} is now AFK. <t:{timestamp}:R>")
        return

    # Handle user returning from AFK
    if message.author.display_name.lower() in afk_users:
        del afk_users[message.author.display_name.lower()]
        await message.channel.send(f"{message.author.display_name} is no longer AFK.")

    # Additional logic for handling AFK users mentioned
    for display_name, timestamp in afk_users.items():
        if display_name in message.content.lower() and message.author.display_name != "Karl":
            await message.channel.send(f"{message.author.display_name}, {display_name} is currently AFK since <t:{int(timestamp)}:R>.")
            return

client.run(TOKEN)
