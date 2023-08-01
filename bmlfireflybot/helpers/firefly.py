import requests

from bmlfireflybot import FIREFLY_TOKEN, FIREFLY_ENDPOINT


class FireflyAPI:
    def __init__(self):
        # Set the base URL and API key for the API.
        self.base_url = FIREFLY_ENDPOINT
        self.api_key = FIREFLY_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "accept": "application/vnd.api+json",
        }

    def _get(self, url, body=None):
        url = f"{self.base_url}/{url}"
        print(url)

        return requests.get(
            url,
            headers=self.headers
        )

    def get_transactions(self, start_date: str = None, end_date: str = None) -> None:
        print('firefly:transactions:getting all transactions')
        res = self._get('transactions')

        print('firefly:transactions:returning json response')
        return res.json()

    def get_most_recent_categories(self):
        transactions = self.get_transactions()

        categories = []

        if transactions is not None:
            for transaction in transactions['data']['transactions']:
                category = transaction['category_id']

                if category not in categories:
                    categories.append(category)

        return categories
