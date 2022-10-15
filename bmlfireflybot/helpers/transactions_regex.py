import re

from bmlfireflybot.database.models.Transaction import Transaction


async def extract_transaction_data(message):
    regex = re.compile(
        r'.*(?P<card_number>\d{4}).*(?P<date>\d{2}\/\d{2}\/\d{2}).*(?P<time>\d{2}:\d{2}:\d{2}).*(?P<currency>MVR|USD)(?P<amount>\d*.\d{2}).*at\s(?P<location>.*)\swas.*No.(?P<ref_no>\d*),.*:(?P<approval_code>\d*)'
    )

    results = regex.match(message)

    return results.groupdict()
