from tortoise.contrib.sanic import register_tortoise
from sanic import Sanic

from main.config import current_env as config
from main.controllers import bp

app = Sanic("pemilos")
app.update_config(config.to_dict())

app.blueprint(bp)

app.static("/static", app.config.STATIC_DIR)

register_tortoise(
    app,
    db_url=config.DB_URL,
    modules={"models": ["main.models"]},
    generate_schemas=True,
)
