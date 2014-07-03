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

    def test_account(self):
        "test the account class"
        self.assertEqual(self.account.savings_interest_rate, 0.01)
        self.assertEqual(self.account.balance, 0.0,
                         "An empty account should have a zero balance.")
