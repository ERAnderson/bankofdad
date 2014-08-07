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
    ALLOWANCE_NAME, DEPOSIT_NAME, INTEREST_NAME, WITHDRAWAL_NAME,
    ALLOWANCE_COMMENT, INTEREST_COMMENT,
)
from bankofdad.model.person import Person
from bankofdad.model.transaction import Transaction
from bankofdad.util.time_utils import (
    next_saturday_from_date, next_sunday_from_date
)

# Module level variables - TODO - move to config file
default_allowance_period = timedelta(7)
default_interest_period = default_allowance_period
savings_interest_rate = 0.01
loan_interest_rate = 0.05


class Account(HasTraits):
    savings_interest_rate = Float(1. / 100.)
    loan_interest_rate = Float(2. / 100.)
    owner = Instance(Person)
    kind = Enum("Savings")
    balance = Property(Float, depends_on=['transaction_amounts'])
    last_interest = Date
    next_interest = Property(Date, depends_on="last_interest")
    last_allowance = Date
    next_allowance = Property(Date, depends_on="last_allowance")
    start_date = Date

    transactions = List(Instance(Transaction))
    transaction_amounts = Property(Array,
                                   depends_on=['transactions',
                                               'transactions[]'])

    # Defaults
    def _last_interest_default(self):
        return self.start_date

    def _last_allowance_default(self):
        return self.start_date

    def _start_date_default(self):
        return date.today()

    # Property calcs
    @cached_property
    def _get_balance(self):
        if len(self.transactions) > 0:
            balance = np.sum(self.transaction_amounts)
        else:
            balance = 0.0
        return balance

    @cached_property
    def _get_next_interest(self):
        return next_saturday_from_date(self.last_interest)

    @cached_property
    def _get_next_allowance(self):
        return next_sunday_from_date(self.last_allowance)

    @cached_property
    def _get_transaction_amounts(self):
        amounts = []
        for t in self.transactions:
            if t.kind in [WITHDRAWAL_NAME]:
                amounts.append(-1 * t.amount)
            else:
                amounts.append(t.amount)
        return np.array(amounts)

    def weekly_allowance_at_date(self, date):
        return self.owner.age_at_date(date) / 2.0  # dollars

    def update(self):
        """ Add interest and allowance transactions to bring the account up to
        date.
        """
        while date.today() >= self.next_allowance:
            self.apply_allowance(self.next_allowance)
            self.last_allowance = self.next_allowance
        while date.today() >= self.next_interest:
            self.apply_interest(self.next_interest)
            self.last_interest = self.next_interest

    # Account Actions
    def apply_allowance(self, date):
        transaction = Transaction(
            amount=self.weekly_allowance_at_date(date),
            comment=ALLOWANCE_COMMENT.format(date.isoformat()),
            kind=ALLOWANCE_NAME,
            time_stamp=date,
        )
        self.transactions.append(transaction)

    def apply_interest(self, date):
        if self.balance > 0:
            amount = self.balance * savings_interest_rate
        else:
            amount = self.balance * loan_interest_rate
        transaction = Transaction(
            amount=amount,
            comment=INTEREST_COMMENT.format(date.isoformat()),
            kind=INTEREST_NAME,
            time_stamp=date,
        )
        self.transactions.append(transaction)

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

    def make_withdrawal(self, amount, time_stamp=None, comment=""):
        if time_stamp is None:
            time_stamp = date.today()
        transaction = Transaction(
            amount=amount,
            comment=comment,
            kind=WITHDRAWAL_NAME,
            time_stamp=time_stamp,
            )
        self.transactions.append(transaction)
