# Standard library imports
from datetime import date, timedelta

# Math imports
import numpy as np

# ETS imports
from traits.api import (
    Array, cached_property, Date, Enum, Float, HasTraits, Instance, List,
    Property
)

# Local imports
from bankofdad.model.constants import (
    ALLOWANCE_NAME, DEPOSIT_NAME, INTEREST_NAME, WITHDRAWAL_NAME
)
from bankofdad.model.person import Person
from bankofdad.model.transaction import Transaction
from bankofdad.util.time_utils import previous_saturday, previous_sunday

# Module level variables - TODO - move to config file
allowance_period = timedelta(7)
interest_period = allowance_period
savings_interest_rate = 0.01
loan_interest_rate = 0.05

ALLOWANCE_COMMENT = "Allowance for date {}."


class Account(HasTraits):
    savings_interest_rate = Float(1. / 100.)
    loan_interest_rate = Float(2. / 100.)
    owner = Instance(Person)
    kind = Enum("Savings")
    balance = Property(Float)
    last_interest = Date
    next_interest = Property(Date, depends_on="last_interest")
    last_allowance = Date
    next_allowance = Property(Date, depends_on="last_allowance")

    transactions = List(Instance(Transaction))
    transaction_amounts = Property(Array,
                                   depends_on=['transactions',
                                               'transactions_items'])

    # Defaults

    # Property calcs
    @cached_property
    def _get_balance(self):
        if len(self.transactions) > 0:
            balance = np.sum(self.transaction_amounts)
        else:
            balance = 0.0
        return balance

    def _get_next_interest(self):
        return previous_saturday()

    def _get_next_allowance(self):
        return previous_sunday()

    def _get_transaction_amounts(self):
        amounts = []
        for t in self.transactions:
            if t.kind in [WITHDRAWAL_NAME]:
                amounts.append(-1 * t.amount)
            else:
                amounts.append(t.amount)
        return amounts

    def weekly_allowance_at_date(self, date):
        return self.owner.age_at_date(date) / 2.0  # dollars

    def update(self):
        if date.today() >= self.next_interest:
            self.apply_allowance()
            self.next_interest += interest_period
        if date.today() >= self.next_allowance:
            self.apply_allowance()
            self.next_allowance += allowance_period

    # Account Actions
    def apply_allowance(self, date):
        transaction = Transaction(
            amount=self.weekly_allowance_at_date(date),
            comment=ALLOWANCE_COMMENT.format(date.isoformat()),
            kind=ALLOWANCE_NAME,
            time_stamp=date,
        )
        self.transactions.append(transaction)

    def apply_interest(self):
        if self.balance > 0:
            self.balance *= 1. + savings_interest_rate
        else:
            self.balace *= 1. + loan_interest_rate
        self.last_interest = self.next_interest

    def make_deposit(self, amount, time_stamp=None, comment=""):
        if time_stamp is None:
            time_stamp = date.today()
        transaction = Transaction(
            amount=amount,
            comment=comment,
            kind=DEPOSIT_NAME,
            time_stamp=time_stamp,
            )
        self.transactions.append(transaction)
