import json, math

from app.grandpy import GrandPy

class TestTools:

    def setup_method(self):
        pass

    def teardown_method(self):
        pass

    def ask_grandpy(self, message, key="answer", options={}):

        """Pose une question à GrandPy. Renvoie la réponse sous la forme str épuré de tout html"""

        message_obj = {"user_message": message, "options": options}
        raw_response = GrandPy("127.0.0.1").build_response(message_obj)
        response_formatted = json.loads(raw_response).get(key)

        return response_formatted.replace("<br>", "")
    
    def get_fake_weather_data(self, user_location):

        round = lambda x: math.ceil(x) if x - math.floor(x) > 0.5 else math.floor(x)

        if not user_location: return None

        current_f = {
            "weather": [{
                "description": "couvert",
                "icon": "04d"
            }],
            "main": {
                "temp": 21.94,
                "feels_like": 18.89,
                "temp_min": 21,
                "temp_max": 24.44,
                "humidity": 40
            },
            "name": "Paris"            
        }

        daily_f = {
            "daily": [
                {"temp": {
                    "min": 21,
                    "max": 24.44,
                }}
            ]
        }

        forecast = {**current_f, **daily_f}

        fake_weather_data = dict(
            tcur = round(forecast["main"]["temp"]),
            city = forecast["name"],
            description = forecast["weather"][0]["description"],
            icon = forecast["weather"][0]["icon"],
            tmin = round(forecast["daily"][0]["temp"]["min"]),
            tmax = round(forecast["daily"][0]["temp"]["max"])
        )

        return fake_weather_data

    def get_fake_api_data(self, api_name):
        
        gm_api_response = {
            "html_attributions": [],
            "results": [
                {
                    "formatted_address": "7 Cité Paradis, 75010 Paris, France",
                    "geometry": {
                        "location": {
                            "lat": 48.8747265,
                            "lng": 2.3505517
                        }
                    },
                    "name": "Openclassrooms",
                }
            ]
        }

        wiki_api_response = {
            "query": {
                "pages": [
                    {
                        "title": "Cité Paradis",
                        "extract": "La cité Paradis est une voie publique située dans le 10e arrondissement de Paris.\n\n\nSituation et accès\nLa cité Paradis est une voie publique située dans le 10e arrondissement de Paris. Elle est en forme de té, une branche débouche au 43, rue de Paradis, la deuxième au 57, rue d'Hauteville et la troisième en impasse."
                    }
                ]
            }
        }
        return gm_api_response if api_name == "maps" else wiki_api_response
