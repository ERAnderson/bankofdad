# ETS imports
from traits.api import HasTraits, Date, Enum, Float, String


class Transaction(HasTraits):
    trans_date = Date
    amount = Float
    comment = String
    kind = Enum("withdrawal", "deposit", "allowance", "interest")

    def __repr__(self):
        return "{}, {} ${:.2f} '{}'".format(self.trans_date, self.kind,
                                            self.amount, self.comment)

    def by_date(self):
        return self.trans_date
