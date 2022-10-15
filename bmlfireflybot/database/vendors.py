from bmlfireflybot.database import database
from bmlfireflybot.database.models.Vendor import Vendor


class VendorsDB:
    def __init__(self):
        self.vendors = database()['vendors']

    def get(self):
        vendors = self.vendors.find()

        return [Vendor(x) for x in vendors]

    def find(self, vendor_id):
        query = {
            "_id": vendor_id
        }
        record = self.vendors.find_one(query)

        if record:
            return Vendor(record)

        return None

    def find_by_name(self, vendor_name):
        query = {
            'name': vendor_name
        }

        record = self.vendors.find_one(query)

        if record:
            return Vendor(record)

        return None

    def create(self, vendor_name):
        data = {
            'name': vendor_name
        }

        self.vendors.insert_one(data)

        return self.find(vendor_name)

    def find_or_create(self, vendor_name):
        vendor = self.find(vendor_name)

        if vendor is None:
            self.create(vendor_name)
            vendor = self.find(vendor_name)

        return vendor

    def delete(self, vendor_name):
        self.vendors.delete_many({'name': vendor_name})