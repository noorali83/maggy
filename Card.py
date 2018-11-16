class Card:

    def __init__(self, number, expiry_date, balance) -> None:
        super().__init__()
        self.number = number
        self.expiry_date = expiry_date
        self.balance = balance

    def add_balance(self, top_up_amount):
        self.balance = self.balance + top_up_amount

    def getAmount(self):
        return self.balance

    def getCardNumber(self):
        return self.number

    def has_sufficient_balance(self, purchase_amount):
        return self.balance - purchase_amount >= 0

    def deduct_balance(self, purchase_amount):
         self.balance = self.balance - purchase_amount
