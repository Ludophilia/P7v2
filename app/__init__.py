from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__) # __name__ == "app" (package/directory name)
app.config.from_object("config")
db = SQLAlchemy(app)

from app import views, models #POURQUOI ON DOIT FAIRE ÇA ? (Pour que la vue soit executée ? )