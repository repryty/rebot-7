import discord
from dotenv import load_dotenv
import os
from google import genai
import pickle
from typing import Dict, List
import traceback
import sys

from commands import COMMANDS_LIST
from config import ADMIN_USER
from utils import signal
from dataclass import ClientData, GeminiConfig, GeminiData, MetronomeData
from gemini import gemini_worker
from metronome import metronome_worker

load_dotenv(verbose=True)

GEMINI_TOKEN = os.getenv("REBOT_GEMINI_TOKEN")

guild_genai: Dict[int, genai.Client] = {}
guild_genai_config: Dict[int, GeminiConfig] = {}
guild_metronome: Dict[int, MetronomeData] = {}
gemini_queue: List[GeminiData] = []

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    global guild_genai_config, guild_genai
    await signal(client, "REEBOT is online.")
    await client.change_presence(
        activity=discord.Game("정상작동")
    )

    os.makedirs("data", exist_ok=True)

    try:
        with open(f"data/guild_genai.pickle", "rb") as f:
            guild_genai = pickle.load(f)
    except FileNotFoundError:
        guild_genai = {}
    
    try:
        with open(f"data/guild_genai_config.pickle", "rb") as f:
            guild_genai_config = pickle.load(f)
    except FileNotFoundError:
        guild_genai_config = {}

    # await init_worker(client, gemini_queue, guild_genai_config)
    client.loop.create_task(gemini_worker(client, gemini_queue, guild_genai_config))
    await signal(client, "Gemini Worker Started")

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    # print(1)
    if not message.content.startswith("ㄹ "): return
    await signal(client, f"{'[ADMIN]' if message.author.id in ADMIN_USER else '[USER]'} {message.content}")

    guild_id = message.guild.id
    if not guild_genai.get(guild_id):
        guild_genai[guild_id] = genai.Client(api_key=GEMINI_TOKEN)
    if not guild_genai_config.get(guild_id):
        guild_genai_config[guild_id] = GeminiConfig()
    if not guild_metronome.get(guild_id):
        guild_metronome[guild_id] = MetronomeData()

    client_data = ClientData(client, message, guild_genai_config[guild_id], guild_genai[guild_id], guild_metronome[guild_id])

    command = message.content.split()[1]
    if command in COMMANDS_LIST.keys():
        try:
            client_data: ClientData = await COMMANDS_LIST[command](client_data)
            guild_genai[guild_id] = client_data.genai_client
            guild_genai_config[guild_id] = client_data.genai_config
            guild_metronome[guild_id] = client_data.metronome_data
            
            if client_data.metronome_data.voice_client is not None:
                client.loop.create_task(metronome_worker(guild_metronome[guild_id].voice_client, guild_metronome[guild_id].tempo))
        except Exception:
            await message.add_reaction("❌")
            error_type, error_value, error_traceback = sys.exc_info()
            error_message = f"Error: {error_type.__name__}: {error_value}\n{''.join(traceback.format_tb(error_traceback))}"
            await signal(client, error_message)
    else:
        gemini_queue.append(GeminiData(message, guild_genai[guild_id], guild_genai_config[guild_id]))

if __name__ == "__main__":
    client.run(os.getenv("REBOT_DISCORD_TOKEN"))