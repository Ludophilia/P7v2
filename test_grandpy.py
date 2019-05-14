from flask_testing import LiveServerTestCase
from app import app
from app.grandpy import requests, GrandPy
from selenium import webdriver
import time
import json

class TestGrandPy():

    def test_what_answer_message_returns(self):
        
        self.gp = GrandPy()
        
        test = {
            'gp_message': 'Bien sûr mon poussin ! La voici : 7 Cité Paradis, 75010 Paris.\n',
            'pi_location': {'lat': 48.8747265, 'lng': 2.3505517}
            }
        
        test_jsf = json.dumps(test, ensure_ascii=False, sort_keys=True)

        answer_adr = self.gp.answer_message("adresse oc connaitre")

        assert test_jsf == answer_adr