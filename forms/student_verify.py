from wtforms import Form, StringField, PasswordField, SubmitField, validators

class VerifyForm(Form):
    nis = StringField('Student ID', [validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired()])
