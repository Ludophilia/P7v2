from app import app
from app.grandpy import requests, GrandPy

class TestWikimediaApiDataTreatment():

    #Objectif?

        # Vérifier que la fonction gp.answer_message("adresse oc connaitre") renvoie bien le json désiré (avec la réponse à la question, les coordonnées et la relance qui contient les infos wikipédia)

        # Vérifier que la fonction get_anecdocte (qui s'alimente de get_wiki_info qui est ici mockée) renvoie bien la chaine de caractère demandée


    def test_if_get_anecdocte_returns_the_right_string(self, monkeypatch):
        
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
        
        print(self.gp.get_anecdocte(wiki_info)) # Retirez après le test

        assert self.gp.get_anecdocte(wiki_info) == "La cité Paradis est une voie publique située dans le 10e arrondissement de Paris. Elle est en forme de té, une branche débouche au 43, rue de Paradis, la deuxième au 57, rue d'Hauteville et la troisième en impasse. [En savoir plus sur <a href='https://fr.wikipedia.org/wiki/Cité_Paradis'>Wikipédia<a>]" #En savoir plus sur Wikipédia