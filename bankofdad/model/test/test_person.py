# standard library imports
import unittest
from datetime import date, timedelta

# local imports
from bankofdad.model.person import Person


class TestPerson(unittest.TestCase):
    def setUp(self):
        self.person = Person()

    def test_person(self):
        "test the Person class"
        p = Person(first_name="test", last_name="case",
                   DOB=date.today() - timedelta(366))
        self.assertEqual(p.age, 1)
