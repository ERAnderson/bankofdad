##############################################################################
# Standard library imports
##############################################################################

from datetime import date, timedelta
import sqlite3
import sqlalchemy
from numpy import genfromtxt

from bod_time import previous_saturday, previous_sunday
from bod_person import Person

# ETS imports
from traits.api import HasTraits, Property, Instance, Int, Date, Enum, Float, \
     String, List
from traitsui.api import View

allowance_period = timedelta(7)
interest_period = allowance_period

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
    weekly_allowance = Property(Float)

    transactions = List(Instance(Transaction))

    def _get_next_interest(self):
        return last_saturday()

    def _get_next_allowance(self):
        return last_sunday()

    def _get_weekly_allowance(self):
        """Weekly rate"""
        return self.owner.age / 2.0 #dollars

    def update(self):
        if date.today() >= self.next_interest:
            self.apply_allowance()
            self.next_interest += interest_period
        if date.today() >= self.next_allowance:
            self.apply_allowance()
            self.next_allowance += allowance_period

    def apply_allowance(self):
        self.balance += self.weekly_allowance
        self.last_allowance = self.next_allowance

    def apply_interest(self):
        if self.balance > 0:
            self.balance *= 1. + savings_interest_rate
        else:
            self.balace *= 1. + loan_interest_rate
        self.last_interest = self.next_interest

    def load_file(self, filename):
        dt = [('Date', "S10"), ('Action', 'S9'), ('Amount', 'S6'), ('Balance', 'S6'),
              ('comment', 'S24'), ('f1', '<f8'), ('f2', '<f8')]
        data = genfromtxt(filename, dtype=dt, comments="#", delimiter="\t",
                          skip_header=1)
        #import ipdb; ipdb.set_trace()
        for trans in data:
            mm, dd, yy = trans["Date"].split("/")
            if trans["Action"].lower().startswith("withdraw"):
                kind = "withdrawal"
            elif trans["Action"].lower().startswith("allow"):
                kind = "allowance"
            elif trans["Action"].lower().startswith("inter"):
                kind = "interest"
            elif trans["Action"].lower().startswith("dep"):
                kind = "deposit"
            self.transactions.append(
                Transaction(
                    trans_date=date(int(yy), int(mm), int(dd)),
                    amount=float(trans["Amount"].replace("$", "")),
                    kind=kind, comment=str(trans["comment"]),
                    ))
#        import IPython; IPython.embed()

if __name__ == "__main__":
    i = Account(owner=Person(first_name="Ian", last_name="Diller"))
    i.load_file('ian.tsv')
    for trans in i.transactions:
        print trans