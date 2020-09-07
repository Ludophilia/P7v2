import json, random, time 
from datetime import date as dt

from app.grandpy import skills  #import app.grandpy.skills as skills
from app.grandpy.skills import basespeech as speech

class GrandPy:

    """Représente GrandPy, le robot qui répond aux messages et joue parfois avec l'utilisateur."""

    def __init__(self, owner_ip_adress):
        self.owner = owner_ip_adress
        #ADD DATABASE OP HERE
        self.memory = {}
        #ADD DATABASE OP HERE
        self.isWaitingForAnAnswer = set()
        #self.answers = 0
    
    #PAS TOYCGER
    def answer_message(self, user_data):

        """Renvoie une réponse (sous forme de json) à l'input utilisteur en fonction des mots clés qui y figurent"""

        user_message = user_data.get("user_message", "")
        matches = skills.Parser().find_matches(user_message)

        message, grandpy_response = "", {}

        #ADD DATABASE OP HERE
        if self.isWaitingForAnAnswer:
            
            #ADD DATABASE OP HERE
            if "#HT" in self.isWaitingForAnAnswer:
                message += self.play_heads_or_tails(matches, message)

        else:

            if "hello" in matches:

                message += skills.say_hello(message)

            if "info" in matches and "website" in matches:
                
                message += skills.give_website_info(message)

            if "play" in matches and "heads" in matches and "tails" in matches:
            
                message += skills.play_heads_or_tails(matches, message)

            if ("how" in matches or "question" in matches) and ("go" in matches) and (
            not "at" in matches):

                message += skills.give_state_of_mind(message)

            if ("question" in matches or "what" in matches) and "time" in matches:

                message += skills.give_time(user_data, message)

            if ("question" in matches or "what" in matches) and "weather" in matches:
                
                message += skills.tell_weather(user_data, message)

            if "oc" in matches and "know" in matches and "address" in matches:

                oc_address = skills.give_oc_address(message, grandpy_response)

                grandpy_response = oc_address.get("grandpy_response") 
                message += oc_address.get("message")

        message += f"{speech.SORRY}" if len(message) == 0 else "" 
        grandpy_response["message"] = message
        return json.dumps(grandpy_response, ensure_ascii=False, sort_keys=True)

    #PAS TOYCGER
    def start_conversation(self):

        """Renvoie un message sympa pour démarrer la conversation avec l'utilisateur """

        starter = f"{speech.STARTER}"

        return starter

    #PAS TOYCGER
    def deal_with_clicks_on_logo(self, user_data):

        """Renvoie une réponse (sous forme de str) à l'utilisateur en fonction du 
        nombre de fois qu'il a appuyé sur le logo de grandpy"""

        nth_time = user_data.get("reactions", "")

        return speech.INTERROGATE_CLICK_ON_LOGO if nth_time == "n0" else speech.ANNOYED.get(nth_time, "...")
