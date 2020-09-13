def init(current):
    from . import _helpers
    current.helpers = _helpers

    from ._middlewares import cookie
    cookie.init(current)
    
    from . import index, election, admin, api
    index.init(current)
    election.init(current)
    admin.init(current)
    api.init(current)
