from sanic import response
from datetime import datetime

format = '%Y-%m-%dT%H:%M'

def init(current):
    app, jinja, models, forms, helpers, config = (
        current.app, current.jinja, current.models, current.forms, current.helpers, current.config
    )
    
    @app.route("/election/verification", methods=['GET', 'POST'])
    @app.route("/election", methods=['GET', 'POST'])
    async def student_verify(request):
        form = forms.VerifyForm(request.form or None)
        errors = []
        if request.method == 'POST' and form.validate():
            try:
                nis = int(form.nis.data)
            except:
                errors = ['NIS harus berupa angka']
            else:
                password = form.password.data
                student = await models.Student.get_or_none(nis=nis)
                if student and student.verify_password(password):
                    data = {
                        'id': student.id,
                        'nis': student.nis,
                        'name': student.name,
                        'classname': student.classname
                    }

                    helpers.login(request, 'student', data)
                    
                    return response.redirect('/election/start')
                else:
                    errors = ['NIS dan/atau password salah']

        return jinja.render("election/verification.html", request, form=form, errors=errors)

    @app.route("/logout", methods=['GET'])
    async def student_logout(request):
        try:
            helpers.logout(request, 'student')
        except KeyError:
            pass

        return response.redirect('/')
    
    @app.route("/election/start", methods=['GET', 'POST'])
    @helpers.authorized('student')
    async def election(request):
        start = config.get('settings', 'election_schedule_start')
        end = config.get('settings', 'election_schedule_end')
        now = datetime.now()
        if now > datetime.strptime(start, format) and datetime.strptime(end, format) > now:
            student = await models.Student.get_or_none(id=helpers.get_account(request, 'student').get('id'))
            if student:
                if student.has_chosen_id != None: return response.redirect('/election/already-voted')

                errors = []
                candidates = await models.Candidate.all()
                form = forms.election.VoteForm(request.form or None)
                form.has_chosen_id.choices = [(x.candidate_number, f'{x.name.split()[0]} ({x.candidate_number})') for x in candidates]
                if request.method == 'POST' and form.validate():
                    try:
                        student.has_chosen_id = form.has_chosen_id.data
                        await student.save()
                        return response.redirect('/election/done')
                        
                    except Exception as e:
                        print(repr(e))
                        errors.append('Terjadi kesalahan. Mohon mencoba kembali')
                
                return jinja.render("election/start.html", request, form=form, errors=errors, candidates=candidates)

            else:
                return response.redirect('/logout')

        else:
            return response.redirect('/')

    @app.route("/election/done", methods=['GET'])
    async def election_done(request):
        if helpers.check_auth(request, 'student'):
            try:
                helpers.logout(request, 'student')
            except KeyError:
                pass

            return jinja.render("election/done.html", request)

        else:
            return response.redirect('/')

    @app.route("/election/already-voted", methods=['GET'])
    @helpers.authorized('student')
    async def election_already_voted(request):
        return jinja.render("election/already_voted.html", request)
    
    @app.route("/election/result", methods=['GET'])
    async def result(request):
        start = config.get('settings', 'result_schedule_start')
        end = config.get('settings', 'result_schedule_end')
        now = datetime.now()
        if now > datetime.strptime(start, format) and datetime.strptime(end, format) > now:
            return jinja.render("election/result.html", request)

        else:
            return response.redirect('/')
