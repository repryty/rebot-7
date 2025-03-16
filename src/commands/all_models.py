from dataclass import ClientData
from . import register_command

@register_command("모델목록")
async def execute(client_data: ClientData):
    await client_data.msg.channel.send(', '.join([i.name[7:] for i in client_data.genai_client.models.list()]))
    return client_data