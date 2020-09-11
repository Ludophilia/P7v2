import random

from app.grandpy.skills.heads_tails import speech
from app.models import db, State, Memory

def play_heads_or_tails(matches, user_data, message):

    """Gère tout ce qui a à voir avec le jeu pile ou face proposé par grandpy. Retourne le paramètre message modifié."""

    owner_ip = user_data.get("owner")
    is_waiting_for_answer = State.query.get({"robot_id": owner_ip, "type": "WAITING", "value":'HT_EVENT'})

    if "play" in matches and is_waiting_for_answer is None:

        waiting_st = State(robot_id=user_data.get("owner"), type="WAITING", value="HT_EVENT")
        db.session.add(waiting_st)
        db.session.commit()

        message += speech.HT_EXPLAIN_RULES

    elif is_waiting_for_answer:

        ht_error = Memory.query.get({"robot_id": owner_ip, "object": "HT_ERROR"})

        if ("heads" in matches) ^ ("tails" in matches):

            playerschoice = 0 if "heads" in matches else 1
            gamesresult = random.randint(0,1)
            gr_readable = ["pile", "face"][gamesresult]

            bravo, shame = speech.HT_PLAYER_VICTORY(gr_readable),speech.HT_PLAYER_DEFEAT(gr_readable)

            message += speech.HT_TOSS_COIN
            message += bravo if playerschoice == gamesresult else shame

            if ht_error: db.session.delete(ht_error)
            db.session.delete(is_waiting_for_answer)
            db.session.commit()

        else:

            if ht_error is None:
                
                new_ht_error = Memory(robot_id=owner_ip, object="HT_ERROR", value=1)
                db.session.add(new_ht_error)
                db.session.commit()

            else:
                ht_error.value = int(ht_error.value) + 1
                db.session.commit()

            ht_error = Memory.query.get({"robot_id": owner_ip, "object": "HT_ERROR"})
            remaining = 3 - int(ht_error.value)

            if remaining == 0:
                message += speech.HT_OUT_OF_TRIES

                db.session.delete(ht_error)
                db.session.delete(is_waiting_for_answer)
                db.session.commit()

            else:
                message += speech.HT_ERROR(remaining)

    return message