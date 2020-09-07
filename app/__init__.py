from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config as cf

app = Flask(__name__) # __name__ == "app" (package/directory name)
app.config.from_object(cf)
db = SQLAlchemy(app)

from app import views, models