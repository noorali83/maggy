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
    card_num = None
    expiry_date = None
    if '.' in card_details:
        c_number, c_expiryDate = card_details.split('.')
        card_num = c_number
        expiry_date = c_expiryDate
    else:
        card_num = card_details

    card_num = re.sub("\D", "", card_num)
    if card_num.__len__() > 14:
        card_num = card_num[:14]
    return card_num, expiry_date


class EmailParser:
    def get_unseen_emails(self):
        new_emails = []
        email_body = None
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login('qkrtoppingup@gmail.com', 'canteen99')
        mail.list()
        mail.select("INBOX")  # connect to inbox.

        result, data = mail.search(None, "UNSEEN")

        ids = data[0]
        id_list = ids.split()
        if len(id_list) > 0:
            # latest_email_id = id_list[-1]

            for id in id_list:
                result, data = mail.fetch(id, '(RFC822)')

                raw_email = data[0][1]

                email_message = email.message_from_bytes(raw_email)

                for part in email_message.walk():
                    if part.get_content_type() == "text/plain":
                        email_body = part.get_payload(decode=True)
                        email_body = email_body.decode('utf-8')
                    else:
                        continue
                new_emails.append(email_body)

        return new_emails

    def get_topups_from_email(self):
        valid_topups = []
        new_emails = self.get_unseen_emails()
        if new_emails is not None and new_emails.__len__() > 0:
            for new_email in new_emails:
                if new_email is not None:
                    price = None
                    customer_name = None
                    school_name = None
                    product_name = None
                    topup = None
                    for line in new_email.splitlines():
                        if '-------------------' in line:
                            if topup is not None:
                                if product_name is not None and 'Top Up' in product_name:
                                    topup.school_name = school_name
                                    valid_topups.append(topup)
                                    topup = Topup(None, None, None)
                            else:
                                topup = Topup(None, None, None)
                        elif 'Product Name:' in line:
                            product_name = self.value_from(line)
                        elif 'Price:' in line:
                            topup.amount = self.getprice(line)
                        elif 'Beneficiary:' in line:
                            customer_name = self.value_from(line).strip()
                            topup.customer_name = customer_name
                        elif 'The following item has just been purchased from' in line:
                            school_name = self.getschoolname(line)
                            school_name = school_name.replace(' using', '').strip()
                        elif 'Note:' in line:
                            card_num, expiry_date = parse_card_details_from(line)
                            if card_num is not None:
                                topup.card_num = card_num
                            if expiry_date is not None:
                                topup.card_expiry_date = expiry_date

        return valid_topups

    def getprice(self, line):
        text, amount = line.split(":")
        return amount.partition("$")[2]

    def value_from(self, line):
        label, value = line.split(":")
        return value

    def getschoolname(self, line):
        schoolname = line.partition('The following item has just been purchased from')[2]
        return schoolname


if __name__ == '__main__':
    email_parser = EmailParser()
    topups = email_parser.get_topups_from_email()

    print('There are ' + str(len(topups)) + ' topups')

    for x in range(len(topups)):
        topup = topups[x]
        print('----------------------')
        print('CardNum ' + topup.card_num)
        print('Amount ' + topup.amount)
        print('School ' + topup.school_name)
        print('customer_name ' + topup.customer_name)
