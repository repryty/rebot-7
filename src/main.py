import discord
from dotenv import load_dotenv
import os
import google.generativeai as genai
import asyncio
import pickle

from commands import *

load_dotenv(verbose=True)

genai.configure(api_key=os.getenv("REBOT_GEMINI_TOKEN"))

intents = discord.Intents.default()
intents.message_content = True

client = discord.Bot(intents=intents)

genai_queue = []
guild_genai = dict()

async def signal(text: str, where_to: int)->None:
    print(text)
    await client.get_channel(where_to).send(text)

@client.listen(once=True)
async def on_ready():
    global genai_queue
    await signal("REBOT is Online", SIGNAL_CHANNEL)
    await client.change_presence(
        activity=discord.Game("리프봇!")
    )

    os.makedirs("data", exist_ok=True)

    with os.scandir("data") as entries:
        for entry in entries:
            with open(f"data/{entry.name}/generativeAI.pickle", "rb") as f:
                guild_genai[int(entry.name)] = pickle.load(f)

    while True:
        if len(genai_queue)>0:
            data = genai_queue.pop(0)
            # print(data)
            guild_genai[data[1]] = await data[0].send_chat(guild_genai.get(data[1]))
        await asyncio.sleep(1.0)

claude = anthropic.Anthropic(api_key=os.getenv("REBOT_ANTHROPIC_KEY"))

@client.listen()
async def on_message(message: discord.Message):
    if not message.content.startswith("ㄹ "): return

    print(f"{'[ADMIN]' if message.author.id in ADMIN_USER else '[USER]'} {message.content}")

    global genai_queue
    global guild_genai

    if not guild_genai.get(message.guild.id):
        guild_genai[message.guild.id] = GenerativeAI()
    
    # print(message.content)
    commands = Commands(client, message, claude, guild_genai[message.guild.id]).COMMANDS_LIST.get(message.content.split()[1])
    # print(message.content[2:])
    if commands!=None:
        await commands()
    else:
        genai_queue.append([Commands(client, message, claude, guild_genai[message.guild.id]), message.guild.id])

if __name__ == "__main__":
    client.run(os.getenv("REBOT_DISCORD_TOKEN"))