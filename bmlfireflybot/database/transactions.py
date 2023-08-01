from bmlfireflybot.database import database
from bmlfireflybot.database.models.Transaction import Transaction


class TransactionsDB:
    def __init__(self):
        self.transactions = database()['transactions']

    def get(self):
        transactions = self.transactions.find()
        return transactions

    def find(self, transaction_id):
        query = {
            "_id": transaction_id
        }

        record = self.transactions.find_one(query)

        if not record:
            return None

        return Transaction.make(record)

    def create(self, transaction_data):

        data = {
            'card_number': transaction_data['card_number'],
            'date': transaction_data['date'],
            'time': transaction_data['time'],
            'currency': transaction_data['currency'],
            'amount': transaction_data['amount'],
            'location': transaction_data['location'],
            'ref_no': transaction_data['ref_no'],
            'approval_code': transaction_data['approval_code'],
        }

        res = self.transactions.insert_one(data)

        return self.find(res.inserted_id)

    def find_or_create(self, transaction_date):
        transaction = self.find(transaction_date)

        if transaction is None:
            self.create(transaction_date)
            transaction = self.find(transaction_date)

        return transaction

    def delete(self, transaction_date):
        self.transactions.delete_many({'name': transaction_date})
