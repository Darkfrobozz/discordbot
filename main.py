import os
import discord
from dotenv import load_dotenv

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
async def on_message(message):
    # Don't reply to yourself
    if message.author == client.user:
        return

    if message.content.lower() == 'ping':
        await message.channel.send('🏓 Pong! Your Raspberry Pi is talking to you.')

# Load the token
TOKEN = os.getenv('DISCORD_TOKEN')

# Check if it actually exists before running
if TOKEN is None:
    print("❌ ERROR: DISCORD_TOKEN not found in .env file!")
else:
    client.run(TOKEN)