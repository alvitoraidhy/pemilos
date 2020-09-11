from sanic import response

def init(current):
    app, jinja, models, forms, helpers = \
        current.app, current.jinja, current.models, current.forms, current.helpers

    @app.route("/admin/dashboard", methods=['GET'])
    @helpers.authorized('admin')
    async def admin_dashboard(request):
        return jinja.render("admin/dashboard.html", request)
