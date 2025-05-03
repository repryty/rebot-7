from dataclass import ClientData
from . import register_command
from config import ADMIN_USER
import pickle

@register_command("purge")
async def execute(client_data: ClientData):
    if client_data.msg.author.id not in ADMIN_USER:
        return client_data
    with open(f"data/guild_genai_config.pickle", "wb") as f:
                    pickle.dump(dict(), f)
    with open(f"data/guild_genai.pickle", "wb") as f:
                    pickle.dump(dict(), f)
    client_data.msg.channel.send("✅")
    return client_data