# Standard library imports
from datetime import date

# ETS imports
from traits.api import HasTraits, Date, Enum, Float, String

# Local imports
from bankofdad.model.constants import (
    ALLOWANCE_NAME, DEPOSIT_NAME, INTEREST_NAME, WITHDRAWAL_NAME
)


class Transaction(HasTraits):
    time_stamp = Date
    amount = Float
    comment = String
    kind = Enum(DEPOSIT_NAME, WITHDRAWAL_NAME, ALLOWANCE_NAME, INTEREST_NAME)

    def __repr__(self):
        return "{}, {} ${:.2f} '{}'".format(self.time_stamp, self.kind,
                                            self.amount, self.comment)

    # Defaults
    def _time_stamp_default(self):
        return date.today()

    def by_date(self):
        return self.time_stamp
