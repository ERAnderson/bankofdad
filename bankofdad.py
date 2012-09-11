from datetime import date, timedelta
import sqlite3
import sqlalchemy

from traits.api import HasTraits

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
    savings_interest_rate = 1. / 100.
    loan_interest_rate = 2. / 100.
    def __init__(self, owner=None, type="savings", initial_balance=0.0):
        self.owner = owner
        assert isinstance(owner, Person)
        self.balance = initial_balance
        self.next_interest = last_saturday()
        self.next_allowance = last_sunday()

    @property
    def weekly_allowance(self):
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

    def apply_interest(self):
        if self.balance > 0:
            self.balance *= 1. + savings_interest_rate
        else:
            self.balace *= 1. + loan_interest_rate
