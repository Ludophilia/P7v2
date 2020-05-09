import os # random, string

FLASK_ENV = os.environ.get('ENV').lower()
SECRET_KEY = os.environ.get("SECRET_KEY") # "".join([random.choice(string.printable) for _ in range(24)])
API_KEY = os.environ.get("API_KEY")