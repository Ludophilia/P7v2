from app.grandpy.skills.tourist_guide import speech
from app.grandpy.skills import APIManager

def get_oc_anecdote():

    """Récupère l'anecdote de GP sur la Cité Paradis et l'url de la fiche wikipédia 
    associée à partir des données jsf (json-formatted) de l'API Wikimedia. 
    Renvoie un str contenant l'anecdote"""

    wiki_data = APIManager().get_location_data("wiki")

    title = wiki_data["query"]["pages"][0]["title"]
    wiki_url = f"https://fr.wikipedia.org/wiki/{title}".replace(" ", "_")
    wikipedia_part = wiki_data["query"]["pages"][0]["extract"].split('\n')[-1]

    knowmore_part = speech.KNOWMORE("Wikipédia", wiki_url)

    return f"{speech.ANECDOTE_STARTER} {wikipedia_part} {knowmore_part}"

def get_oc_coordinates():

    """Renvoie les coordonnés du lieu pour un affichage sur une carte."""

    oc_maps_data_js = APIManager().get_location_data("maps")
    oc_coordinates = oc_maps_data_js["results"][0]["geometry"]["location"]

    return oc_coordinates

def get_oc_address(message):

    """Génère un message où GrandPy donne l'adresse d'openclassrooms."""

    oc_maps_data_js = APIManager().get_location_data("maps")
    oc_address = oc_maps_data_js["results"][0]["formatted_address"].replace(", France", "") 

    message += f"{speech.ADDRESSFOUND(oc_address)}<br>"

    return message