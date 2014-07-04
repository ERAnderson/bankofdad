# standard library imports
from datetime import date, timedelta
import unittest

# local imports
from bankofdad.model.account import Account, savings_interest_rate
from bankofdad.model.person import Person


class TestAccount(unittest.TestCase):
    """ test the bank of dad.
    """
    def setUp(self):
        self.person = Person(
            name="4 yr old",
            DOB=date.today() - timedelta(365 * 4 + 2),
        )
        self.account = Account(
            owner=self.person
        )

    def test_empty_account_balance(self):
        "test an ampty account class"
        self.assertEqual(self.account.balance, 0.0,
                         "An empty account should have a zero balance.")

    def test_adding_a_deposit(self):
        deposit_amount = 1.0
        self.account.make_deposit(deposit_amount)
        self.assertEqual(self.account.balance, deposit_amount)
        self.account.make_deposit(100)
        self.assertEqual(self.account.balance, 101)

    def test_apply_allowance(self):
        self.account.apply_allowance(date.today())
        self.assertEqual(self.account.balance, self.person.age / 2)

    def test_apply_interest(self):
        deposit_amount = 100.
        self.account.make_deposit(deposit_amount)
        self.account.apply_interest(date.today())
        self.assertEqual(self.account.balance,
                         deposit_amount * (1 + savings_interest_rate))
