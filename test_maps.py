from flask_testing import LiveServerTestCase
from app import app
from app.grandpy import requests, GrandPy
from selenium import webdriver
import time


class TestMaps():

    def setUp(self): 
        self.gp = GrandPy()

    def test_if_maps_returns_the_adress(self, monkeypatch): #Qu'est ce que je cherche à tester ? 

        result = {
            "html_attributions": [],
            "results": [
                {
                    "formatted_address": "7 Cité Paradis, 75010 Paris, France",
                    "geometry": {
                        "location": {
                            "lat": 48.8747265,
                            "lng": 2.3505517
                        }
                    },
                    "name": "Openclassrooms",
                }
            ]
        }

        def mockreturn(request): #sans (request) parameter
            return result
        
        monkeypatch.setattr(gp, "get_adress", mockreturn) # Hypothèse : monkeypatch.setattr() redirige la fonction la fonction. EN revanche, c'est quoi ce "get"... Un "attribut" (plus une méthode) de requests. #Ce n'est pas ça...

        assert self.gp.get_adress() == "7 Cité Paradis, 75010 Paris, France" #Que voulez-vous tester ? Adresse récupée par grandpy est égale à "7 Cité Paradis, 75010 Paris, France"

        # Normalement, on est censé récupérer le json via requests.json. 