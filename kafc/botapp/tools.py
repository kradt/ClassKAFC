import telebot
import json
import os
from typing import Literal

cur_dir = os.path.dirname(os.path.abspath(__file__))


# Get dict with all bot_text
def get_text():
    with open(f"{cur_dir}/ua.json", encoding="utf-8") as file:
        bot_text: str = json.load(file)
        return bot_text


# Split the list into sublist
def split_list(arr, wanted_parts=1):
    arrs = []
    while len(arr) > wanted_parts:
        piece = arr[:wanted_parts]
        arrs.append(piece)
        arr = arr[wanted_parts:]
    arrs.append(arr)
    return arrs


# Create Inline Button by dict item
def create_button(text, value, value_type: Literal["call", "url"]):
    button = telebot.types.InlineKeyboardButton(text=text)
    if value_type == "call":
        button.callback_data = value
    elif value_type == "url":
        button.url = value
    else:
        raise ValueError("arg value_type must be 'call' or 'url'")
    return button


# Create Inline Keyboard by dict 
def create_inlineKeyboard(button_items: dict, row: int = 0, value_type: Literal["call", "url"]) -> object:
    """
        value_type can be "call" or "url" only
    """
    keyboard = telebot.types.InlineKeyboardMarkup()
    key_list = []

    for text in button_items:
        call_data = button_items.get(text)
        button = create_button(text, call_data, value_type)
        key_list.append(button)

    if row == 0:
        keyboard.add(*key_list)
        return keyboard

    for i in split_list(key_list, row):
        keyboard.add(*[name for name in i])

    return keyboard
