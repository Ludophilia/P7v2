from sqlalchemy.engine import Engine
from sqlalchemy import event
from datetime import datetime
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
        return f"<Robot object owned by {self.id}>"

class State(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    robot_id = db.Column(db.String(15), db.ForeignKey('robot.id'), nullable=False)
    type = db.Column(db.String(25), nullable=False) #ex: WAITING, FEELING
    value = db.Column(db.String(50), nullable=False) #ex: HT_EVENT, ANGRY

    def __repr__(self):
        return f"<State object of type \"{self.type}\" and value \"{self.value}\" about {self.target}>"

class Memory(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    robot_id = db.Column(db.String(15), db.ForeignKey('robot.id'), nullable=False)
    object = db.Column(db.String(50), nullable=False) #ex: HT_ERROR, OWNER_FAV_COLOR
    value = db.Column(db.String(50), nullable=False) #ex: 1, GREEN

    def __repr__(self):
        return f"<Memory object \"{self.object}\" of value \"{self.value}\" about {self.target}>"
