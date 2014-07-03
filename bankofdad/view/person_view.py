from enaml.widgets.api import Window, Label, Field, Form
from enaml.stdlib.fields import FloatField


enamldef PersonForm(Form):
    attr person
    Label:
        text = 'First Name'
    Field:
        text := person.first_name
    Label:
        text = 'Last Name'
    Field:
        text := person.last_name
    Label:
        text = 'Age'
    FloatField:
        minimum = 0
        value := person.age


enamldef PersonView(Window):
    attr person
    PersonForm:
        person := parent.person

