from wtforms import (
    Form, SelectField, validators
)

class VoteForm(Form):
    has_chosen_id = SelectField('Candidate Number', coerce=int, choices=[(0, '-')])
