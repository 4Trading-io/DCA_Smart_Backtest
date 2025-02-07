# ui_helpers.py

import telebot
from telebot import types

def get_language_keyboard():
    """Return a reply keyboard for language selection."""
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("English", "فارسی")
    return markup

def get_predefined_crypto_keyboard():
    """Return a reply keyboard with common crypto pair options."""
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.row("BTCUSDT", "ETHUSDT", "SOLUSDT", "SUIUSDT", "XRPUSDT")
    return markup

def get_confirmation_inline_keyboard(language="en"):
    """Return an inline keyboard for confirming user inputs."""
    markup = types.InlineKeyboardMarkup()
    if language == "fa":
        yes_text = "✅ بله"
        no_text  = "❌ خیر"
    else:
        yes_text = "✅ Yes"
        no_text  = "❌ No"

    yes_button = types.InlineKeyboardButton(text=yes_text, callback_data="confirm_yes")
    no_button  = types.InlineKeyboardButton(text=no_text, callback_data="confirm_no")
    markup.add(yes_button, no_button)
    return markup

def get_main_menu_keyboard(language="en"):
    """Return a main menu reply keyboard."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if language == "fa":
        markup.row("شروع تحلیل جدید", "راهنما")
    else:
        markup.row("Start New Analysis", "Help")
    return markup
