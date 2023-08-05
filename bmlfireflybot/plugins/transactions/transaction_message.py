import re

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from bmlfireflybot import BmlFireflyBot, FIREFLY, FIREFLY_ENDPOINT
from bmlfireflybot.firefly import the_regex, parse_transaction
from bmlfireflybot.helpers import custom_filters
from playground.main import get_transaction_currency


@BmlFireflyBot.on_message(filters.text & filters.regex(the_regex, re.IGNORECASE))
async def transaction_message_handler(bot, message: Message):
    transaction = parse_transaction(message.text)
    transactions = FIREFLY.find_similar_transactions_by_location(transaction.location)

    buttons = []
    for x in transactions:
        button_label = f"{x['description']} | B:{x['budget_name']} | C:{x['category_name']}"
        buttons.append([InlineKeyboardButton(button_label, callback_data=f"save_as+{x['transaction_journal_id']}")])

    reply_text = f"`{message.text}`" + "\n\n" + "Choose a description to save as, or reply to this with your own: "
    await message.reply(
        reply_text,
        reply_markup=InlineKeyboardMarkup(buttons) if len(buttons) > 0 else None,
        reply_to_message_id=message.id
    )


@BmlFireflyBot.on_callback_query(custom_filters.callback_query('save_as'))
async def save_as_callback(bot: BmlFireflyBot, callback: CallbackQuery):
    await callback.answer()

    referring_transaction = FIREFLY.get_transaction_journal(callback.payload)['data']['attributes']['transactions'][0]

    transaction = parse_transaction(callback.message.reply_to_message.text)
    currency = get_transaction_currency(transaction)

    if transaction.is_foreign():
        firefly_transaction = FIREFLY.create_foreign_withdrawal_transaction(
            description=referring_transaction['description'],
            amount=transaction.local_amount(),
            source_id=1,
            destination_name=transaction.location,
            foreign_currency_id=currency.id,
            foreign_amount=transaction.amount,
            category_name=referring_transaction['category_name'],
            notes=callback.message.reply_to_message.text
        )
    else:
        firefly_transaction = FIREFLY.create_withdrawal_transaction(
            description=referring_transaction['description'],
            amount=transaction.amount,
            source_id=1,
            destination_name=transaction.location,
            category_name=referring_transaction['category_name'],
            notes=callback.message.reply_to_message.text
        )

    await callback.message.edit(
        text=f"Transaction saved as \"{referring_transaction['description']}\"",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "View on Firefly",
                        url=f"{FIREFLY_ENDPOINT}/transactions/show/{firefly_transaction['data']['id']}"
                    )
                ]
            ]
        ),
    )
