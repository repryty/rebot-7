from dataclasses import dataclass
import discord

@dataclass
class Config:
    ADMIN_ID: set[int] = frozenset({
        784412272805412895, 
        742067560144437269
    })

    NOTICE_CHANNEL: int = 1261486436771823700
    BOOTH_NOTICE_CHANNEL: int = 1335158194028154920

    MAIN_COLOR = discord.Colour.from_rgb(34, 75, 176)

    WARN_COLOR = discord.Colour.from_rgb(181, 0, 0)
    
    EMOJI = {
        r"🚪": "<:me:1144858072624406588>",
        r"⭐": "<:star:1144858244909633619>",
        r"❓": "<a:what:1144859308299923536>",
        r"🚫": "<:no:1144857465566003253>",
        r"🌸": "<:hwal:1144858220263907358>",
        r"😊": "<:happy:1144857824866861056>",
        r"✍🏼": "<:grab:1144857312377446410>",
        r"😔": "<:hing:1144858197551759410>",
        r"🫠": "<:liquid:1144857660836036609>",
        r"😢": "<:sad:1144857284112040026>",
    }