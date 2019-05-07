from flask_testing import LiveServerTestCase
from app import app
from app.grandpy import requests, GrandPy
from selenium import webdriver
import time


class TestMaps():

    def test_if_maps_returns_the_adress(self, monkeypatch):
        
        self.gp = GrandPy()
        
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

        def mockreturn(): #sans (request) parameter
            return result

        monkeypatch.setattr(self.gp, "get_maps_info", mockreturn)

        maps_info = self.gp.get_maps_info()

        assert self.gp.get_address(maps_info) == "7 Cité Paradis, 75010 Paris"