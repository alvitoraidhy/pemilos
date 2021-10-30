from wtforms import (
    Form, StringField, PasswordField, IntegerField, FileField, BooleanField, SelectField,
    SubmitField, validators
)

class FindForm(Form):
    id = IntegerField('ID')
    nis = IntegerField('NIS')
    name = StringField('Name')
    grade = SelectField('Grade', 
        choices=[
            ("all", 'All')
            (10, 'X'),
            (11, 'XI'),
            (12, 'XI')
        ], default='all'
    )
    classname = StringField('Classname')
    has_chosen_id = SelectField('Candidate Number', choices=[('all', 'All'), ('any', 'Yes'), ('none','No')], default='all')

class CreateForm(Form):
    nis = IntegerField('Nomor Induk Siswa', [validators.InputRequired()])
    name = StringField('Name', [validators.InputRequired()])
    grade = SelectField('Grade', coerce=int, 
        choices=[
            (10, 'X'),
            (11, 'XI'),
            (12, 'XII')
        ]
    )
    classname = StringField('Classname', [validators.InputRequired()])
    password = PasswordField('Password')
    
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
