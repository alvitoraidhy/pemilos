from sanic import response
from sanic.exceptions import SanicException, abort
from datetime import datetime

format = '%Y-%m-%dT%H:%M'

def init(current):
    app, models, config, helpers = (
        current.app, current.models, current.config, current.helpers
    )

    @app.route("/api/total-students", methods=['GET'])
    @helpers.authorized('admin')
    async def api_total_students(request):
        return response.json({
            'result': await models.Student.all().count()
        })

    @app.route("/api/has-voted", methods=['GET'])
    @helpers.authorized('admin')
    async def api_has_voted(request):
        return response.json({
            'result': await models.Student.filter(has_chosen_id__not_isnull=True).count()
        })

    @app.route("/api/hasnt-voted", methods=['GET'])
    @helpers.authorized('admin')
    async def api_hasnt_voted(request):
        return response.json({
            'result': await models.Student.filter(has_chosen_id__isnull=True).count()
        })

    @app.route("/api/election-info", methods=['GET'])
    async def api_election_end(request):
        format = format = '%Y-%m-%dT%H:%M'
        start = config.get('settings', 'election_schedule_start')
        end = config.get('settings', 'election_schedule_end')
        status = ""
        remaining_time = 0

        now = datetime.now()
        start_time = datetime.strptime(start, format)
        end_time = datetime.strptime(end, format)

        if now < start_time:
            status = "Not started yet"
            remaining_time = (start_time - now).seconds

        elif start_time <= now and now < end_time:
            status = "In progress"
            remaining_time = (end_time - now).seconds
        else:
            status = "Finished"

        return response.json({
            'result': {
                'start': start,
                'end': end,
                'status': status,
                'remaining_time': remaining_time
            }
        })
    
    @app.route("/api/result-info", methods=['GET'])
    async def api_result_end(request):
        format = format = '%Y-%m-%dT%H:%M'
        start = config.get('settings', 'result_schedule_start')
        end = config.get('settings', 'result_schedule_end')
        status = ""
        remaining_time = 0

        now = datetime.now()
        start_time = datetime.strptime(start, format)
        end_time = datetime.strptime(end, format)

        if now < start_time:
            status = "Not started yet"
            remaining_time = (start_time - now).seconds

        elif start_time <= now and now < end_time:
            status = "In progress"
            remaining_time = (end_time - now).seconds
        else:
            status = "Finished"

        return response.json({
            'result': {
                'start': start,
                'end': end,
                'status': status,
                'remaining_time': remaining_time
            }
        })


    @app.route("/api/grade-vote-percentage", methods=['GET'])
    @helpers.authorized('admin')
    async def api_grade_vote_count(request):
        students = await models.Student.all()
        result = dict()
        for x, y in [(10, 'x'), (11, 'xi'), (12, 'xii')]:
            has_voted = await models.Student.filter(grade=x, has_chosen_id__not_isnull=True).count()
            total_students = await models.Student.filter(grade=x).count()
            result[y] = f'{100 * has_voted / total_students}%' if total_students > 0 else '-'

        return response.json({
            'result': result
        })

    @app.route("/api/class-vote-percentage", methods=['GET'])
    @helpers.authorized('admin')
    async def api_vote_count(request):
        classname = request.args.get('class')
        has_voted = await models.Student.filter(classname__icontains=f'{classname} ', has_chosen_id__not_isnull=True).count()
        total_class_students = await models.Student.filter(classname__icontains=f'{classname} ').count()
        return response.json({
            'result': f'{100 * has_voted / total_class_students}%' if total_class_students > 0 else '-'
        })

    @app.route("/api/vote-result", methods=['GET'])
    async def api_candidates_vote(request):
        if not helpers.check_auth(request, 'admin'):
            start = config.get('settings', 'result_schedule_start')
            end = config.get('settings', 'result_schedule_end')
            now = datetime.now()
            if now < datetime.strptime(start, format) or datetime.strptime(end, format) < now:
                raise SanicException('Forbidden', 403)

        candidates = await models.Candidate.all()
        return response.json({
            'result': {
                'candidates': [{
                    'name': candidate.name,
                    'class': candidate.classname,
                    'candidate_number': candidate.candidate_number,
                    'votes': await models.Student.filter(has_chosen_id=candidate.candidate_number).count()
                } for candidate in candidates],
                'abstain_votes': await models.Student.filter(has_chosen_id__isnull=True).count(),
                'total_voted_students': await models.Student.filter(has_chosen_id__not_isnull=True).count(),
                'total_students': len(candidates)
            }
        })
