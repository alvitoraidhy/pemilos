from sanic import response
from datetime import datetime

format = '%Y-%m-%dT%H:%M'

def init(current):
    app, jinja, models, forms, helpers, config = \
        current.app, current.jinja, current.models, current.forms, current.helpers, current.config

    @app.route("/admin/settings", methods=['GET', 'POST'])
    @helpers.authorized('admin')
    async def admin_settings(request):
        form = forms.settings.SettingsForm(request.form or None)

        print(request.form)
        
        errors = []
        if request.method == 'POST' and form.validate():
            try:
                config.set('settings', 'election_schedule_start', form.election_schedule_start.data.strftime(format))
                config.set('settings', 'election_schedule_end', form.election_schedule_end.data.strftime(format))
                config.set('settings', 'result_schedule_start', form.result_schedule_start.data.strftime(format))
                config.set('settings', 'result_schedule_end', form.result_schedule_end.data.strftime(format))

                with open(app.config.APP_CONFIG_FILE, 'w') as f:
                    config.write(f)

                return response.redirect('/admin/settings')
            except Exception as e:
                errors.append(f'An error occurred: {repr(e)}')

        try:
            form.election_schedule_start.data = datetime.strptime(config.get('settings', 'election_schedule_start'), format)
            form.election_schedule_end.data = datetime.strptime(config.get('settings', 'election_schedule_end'), format)
            form.result_schedule_start.data = datetime.strptime(config.get('settings', 'result_schedule_start'), format)
            form.result_schedule_end.data = datetime.strptime(config.get('settings', 'result_schedule_end'), format)
        except:
            pass

        return jinja.render("admin/settings.html", request, form=form, errors=errors)
