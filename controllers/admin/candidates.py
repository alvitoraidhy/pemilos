from sanic import response
from sanic.exceptions import SanicException, abort
from datetime import datetime


def init(current):
    app, jinja, models, forms, helpers = \
        current.app, current.jinja, current.models, current.forms, current.helpers

    @app.route("/admin/candidates", methods=['GET'])
    @helpers.authorized('admin')
    async def candidates_table(request):
        rows = await models.Candidate.all()
        return jinja.render("admin/candidates/table.html", request, rows=rows)

    @app.route("/admin/candidates/create", methods=['GET', 'POST'])
    @helpers.authorized('admin')
    async def candidates_create(request):
        form = forms.candidates.CreateForm(request.form or None)
        errors = []
        if request.method == 'POST' and form.validate():
            try:
                upload_file = request.files['image'][0]
                file_body = upload_file.body

                file_name_type = upload_file.name.split('.')[-1]
                if file_name_type == "jpg":
                    # 5 MB limit
                    if len(file_body) < (5 * 1024 * 1024):
                        filename = f'{ datetime.now().strftime("%Y%m%d-%H%M%S-%f") }.jpg'

                        await helpers.process_upload(app, file_body, filename)

                        data = { **form.data }
                        data['image'] = f'{app.config.UPLOAD_URL}/{filename}'

                        new_candidate = models.Candidate(**data)
                        await new_candidate.save()

                        return response.redirect('/admin/candidates')
                    else:
                        errors.append('File is too large!')
                else:
                    errors.append('Image must be a JPG!')    
                
            except Exception as e:
                print(repr(e))
                errors.append('Invalid submitted data!')

        return jinja.render("admin/candidates/create.html", request, form=form, errors=errors)

    @app.route("/admin/candidates/<candidate_number:int>", methods=['GET'])
    @helpers.authorized('admin')
    async def candidates_read(request, candidate_number):
        row = await models.Candidate.get_or_none(candidate_number=candidate_number)
        if row:
            return jinja.render("admin/candidates/read.html", request, row=row)
        else:
            raise SanicException('Not Found', 404)

    @app.route("/admin/candidates/<candidate_number:int>/edit", methods=['GET', 'POST'])
    @helpers.authorized('admin')
    async def candidates_edit(request, candidate_number):
        row = await models.Candidate.get_or_none(candidate_number=candidate_number)
        if row:
            form = forms.candidates.EditForm(
                formdata=request.form or None,
                obj=row
            )
            errors = []
            if request.method == 'POST' and form.validate():
                try:
                    data = { **form.data }

                    upload_file = request.files['image'][0]
                    file_body = upload_file.body

                    if len(file_body) == 0:
                        row.update_from_dict(data)
                        await row.save()
                        return response.redirect(f'/admin/candidates/{row.candidate_number}')
                    
                    else:
                        file_name_type = upload_file.name.split('.')[-1]
                        if file_name_type == "jpg":    
                            # 5 MB limit
                            if len(file_body) < (5 * 1024 * 1024):
                                filename = f'{ datetime.now().strftime("%Y%m%d-%H%M%S-%f") }.jpg'

                                await helpers.process_upload(app, file_body, filename)

                                data['image'] = f'{app.config.UPLOAD_URL}/{filename}'

                                row.update_from_dict(data)
                                await row.save()

                                return response.redirect(f'/admin/candidates/{row.candidate_number}')
                            else:
                                errors.append('File is too large!')
                        else:
                            errors.append('Image must be a JPG!')    

                except Exception as e:
                    print(repr(e))
                    errors.append('Invalid submitted data!')

            return jinja.render("admin/candidates/edit.html", request, row=row, form=form, errors=errors)

        else:
            raise SanicException('Not Found', 404)

    @app.route("/admin/candidates/<candidate_number:int>/delete", methods=['GET', 'POST'])
    @helpers.authorized('admin')
    async def candidates_delete(request, candidate_number):
        row = await models.Candidate.get_or_none(candidate_number=candidate_number)
        if row:
            form = forms.candidates.DeleteForm(request.form)
            errors = []
            if request.method == 'POST' and form.validate():
                print(form.confirmation.data)
                if form.confirmation.data == True:
                    try:
                        await row.delete()

                    except Exception as e:
                        print(repr(e))
                    
                    return response.redirect('/admin/candidates')
                else:
                    return response.redirect(f'/admin/candidates/{row.candidate_number}')

            return jinja.render("admin/candidates/delete.html", request, row=row, form=form, errors=errors)
        else:
            raise SanicException('Not Found', 404)
