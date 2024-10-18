import discord
import requests
import random
import os
import re
import io
from dotenv import load_dotenv
from base64 import b64decode
from thingies import messages, how_commands, safe_eval, get_online_players, format_player_names

# Load environment variables
load_dotenv(dotenv_path="/DATA/Documents/alinea_bot/meow.env")
load_dotenv(dotenv_path="meow.env")
encoded_token = os.getenv("DISCORD_BOT_TOKEN")

if encoded_token:
    TOKEN = b64decode(encoded_token).decode()
else:
    print("Error: DISCORD_BOT_TOKEN is not set in the environment variables.")

CHANNEL_ID = 782651599926984704
COMMAND_PREFIX = ["--", "!"]

client = discord.Client()

# List to store AFK users
afk_users = []

# Preload sound files
correct_sound = requests.get("https://www.myinstants.com/media/sounds/correct.mp3").content
incorrect_sound = requests.get("https://www.myinstants.com/media/sounds/extremely-loud-incorrect-buzzer_0cDaG20.mp3").content

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

            if message.author.id == 897329902863384577 or message.author.display_name.lower() in ["aartizz", "notaartizz"]:
                await message.channel.send("nuh uh", reference=message)
                return
            
            # AFK Handling
            if command_body == "afk":
                if len(afk_users) == 0:
                    await message.channel.send(f"No one's AFK rn :3")
                else:
                    await message.channel.send(f"There are currently {len(afk_users)} AFK: {', '.join(sorted(afk_users))}", reference=message)    
                return
            
            # Online Handling
            elif command_body == "online":
                players, player_count = get_online_players()
                if players is not None:
                    player_names = format_player_names(players)
                    await message.channel.send(f"There are {player_count} people online: `{', '.join(player_names)}`", reference=message)
                else:
                    await message.channel.send("The server is currently offline or no players are online.", reference=message)
                return

            # Math Handling
            elif command_body.startswith("math "):
                equation = command_body[len("math "):]

                # Limit the input to 10 characters
                if len(equation) > 10:
                    await message.channel.send("Jump. <:mgc:1206606541206069300>", reference=message)
                    return

                equation = equation.replace('x', '*')  # Change 'x' to '*'
                
                # Ensure only valid characters are included in the equation
                equation = re.sub(r'[^0-9+\-*/().% ]', '', equation)
                
                # Special case: "Whats 9 plus 10?"
                if equation in ["9+10", "10+9"]:
                    await message.channel.send(f"`{equation}` is equal to `21`.", reference=message)
                    return

                # Check for forbidden '**' operator
                if '**' in equation:
                    await message.channel.send("Error: '**' operator is not allowed.", reference=message)
                    return

                # Evaluate the equation safely
                result = safe_eval(equation)
                if result is not None:
                    await message.channel.send(f"`{equation}` is equal to `{result}`.", reference=message)
                else:
                    await message.channel.send("Error: Invalid equation.", reference=message)
                return  # Exit after handling the command

            # Handle percentage commands dynamically for any "how" command
            if command_body.startswith("how"):
                # Extract the base command and input text after it
                parts = command_body.split(" ", 1)
                cmd = parts[0]  # The command itself, e.g., "howgay", "howdumb"
                input_text = parts[1].strip() if len(parts) > 1 else ""

                base_response = cmd[3:]

                # Check for matching command and input text in the command_conditions
                if cmd in how_commands:
                    for names, fixed_percentage in how_commands[cmd]:
                        if input_text.lower() in [name.lower() for name in names]:
                            percentage = fixed_percentage if fixed_percentage is not None else random.randint(75, 100)
                            break
                if cmd == "howsexy" and input_text.lower() not in ["aartizz", "arti", "<@897329902863384577>"]:
                    percentage = 420
                elif cmd == "howsexy":
                    percentage = random.randint(1, 25)
                elif cmd == "howbeautiful":
                    percentage = 1000
                else:
                    percentage = random.randint(1, 100)  # Default case
                # Send the response message
                await message.channel.send(f"{input_text} is {percentage}% {base_response}!", reference=message)
                return

            # Charisma Check
            elif command_body.startswith("charismacheck"):
                percentage = random.randint(1, 100)
                if message.reference and message.reference.resolved:
                    await message.channel.send(f"{message.reference.resolved.author.display_name}, you have {percentage}% Charisma today.", reference=message.reference)
                else:
                    await message.channel.send(f"You have {percentage}% Charisma today.", reference=message)
                return

            # Love checker
            elif command_body.startswith("lovechecker"):
                parts = command_body.split(" ", 1)
                cmd = parts[0]
                input_text = parts[1].strip() if len(parts) > 1 else ""
                if len(input_text) > 20:
                    await message.channel.send("Jump. <:mgc:1206606541206069300>", reference=message)
                    return

                if input_text.lower() in ["tobias and noiko", "noiko and tobias", "alvor and donkey", "donkey and alvor", "mike and toasted", "toasted and mike", "dub and mellie", "mellie and dub"]:
                    percentage = 200
                else:
                    percentage = random.randint(1, 100)
                await message.channel.send(f"{input_text} are {percentage}% in love <3", reference=message)
                return

            # Skibidi coin flip
            elif command_body.startswith("cf"):
                cf = random.randint(0,1)
                if cf == 0:
                    await message.channel.send("Heads.", reference=message)
                else:
                    await message.channel.send("Tails.", reference=message)
            
            # Yes/No check
            elif command_body.startswith("yn"):
                yn = random.randint(0,1)
                if yn == 0:
                    await message.channel.send("Yes.", reference=message)
                else:
                    await message.channel.send("No.", reference=message)

    if message.content.lower().startswith("meow, give me a fact"):
        await message.channel.send(random.choice(messages), reference=message)  
        return  
    elif message.content.lower().startswith("meow, lobotomize"):
        if message.reference is not None:
            await message.channel.send("🧠🔨", reference=message.reference)
        else:
            await message.channel.send("🧠🔨", reference=message)
        return
    elif message.content.lower().startswith("meow, kill this guy"):
        if message.reference is not None:
            await message.channel.send("🔫💨", reference=message.reference)
        else:
            await message.channel.send("🔫💨", reference=message)
        return
    
    elif "southside" in message.content:
        await message.channel.send("*shivers*")
    
    # AFK Handling
    if message.author.display_name.lower() not in afk_users and message.content.lower().startswith("afk"):
        if message.author.id == 897329902863384577 or message.author.display_name.lower() in ["aartizz", "notaartizz"]:
            await message.channel.send("nuh uh", reference=message)
            return
        afk_users.append(message.author.display_name)
        await message.channel.send("bet :3", reference=message)
        return

    # Handle user returning from AFK
    if message.author.display_name in afk_users:
        if not any(skibidi in message.content.lower() for skibidi in ["wb", "welcome back"]):
            afk_users.remove(message.author.display_name)
            await message.channel.send(f"{message.author.display_name}, wb :3", reference=message)
            return
    if message.author.id == 728771876356096013 and "left the game" in message.content.lower():
        for name in afk_users[:]:
            if name.lower() == message.content.lower().split(' left the game')[0].strip():
                afk_users.remove(name)
                await message.channel.send(f"{name} removed from AFK", reference=message)
                return
                
    # Check for "incorrect buzzer"
    elif "incorrect buzzer" in message.content.lower():
        await message.channel.send(file=discord.File(io.BytesIO(incorrect_sound), filename="incorrect.mp3"), reference=message)
        return 

    # Check for "correct buzzer"
    elif "correct buzzer" in message.content.lower():
        await message.channel.send(file=discord.File(io.BytesIO(correct_sound), filename="correct.mp3"), reference=message)
        return

    elif "meow never lies" in message.content.lower() or "meow doesnt lie" in message.content.lower():
        await message.channel.send("It's true <:veggie_skewer:1018647222793027584>", reference=message)

    # Check for "meow"
    elif re.search(r"\bmeow\b", message.content.lower()):
        await message.channel.send("That's me! <:dragon_head:1021517949737119856>", reference=message)

    elif re.search(r"\bliar\b", message.content.lower()) or re.search(r"\blies\b", message.content.lower()):
        await message.channel.send("meow never lies <:dragon_head:1021517949737119856>", reference=message)

    # Check for Kawaii language
    elif any(meow in message.content.lower() for meow in ["uwu", "owo", "qwq"]):
        if random.randint(1,4) == 1:
            await message.channel.send("OwO?", reference=message)
    
    # facts :3
    elif random.randint(1, 1000) == 420:
        await message.channel.send(random.choice(messages))

client.run(TOKEN)