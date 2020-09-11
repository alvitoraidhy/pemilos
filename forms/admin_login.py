from wtforms import Form, StringField, PasswordField, SubmitField, validators

class AdminLoginForm(Form):
    username = StringField('Username', [validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired()])
    submit = SubmitField('Login')
