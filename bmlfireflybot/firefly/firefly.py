import datetime
import json
import sys

import requests
from fuzzywuzzy import fuzz


class FireflyAPI:
    def __init__(self, base_url, api_key):
        # Set the base URL and API key for the API.
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "accept": "application/vnd.api+json",
        }

    def _construct_url(self, url):
        return f"{self.base_url}/api/v1/{url}"

    def _get(self, url, params=None):
        return requests.get(
            self._construct_url(url),
            headers=self.headers,
            params=params
        )

    def _post(self, url, body):
        return requests.post(
            self._construct_url(url),
            headers=self.headers,
            json=body
        )

    def get_transactions(self):
        print('firefly:transactions:getting all transactions')
        res = self._get('transactions')

        print('firefly:transactions:returning json response')
        return res.json()

    def get_transaction_journal(self, transaction_id):
        res = self._get(f'transaction-journals/{transaction_id}')
        return res.json()

    def get_accounts(self):
        print('firefly:accounts:getting all accounts')
        res = self._get('accounts')

        print('firefly:accounts:returning json response')
        return res.json()

    def get_expense_accounts(self):
        print('firefly:accounts:getting all expense accounts')
        res = self._get('accounts', params={'type': 'expense'})

        print('firefly:accounts:returning json response')
        return res.json()

    def find_account_by_name(self, name):
        print(f'firefly:accounts:finding account by name: {name}')
        name = name.lower()

        accounts = self.get_accounts()

        if accounts is not None:
            for account in accounts['data']:
                if account['attributes']['name'].lower() == name:
                    print('firefly:accounts:found account')
                    return account

        print('firefly:accounts:could not find account')
        return None

    def get_most_recent_categories(self):
        transactions = self.get_transactions()

        categories = []

        if transactions is not None:
            for transaction in transactions['data']['transactions']:
                category = transaction['category_id']

                if category not in categories:
                    categories.append(category)

        return categories

    @staticmethod
    def _write_json(data, filename):
        with open(filename, 'w') as f:
            f.write(json.dumps(data))

    def get_currency(self, input_currency):
        currencies = self._get('currencies').json()

        for currency in currencies['data']:
            # Only go through enabled currencies
            if currency['attributes']['enabled']:
                # Check if the currency code matches the input currency
                if currency['attributes']['code'] == input_currency:
                    return currency

        return None

    @staticmethod
    def fuzzy_search(x, y, threshold=40):
        return fuzz.ratio(x.lower(), y.lower()) >= threshold

    def find_similar_transactions_by_location(self, location):
        transactions = self.get_transactions()

        similar_transactions = []

        for transaction in transactions['data']:
            if transaction['attributes']['group_title'] is None:
                the_transaction = transaction['attributes']['transactions'][0]

                if self.fuzzy_search(the_transaction['destination_name'], location):
                    similar_transactions.append(the_transaction)

        return similar_transactions

    def create_withdrawal_transaction(
            self, description, amount, source_id,
            destination_name, category_name=None, notes=None
    ):
        response = self._post('transactions', {
            'transactions': [
                {
                    'type': 'withdrawal',
                    'date': datetime.datetime.now().__str__(),
                    'description': description,
                    'amount': amount,
                    'category_name': category_name,
                    'source_id': source_id,
                    'destination_name': destination_name,
                    'notes': notes
                }
            ]
        })

        return response.json()

    def create_foreign_withdrawal_transaction(
            self, description, amount, source_id, destination_name,
            foreign_currency_id=None, foreign_amount=None, category_name=None,
            notes=None
    ):
        response = self._post('transactions', {
            'transactions': [
                {
                    'type': 'withdrawal',
                    'date': datetime.datetime.now().__str__(),
                    'description': description,
                    'amount': amount,
                    'foreign_amount': foreign_amount,
                    'foreign_currency_id': foreign_currency_id,
                    'category_name': category_name,
                    'source_id': source_id,
                    'destination_name': destination_name,
                    'notes': notes
                }
            ]
        })

        return response.json()
