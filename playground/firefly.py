import requests


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

    def _get(self, url, params=None):
        url = f"{self.base_url}/api/v1/{url}"
        print(url)

        return requests.get(
            url,
            headers=self.headers,
            params=params
        )

    def get_transactions(self):
        print('firefly:transactions:getting all transactions')
        res = self._get('transactions')

        print('firefly:transactions:returning json response')
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
