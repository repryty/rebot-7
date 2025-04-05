from dataclass import ClientData
from . import register_command
from config import MAIN_COLOR
from discord import Embed

@register_command("g")
@register_command("grounding")
async def execute(client_data: ClientData):
    client_data.genai_config.isGroundingEnable = not client_data.genai_config.isGroundingEnable
    await client_data.msg.channel.send(embed=Embed(title="REBOT LLM", color=MAIN_COLOR).add_field(name="Grounding 설정이 변경되었습니다.", value="True" if client_data.genai_config.isGroundingEnable else "False"))
    return client_data