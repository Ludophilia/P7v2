from app.grandpy.skills.base import basespeech
from app.grandpy import skills
from app.models import State

def answer_message(matches, user_data):

    """Construit la réponse textuelle à l'input utilisteur en fonction des mots clés qui y figurent"""

    answer = ""
    owner = user_data.get("owner")
    is_waiting_for_answers = State.query.filter_by(robot_id=owner, type="WAITING").all()

    if is_waiting_for_answers:

        for pending in is_waiting_for_answers:

            if pending.value == "HT_EVENT":

                answer += skills.play_heads_or_tails(matches, user_data, answer)

    else:

        if "hello" in matches:

            answer += skills.say_hello(answer)

        if "info" in matches and "website" in matches:
            
            answer += skills.give_website_info(answer)

        if ("play" in matches and "heads" in matches and "tails" in matches):
        
            answer += skills.play_heads_or_tails(matches, user_data, answer)

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