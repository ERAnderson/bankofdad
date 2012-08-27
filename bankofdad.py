from datetime import date, timedelta
import sqlite3
import sqlalchemy

from traits.api import HasTraits

allowance_period = timedelta(7)

class Person(object):
    def __init__(self, first_name="", last_name="", DOB=(2000,1,1)):
        self.first_name=first_name
        self.last_name=last_name
        self.DOB=date(*DOB)

    @property
    def age(self):
        time_since_birth = date.today() - self.DOB
        return int(time_since_birth.days / 365.25 * 2.) / 2.

class Account(object):
    def __init__(self, owner=None, type="savings", initial_balance=0.0):
        self.owner = owner
        assert isinstance(owner, Person)
        self.balance = initial_balance
        self.next_allowance = date.today()
        self.next_interest = date.today()

    @property
    def weekly_allowance(self):
        """Weekly rate"""
        return self.owner.age / 2.0 #dollars

    def update(self):
        if date.today() >= self.next_allowance:
            self.apply_allowance()
            self.next_allowance += allowance_period

    def apply_allowance(self):
        self.balance += self.weekly_allowance
