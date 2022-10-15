from pyrogram import emoji

from bmlfireflybot.database.vendors import VendorsDB


class Transaction:
    def __init__(self, transaction_data):
        self._id = transaction_data['_id']
        self.card_number = transaction_data['card_number']
        self.date = transaction_data['date']
        self.time = transaction_data['time']
        self.currency = transaction_data['currency']
        self.amount = transaction_data['amount']
        self.location = transaction_data['location']
        self.ref_no = transaction_data['ref_no']
        self.approval_code = transaction_data['approval_code']
        self.category = transaction_data['categories'] if 'categories' in transaction_data else None

    def get_hash(self):
        return hash(self)

    @staticmethod
    def make(record):
        return Transaction(record)

    def get_vendor(self):
        return self.location.lower()

    def format_transaction(self, category=None):
        formatted_message = (
            f"{emoji.SHOPPING_BAGS}: {self.location}\n"
            f"{emoji.COIN}: `{self.currency}{self.amount}`\n"
            f"{emoji.CREDIT_CARD}: `{self.card_number}`"
        )

        if category:
            formatted_message += (
                f"\n\n{emoji.CLIPBOARD}: `{category}`"
            )
        else:
            formatted_message += (
                f"\n\n{emoji.STOP_SIGN}This vendor has not been categorized yet! Please add a category!"
            )

        return formatted_message

    @property
    def id(self):
        return self._id
