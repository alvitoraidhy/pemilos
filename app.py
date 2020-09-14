from sanic import Sanic
from sanic_jinja2 import SanicJinja2
from tortoise.contrib.sanic import register_tortoise
from configparser import ConfigParser
import os
import config, models, forms, controllers

app = Sanic("app")
app.config.from_object(config.classes[os.environ.get('ENV', 'development')])

app.static('/static', app.config.STATIC_DIR)
app.static(app.config.UPLOAD_URL, app.config.UPLOAD_DIR)

config = ConfigParser()

if not os.path.isfile(app.config.APP_CONFIG_FILE):  
  config.read('app_config_default.ini')
  with open(app.config.APP_CONFIG_FILE, 'w') as f:
    config.write(f)

config.read(app.config.APP_CONFIG_FILE)

jinja = SanicJinja2(app)

class current:
  app, jinja, models, forms, config = app, jinja, models, forms, config

controllers.init(current)
  
register_tortoise(
  app, db_url=app.config.DB_URL, modules={"models": ["models"]}, generate_schemas=True
)


if __name__ == "__main__":
  app.run(
    host=app.config.APP_HOST,
    port=app.config.APP_PORT,
    debug=app.config.DEBUG,
    workers=app.config.WORKERS
  )
