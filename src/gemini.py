import sys
from google.genai import types
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
import discord
import asyncio
import traceback
import os
from google import genai
import pathlib

from dataclass import GeminiConfig

from utils import signal, apply_custom_emoji
from config import WAITING_EMOJI

# client = None
# gemini_queue = None
# guild_genai_config = None

# async def init_worker(discord_client, queue, config):
#     global client, gemini_queue, guild_genai_config
#     client = discord_client
#     gemini_queue = queue
#     guild_genai_config = config

google_search_tool = Tool(
    google_search = GoogleSearch()
)

async def gemini_worker(client, gemini_queue, guild_genai_config):
    from dataclass import GeminiData
    while True:
        try:
            if gemini_queue:
                gemini_data: GeminiData = gemini_queue.pop(0)

                history = await call_gemini(gemini_data.guild_genai, gemini_data.msg, gemini_data.config, client)
                old_config = guild_genai_config[gemini_data.msg.guild.id]
                guild_genai_config[gemini_data.msg.guild.id] = GeminiConfig(old_config.temp, old_config.model, old_config.system_instruction, history)
            await asyncio.sleep(1)
        except Exception:
            await gemini_data.msg.add_reaction("❌")
            error_type, error_value, error_traceback = sys.exc_info()
            error_message = f"Error: {error_type.__name__}: {error_value}\n{''.join(traceback.format_tb(error_traceback))}"
            await signal(client, error_message)

async def call_gemini(genai_client: genai.Client, msg: discord.Message, config: GeminiConfig, client: discord.Client):
    gemini_tool = []
    
    if config.isGroundingEnable:
        gemini_tool.append(google_search_tool)
        print("grounding is enabled")
    
    ignored_files, attachments = [], []
    for i, attachment in enumerate(msg.attachments):
        filename = f"{msg.author.id}-{i}.{attachment.filename.split(".")[-1]}" # {userid}-{i}.{png,jpg,..etc}
        
        match attachment.filename.split(".")[-1]:
            case "jpg":
                mime_type = "image/jpeg"
            case "jpeg":
                mime_type = "image/jpeg"
            case "png":
                mime_type = "image/png"
            case "webp":
                mime_type = "image/webp"
            case "heif":
                mime_type = "image/heif"
            case "pdf":
                mime_type = "application/pdf"
            case "js":
                mime_type = "application/x-javascript"
            case "py":
                mime_type = "application/x-python"
            case "txt":
                mime_type = "text/plain"
            case "html":
                mime_type = "text/html"
            case "css":
                mime_type = "text/css"
            case "md":
                mime_type = "text/md"
            case "csv":
                mime_type = "text/csv"
            case "xml":
                mime_type = "text/xml"
            case "rtf":
                mime_type = "text/rtf"
            case "wav":
                mime_type = "audio/wav"
            case "mp3":
                mime_type = "audio/mp3"
            case "aiff":
                mime_type = "audio/aiff"
            case "aac":
                mime_type = "audio/aac"
            case "ogg":
                mime_type = "audio/ogg"
            case "flac":
                mime_type = "audio/flac"
            case "mp4":
                mime_type = "video/mp4"
            case "mpg":
                mime_type = "video/mpeg"
            case "mov":
                mime_type = "video/mov"
            case "avi":
                mime_type = "video/avi"
            case "flv":
                mime_type = "video/x-flv"
            case "mpg":
                mime_type = "video/mpg"
            case "webm":
                mime_type = "video/webm"
            case "wmv":
                mime_type = "video/wmv"
            case "3gpp":
                mime_type = "video/3gpp"
            case _:
                ignored_files.append(attachment.filename)
                break

        await attachment.save(fp=filename)

        # with open(filename, "rb") as f:
        #     data = base64.b64encode(f.read()).decode('utf-8')
        #     attachments.append({"mime_type": mime_type, "data": data})

        attachments.append(types.Part.from_bytes(
            data=pathlib.Path(filename).read_bytes(),
            mime_type=mime_type
        ))

        os.remove(filename)

    is_image_model = "image" in config.model
    if is_image_model:
        chat = genai_client.chats.create(
            model=config.model, 
            history=config.history, 
            config=types.GenerateContentConfig(
                temperature=config.temp,
                response_modalities=['Text', 'Image']
                )
            )
    else:
        chat = genai_client.chats.create(
            model=config.model, 
            history=config.history, 
            config=types.GenerateContentConfig(
                system_instruction=config.system_instruction, 
                temperature=config.temp,
                tools=gemini_tool,
                )
            )
    all_output = ""
    output = ""

    if ignored_files:
            output=f"-# 일부 파일은 처리되지 않았습니다: ({', '.join(ignored_files)})\n"
    all_output = output

    sent_msg: discord.Message = await msg.channel.send(WAITING_EMOJI)
    if is_image_model:
        response = chat.send_message([msg.content[2:]]+attachments)
        for chunk in response.candidates[0].content.parts:
            if chunk.text is not None:
                all_output+=chunk.text
                output+=chunk.text
                if len(output)<1801:
                    await sent_msg.edit(apply_custom_emoji(output))
                else:
                    await sent_msg.edit(apply_custom_emoji(output[:1800]))
                    output = output[1800:]
                    sent_msg = await msg.channel.send(apply_custom_emoji(output))
            elif chunk.inline_data is not None:
                filename = f"{msg.guild.id}.png"
                with open(filename, 'wb') as f:
                    f.write(chunk.inline_data.data)
                await msg.channel.send(file=discord.File(filename))
                os.remove(filename)
    else:
        response = chat.send_message_stream([msg.content[2:]]+attachments)
        for chunk in response:
            all_output+=chunk.text
            output+=chunk.text
            if len(output)<1801:
                await sent_msg.edit(apply_custom_emoji(output))
            else:
                await sent_msg.edit(apply_custom_emoji(output[:1800]))
                output = output[1800:]
                sent_msg = await msg.channel.send(apply_custom_emoji(output))
    
    await sent_msg.add_reaction("✅")

    return chat.get_history()