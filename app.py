from sanic import Sanic
from sanic_jinja2 import SanicJinja2
from sanic_cookies import AuthSession, InCookieEncrypted, login_required
from tortoise.contrib.sanic import register_tortoise
import logging, os
import config, models, forms

app = Sanic("app")
app.config.from_object(config.classes[os.environ.get('ENV', 'development')])

jinja = SanicJinja2(app)

auth_session = AuthSession(
    app,
    master_interface=InCookieEncrypted(app.config.SESSION_KEY)
)

# logging.basicConfig(level=logging.DEBUG)

register_tortoise(
    app, db_url=app.config.DB_URL, modules={"models": ["models"]}, generate_schemas=True
)

class current:
  app, jinja, models, forms = app, jinja, models, forms

import controllers

controllers.init(current)

if __name__ == "__main__":
  app.run(host=app.config.APP_HOST, port=app.config.APP_PORT)
