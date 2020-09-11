from datetime import datetime

from sqlalchemy.engine import Engine
from sqlalchemy import event

from app import db

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

class Robot(db.Model):
    id = db.Column(db.String(15), primary_key=True) #ip adress
    creation_date = db.Column(db.DateTime, default=datetime.utcnow())
    states = db.relationship('State', backref="target", lazy=True, cascade="all, delete-orphan")
    memory = db.relationship('Memory', backref="target", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<{self.id}>"

class State(db.Model):
    robot_id = db.Column(db.String(15), db.ForeignKey('robot.id'), primary_key=True, nullable=False)
    type = db.Column(db.String(25), primary_key=True, nullable=False) #ex: WAITING, FEELING
    value = db.Column(db.String(50), primary_key=True, nullable=False) #ex: HT_EVENT, ANGRY

    def __repr__(self):
        return f"<State of {self.target} : type=\"{self.type}\", value=\"{self.value}\">"

class Memory(db.Model):
    robot_id = db.Column(db.String(15), db.ForeignKey('robot.id'), primary_key=True, nullable=False)
    object = db.Column(db.String(50), primary_key=True, nullable=False) #ex: HT_ERROR, OWNER_FAV_COLOR
    value = db.Column(db.String(50), nullable=False) #ex: 1, GREEN

    def __repr__(self):
        return f"<Memory of {self.target} : object=\"{self.object}\", value=\"{self.value}\">"
