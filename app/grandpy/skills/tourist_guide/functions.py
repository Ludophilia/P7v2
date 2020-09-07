from app.grandpy.skills.tourist_guide import speech
from app.grandpy.skills import APIManager

def get_anecdocte(jsf_wiki_data):

    """Récupère l'anecdocte de GP sur la Cité Paradis et l'url de la fiche wikipédia 
    associée à partir des données jsf (json-formatted) de l'API Wikimedia. 
    Renvoie un str contenant l'anecdocte"""

    title = jsf_wiki_data["query"]["pages"][0]["title"]
    wiki_url = f"https://fr.wikipedia.org/wiki/{title}".replace(" ", "_")

    wikipedia_part = jsf_wiki_data["query"]["pages"][0]["extract"].split('\n')[-1]
    knowmore_part = speech.KNOWMORE("Wikipédia", wiki_url)

    return f"{speech.ANECDOCTE_STARTER} {wikipedia_part} {knowmore_part}"

def give_oc_address(message, grandpy_response):

    """Génère un message où GrandPy donne l'adresse d'openclassrooms.Génère aussi un autre message contenant une anecdocte sur la rue d'OC et renvoie les coordonnés du lieu pour un affichage sur une carte."""

    api_manager = APIManager()

    oc_maps_data_js = api_manager.get_location_data("maps")
    oc_address = oc_maps_data_js["results"][0]["formatted_address"].replace(", France", "") 

    message += f"{speech.ADDRESSFOUND(oc_address)}<br>"

    grandpy_response.update(
        anecdocte = get_anecdocte(api_manager.get_location_data("wiki")),
        location = oc_maps_data_js["results"][0]["geometry"]["location"]
    )

    return {"message": message, "grandpy_response": grandpy_response}