import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from lucky_club import app
from lucky_club.database import db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()