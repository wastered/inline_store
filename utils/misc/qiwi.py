import datetime
import uuid
from dataclasses import dataclass

import pyqiwi

from data import config
from data.config import QIWI_TOKEN, WALLET_QIWI

wallet = pyqiwi.Wallet(token=QIWI_TOKEN, number=WALLET_QIWI)


class NotEnoughMoney(Exception):
    pass


class NoPaymentFound(Exception):
    pass


@dataclass
class Payment:
    # amount: int
    amount: float
    id: str = None
    
    def create(self):
        self.id = str(uuid.uuid4())
    
    def check_payment(self):
        transactions = wallet.history(start_date=datetime.datetime.now() - datetime.timedelta(days=2))
        transactions = transactions.get("transactions")
        for transaction in transactions:
            if transaction.comment:
                if str(self.id) in transaction.comment:
                    if float(transaction.total.amount) >= float(self.amount):
                        return True
                    else:
                        raise NotEnoughMoney
        else:
            raise NoPaymentFound
    
    @property
    def invoice(self):
        link = "https://oplata.qiwi.com/create?publicKey={pubkey}&amount={amount}&comment={comment}"
        return link.format(pubkey=config.QIWI_PUBKEY, amount=self.amount, comment=self.id)
