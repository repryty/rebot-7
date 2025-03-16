from dataclasses import dataclass, field
import discord

from config import DEFAULT_INSTRUCTION

from typing import TYPE_CHECKING
# if TYPE_CHECKING:
from google import genai

@dataclass
class GeminiConfig:
    temp: int = 1
    model: str = "gemini-2.0-flash"
    system_instruction: str = DEFAULT_INSTRUCTION
    history: list = field(default_factory=list) 

@dataclass
class ClientData:
    client: discord.Client
    msg: discord.Message
    genai_config: GeminiConfig
    genai_client: genai.Client

@dataclass
class GeminiData:
    # sent_msg: discord.Message
    msg: discord.Message
    guild_genai: genai.Client
    config: GeminiConfig
