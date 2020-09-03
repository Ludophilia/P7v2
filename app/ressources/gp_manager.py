from app.ressources.grandpy import GrandPy
from app.models import db, Grandpy

#gp_owners = {}

def pick_the_right_grandpy_instance(user_ip):

    #global gp_owners #-_-"

    # N'enregistre pas l'objet grandpy pour le moment

    if not Grandpy.query.get(user_ip):
        db.session.add(GrandPy(id=f"{user_ip}"))
        db.session.commit()

    # if user_ip not in gp_owners: 
    #     gp_owners[user_ip] = GrandPy(user_ip)

    # return gp_owners.get(user_ip)

    return Grandpy(user_ip)