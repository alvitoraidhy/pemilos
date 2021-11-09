def init(current):
    app, jinja = current.app, current.jinja

    @app.route("/", methods=['GET', 'POST'])
    async def index(request):
        return jinja.render("index.html", request)
