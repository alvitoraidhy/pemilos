from wtforms import Form, StringField, PasswordField, SubmitField, validators

class VerifyForm(Form):
    nis = StringField('Nomor Induk Siswa', [validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired()])
