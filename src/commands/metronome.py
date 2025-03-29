# from dataclass import ClientData
# from . import register_command
# from config import WARN_COLOR, MAIN_COLOR

# # import discord
# from discord import Embed
# import asyncio


# @register_command("메트로놈")
# async def execute(client_data: ClientData):
#     channel = client_data.msg.author.voice.channel
#     if channel == None:
#         await client_data.msg.channel.send(embed=Embed(title="REBOT METRONOME", color=WARN_COLOR).add_field(name="음성 채널에 연결해주세요!", value=""))
#         return client_data
#     if client_data.metronome_data.voice_client is None:
#         client_data.metronome_data.voice_client = await channel.connect()
#     if len(client_data.msg.content)>6: # 6
#         arg = client_data.msg.content[7:]
#         if arg == "OFF":
#             await client_data.metronome_data.voice_client.disconnect()
#         else:
#             client_data.metronome_data.tempo=int(arg)
#             await client_data.msg.channel.send(embed=Embed(title="REBOT METRONOME", color=MAIN_COLOR).add_field(name="빠르기가 설정되었습니다.", value=f"{client_data.msg.content[6:]}RPM"))
    
#     return client_data