from dataclass import ClientData
from . import register_command
from config import ADMIN_USER

@register_command("quit")
async def execute(client_data: ClientData):
    if client_data.msg.author.id not in ADMIN_USER: return
    quit()
    