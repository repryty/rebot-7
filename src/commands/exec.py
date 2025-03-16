from dataclass import ClientData
from . import register_command
from config import ADMIN_USER

@register_command("exec")
async def execute(client_data: ClientData):
    if client_data.msg.author.id not in ADMIN_USER: return
    await client_data.msg.channel.send(f"```\n{exec(client_data.msg.content[7:])}\n```")
    return client_data