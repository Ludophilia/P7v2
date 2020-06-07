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
                
        """ Vérifie que la fonction get_anecdocte (qui s'alimente de get_wiki_info qui est ici mockée) renvoie bien la chaine de caractère demandée """

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
        anecdocte_and_url = self.gp.get_anecdocte_and_url(wiki_data_js)

        expected_anecdocte = "Mais t'ai-je déjà raconté l'histoire de ce quartier qui m'a vu en culottes courtes ? La cité Paradis est une voie publique située dans le 10e arrondissement de Paris. Elle est en forme de té, une branche débouche au 43, rue de Paradis, la deuxième au 57, rue d'Hauteville et la troisième en impasse. "
        expected_wiki_url = "[En savoir plus sur <a href='https://fr.wikipedia.org/wiki/Cité_Paradis' target='_blank'>Wikipédia</a>]"

        assert anecdocte_and_url["anecdocte"] == expected_anecdocte
        assert anecdocte_and_url["wiki_url"] == expected_wiki_url

class TestParser():

    @pytest.mark.this9
    def test_if_build_stopwords_output_the_expected_stopwords_list(self):

        pass
        
        #Implémentation modifiée

        # self.gp = GrandPy()
        # stopwords_list = self.gp.stopwords()
        # samples = ["nous-mêmes", "différentes", "ouverts", "dire", "directe", "absolument", "dit", "dite", "dits",
        # "divers", "comme", "suivantes", "ès", "dix-huit", "strictement", "rare", "dixième", "doit", "doivent"]

        # assert len(stopwords_list) >= 600 and type(stopwords_list) == type([])
        # for sample in samples: assert sample in stopwords_list

    @pytest.mark.this8
    def test_if_remove_punctuation_remove_punctuation_from_user_input(self):

        pass
        
        #Implémentation modifiée
        
        # self.gp = GrandPy()

        # test_string = self.gp.extract_keywords("  Salut????!?!,' {comment} tu vas depuis le temps!!!, vieille; branche velue? ;)            ")
        # expected_result = "Salut comment tu vas depuis le temps vieille branche velue"

        # assert test_string == expected_result and type(test_string) == type("")

    @pytest.mark.this7
    def test_if_remove_stopwords_remove_stopwords_from_user_input(self):
        
        self.gp = GrandPy()
        test_string = self.gp.extract_keywords("Salut, salut mon gros gros pote! Comment tu vas depuis le temps, vieille branche velue? ;)")
        # test_string = self.gp.remove_stopwords("Salut tu connais l'adresse d'oc")

        # expected_result = "Salut comment tu vas depuis le temps vieille branche velue "
        expected_result =['salut', 'gros', 'pote', 'temps', 'vieille', 'branche', 'velue']
        
        assert test_string == expected_result and type(test_string) == type([])
        # assert type(test_string) == type("")
        # print("DE REMOVE_STOPWORDS", test_string)

class TestGrandPy():

    @pytest.mark.this6a
    def test_what_answer_message_returns_if_the_user_says_hello_and_asks_for_OC_address(self):
        
        self.gp = GrandPy()
        
        hello_pattern = r"[Bb]onjour|[Bb]jr|[Ss]a?lu?t|[Yy]o|[Hh]i"
        expected_message = 'Bien sûr mon poussin ! La voici : 7 Cité Paradis, 75010 Paris.\n'
        
        grandpy_answer = self.gp.answer_message("salut grandpy ! Connais-tu l'adresse d'oc?")
        grandpy_message = json.loads(grandpy_answer)["message"]

        assert expected_message in grandpy_message
        assert re.search(hello_pattern, grandpy_message)

    @pytest.mark.this6b
    def test_what_answer_message_returns_if_the_user_says_nothing_interesting(self):
        
        self.gp = GrandPy()
        grandpy_answer = json.loads(self.gp.answer_message("Wow"))

        expected_answer = "Désolé, je ne sais rien faire d'autre que saluer ou donner une certaine adresse... :/"

        assert grandpy_answer['message'] == expected_answer

    @pytest.mark.this6
    def test_what_answer_message_returns_if_the_user_says_hello(self):
        
        self.gp = GrandPy()

        hello_pattern = r"[Bb]onjour|[Bb]jr|[Ss]a?lu?t|[Yy]o|[Hh]i"
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