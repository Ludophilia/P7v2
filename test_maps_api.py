from app import app
from app.grandpy import requests, GrandPy

class TestMapsApiDataTreatment():

    def test_if_get_address_returns_the_correct_address(self, monkeypatch):
        
        self.gp = GrandPy()
        
        gm_api_response = {
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

        def mock_gm_api_response():
            return gm_api_response

        monkeypatch.setattr(self.gp, "get_maps_info", mock_gm_api_response)

        maps_info = self.gp.get_maps_info() 

        assert self.gp.get_address(maps_info) == "7 Cité Paradis, 75010 Paris"