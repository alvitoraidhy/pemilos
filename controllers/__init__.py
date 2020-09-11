def init(current):
    from . import _helpers
    current.helpers = _helpers

    from ._middlewares import cookie
    cookie.init(current)
    
    from . import index, election, admin
    index.init(current)
    election.init(current)
    admin.init(current)
