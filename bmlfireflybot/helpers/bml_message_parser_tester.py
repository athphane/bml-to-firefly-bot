import re

messages = [
    'Transaction from 9516 on 13/10/22 at 16:37:39 for MVR350.00 at MAXCOM TECHNOLOGIES was processed. Reference No:101380550316, Approval Code:550316.',
    'Transaction from 9516 on 13/10/22 at 13:25:48 for MVR65.00 at THE DOUGH BY JELLY was processed. Reference No:101380509689, Approval Code:509689.',
    'BML Internet Banking: Your One Time Password is 383186. It will expire after use or after 12/10/2022 19:27:21. Do not share your OTP.',
    'Transaction from 9516 on 12/10/22 at 14:01:18 for MVR72.00 at VILLA MART was processed. Reference No:101280306692, Approval Code:306692.',
    'Transaction from 9516 on 12/10/22 at 10:14:17 for USD10.68 at PAYPAL *SPOTIFYUSAI       was processed. Reference No:228505090366, Approval Code:090366.'
]

# def determine_category(input_vendor):
#     for vendor in vendors:
#         if

if __name__ == '__main__':
    for message in messages:

        if message.startswith('Transaction from '):
            regex = re.compile(r'.*(?P<card_number>\d{4}).*(?P<date>\d{2}\/\d{2}\/\d{2}).*(?P<time>\d{2}:\d{2}:\d{2}).*(?P<currency>MVR|USD)(?P<amount>\d*.\d{2}).*at\s(?P<location>.*)\swas.*No.(?P<ref_no>\d*),.*:(?P<approval_code>\d*)')
            results = regex.match(message)
            print(results.groupdict())


