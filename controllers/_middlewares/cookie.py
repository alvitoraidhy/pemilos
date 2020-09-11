from sanic import response
from itsdangerous.serializer import Serializer
from itsdangerous.exc import BadSignature
import json

def init(current):
    app = current.app

    @app.middleware('request')
    async def check_signed_cookies(request):
        s = Serializer(app.config.SECRET_KEY)
        session = request.cookies.get('session')
        if session:
            try:
                request.ctx.session = s.loads(session)
            except BadSignature:
                request.cookies.pop('session')
                request.ctx.session = dict()
        else:
            request.ctx.session = dict()

    @app.middleware('response')
    async def sign_cookies(request, response):
        s = Serializer(app.config.SECRET_KEY)
        try:
            response.cookies['session'] = s.dumps(request.ctx.session)
            response.cookies['session']['max-age'] = 86400
        except AttributeError:
            pass
