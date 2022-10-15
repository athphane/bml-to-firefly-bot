class Vendor:
    def __init__(self, data):
        self.name = data['name']
        self.categories = data['categories']

    def get_categories(self):
        return self.categories

    def has_multiple_categories(self):
        return len(self.categories) > 1
