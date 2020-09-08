from app.grandpy.skills.base import basespeech
from app.grandpy import skills

def answer_message(matches, user_data):

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