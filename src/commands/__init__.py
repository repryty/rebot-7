import os
import importlib

from . import *

COMMANDS_LIST = {}

def register_command(name: str):
    def decorator(func):
        global COMMANDS_LIST
        COMMANDS_LIST[name] = func
        return func
    return decorator

current_dir = os.path.dirname(os.path.abspath(__file__))
for file in os.listdir(current_dir):
    if file.endswith('.py') and file != '__init__.py':
        module_name = file[:-3]
        module = importlib.import_module(f"commands.{module_name}")

# from dataclass import ClientData
# from . import register_command

# @register_command("")
# async def execute(client_data: ClientData):

#     return client_data