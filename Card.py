class Card:

    def __init__(self, number, amount) -> None:
        super().__init__()
        self.number = number
        self.amount = amount

    def top_up(self, top_up_amount):
        self.amount = self.amount + top_up_amount

    def getAmount(self):
        return self.amount

    def getCardNumber(self):
        return self.number

    def has_sufficient_balance(self, purchase_amount):
        return self.amount - purchase_amount >= 0

    def deduct_amount(self, purchase_amount):
         self.amount = self.amount - purchase_amount
