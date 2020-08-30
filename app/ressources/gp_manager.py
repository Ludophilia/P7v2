from app.ressources.grandpy import GrandPy

gp_owners = {}

def pick_the_right_grandpy_instance(user_ip):

    global gp_owners #-_-"

    if user_ip not in gp_owners: 
        gp_owners[user_ip] = GrandPy(user_ip)

    return gp_owners.get(user_ip)