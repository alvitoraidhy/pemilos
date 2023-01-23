from sanic.response import text
from sanic import Sanic

from main.config import current_env as config

app = Sanic("pemilos")
app.update_config(config.to_dict())

app.static("/static", app.config.STATIC_DIR)
