# standard library imports
import unittest
from datetime import date, timedelta

# local imports
from bankofdad import Account, Person

class TestBank(unittest.TestCase):
    """ test the bank of dad.
    """

    def test_person(self):
        "test the Person class"
        p = Person(first_name="test", last_name="case",
                   DOB=date.today() - timedelta(366))
        self.assertEqual(p.age, 1)

    def test_account(self):
        "test the account class"
        p = Person(first_name="test", last_name="case",
                   DOB=date.today() - timedelta(366))
        a = Account(owner=p)
        self.assertEqual(a.savings_interest_rate, 0.01)
        self.assertEqual(a.weekly_allowance, 0.5)

if __name__ == "__main__":
    unittest.main()