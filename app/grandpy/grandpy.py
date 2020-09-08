import json

from app.grandpy import skills
from app.grandpy.skills import basespeech

class GrandPy:

    """Représente GrandPy, le robot qui répond aux messages et joue parfois avec l'utilisateur."""

    def __init__(self, owner_ip_adress):
        self.owner = owner_ip_adress
    
    def __answer_message(self, matches, user_data):

        """Construit la réponse textuelle à l'input utilisteur en fonction des mots clés qui y figurent"""

        answer = ""

        if "hello" in matches:

            answer += skills.say_hello(answer)

        if "info" in matches and "website" in matches:
            
            answer += skills.give_website_info(answer)

        if "play" in matches and "heads" in matches and "tails" in matches:
        
            answer += skills.play_heads_or_tails(matches, answer)

        if ("how" in matches or "question" in matches) and ("go" in matches) and (
        not "at" in matches):

            answer += skills.give_state_of_mind(answer)

        if ("question" in matches or "what" in matches) and "time" in matches:

            answer += skills.give_time(user_data, answer)

        if ("question" in matches or "what" in matches) and "weather" in matches:
            
            answer += skills.tell_weather(user_data, answer)

        if "oc" in matches and "know" in matches and "address" in matches:

            answer += skills.get_oc_address(answer)

        answer += f"{basespeech.SORRY}" if len(answer) == 0 else ""

        return answer

    def build_response(self, user_data):

        """Renvoie une réponse (sous forme de json) à renvoyer à l'utilisateur en prenant en compte les mots clés qui y figurent"""

        user_message = user_data.get("user_message", "")
        matches = skills.Parser().find_matches(user_message)

        grandpy_response = {}

        if "oc" in matches and "know" in matches and "address" in matches:

            grandpy_response["oc_anecdote"] = skills.get_oc_anecdote()
            grandpy_response["oc_coordinates"] = skills.get_oc_coordinates()

        grandpy_response["answer"] = self.__answer_message(matches, user_data)

        return json.dumps(grandpy_response, ensure_ascii=False, sort_keys=True)

    def start_conversation(self):

        """Renvoie un message sympa pour démarrer la conversation avec l'utilisateur """

        starter = f"{basespeech.STARTER}"

        return starter

    def deal_with_clicks_on_logo(self, user_data):

        """Renvoie une réponse (sous forme de str) à l'utilisateur en fonction du 
        nombre de fois qu'il a appuyé sur le logo de grandpy"""

        nth_time = user_data.get("reactions", "")

        return basespeech.INTERROGATE_CLICK_ON_LOGO if nth_time == "n0" else basespeech.ANNOYED.get(nth_time, "...")
