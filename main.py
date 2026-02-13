import os
import discord
from dotenv import load_dotenv
from discord import Message

# Load keys from the .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Define Intents (Must match what you toggled in the Dev Portal)
intents = discord.Intents.default()
intents.message_content = True 

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ Success! Logged in as {client.user}')

@client.event
async def on_message(message : Message):
    if message.author == client.user:
        return

    # Use 'in' to check if 'ping' exists anywhere in the message
    if 'ping' in message.content.lower():
        await message.channel.send(f'🏓 Pong! I heard you, {message.author.name}!')


# Load the token
TOKEN = os.getenv('DISCORD_TOKEN')

# Check if it actually exists before running
if TOKEN is None:
    print("❌ ERROR: DISCORD_TOKEN not found in .env file!")
else:
    client.run(TOKEN)