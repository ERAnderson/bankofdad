from datetime import date
from traits.api import HasTraits, String, Date, Property, Int

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
