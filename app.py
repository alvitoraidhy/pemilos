from sanic import Sanic
from sanic_jinja2 import SanicJinja2
from tortoise.contrib.sanic import register_tortoise
import os
import config, models, forms, controllers

app = Sanic("app")
app.config.from_object(config.classes[os.environ.get('ENV', 'development')])

app.static('/static', app.config.STATIC_DIR)
app.static(app.config.UPLOAD_URL, app.config.UPLOAD_DIR)

jinja = SanicJinja2(app)

class current:
  app, jinja, models, forms = app, jinja, models, forms

controllers.init(current)
  
register_tortoise(
  app, db_url=app.config.DB_URL, modules={"models": ["models"]}, generate_schemas=True
)

if __name__ == "__main__":
  app.run(
    host=app.config.APP_HOST,
    port=app.config.APP_PORT,
    debug=app.config.DEBUG
  )
