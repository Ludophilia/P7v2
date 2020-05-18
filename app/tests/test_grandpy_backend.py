from app import app
from app.grandpy import requests, GrandPy
import json, pytest

class TestMapsApiDataTreatment():

    @pytest.mark.this2
    def test_if_get_maps_info_retrieves_the_expected_data(self):
        
        self.gp = GrandPy()

        maps_info = self.gp.get_maps_info() 

        assert self.gp.get_address(maps_info) == "7 Cité Paradis, 75010 Paris"

    @pytest.mark.that
    def test_if_mocked_get_address_returns_the_correct_address(self, monkeypatch):
        
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

class TestWikimediaApiData():

    #Objectif?

        # Vérifier que la fonction gp.answer_message("adresse oc connaitre") renvoie bien le json désiré (avec la réponse à la question, les coordonnées et la relance qui contient les infos wikipédia)
    
    @pytest.mark.this3
    def test_if_get_wiki_info_retrieves_the_expected_data(self):

        # Vérifier que la fonction wiki_info renvoie bien ce qui est attendu.

        self.gp = GrandPy()

        expected_wikimedia_api_response = {
            "parse": {
                "title": "Cité Paradis",
                "pageid": 5653202,
                "wikitext": {
                    "*": "== Situation et accès ==\nLa cité Paradis est une voie publique située dans le [[10e arrondissement de Paris|{{10e|arrondissement}}]] de [[Paris]]. Elle est en forme de [[wikt:té|té]], une branche débouche au 43, [[rue de Paradis]], la deuxième au 57, [[rue d'Hauteville]] et la troisième en impasse.\n\n<gallery mode=\"packed\" caption=\"Vues de la cité\" heights=\"150\">\nFile:P1290748 Paris X cite Paradis detail rwk.jpg\nFile:P1290749 Paris X cite Paradis rwk.jpg\n</gallery>\n\nCe site est desservi par les lignes {{Métro de Paris/correspondances avec intitulé|8|9}} à la [[Liste des stations du métro de Paris|station de métro]] [[Bonne-Nouvelle (métro de Paris)|''Bonne-Nouvelle'']] et par la ligne {{Métro de Paris/correspondances avec intitulé|7}} à la station [[Poissonnière (métro de Paris)|''Poissonnière'']]."
                        }
                }
            }
        
        assert self.gp.get_wiki_info() == expected_wikimedia_api_response

    def test_if_get_anecdocte_process_api_data_the_right_wiki(self, monkeypatch):
                
        # Vérifier que la fonction get_anecdocte (qui s'alimente de get_wiki_info qui est ici mockée) renvoie bien la chaine de caractère demandée

        self.gp = GrandPy()
        
        wikimedia_api_response = {
            "parse": {
                "title": "Cité Paradis",
                "pageid": 5653202,
                "wikitext": {
                    "*": "== Situation et accès ==\nLa cité Paradis est une voie publique située dans le [[10e arrondissement de Paris|{{10e|arrondissement}}]] de [[Paris]]. Elle est en forme de [[wikt:té|té]], une branche débouche au 43, [[rue de Paradis]], la deuxième au 57, [[rue d'Hauteville]] et la troisième en impasse.\n\n<gallery mode=\"packed\" caption=\"Vues de la cité\" heights=\"150\">\nFile:P1290748 Paris X cite Paradis detail rwk.jpg\nFile:P1290749 Paris X cite Paradis rwk.jpg\n</gallery>\n\nCe site est desservi par les lignes {{Métro de Paris/correspondances avec intitulé|8|9}} à la [[Liste des stations du métro de Paris|station de métro]] [[Bonne-Nouvelle (métro de Paris)|''Bonne-Nouvelle'']] et par la ligne {{Métro de Paris/correspondances avec intitulé|7}} à la station [[Poissonnière (métro de Paris)|''Poissonnière'']]."
                        }
                }
            }

        def mock_wm_api_response(): 
            return wikimedia_api_response

        monkeypatch.setattr(self.gp, "get_wiki_info", mock_wm_api_response)

        wiki_info = self.gp.get_wiki_info()
        
        assert self.gp.get_anecdocte(wiki_info) == {
            "anecdocte": "La cité Paradis est une voie publique située dans le 10e arrondissement de Paris. Elle est en forme de té, une branche débouche au 43, rue de Paradis, la deuxième au 57, rue d'Hauteville et la troisième en impasse.",
            "url": "https://fr.wikipedia.org/wiki/Cité_Paradis"
        }

class TestGrandPy():

    def test_what_answer_message_returns_if_the_user_asks_for_OC_address(self):
        
        self.gp = GrandPy()
        
        expected_answer = {
            'gp_message': 'Bien sûr mon poussin ! La voici : 7 Cité Paradis, 75010 Paris.\n',
            'pi_location': {'lat': 48.8748465, 'lng': 2.3504873}, #lat 48.8747265 et lng ont changé 2.3505517
            'pi_anecdocte' : {"anecdocte": "La cité Paradis est une voie publique située dans le 10e arrondissement de Paris. Elle est en forme de té, une branche débouche au 43, rue de Paradis, la deuxième au 57, rue d'Hauteville et la troisième en impasse.",
            "url": "https://fr.wikipedia.org/wiki/Cité_Paradis"}
            }
        
        expected_answer_js = json.dumps(expected_answer, ensure_ascii=False, sort_keys=True)

        grandpy_answer = self.gp.answer_message("adresse oc connaitre")

        assert expected_answer_js == grandpy_answer