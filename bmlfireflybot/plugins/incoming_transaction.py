from pprint import pprint

from pykeyboard import InlineKeyboard, InlineButton
from pyrogram import Client
from pyrogram import emoji
from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup
from pyrogram.types import Message

from bmlfireflybot.database.models.Transaction import Transaction
from bmlfireflybot.database.models.Vendor import Vendor
from bmlfireflybot.database.transactions import TransactionsDB
from bmlfireflybot.database.vendors import VendorsDB
from bmlfireflybot.helpers import custom_filters
from bmlfireflybot.helpers.firefly import FireflyAPI
from bmlfireflybot.helpers.transactions_regex import extract_transaction_data


@Client.on_message(filters.text & filters.regex('Transaction from'))
async def incoming_transaction(bot, message: Message):
    # On message, create new transaction record on bot db and save.
    transaction_data = await extract_transaction_data(message.text)
    transaction: Transaction = TransactionsDB().create(transaction_data)

    # If the vendor is not recognized, that means it also does not have a determined category.
    # Add to the message and inform that they should categorize the vendor.

    vendor: Vendor = VendorsDB().find(transaction.get_vendor())

    keyboard = InlineKeyboard(row_width=3)

    if vendor:
        if vendor.has_multiple_categories():
            for x in vendor.get_categories():
                keyboard.add(
                    InlineButton('1', f"set_category+{transaction.id}:{x.name}"),
                )

    new_message = transaction.format_transaction(vendor)

    if not vendor:
        keyboard.add(
            InlineButton(
                f"{emoji.SHOPPING_BAGS} Assign Category",
                f"assign_category+{transaction.ref_no}:{transaction_data['location'].lower()}"
            )
        )

    await message.reply(new_message, reply_markup=keyboard, reply_to_message_id=message.id)
    # Bot should provide a button where it says "Assign Category".
    # User must simply send a text with the preferred category.

    # Go back to the top

    # If the vendor is recognized, then the formatted message should contain the category in
    # the message as well

    # The user will be shown a button list of categories that have already been assigned to the vendor.
    # A button should be provided to add a category by typing in another category.

    # If an existing category is selected, then the message should reflect this change
    # If a new category is added, the new category should be assigned to the vendor, and then the
    # message should also be updated with the new category.

    # A button should be provided to approve the categorization and add to FireFly
    # Once the transaction is added to FireFly, the formatted message should show that it's been added to
    # FireFly, and a new button should be shown, linking directly to the newly created transaction.


@Client.on_callback_query(custom_filters.callback_query('assign_category'))
async def assign_category_to_vendor_step_one(_, callback: CallbackQuery):
    await callback.answer(callback.payload)

    keyboard = InlineKeyboard(row_width=3)
    keyboard.add(
        InlineButton(f"Transaction for {callback.payload}", f"fake_button+{callback.payload.split(':')[0]}")
    )

    await callback.edit_message_text('Reply to this message with a new category to assign', reply_markup=keyboard)


@Client.on_message(filters.reply & filters.text)
async def save_new_category_to_vendor(bot, message: Message):

    transactions = FireflyAPI().get_transactions()

    pprint(transactions, indent=4)

    if not isinstance(message.reply_to_message.reply_markup, InlineKeyboardMarkup):
        return

    transaction_id = message.reply_to_message.reply_markup.inline_keyboard[0][0].callback_data

    if transaction_id.startswith('fake_button+'):
        transaction_id = transaction_id.lstrip('fake_button+')

    transaction = TransactionsDB().find(transaction_id)

    if transaction:
        vendor: Vendor = VendorsDB().find(transaction.get_vendor())

        if vendor:
            VendorsDB().assign_category(transaction.get_vendor(), message.text)
            categories = VendorsDB().get_categories(transaction.get_vendor())

    await message.reply(message.text)


@Client.on_callback_query(custom_filters.callback_query('fake_button'))
async def fake_button(_, callback: CallbackQuery):
    await callback.answer()
