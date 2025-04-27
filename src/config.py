import discord

WAITING_EMOJI = "<a:loading:1264015095223287878>"

with open("system_instruction/default_instruction.txt", "r", encoding="utf8") as f:
    DEFAULT_INSTRUCTION = f.read()

EMOJIES = {
    "🚪": "<:me:1144858072624406588>",
    "⭐": "<:star:1144858244909633619>",
    "❓": "<a:what:1144859308299923536>",
    "🚫": "<:no:1144857465566003253>",
    "🌸": "<:hwal:1144858220263907358>",
    "😊": "<:happy:1144857824866861056>",
    "✍🏼": "<:grab:1144857312377446410>",
    "😔": "<:hing:1144858197551759410>",
    "🫠": "<:liquid:1144857660836036609>",
    "😢": "<:sad:1144857284112040026>",
}

ADMIN_USER = [784412272805412895, 742067560144437269]

SIGNAL_CHANNEL = 1261486436771823700

MAIN_COLOR = discord.Colour.from_rgb(34, 75, 176) #224bb0
WARN_COLOR = discord.Colour.from_rgb(181, 0, 0) #b50000