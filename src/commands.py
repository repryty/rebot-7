import discord
import google.generativeai as genai
import anthropic
from dataclasses import dataclass
import base64
import os
import pickle
import re

from config import *

def apply_custom_emoji(inp: str)->str:
    for target, emoji in EMOJIES.items():
        inp = re.sub(target, emoji, inp)
    return inp

@dataclass
class GenerativeAI:
    model = "gemini-1.5-flash"
    is_gemini = True
    system_instruction = DEFAULT_INSTRUCTION
    temperature = 1.0
    max_token = 8192
    genration_config = {
        "temperature": 1.0,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    gemini_history = []
    claude_history = []

class Commands:
    def __init__(self, client: discord.client, msg: discord.Message, claude: anthropic.Anthropic, generativeAI: GenerativeAI) -> None:
        self.client: discord.client = client
        self.msg: discord.Message = msg # 유저가 호출한 메세지
        self.claude = claude
        self.generativeAI = generativeAI

        self.COMMANDS_LIST = {
            "핑": self.ping,
            "모델": self.model_list,
            "초기화": self.reset_model,
            "temp": self.set_temp,
            "eval": self.eval,
            "quit": self.quit,
            "명령어": self.print_commands_list
        }

    async def print_commands_list(self) -> None:
        await self.msg.channel.send(", ".join(self.COMMANDS_LIST.keys()))

    async def eval(self) -> None:
        if self.msg.author.id not in ADMIN_USER: return
        await self.msg.channel.send(f"```\n{eval(self.msg.content[7:])}\n```")

    async def quit(self) -> None:
        if self.msg.author.id not in ADMIN_USER: return
        quit()

    async def ping(self) -> None:
        await self.msg.channel.send(f"{self.client.latency * 1000:.3f}ms")
        
    async def model_list(self) -> None:
        gemini_model_list = ["gemini-1.5-pro", "gemini-1.5-flash"]+[i.name[7:] for i in genai.list_models() if ("generateContent" in i.supported_generation_methods) and ("exp" in i.name)]
        claude_model_list = ["claude-3-7-sonnet-latest", "claude-3-5-haiku-latest", "claude-3-opus-latest"]
        model_list = gemini_model_list+claude_model_list
        

        dropdown = discord.ui.Select(
            placeholder="모델 선택",
            options=[discord.SelectOption(label=i) for i in model_list]
        )

        async def callback(x: discord.Interaction):
            self.generativeAI.model = x.data['values'][0]
            self.generativeAI.is_gemini = "claude" not in self.generativeAI.model
            await x.response.send_message(embed=discord.Embed(title="REBOT LLM", color=MAIN_COLOR).add_field(name="다음 모델로 지정되었습니다!", value=x.data['values'][0]))

        dropdown.callback = callback

        view = discord.ui.View()
        view.add_item(dropdown)

        sent_msg = await self.msg.channel.send(embed=discord.Embed(title="REBOT LLM", color=MAIN_COLOR).add_field(name="모델을 선택해주세요!", value=f"현재 모델: {self.generativeAI.model}"), view=view)
        # await self.msg.channel.send(str(model_list))
    
    async def send_chat(self, generativeAI: GenerativeAI)->None:
        ignored_files = []
        
        gemini_attachments = []
        claude_attachments = []
        for i, attachment in enumerate(self.msg.attachments):
            filename = f"{self.msg.author.id}-{i}.{attachment.filename.split(".")[-1]}" # {userid}-{i}.{png,jpg,..etc}
            
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

            with open(filename, "rb") as f:
                data = base64.b64encode(f.read()).decode('utf-8')
                gemini_attachments.append({"mime_type": mime_type, "data": data})
                claude_attachments.append({
                    "type": "image", 
                    "source": {
                        "type": "base64",
                        "media_type": mime_type,
                        "data": data
                }})

            os.remove(filename)
        
        output = ""

        if ignored_files:
            output=f"-# 일부 파일은 처리되지 않았습니다: ({', '.join(ignored_files)})\n"

        all_output = output

        if generativeAI.is_gemini:
            model = genai.GenerativeModel(generativeAI.model, system_instruction=DEFAULT_INSTRUCTION).start_chat(history=generativeAI.gemini_history)

            response = model.send_message([self.msg.content[2:]]+gemini_attachments, generation_config={
                "temperature": generativeAI.temperature,
                "max_output_tokens": generativeAI.max_token,
            }, stream=True)
            sent_msg = await self.msg.channel.send("<a:loading:1264015095223287878>")
            for chunk in response:
                all_output+=chunk.text
                output=apply_custom_emoji(output+chunk.text)

                if len(output) >1900:
                    await sent_msg.edit("\n".join(output.split("\n")[0:-1]))
                    output = output.split("\n")[-1]
                    sent_msg = await self.msg.channel.send(output)

                await sent_msg.edit(output)
            # print(generativeAI.claude_history)
            
        else:
            generativeAI.claude_history.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": self.msg.content[2:]}
                ] + claude_attachments
                })
            sent_msg = await self.msg.channel.send("<a:loading:1264015095223287878>")
            with self.claude.messages.stream(
                model=self.generativeAI.model,
                max_tokens=2400,
                temperature=generativeAI.temperature,
                system=generativeAI.system_instruction,
                messages=generativeAI.claude_history
            ) as stream: # message.content[0].text
                for text in stream.text_stream:
                    output+=text
                    all_output+=text

                    if len(output) >1900:
                        await sent_msg.edit("\n".join(output.split("\n")[0:-1]))
                        output = output.split("\n")[-1]
                        sent_msg = await self.msg.channel.send(output)

                    await sent_msg.edit(content=output)

            generativeAI.claude_history.pop()
            
        generativeAI.claude_history+=[
            {
                "role": "user", 
                "content": [
                    {"type": "text", "text": self.msg.content[2:]}
                    ] + claude_attachments
            },
            {"role": "assistant", "content": all_output}]
        generativeAI.gemini_history+=[
            {
                "role": "user",
                "parts": [self.msg.content[2:]]+gemini_attachments
            },
            {
                "role": "model",
                "parts": all_output
            }
        ]

        os.makedirs(f"data/{self.msg.guild.id}", exist_ok=True)

        with open(f"data/{self.msg.guild.id}/generativeAI.pickle", "wb") as f:
            pickle.dump(generativeAI, f)

        await sent_msg.add_reaction("✅")

        return generativeAI

    async def reset_model(self):
        self.generativeAI.claude_history = []
        self.generativeAI.gemini_history = []

        await self.msg.channel.send(embed=discord.Embed(title="REBOT LLM", color=MAIN_COLOR).add_field(name="초기화에 성공했습니다!", value="Temperature, 모델은 초기화되지 않습니다."))

    async def set_temp(self):
        if len(self.msg.content)==6:
            await self.msg.channel.send(embed=discord.Embed(title="REBOT LLM", color=MAIN_COLOR).add_field(name=f"현재 Temperature는 {self.generativeAI.temperature}입니다.", value="Gemini는 0~2, Claude는 0~1 범위에서 설정됩니다."))        
        else:
            if self.generativeAI.is_gemini:
                self.generativeAI.temperature = max(0, min(2, float(self.msg.content[7:])))
            else:
                self.generativeAI.temperature = max(0, min(1, float(self.msg.content[7:])))

            await self.msg.channel.send(embed=discord.Embed(title="REBOT LLM", color=MAIN_COLOR).add_field(name=f"Temperature가 {self.generativeAI.temperature}로 설정되었습니다.", value="Gemini는 0~2, Claude는 0~1 범위에서 설정됩니다."))