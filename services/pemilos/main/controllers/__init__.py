from sanic import Blueprint

from .index import bp as index

bp = Blueprint.group(index, url_prefix="/")
