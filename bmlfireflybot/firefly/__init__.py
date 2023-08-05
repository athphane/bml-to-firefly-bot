from bmlfireflybot.firefly.firefly import FireflyAPI
from bmlfireflybot.firefly.helpers import parse_transaction

the_regex = r"Transaction from (\d+) on ((?:\d{2}/){2}\d{2} at \d{2}:\d{2}:\d{2}) for ([A-Za-z]+)(\d+\.\d{2}) at (" \
            r".*?) was processed"
