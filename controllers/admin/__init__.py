def init(current):
    from . import auth, dashboard, candidates, students, settings
    auth.init(current)
    dashboard.init(current)
    candidates.init(current)
    students.init(current)
    settings.init(current)
