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

        ht_remaining = Memory.query.get({"robot_id": owner_ip, "object": "HT_REMAINING"})

        if ("heads" in matches) ^ ("tails" in matches):

            playerschoice = 0 if "heads" in matches else 1
            gamesresult = random.randint(0,1)
            gr_readable = ["pile", "face"][gamesresult]

            bravo, shame = speech.HT_PLAYER_VICTORY(gr_readable),speech.HT_PLAYER_DEFEAT(gr_readable)

            message += speech.HT_TOSS_COIN
            message += bravo if playerschoice == gamesresult else shame

            if ht_remaining: db.session.delete(ht_remaining)
            db.session.delete(is_waiting_for_answer)
            db.session.commit()

        else:

            if ht_remaining is None:
                
                ht_remaining = Memory(robot_id=owner_ip, object="HT_REMAINING", value=2)
                db.session.add(ht_remaining)
                db.session.commit()

            else:
                ht_remaining.value = int(ht_remaining.value) - 1
                db.session.commit()

            state_of_the_game = Memory.query.get({"robot_id": owner_ip, "object": "HT_REMAINING"})
            ht_remaining = int(state_of_the_game.value)

            if ht_remaining == 0:
                message += speech.HT_OUT_OF_TRIES

                db.session.delete(state_of_the_game)
                db.session.delete(is_waiting_for_answer)
                db.session.commit()

            else:
                message += speech.HT_ERROR(ht_remaining)

    return message