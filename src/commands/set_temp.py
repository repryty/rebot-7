import discord

from dataclass import ClientData
from . import register_command
from config import MAIN_COLOR

@register_command("temp")
async def execute(client_data: ClientData):
    if len(client_data.msg.content)==6:
        await client_data.msg.channel.send(embed=discord.Embed(title="REBOT LLM", color=MAIN_COLOR).add_field(name=f"현재 Temperature는 {client_data.genai_config.temp}입니다.", value="Gemini는 0~2, Claude는 0~1 범위에서 설정됩니다."))        
    else:
        client_data.genai_config.temp = max(0, min(2, float(client_data.msg.content[7:])))

        await client_data.msg.channel.send(embed=discord.Embed(title="REBOT LLM", color=MAIN_COLOR).add_field(name=f"Temperature가 {client_data.genai_config.temp}로 설정되었습니다.", value="Gemini는 0~2, Claude는 0~1 범위에서 설정됩니다."))

    return client_data