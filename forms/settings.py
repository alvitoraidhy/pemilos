from wtforms import (
    Form, SubmitField, validators
)
from wtforms.fields.html5 import DateTimeLocalField

format = '%Y-%m-%dT%H:%M'

class SettingsForm(Form):
    election_schedule_start = DateTimeLocalField('Start of Election', [validators.InputRequired()], format=format)
    election_schedule_end = DateTimeLocalField('End of Election', [validators.InputRequired()], format=format)
    result_schedule_start = DateTimeLocalField('Start of Result Announcement', [validators.InputRequired()], format=format)
    result_schedule_end = DateTimeLocalField('End of Result Announcement', [validators.InputRequired()], format=format)

    submit = SubmitField('Submit')
