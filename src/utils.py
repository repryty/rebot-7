from config import SIGNAL_CHANNEL, EMOJIES
import re

async def signal(client, text: str, where_to: int = SIGNAL_CHANNEL)->None:
    print(text)
    try:
        await client.get_channel(where_to).send(text)
    except Exception as e:
        print(f"Error: {e}")

def apply_custom_emoji(inp: str)->str:
    for target, emoji in EMOJIES.items():
        inp = re.sub(target, emoji, inp)
    return inp