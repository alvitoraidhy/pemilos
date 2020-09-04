def init(current):
    app, jinja, models, forms = current.app, current.jinja, current.models, current.forms

    @app.route("/", methods=['GET', 'POST'])
    async def index(request):
        return jinja.render("index.html", request)
