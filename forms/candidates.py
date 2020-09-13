from wtforms import (
    Form, StringField, PasswordField, TextAreaField, IntegerField, FileField, BooleanField, SubmitField, 
    validators
)

class CreateForm(Form):
    nis = IntegerField('Nomor Induk Siswa', [validators.InputRequired()])
    nisn = IntegerField('Nomor Induk Siswa Nasional', [validators.InputRequired()])
    name = StringField('Name', [validators.InputRequired()])
    classname = StringField('Classname', [validators.InputRequired()])

    candidate_number = IntegerField('Candidate Number', [validators.InputRequired()])
    image = FileField('Image File')
    vision = TextAreaField('Vision', [validators.InputRequired()])
    mission = TextAreaField('Mission', [validators.InputRequired()])
    
    submit = SubmitField('Submit')

class EditForm(CreateForm):
    pass

class DeleteForm(Form):
    confirmation = BooleanField("Are you sure you want to delete this row?")
    submit = SubmitField('Submit')
