class Topup:

    def __init__(self, card_num, amount, card_expiry_date=None, customer_name=None, school_name=None) -> None:
        super().__init__()
        self.card_num = card_num
        self.amount = amount
        self.customer_name = customer_name
        self.school_name = school_name
        self.card_expiry_date = card_expiry_date
