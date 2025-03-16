from dataclass import ClientData
from . import register_command

@register_command("명령어")
async def execute(client_data: ClientData):
    from . import COMMANDS_LIST
    await client_data.msg.channel.send(", ".join(COMMANDS_LIST))
    return client_data