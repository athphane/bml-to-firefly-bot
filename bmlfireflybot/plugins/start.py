import re

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from bmlfireflybot import BmlFireflyBot, FIREFLY, FIREFLY_ENDPOINT
from bmlfireflybot.firefly import the_regex
from bmlfireflybot.firefly.helpers import parse_transaction, get_transaction_currency
from bmlfireflybot.firefly.objects import ParsedTransaction, Currency
from bmlfireflybot.helpers import custom_filters


@BmlFireflyBot.on_message(filters.command('start'))
def start_command(bot, message):
    message.reply('Hello from BML to Firefly-III bot.')


