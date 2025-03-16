import base64

from dataclass import ClientData
from . import register_command

@register_command("b64d")
async def execute(client_data: ClientData):
    await client_data.msg.channel.send(base64.b64decode(client_data.msg.content[7:].encode('utf-8')).decode('utf-8'))
    return client_data