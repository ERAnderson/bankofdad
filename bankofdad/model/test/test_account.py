# standard library imports
from datetime import date
import unittest

# local imports
from bankofdad.model.account import Account
from bankofdad.model.person import Person


class TestAccount(unittest.TestCase):
    """ test the bank of dad.
    """
    def setUp(self):
        self.person = Person(
            name="test",
            DOB=date.today(),
        )
        self.account = Account(
            owner=self.person
        )

    def test_empty_account(self):
        "test an ampty account class"
        self.assertEqual(self.account.balance, 0.0,
                         "An empty account should have a zero balance.")

    def test_adding_a_deposit(self):
        deposit_amount = 1.0
        self.account.make_deposit(
            amount=deposit_amount,
            comment="test",
        )
        self.assertEqual(self.account.balance, deposit_amount)
