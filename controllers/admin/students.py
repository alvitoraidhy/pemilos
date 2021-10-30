from sanic import response
from sanic.exceptions import SanicException, abort
from datetime import datetime
from urllib.parse import urlencode 
import csv, tempfile

ROWS_PER_PAGE=15

def init(current):
    app, jinja, models, forms, helpers = \
        current.app, current.jinja, current.models, current.forms, current.helpers

    @app.route("/admin/students", methods=['GET'])
    @helpers.authorized('admin')
    async def students_table(request):
        page = int(request.args.get('page', 1))
        form = forms.students.FindForm(request.args)
        form.has_chosen_id.choices += [(x.candidate_number, f'{x.candidate_number}') for x in (await models.Candidate.all())]
        query = []
        if form.validate():
            data, filter_dict = { key: value for key, value in form.data.items() }, dict()
            try:
                has_chosen_id = int(data['has_chosen_id'])
                filter_dict['has_chosen_id__icontains'] = has_chosen_id

            except:
                if form.has_chosen_id.data == 'any':
                    filter_dict['has_chosen_id__not_isnull'] = True
                elif form.has_chosen_id.data == 'none':
                    filter_dict['has_chosen_id__isnull'] = True
            
            data.pop('has_chosen_id', None)

            query = [(key, data[key]) for key in data.keys() if data[key]]
            filter_dict = {**filter_dict, **{ f'{ key}__icontains': value for key, value in query } }
            
            rows = await models.Student.filter(**filter_dict).offset((page-1) * ROWS_PER_PAGE).limit(ROWS_PER_PAGE)
        
        else: 
            rows = await models.Student.all().offset((page-1) * ROWS_PER_PAGE).limit(ROWS_PER_PAGE)

        return jinja.render(
            "admin/students/table.html", request,
            form=form,
            rows=rows,
            page=page,
            next=urlencode((*query, ('page', page + 1))) if len(rows) > 0 else None,
            previous=urlencode((*query, ('page', page - 1))) if page > 1 else None
        )

    @app.route("/admin/students/batch-delete", methods=['POST'])
    @helpers.authorized('admin')
    async def students_batch_delete(request):
        form = forms.students.FindForm(request.form or None)
        form.has_chosen_id.choices += [(x.candidate_number, f'{x.candidate_number}') for x in (await models.Candidate.all())]

        if form.validate():
            data, filter_dict = { key: value for key, value in form.data.items() }, dict()
            try:
                has_chosen_id = int(data['has_chosen_id'])
                filter_dict['has_chosen_id__icontains'] = has_chosen_id

            except:
                if form.has_chosen_id.data == 'any':
                    filter_dict['has_chosen_id__not_isnull'] = True
                elif form.has_chosen_id.data == 'none':
                    filter_dict['has_chosen_id__isnull'] = True
            
            data.pop('has_chosen_id', None)

            query = [(key, data[key]) for key in data.keys() if data[key]]
            filter_dict = {**filter_dict, **{ f'{ key}__icontains': value for key, value in query } }
            
            await models.Student.filter(**filter_dict).delete()

            return response.redirect('/admin/students')
        
        else: 
            raise SanicException('Bad Request', 400)

    @app.route("/admin/students/create", methods=['GET', 'POST'])
    @helpers.authorized('admin')
    async def students_create(request):
        form = forms.students.CreateForm(request.form or None)
        form.has_chosen_id.choices += [(x.candidate_number, f'{x.name.split()[0]} ({x.candidate_number})') for x in (await models.Candidate.all())]
        errors = []
        if request.method == 'POST' and form.validate():
            try:
                data = { **form.data }


                data['has_chosen_id'] = data['has_chosen_id'] or None

                new_student = models.Student(**data)
                new_student.set_password(data['password'])
                await new_student.save()

                return response.redirect('/admin/students')
                
            except Exception as e:
                print(repr(e))
                errors.append('Invalid submitted data!')

        return jinja.render("admin/students/create.html", request, form=form, errors=errors)

    @app.route("/admin/students/<id:int>", methods=['GET'])
    @helpers.authorized('admin')
    async def students_read(request, id):
        row = await models.Student.get_or_none(id=id).prefetch_related('has_chosen')
        if row:
            return jinja.render("admin/students/read.html", request, row=row)
        else:
            raise SanicException('Not Found', 404)

    @app.route("/admin/students/<id:int>/edit", methods=['GET', 'POST'])
    @helpers.authorized('admin')
    async def students_edit(request, id):
        row = await models.Student.get_or_none(id=id)
        if row:
            form = forms.students.EditForm(
                formdata=request.form or None,
                obj=row
            )
            form.has_chosen_id.choices += [(x.candidate_number, f'{x.name.split()[0]} ({x.candidate_number})') for x in (await models.Candidate.all())]
            errors = []
            if request.method == 'POST' and form.validate():
                try:
                    data = { **form.data }

                    data['has_chosen_id'] = data['has_chosen_id'] or None

                    row.update_from_dict(data)

                    if data.get('password'):
                        row.set_password(data['password'])
                        
                    await row.save()
                    return response.redirect(f'/admin/students/{row.id}')

                except Exception as e:
                    print(repr(e))
                    errors.append('Invalid submitted data!')

            return jinja.render("admin/students/edit.html", request, row=row, form=form, errors=errors)

        else:
            raise SanicException('Not Found', 404)

    @app.route("/admin/students/<id:int>/delete", methods=['GET', 'POST'])
    @helpers.authorized('admin')
    async def students_delete(request, id):
        row = await models.Student.get_or_none(id=id)
        if row:
            form = forms.students.DeleteForm(request.form)
            errors = []
            if request.method == 'POST' and form.validate():
                print(form.confirmation.data)
                if form.confirmation.data == True:
                    try:
                        await row.delete()

                    except Exception as e:
                        print(repr(e))
                    
                    return response.redirect('/admin/students')
                else:
                    return response.redirect(f'/admin/students/{row.id}')

            return jinja.render("admin/students/delete.html", request, row=row, form=form, errors=errors)
        else:
            raise SanicException('Not Found', 404)

    @app.route("/admin/students/import-csv", methods=['GET', 'POST'])
    @helpers.authorized('admin')
    async def students_import_csv(request):
        form = forms.students.ImportCSVForm(request.form)
        csv_format = ['nis','name','grade','classname','password','has_chosen_id']
        errors = []
        result = None
        if request.method == 'POST' and form.validate():
            try:
                upload_file = request.files['csv'][0]
                file_body = upload_file.body

                file_name_type = upload_file.name.split('.')[-1]
                if file_name_type == "csv":
                    # 5 MB limit
                    if len(file_body) < (5 * 1024 * 1024):
                        csv_reader = csv.reader(file_body.decode("utf-8").splitlines(), delimiter=',')
                        success_insert = 0
                        i = 0
                        for row in csv_reader:
                            if i > 0:
                                try:
                                    formatted_row = [x.strip() for x in row]
                                    data = { csv_format[x]: formatted_row[x] for x in range(len(csv_format)) }

                                    if not data['has_chosen_id']: data['has_chosen_id'] = None
                                    
                                    new_student = models.Student(**data)
                                    new_student.set_password(data['password'])
                                    await new_student.save()
                                    success_insert += 1
                                except Exception as e:
                                    errors.append(f'row {i}: {repr(e)}')
                            
                            i += 1
                        
                        result = f'Successfully inserted {success_insert} row(s)'
                    else:
                        errors.append('File is too large!')
                else:
                    errors.append('File must be a CSV!')    
                
            except Exception as e:
                print(repr(e))
                errors.append('Invalid submitted data!')
      
        return jinja.render("admin/students/import-csv.html", request, form=form, errors=errors, result=result, csv_format=str(csv_format))
