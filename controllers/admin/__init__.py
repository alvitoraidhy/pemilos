def init(current):
    from . import auth, dashboard, candidates
    auth.init(current)
    dashboard.init(current)
    candidates.init(current)
