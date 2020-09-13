from wtforms import (
    Form, StringField, PasswordField, TextAreaField, IntegerField, FileField, BooleanField, SelectField,
    SubmitField, validators
)

class FindForm(Form):
    id = IntegerField('ID')
    nis = IntegerField('NIS')
    nisn = IntegerField('NISN')
    name = StringField('Name')
    classname = StringField('Classname')
    has_chosen_id = SelectField('Candidate Number', coerce=int, choices=[(0, '-')])

class CreateForm(Form):
    nis = IntegerField('Nomor Induk Siswa', [validators.InputRequired()])
    nisn = IntegerField('Nomor Induk Siswa Nasional', [validators.InputRequired()])
    name = StringField('Name', [validators.InputRequired()])
    grade = SelectField('Grade', coerce=int, 
        choices=[
            (10, 'X'),
            (11, 'XI'),
            (12, 'XI')
        ]
    )
    classname = StringField('Classname', [validators.InputRequired()])
    
    has_chosen_id = SelectField('Candidate Number', coerce=int, choices=[(0, '-')])
    
    submit = SubmitField('Submit')

class EditForm(CreateForm):
    pass

class DeleteForm(Form):
    confirmation = BooleanField("Are you sure you want to delete this row?")
    submit = SubmitField('Submit')

class ImportCSVForm(Form):
    csv = FileField('Upload CSV File')
    submit = SubmitField('Submit')
