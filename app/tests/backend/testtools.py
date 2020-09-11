import json, math

from app.grandpy import GrandPy
from app.tests.backend import fake_data as fakeaf

class TestTools:

    def ask_grandpy(self, message, key="answer", options={}):

        """Pose une question à GrandPy. Renvoie la réponse sous la forme str épuré de tout html"""

        message_obj = {"user_message": message, "options": options}
        raw_response = GrandPy("127.0.0.1").build_response(message_obj)
        response_formatted = json.loads(raw_response).get(key)

        return response_formatted if key != "answer" else response_formatted.replace("<br>", "")
    
    def get_fake_weather_data(self, user_location):

        round = lambda x: math.ceil(x) if x - math.floor(x) > 0.5 else math.floor(x)

        if not user_location: return None
        
        forecast = {**fakeaf.OW_CURRENT_F, **fakeaf.OW_DAILY_F}

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
        
        return fakeaf.GM_API_RESPONSE if api_name == "maps" else fakeaf.WM_API_RESPONSE
