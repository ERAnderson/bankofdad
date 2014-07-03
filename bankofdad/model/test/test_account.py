# standard library imports
import unittest

# local imports
from bankofdad import Account


class TestAccount(unittest.TestCase):
    """ test the bank of dad.
    """
    def setUp(self):
        self.account = Account()

    def test_account(self):
        "test the account class"
        self.assertEqual(self.account.savings_interest_rate, 0.01)
        self.assertEqual(self.account.weekly_allowance, 0.5)
