from sanic_ext import render
from sanic import Blueprint

bp = Blueprint("index")


@bp.route("/", methods=["GET", "POST"])
async def index(request):
    return await render("index.html", context={"request": request})
