from sanic import response

def init(current):
    app, jinja, models, forms = current.app, current.jinja, current.models, current.forms

    @app.route("/login", methods=['GET', 'POST'])
    async def student_login(request):
        form = forms.LoginForm(request.form or None)
        errors = []
        if request.method == 'POST' and form.validate():
            try:
                nis = int(form.nis.data)
                nisn = int(form.nisn.data)
            except:
                errors = ['NIS dan NISN harus berupa angka!']
            else:
                student = await models.Student.filter(nis=int(nis), nisn=int(nisn))
                if student:
                    async with request['session']:
                        authorized_user = {
                            'user_id': student.id,
                            'name': student.name,
                            'classname': student.classname,
                            'nis': student.nis
                        }
                        await request.app.exts.auth_session.login_user(request, authorized_user)
                        return response.json("True")
                errors = ['NIS atau NISN salah!']

        return jinja.render("login.html", request, form=form, errors=errors)
