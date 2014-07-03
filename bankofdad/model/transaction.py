# ETS imports
from traits.api import HasTraits, Date, Enum, Float, String

# Local imports
from bankofdad.model.constants import (
    ALLOWANCE_NAME, DEPOSIT_NAME, INTEREST_NAME, WITHDRAWAL_NAME
)


class Transaction(HasTraits):
    trans_date = Date
    amount = Float
    comment = String
    kind = Enum(DEPOSIT_NAME, WITHDRAWAL_NAME, ALLOWANCE_NAME, INTEREST_NAME)

    def __repr__(self):
        return "{}, {} ${:.2f} '{}'".format(self.trans_date, self.kind,
                                            self.amount, self.comment)

    def by_date(self):
        return self.trans_date
