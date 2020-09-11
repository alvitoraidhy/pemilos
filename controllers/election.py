from sanic import response

def init(current):
    app, jinja, models, forms = current.app, current.jinja, current.models, current.forms

    @app.route("/election", methods=['GET'])
    async def election_index(request):
        return jinja.render("election/index.html", request)

    @app.route("/election/verification", methods=['GET', 'POST'])
    async def student_verify(request):
        form = forms.VerifyForm(request.form or None)
        errors = []
        if request.method == 'POST' and form.validate():
            try:
                nis = int(form.nis.data)
                nisn = int(form.nisn.data)
            except:
                errors = ['NIS and NISN must be numbers!']
            else:
                student = await models.Student.filter(nis=int(nis), nisn=int(nisn))
                if student:
                    session = request.ctx.session

                    session['student'] = {
                        'nis': student.nis,
                        'name': student.name,
                        'classname': student.classname
                    }
                    
                    return response.json("True")
                errors = ['Wrong NIS or NISN!']

        return jinja.render("election/verification.html", request, form=form, errors=errors)
