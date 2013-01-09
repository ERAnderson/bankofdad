from datetime import date
from traits.api import HasTraits, String, Date, Property, Float

class Person(HasTraits):
    first_name = String
    last_name = String
    DOB = Date
    age = Property(Float, depends_on="DOB")

    def _get_age(self):
        """Return age rounded to the nearest 1/2 year.
        """
        time_since_birth = date.today() - self.DOB
        return int(time_since_birth.days / 365.25 * 2.) / 2.

if __name__ == '__main__':
    import enaml
    from enaml.stdlib.sessions import show_simple_view, simple_session
    from enaml.qt.qt_application import QtApplication

    eld = Person(first_name="Eliza", last_name="Diller", DOB=date(2003,6,9))
    print "{} {} is {} years old.".format(eld.first_name, eld.last_name, eld.age)
    with enaml.imports():
        from bod_person_view import PersonView
    eld_view = PersonView(person=eld)
    session = simple_session(
        eld.first_name, 
        'A view of the Person {} {}'.format(eld.first_name, eld.last_name),
        PersonView, person=eld
        )

    app = QtApplication([session])
    app.start_session(eld.first_name)
    app.start()
#    show_simple_view(eld_view)
