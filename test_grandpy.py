from app import app
from app.grandpy import requests, GrandPy
import json

class TestGrandPy():

    def test_what_answer_message_returns_if_the_user_asks_for_OC_address(self):
        
        self.gp = GrandPy()
        
        expected_answer = {
            'gp_message': 'Bien sûr mon poussin ! La voici : 7 Cité Paradis, 75010 Paris.\n',
            'pi_location': {'lat': 48.8747265, 'lng': 2.3505517}
            }
        
        expected_answer_js = json.dumps(expected_answer, ensure_ascii=False, sort_keys=True)

        answer_adr = self.gp.answer_message("adresse oc connaitre")

        assert expected_answer_js == answer_adr