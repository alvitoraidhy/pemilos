from sanic import response

def init(current):
    app, jinja, models, forms, helpers = \
        current.app, current.jinja, current.models, current.forms, current.helpers

    @app.route("/admin/login", methods=['GET', 'POST'])
    async def admin_login(request):
        if helpers.check_auth(request, 'admin'): return response.redirect('/admin/dashboard')

        form = forms.AdminLoginForm(request.form or None)
        errors = []
        if request.method == 'POST' and form.validate():
            try:
                username = str(form.username.data)
                password = str(form.password.data)

                admin = await models.Admin.get(username=username)
                admin.verify_password(password)

                helpers.login(request, 'admin', await admin.serialize())

                return response.redirect('/admin/dashboard')
            except:
                errors = ['Invalid username or password!']

        return jinja.render("admin/login.html", request, form=form, errors=errors)

    @app.route("/admin/logout", methods=['GET'])
    async def admin_logout(request):
        try:
            helpers.logout(request, 'admin')
        except KeyError:
            pass

        return response.redirect('/admin/login')
