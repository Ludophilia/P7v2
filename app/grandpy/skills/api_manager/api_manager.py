import math, json
import config as cf, os.path as pth
from typing import Optional

import requests

class APIManager:
    
    """Représente l'APIManager, c'est à dire le système qui télécharge les données des différentes 
    API et les rend disponible à d'autres systèmes"""

    def __get_closest_wiki_page(self, coordinates: dict) -> Optional[str]:

        """Récupère le titre de la wikipédia la plus proche des coordonnées du point d'intérêt 
        et les retourne sous forme de str"""

        latitude, longitude = coordinates["lat"], coordinates["lng"]

        geo_wiki_url = f"https://fr.wikipedia.org/w/api.php?action=query"\
                       f"&list=geosearch&format=json&formatversion=2"\
                       f"&gscoord={latitude}|{longitude}&gsradius=100&gslimit=1"

        geo_wiki_data = requests.get(geo_wiki_url).json()
        results = geo_wiki_data["query"]["geosearch"]
        
        if len(results) == 0: return None

        closest_wiki_page = results[0]["title"]

        return closest_wiki_page

    def get_wiki_data(self, coordinates: dict) -> Optional[dict]:

        """Telecharge les données wikipédia proche du point d'intérêt et les retourne 
        sous forme de dict"""

        # ex coordinates - {'lat': 48.88670459999999, 'lng': 2.3431043}

        closest_wiki_page = self.__get_closest_wiki_page(coordinates)
        if closest_wiki_page is None: return None

        wiki_url = f"https://fr.wikipedia.org/w/api.php?action=query"\
                   f"&format=json&prop=extracts&titles={closest_wiki_page}"\
                   f"&formatversion=2&exsentences=3&exlimit=1"\
                   f"&explaintext=1&exsectionformat=plain"

        wiki_data = requests.get(wiki_url).json()

        return wiki_data

    def get_maps_data(self, place_of_interest: str) -> Optional[dict]:

        """Telecharge les données Maps sur le point d'intérêt et les retourne sous 
        forme de dict"""
        
        maps_url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?"\
                    f"input={place_of_interest}&inputtype=textquery&language=fr"\
                    f"&key={cf.GM_API_KEY}&fields=name,formatted_address,geometry"

        maps_data = requests.get(maps_url).json()
        
        status = maps_data["status"]

        return maps_data if status == "OK" else None

    def get_weather_data(self, user_location):
        
        """Acquiert les données météo de et renvoie certaine d'entres elles sous 
        forme de dict."""

        latitude, longitude = user_location["latitude"], user_location["longitude"]
        round = lambda x: math.ceil(x) if x - math.floor(x) > 0.5 else math.floor(x)

        owm_cur_url = f"https://api.openweathermap.org/data/2.5/weather?"\
                      f"lat={latitude}&lon={longitude}&appid={cf.OWM_API_KEY}"\
                      "&lang=fr&units=metric"
        owm_dal_url = f"https://api.openweathermap.org/data/2.5/onecall?"\
                      f"lat={latitude}&lon={longitude}&appid={cf.OWM_API_KEY}"\
                      f"&lang=fr&units=metric&exclude=current,hourly"
                
        forecast = {
            **requests.get(owm_cur_url).json(),
            **requests.get(owm_dal_url).json()
        }

        weather_data = dict(
            tcur = round(forecast["main"]["temp"]),
            city = forecast["name"],
            description = forecast["weather"][0]["description"],
            icon = forecast["weather"][0]["icon"],
            tmin = round(forecast["daily"][0]["temp"]["min"]),
            tmax = round(forecast["daily"][0]["temp"]["max"])
        )
        return weather_data
