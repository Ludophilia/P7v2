import os

# DEBUGGER SETTINGS

DEBUG = True
TESTING = True
LIVESERVER_PORT = 8943
LIVESERVER_TIMEOUT = 10

# FLASK SETTINGS

FLASK_ENV = os.environ.get('ENV').lower()
SECRET_KEY = os.environ.get("SECRET_KEY") # "".join([random.choice(string.printable) for _ in range(24)])

# FLASK SQL ALCHEMY SETTINGS
SQLALCHEMY_DATABASE_URI = "sqlite:///database_test.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# API KEYS

GM_API_KEY = os.environ.get("GM_API_KEY")
FA_KEY = os.environ.get("FA_KEY")
OWM_API_KEY = os.environ.get("OWM_API_KEY")

