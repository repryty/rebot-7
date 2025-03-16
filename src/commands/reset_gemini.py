import discord

from dataclass import ClientData
from . import register_command
from config import MAIN_COLOR

@register_command("초기화")
async def execute(client_data: ClientData):
    client_data.genai_config.history = []

    await client_data.msg.channel.send(embed=discord.Embed(title="REBOT LLM", color=MAIN_COLOR).add_field(name="초기화에 성공했습니다!", value="Temperature, 모델은 초기화되지 않습니다."))

    return client_data