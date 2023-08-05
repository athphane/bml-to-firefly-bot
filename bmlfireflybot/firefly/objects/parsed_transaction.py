class ParsedTransaction(object):
    def __init__(self, card_num, datetime, currency, amount, location, raw):
        self.card_num: str = card_num
        self.datetime = datetime
        self.currency: str = currency
        self.amount: float = float(amount)
        self.location: str = location
        self.raw = raw

        self.clean_transaction_location()

    def clean_transaction_location(self):
        self.location = self.location.split('*')[0]

    def local_amount(self):
        if self.currency == 'USD':
            return self.amount * 15.42

        if self.currency == 'EUR':
            return self.amount * 16.80

        return self.amount

    def is_foreign(self):
        return self.currency != 'MVR'

    def __str__(self):
        return f'{self.card_num} | {self.datetime} | {self.currency} | {self.amount} | {self.location}'
