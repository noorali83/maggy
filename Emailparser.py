# Read Email Script
import imaplib
import email
import re

from application.models import Card
from Topup import Topup


def parse_card_details_from(card_details_text):
    text, card_details = card_details_text.split(":")
    card_details = card_details.rstrip('"')
    card_details = card_details.lstrip('"')
    card_num, expiry_date = card_details.split('.')
    card_num = re.sub("\D", "", card_num)
    return card_num, expiry_date


class EmailParser:

    def get_unseen_email(self):
        email_body = None
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login('nooralitestapp@gmail.com', 'EnUlagam2415*')
        mail.list()
        mail.select("INBOX")  # connect to inbox.

        result, data = mail.search(None, "UNSEEN")

        ids = data[0]
        id_list = ids.split()
        if len(id_list) > 0:
            latest_email_id = id_list[-1]

            result, data = mail.fetch(latest_email_id, '(RFC822)')

            raw_email = data[0][1]

            email_message = email.message_from_bytes(raw_email)

            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    email_body = part.get_payload(decode=True)
                    email_body = email_body.decode('utf-8')
                else:
                    continue

        return email_body

    def get_topups(self):
        valid_topups = []
        email_body = self.get_unseen_email()
        if email_body is not None:
            price = None
            customer_name = None
            school_name = None
            for line in email_body.splitlines():
                topup = Topup(None, None, None)
                if 'Price:' in line:
                    price = self.getprice(line)
                elif 'Customer Name' in line:
                    customer_name = self.getcustomername(line)
                elif 'The following item has just been purchased from' in line:
                    school_name = self.getschoolname(line)
                elif 'Note:' in line:
                    card_num, expiry_date = parse_card_details_from(line)
                    topup.card_num = card_num
                    topup.amount = price
                    topup.customer_name = customer_name
                    topup.school_name = school_name
                    topup.card_expiry_date = expiry_date
                    valid_topups.append(topup)
        return valid_topups

    def getprice(self, line):
        text, amount = line.split(":")
        return amount.partition("$")[2]

    def getcustomername(self, line):
        text, user_name = line.split(":")
        return user_name

    def getschoolname(self, line):
        schoolname = line.partition('The following item has just been purchased from')[2]
        return schoolname


if __name__ == '__main__':
    email_parser = EmailParser()
    topups = email_parser.get_topups()

    print('There are ' + str(len(topups)) + ' topups')

    for x in range(len(topups)):
        topup = topups[x]
        print('----------------------')
        print('CardNum ' + topup.card_num)
        print('Expiry Date ' + topup.card_expiry_date)
        print('Amount ' + topup.amount)
        print('School ' + topup.school_name)
        print('customer_name ' + topup.customer_name)
