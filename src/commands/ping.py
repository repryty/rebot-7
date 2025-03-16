from dataclass import ClientData
from . import register_command

@register_command("핑")
async def execute(client_data: ClientData):
    await client_data.msg.channel.send(f"{client_data.client.latency * 1000:.3f}ms")
    return client_data