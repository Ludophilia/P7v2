from app import app
from app.grandpy import requests, GrandPy
import json

class TestGrandPy():

    def test_what_answer_message_returns_if_the_user_asks_for_OC_address(self):
        
        self.gp = GrandPy()
        
        expected_answer = {
            'gp_message': 'Bien sûr mon poussin ! La voici : 7 Cité Paradis, 75010 Paris.\n',
            'pi_location': {'lat': 48.8747265, 'lng': 2.3505517},
            'pi_anecdocte' : "La cité Paradis est une voie publique située dans le 10e arrondissement de Paris. Elle est en forme de té, une branche débouche au 43, rue de Paradis, la deuxième au 57, rue d'Hauteville et la troisième en impasse. [En savoir plus sur <a href='https://fr.wikipedia.org/wiki/Cité_Paradis'>Wikipédia<a>]"
            }
        
        expected_answer_js = json.dumps(expected_answer, ensure_ascii=False, sort_keys=True)

        grandpy_answer = self.gp.answer_message("adresse oc connaitre")

        assert expected_answer_js == grandpy_answer