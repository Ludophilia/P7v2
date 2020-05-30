from app import app
from app.grandpy import requests, GrandPy
import json, pytest, re

class TestMapsApiDataTreatment():

    @pytest.mark.this2
    def test_if_get_maps_info_retrieves_the_expected_data(self):
        
        self.gp = GrandPy()

        maps_info = self.gp.get_api_data("maps") 

        assert self.gp.get_address(maps_info) == "7 Cité Paradis, 75010 Paris"

    @pytest.mark.this
    def test_if_mocked_get_address_returns_the_correct_address(self, monkeypatch):
        
        self.gp = GrandPy()

        def mocked_get_api_data(source):
            
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
            return gm_api_response

        monkeypatch.setattr(self.gp, "get_api_data", mocked_get_api_data)

        maps_info = self.gp.get_api_data("maps")

        assert self.gp.get_address(maps_info) == "7 Cité Paradis, 75010 Paris"

class TestWikimediaApiDataTreatment():
    
    @pytest.mark.this3
    def test_if_get_wiki_info_retrieves_the_expected_data(self):

        self.gp = GrandPy()

        expected_anecdocte = "La cité Paradis est une voie publique située dans le 10e arrondissement de Paris. Elle est en forme de té, une branche débouche au 43, rue de Paradis, la deuxième au 57, rue d'Hauteville et la troisième en impasse."
        expected_wiki_url = "https://fr.wikipedia.org/wiki/Cité_Paradis"

        wiki_data_js = self.gp.get_api_data("wiki")
        anecdocte_and_url = self.gp.get_anecdocte_and_wiki_url(wiki_data_js)

        assert anecdocte_and_url["url"] == expected_wiki_url
        assert anecdocte_and_url["anecdocte"] == expected_anecdocte

    @pytest.mark.this4
    def test_if_get_anecdocte_process_api_data_the_right_way(self, monkeypatch):
                
        # Vérifier que la fonction get_anecdocte (qui s'alimente de get_wiki_info qui est ici mockée) renvoie bien la chaine de caractère demandée

        self.gp = GrandPy()

        def mocked_get_api_data(source): 
        
            api_data_js = {
                "query": {
                    "pages": [
                        {
                            "title": "Cité Paradis",
                            "extract": "La cité Paradis est une voie publique située dans le 10e arrondissement de Paris.\n\n\nSituation et accès\nLa cité Paradis est une voie publique située dans le 10e arrondissement de Paris. Elle est en forme de té, une branche débouche au 43, rue de Paradis, la deuxième au 57, rue d'Hauteville et la troisième en impasse."
                        }
                    ]
                }
            }
            return api_data_js

        monkeypatch.setattr(self.gp, "get_api_data", mocked_get_api_data)

        wiki_data_js = self.gp.get_api_data("wiki")
        anecdocte_and_url = self.gp.get_anecdocte_and_wiki_url(wiki_data_js)

        expected_anecdocte = "La cité Paradis est une voie publique située dans le 10e arrondissement de Paris. Elle est en forme de té, une branche débouche au 43, rue de Paradis, la deuxième au 57, rue d'Hauteville et la troisième en impasse."
        expected_wiki_url = "https://fr.wikipedia.org/wiki/Cité_Paradis"

        assert anecdocte_and_url["url"] == expected_wiki_url
        assert anecdocte_and_url["anecdocte"] == expected_anecdocte

class TestGrandPy():

    @pytest.mark.this6
    def test_what_answer_message_returns_if_the_user_says_hello(self):
        
        self.gp = GrandPy()

        hello_pattern = r"([Bb]onjour|[Bb]jr|[Ss]a?lu?t|[Yy]o|[Hh]i)"
        grandpy_answer = json.loads(self.gp.answer_message("salut"))

        assert re.search(hello_pattern, grandpy_answer['message'])
        print("Réponse de GP:", grandpy_answer['message'])

    @pytest.mark.this5
    def test_what_answer_message_returns_if_the_user_asks_for_OC_address(self):
        
        self.gp = GrandPy()
        
        expected_answer = {
            'message': 'Bien sûr mon poussin ! La voici : 7 Cité Paradis, 75010 Paris.\n',
            'location': {'lat': 48.8748465, 'lng': 2.3504873}, #lat 48.8747265 et lng ont changé 2.3505517
            'anecdocte_and_url' : {"anecdocte": "La cité Paradis est une voie publique située dans le 10e arrondissement de Paris. Elle est en forme de té, une branche débouche au 43, rue de Paradis, la deuxième au 57, rue d'Hauteville et la troisième en impasse.",
            "url": "https://fr.wikipedia.org/wiki/Cité_Paradis"}
            }
        
        expected_answer_js = json.dumps(expected_answer, ensure_ascii=False, sort_keys=True)

        grandpy_answer = self.gp.answer_message("adresse oc connaitre")

        assert expected_answer_js == grandpy_answer