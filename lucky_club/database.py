from flask import current_app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db():
    # TODO Add other modules here
    import lucky_club.users_manager.models
    import lucky_club.api.categories.models
    import lucky_club.api.lots.models
    import lucky_club.api.account.models
    import lucky_club.api.attaches.models
    import lucky_club.api.profile.models

    db.init_app(current_app)
    db.create_all()
