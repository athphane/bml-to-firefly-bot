import re

from bmlfireflybot import FIREFLY
from bmlfireflybot.firefly import the_regex
from bmlfireflybot.firefly.objects import ParsedTransaction, Currency


def parse_transaction(transaction_message: str):
    match = re.search(the_regex, transaction_message)

    if not match:
        return None

    card_num = match.group(1)
    datetime = match.group(2)
    currency = match.group(3)
    amount = match.group(4)
    location = match.group(5)

    return ParsedTransaction(card_num, datetime, currency, amount, location, transaction_message)


def get_transaction_currency(input_transaction: ParsedTransaction) -> Currency:
    currency_obj = FIREFLY.get_currency(input_transaction.currency)

    return Currency(
        currency_obj['id'],
        currency_obj['attributes']['code'],
        currency_obj['attributes']['name'],
        currency_obj['attributes']['symbol']
    )
