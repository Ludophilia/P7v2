import json

import pytest
from flask_testing import TestCase

from app import app
from app.models import db, Robot, State, Memory
from app.tests.backend.testtools import TestTools as Tools 
import config_tests as config

@pytest.mark.gpht #31/07/20 - OK
class TestHeadsTails(TestCase):

    def create_app(self):
        app.config.from_object(config)
        return app

    def setUp(self):
        print("Setting the game Up...")
        db.create_all()
        db.session.add(Robot(id=f"127.0.0.1"))
        db.session.commit()
    
    def tearDown(self):
        print("tearing it Down...")
        db.drop_all()

    @pytest.mark.gpht1
    def test_a_game_of_heads_or_tails(self):

        for choice in ["Pile", "pile", "Face", "face"]:
        
            actual_answer1 = Tools().ask_grandpy("Jouons à pile ou face")
            expected_answer1 = "OK ! Je tire une pièce au hasard, devine le résultat !Pile ou face ?"
            new_state = State.query.get({"robot_id": "127.0.0.1", "type": "WAITING", "value":"HT_EVENT"})

            assert actual_answer1 == expected_answer1
            assert new_state is not None

            actual_answer2 = Tools().ask_grandpy(choice) # self.send_and_unwrap(self.wrap_message(props))

            hresults = [f"BRAVO ! La réponse est bien {gr_readable}, tu as gagné 🎊!" for gr_readable in ["pile", "face"]]
            tresults = [f"PERDU 🤡! La réponse est {gr_readable} ! Une prochaine fois peut-être !" for gr_readable in ["pile", "face"]]
            expected_answer2 = ["Je lance la pièce et..." + result for result in hresults + tresults]

            state = State.query.get({"robot_id": "127.0.0.1", "type": "WAITING", "value":"HT_EVENT"})

            assert actual_answer2 in expected_answer2
            assert state is None

    @pytest.mark.gpht2
    def test_how_a_game_of_heads_or_tails_that_goes_wrong_is_handled_by_grandpy(self):
        
        Tools().ask_grandpy("jouons à pile ou face")

        for message, error_time in [("pile et face lol", 2), ("pile et face !!", 1), ("je persiste: pile ET face", 0)]:

            try_again = f"Désolé, je n'ai pas compris ta réponse. Peux-tu recommencer ?Il te reste {error_time} essai{'s' if error_time > 1 else ''} !!Pile ou face ?"
            too_bad = "Désolé, tu as épuisé tes essais ! Le jeu pile ou face est terminé ! À une prochaine fois peut-être 🎲!"
            expected_answer = try_again if error_time > 0 else too_bad

            actual_answer = Tools().ask_grandpy(message)
            ht_error = Memory.query.get({'robot_id': '127.0.0.1', 'object': 'HT_REMAINING'})
            isWaitingForAnAnswer = State.query.get({'robot_id': '127.0.0.1', 'type': 'WAITING', 'value': 'HT_EVENT'})

            assert actual_answer == expected_answer
            assert int(ht_error.value) == error_time if error_time > 0 else ht_error is None
            if error_time == 0: assert isWaitingForAnAnswer is None
