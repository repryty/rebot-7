import discord

from dataclass import ClientData
from . import register_command
from config import MAIN_COLOR

@register_command("모델")
async def execute(client_data: ClientData):
    model_name = client_data.msg.content[5:]
    if model_name:
        client_data.genai_config.model=model_name
        await client_data.msg.channel.send(embed=discord.Embed(title="REBOT LLM", color=MAIN_COLOR).add_field(name="다음 모델로 지정되었습니다.", value=model_name))
    else:
        gemini_model_list = ["gemini-2.0-flash", "gemini-2.0-flash-lite"]+[i.name[7:] for i in client_data.genai_client.models.list() if ("generateContent" in i.supported_actions) and (("exp" in i.name) or ("preview" in i.name)]
        model_list = gemini_model_list
        

        dropdown = discord.ui.Select(
            placeholder="모델 선택",
            options=[discord.SelectOption(label=i) for i in model_list]
        )

        async def callback(x: discord.Interaction):
            client_data.genai_config.model = x.data['values'][0]
            await x.response.send_message(embed=discord.Embed(title="REBOT LLM", color=MAIN_COLOR).add_field(name="다음 모델로 지정되었습니다.", value=x.data['values'][0]))

        dropdown.callback = callback

        view = discord.ui.View()
        view.add_item(dropdown)

        await client_data.msg.channel.send(embed=discord.Embed(title="REBOT LLM", color=MAIN_COLOR).add_field(name="모델을 선택해주세요.", value=f"현재 모델: {client_data.genai_config.model}"), view=view)
        # await self.msg.channel.send(str(model_list))
    
    return client_data
