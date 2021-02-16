import json

from app.grandpy import skills
from app.grandpy.skills import basespeech as speech

from app.models import State, Memory

class GrandPy:

    """Représente GrandPy, le robot qui répond aux messages et joue parfois avec l'utilisateur."""

    def __init__(self, owner_ip_adress):
        self.owner = owner_ip_adress
    
    def start_conversation(self):

        """Renvoie un message sympa pour démarrer la conversation avec l'utilisateur """

        waiting_for_htev = State.query.get({'robot_id': self.owner, 'type':'WAITING', 'value':'HT_EVENT'})
        state_of_the_game = Memory.query.get({'robot_id': self.owner, 'object': 'HT_REMAINING'})

        remaining = int(state_of_the_game.value) if state_of_the_game else 3

        starter = f"{speech.STARTER + speech.HT_REMINDER(waiting_for_htev, remaining)}"

        return starter

    def deal_with_clicks_on_logo(self, user_data):

        """Renvoie une réponse (sous forme de str) à l'utilisateur en fonction du 
        nombre de fois qu'il a appuyé sur le logo de grandpy"""

        nth_time = user_data.get("reactions", "")

        return speech.INTERROGATE_CLICK_ON_LOGO if nth_time == "n0" else speech.ANNOYED.get(nth_time, "...")

    def build_response(self, user_data):

        """Renvoie une réponse (sous forme de json) à renvoyer à l'utilisateur en prenant en compte les mots clés qui y figurent"""

        user_message = user_data.get("user_message", "")

        parser = skills.Parser()
        matches = parser.find_matches(user_message)

        grandpy_response = {}

        if "know" in matches and "address" in matches:

            place_of_interest = parser.extract_place_from_user_message(user_message) # ex : tour eiffel
            user_data["place_of_interest"] = place_of_interest

            tourist_guide = skills.TouristGuide(place_of_interest)
            user_data["tourist_guide"] = tourist_guide

            coordinates = tourist_guide.get_coordinates(place_of_interest)
            anecdote = tourist_guide.get_anecdote(coordinates, matches)

            grandpy_response["oc_coordinates"] = coordinates
            grandpy_response["oc_anecdote"] = anecdote

        user_data["owner"] = self.owner
        grandpy_response["answer"] = skills.answer_message(matches, user_data)

        return json.dumps(grandpy_response, ensure_ascii=False, sort_keys=True)
