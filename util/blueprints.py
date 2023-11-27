import routes


def register_blueprints(app):
    app.register_blueprint(routes.auth)
    app.register_blueprint(routes.categories)
    app.register_blueprint(routes.goal_logs)
    app.register_blueprint(routes.goals)
    app.register_blueprint(routes.users)
