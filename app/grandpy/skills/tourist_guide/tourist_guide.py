from typing import Optional

from app.grandpy.skills.tourist_guide import speech
from app.grandpy.skills import APIManager

class TouristGuide:

    def __init__(self, place_of_interest: str): #Pourquoi init avec poi ? Déclencher une rech directement ?
        self.coordinates = dict()
        self.wiki_data = None
        self.place_of_interest = place_of_interest
        self.maps_data = APIManager().get_maps_data(place_of_interest)

    def get_anecdote(self, coordinates: dict, matches: list) -> str:

        """Récupère l'anecdote de GP et l'url de la fiche wikipédia associée à partir 
        des données jsf (json-formatted) de l'API Wikimedia. Renvoie un str contenant l'anecdote."""

        if self.coordinates != coordinates:
            self.wiki_data = APIManager().get_wiki_data(coordinates)
            self.coordinates = coordinates

        if self.wiki_data is None: return speech.NO_ANECDOTE

        starter = f"{speech.ANECDOTE_STARTER} " if "oc" in matches else ""
        wiki_part = self.wiki_data["query"]["pages"][0]["extract"]#.split('\n')[-1]
        title = self.wiki_data["query"]["pages"][0]["title"].replace("'", "%27")
        wiki_url = f"https://fr.wikipedia.org/wiki/{title}".replace(" ", "_")
        knowmore_part = speech.KNOWMORE("Wikipédia", wiki_url)

        return f"{starter}" + f"{wiki_part} {knowmore_part}<br>"

    def get_coordinates(self, place_of_interest: str) -> Optional[dict]:

        """Renvoie les coordonnés du lieu pour un affichage sur une carte."""

        if self.place_of_interest != place_of_interest:
            self.maps_data = APIManager().get_maps_data(place_of_interest)
            self.place_of_interest = place_of_interest

        if self.maps_data is None: return None

        coordinates = self.maps_data["candidates"][0]["geometry"]["location"]

        return coordinates

    def get_address(self, place_of_interest: str, message: str) -> str:

        """Génère un message où GrandPy donne l'adresse du lieu d'intérêt"""

        if self.place_of_interest != place_of_interest:
            self.maps_data = APIManager().get_maps_data(place_of_interest)
            self.place_of_interest = place_of_interest

        if self.maps_data is None: return speech.NO_ADDRESS

        address = self.maps_data["candidates"][0]["formatted_address"].replace(", France", "") 

        message += f"{speech.ADDRESSFOUND(address)}<br>"

        return message