import math, json
import config as cf, os.path as pth

import requests

class APIManager:
    
    """Représente l'APIManager, c'est à dire le système qui télécharge les données des différentes 
    API et les rend disponible à d'autres systèmes"""

    def get_location_data(self, api_name):

        """Telecharge les données Maps sur OC ou de Wikipédia sur la Cité Paradis 
        si elles n'existent pas, les stocke dans un fichier .js, et les rappelle sous forme de dict"""
        
        maps_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=openclassrooms+paris&key={cf.GM_API_KEY}"
        wiki_url = "https://fr.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&titles=Cité Paradis&formatversion=2&exsentences=3&exlimit=1&explaintext=1&exsectionformat=plain"

        data_url = maps_url if api_name == "maps" else wiki_url
        data_pth = f"app/ressources/{api_name}_data.json"

        if not pth.exists(data_pth): 
            with open(data_pth, "w") as f:
                f.write(requests.get(data_url).text)

        with open(data_pth, "r") as f:
            json_formatted_api_data = json.loads(f.read())

        return json_formatted_api_data

    def get_weather_data(self, user_location):
        
        """Acquiert les données météo de et renvoie certaine d'entres elles sous forme de dict."""

        latitude, longitude = user_location["latitude"], user_location["longitude"]
        round = lambda x: math.ceil(x) if x - math.floor(x) > 0.5 else math.floor(x)

        owm_cur_url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={cf.OWM_API_KEY}&lang=fr&units=metric"
        owm_dal_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={latitude}&lon={longitude}&appid={cf.OWM_API_KEY}&lang=fr&units=metric&exclude=current,hourly"

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
