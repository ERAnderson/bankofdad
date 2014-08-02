# Standard library imports
from datetime import date, timedelta
import unittest

# Math imports

# ETS imports

# Local imports
from ..time_utils import (
    next_iso_weekday_from_date, next_saturday_from_date, next_sunday_from_date,
    SATURDAY, SUNDAY
)


class TestTimeUtils(unittest.TestCase):
    def setUp(self):
        self.known_friday = date(2014, 8, 1)
        self.known_saturday = date(2014, 8, 2)
        self.known_sunday = date(2014, 8, 3)

    def test_next_iso_weekday_from_date(self):
        self.assertEqual(
            next_iso_weekday_from_date(self.known_friday, SATURDAY),
            self.known_saturday,
            "Next Saturday after {} should be {}".format(self.known_friday,
                                                         self.known_saturday))
        self.assertEqual(
            next_iso_weekday_from_date(self.known_friday, SUNDAY),
            self.known_sunday,
            "Next Sunday after {} should be {}".format(self.known_friday,
                                                       self.known_sunday))
        next_saturday = self.known_saturday + timedelta(7)
        self.assertEqual(
            next_iso_weekday_from_date(self.known_saturday, SATURDAY),
            next_saturday,
            "Next Saturday after {} should be {}".format(self.known_saturday,
                                                         next_saturday))

    def test_next_saturday(self):
        self.assertEqual(
            next_saturday_from_date(self.known_friday),
            self.known_saturday,
            "Next Saturday after {} should be {}".format(self.known_friday,
                                                         self.known_saturday))

    def test_next_sunday(self):
        self.assertEqual(
            next_sunday_from_date(self.known_friday),
            self.known_sunday,
            "Next Sunday after {} should be {}".format(self.known_friday,
                                                       self.known_sunday))


if __name__ == "__main__":
    unittest.main()
