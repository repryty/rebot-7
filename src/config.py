import discord

WAITING_EMOJI = "<a:loading:1264015095223287878>"

with open("system_instruction/default_instruction.txt", "r", encoding="utf8") as f:
    DEFAULT_INSTRUCTION = f.read()

ADMIN_USER = [784412272805412895]

SIGNAL_CHANNEL = 1261486436771823700

MAIN_COLOR = discord.Colour.from_rgb(34, 75, 176) #224bb0
WARN_COLOR = discord.Colour.from_rgb(181, 0, 0) #b50000