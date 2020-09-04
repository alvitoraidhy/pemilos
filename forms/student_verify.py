from wtforms import Form, StringField, PasswordField, SubmitField, validators

class VerifyForm(Form):
    nis = StringField('Nomor Induk Siswa', [validators.InputRequired()])
    nisn = PasswordField('Nomor Induk Siswa Nasional', [validators.InputRequired()])
    submit = SubmitField('Login')
