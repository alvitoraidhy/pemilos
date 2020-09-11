from sanic.exceptions import abort
from functools import wraps

def check_auth(request, account_type):
    return True if request.ctx.session.get(account_type) else False

def authorized(account_type):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            # run some method that checks the request
            # for the client's authorization status
            if check_auth(request, account_type):
                # the user is authorized.
                # run the handler method and return the response
                response = await f(request, *args, **kwargs)
                return response
            else:
                # the user is not authorized.
                abort(403)

        return decorated_function
    return decorator

def login(request, account_type: str, data: dict):
    session = request.ctx.session
    session[account_type] = data
    return True

def logout(request, account_type: str):
    session = request.ctx.session
    session.pop(account_type)
    return None

def get_account(request, account_type: str):
    session = request.ctx.session
    return session.get(account_type)
