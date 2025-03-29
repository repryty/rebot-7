import asyncio
import discord
import time

async def metronome_worker(voice_client: discord.VoiceClient, tempo: int):
    SLEEP_TIME = 60 / tempo - 00.12
    while True:
        print(time.time())
        await voice_client.play(discord.FFmpegPCMAudio("media/metronome.mp3"), wait_finish=True)
        await asyncio.sleep(SLEEP_TIME)