import os

# Statement for enabling the development environment
DEBUG = False

SITE_NAME = "Lucky club"

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
# SQLite for this example
# SQLALCHEMY_DATABASE_URI = 'postgresql://catalog:W>HD;@Zq7tnY3BQA@localhost/item_catalog'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "TLuUFarPdqHRlWikPvlMHiqy3oGIeutgYk5x5U8n"

# Secret key for signing cookies
SECRET_KEY = "TLuUFarssdPdqHRlWdsdgikPvlMHiqhhy3oGIggeutgYk5x5U8n"

FIREBASE_API_KEY = "AIzaSyB9LhiF3IUAIhKtbxzP2dKW8FtVQq7BU70"
FIREBASE_PROJECT_ID = "luckyclub-897a7"
FIREBASE_AUTH_SIGN_IN_OPTIONS = "email,google"

# Lots per page
PER_PAGE = 20

# TODO change it for real database
UPLOADED_PHOTOS_DEST = os.path.join(BASE_DIR, 'lucky_club/static/media')
UPLOADED_PHOTOS_URL = "http://127.0.0.1:8000/static/media/"
