def init(current):
    from ._middlewares import cookie
    cookie.init(current)
    
    from . import index, election
    index.init(current)
    election.init(current)
