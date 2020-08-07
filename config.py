import os

# FLASK SETTINGS

FLASK_ENV = os.environ.get('ENV').lower()
SECRET_KEY = os.environ.get("SECRET_KEY") # "".join([random.choice(string.printable) for _ in range(24)])

# API KEYS

GM_API_KEY = os.environ.get("GM_API_KEY")
FA_KEY = os.environ.get("FA_KEY")
OWM_API_KEY = os.environ.get("OWM_API_KEY")

if os.environ.get('ENV') == "DEVELOPMENT":
    DEBUG = True