import os
import discord
from dotenv import load_dotenv
from discord import Message

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

from minimax_template import run_ralph
from openai.types.chat import ChatCompletionMessageParam


@client.event
async def on_ready():
    print(f"✅ Success! Logged in as {client.user}")


@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return

    messages: list[ChatCompletionMessageParam] = [
        {"role": "user", "content": message.content}
    ]
    response = run_ralph(messages)
    if response and response.choices[0].message.content:
        await message.channel.send(response.choices[0].message.content)


TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN is None:
    print("❌ ERROR: DISCORD_TOKEN not found in .env file!")
else:
    client.run(TOKEN)
