import time
import logging
import googletrans
from googletrans import Translator
import json
from aiogram import Bot, Dispatcher, executor, types, filters

TOKEN = "<REDACTED>"
INITIAL_MESSAGE = "Hello {}, following languages are supported for the translation ([abbreviature] — [language]):\n" \
                  + "".join([f"{key} — {value}\n" for key, value in googletrans.LANGUAGES.items()]) \
                  + "* — default\n"
SEND_YOUR_TEXT = "Send your text for the translation:"
ERROR = "ERROR!"
ASK_ABOUT_LANGUAGE_SRC = "Language source abbreviature (default: auto-detect):"
ASK_ABOUT_LANGUAGE_DEST = "Language destination abbreviature (default: en):"
TRANSLATED_TEXT = "Translated text:\n{}"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)
translator = Translator(service_urls=['translate.google.com'])
