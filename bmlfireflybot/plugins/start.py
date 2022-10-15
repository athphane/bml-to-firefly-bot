from pyrogram import Client
from pyrogram import filters


@Client.on_message(filters.command('start'))
def start_command(bot, message):
    message.reply('Hello from BML to Firefly-III bot.')
