###############################################################################

# Stand library imports
from datetime import date, timedelta
import sqlite3
import sqlalchemy
from numpy import genfromtxt

# ETS imports
from traits.api import HasTraits, Property, Instance, Int, Date, Enum, Float, \
     String, List
from traitsui.api import View

allowance_period = timedelta(7)
interest_period = allowance_period

def previous_saturday(today):
    today_day_of_week = today.isoweekday()
    days_since_saturday = 6 - today_day_of_week
    if days_since_saturday == 0:
        days_since_saturday = 7
    return today - timedelta(days_since_saturday)

def previous_sunday(today):
    today_day_of_week = today.isoweekday()
    days_since_sunday = 7 - today_day_of_week
    if days_since_sunday == 0:
        days_since_sunday = 7
    return today - timedelta(days_since_sunday)

class Person(HasTraits):
    first_name = String
    last_name = String
    DOB = Date
    age = Property(Int, depends_on="DOB")

    def _get_age(self):
        """Return age rounded to the nearest 1/2 year.
        """
        time_since_birth = date.today() - self.DOB
        return int(time_since_birth.days / 365.25 * 2.) / 2.

class Transaction(HasTraits):
    trans_date = Date
    amount = Float
    comment = String
    kind = Enum("withdrawal", "deposit", "allowance", "interest")
    def __repr__(self):
        return "{}, {} ${:.2f} '{}'".format(self.trans_date, self.kind, 
                                            self.amount, self.comment)

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


if __name__ == "__main__":
    w = Transaction(kind = "withdrawal", trans_date=date.today(),
                    amount=10.34, comment="test transaction")
    print w
