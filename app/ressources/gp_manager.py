from app.ressources.grandpy import GrandPy

owners = {}

def pick_the_right_grandpy_instance(user_ip):

    global owners #-_-"

    if user_ip not in owners: 
        owners[user_ip] = GrandPy(user_ip)

    return owners.get(user_ip)