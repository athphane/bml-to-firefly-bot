import json
import re

from playground.firefly import FireflyAPI


smses = [
    "Transaction from 9516 on 01/08/23 at 21:54:32 for MVR115.00 at MR SUB was processed. Reference No:080149480211, Approval Code:480211.",
    "Transaction from 9516 on 01/08/23 at 21:44:20 for MVR221.00 at REDWAVE CITY SQUARE was processed. Reference No:080149475618, Approval Code:475618.",
    "Transaction from 9516 on 01/08/23 at 21:28:47 for MVR225.00 at LINCHPIN was processed. Reference No:080149469059, Approval Code:469059.",
    "Transaction from 9516 on 01/08/23 at 19:05:36 for EUR20.00 at Riot* AE3LAD658GJ4        was processed. Reference No:321314725807, Approval Code:725807.",
    "Transaction from 9516 on 01/08/23 at 18:07:29 for MVR69.50 at FRESH SEASON was processed. Reference No:080149405072, Approval Code:405072."
]

if __name__ == '__main__':
    firefly = FireflyAPI('https://firefly.athfan.com', firefly_api_key)

    accounts = firefly.find_account_by_name('Riot')

    # write json response to file
    with open('accounts.json', 'w') as f:
        f.write(json.dumps(accounts))

    # for account in accounts['data']:
    #     print(account['attributes']['name'])



    # pattern = r"Transaction from (\d+) on ((?:\d{2}/){2}\d{2} at \d{2}:\d{2}:\d{2}) for ([A-Za-z]+)(\d+\.\d{2}) at (.*?) was processed"

    # for sms in smses:
    #     match = re.search(pattern, sms)

        # if match:
        #     card_num = match.group(1)
        #     datetime = match.group(2)
        #     currency = match.group(3)
        #     amount = match.group(4)
        #     location = match.group(5)
        #     print(' | '.join([card_num, datetime, currency, amount, location]))

