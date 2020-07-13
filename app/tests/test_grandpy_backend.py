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
        anecdocte = self.gp.get_anecdocte(wiki_data_js)

        expected_anecdocte = "Mais t'ai-je déjà raconté l'histoire de ce quartier qui m'a vu en culottes courtes ? La cité Paradis est une voie publique située dans le 10e arrondissement de Paris. Elle est en forme de té, une branche débouche au 43, rue de Paradis, la deuxième au 57, rue d'Hauteville et la troisième en impasse. "
        expected_wiki_url = "[En savoir plus sur <a href='https://fr.wikipedia.org/wiki/Cité_Paradis' target='_blank'>Wikipédia</a>]"

        assert anecdocte == f"{expected_anecdocte}{expected_wiki_url}"

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

    @pytest.mark.testgp1
    def test_what_answer_message_returns_if_the_user_says_hello_and_asks_for_OC_address(self):
        
        self.gp = GrandPy()
        
        hello_pattern = r"[Bb]onjour|[Bb]jr|[Ss]a?lu?t|[Yy]o|[Hh]i"
        expected_message = 'Bien sûr mon poussin ! La voici : 7 Cité Paradis, 75010 Paris.\n'
        
        grandpy_answer = self.gp.answer_message("salut grandpy ! Connais-tu l'adresse d'oc?")
        grandpy_message = json.loads(grandpy_answer)["message"]

        assert expected_message in grandpy_message
        assert re.search(hello_pattern, grandpy_message)

    @pytest.mark.testgp2
    def test_what_answer_message_returns_if_the_user_says_nothing_interesting(self):
        
        self.gp = GrandPy()
        grandpy_answer = json.loads(self.gp.answer_message("Wow"))

        expected_answer = "Désolé, je ne sais rien faire d'autre que saluer ou donner une certaine adresse... :/"

        assert grandpy_answer['message'] == expected_answer

    @pytest.mark.testgp3
    def test_what_answer_message_returns_if_the_user_says_hello(self):
        
        self.gp = GrandPy()

        hello_pattern = r"[Bb]onjour|[Bb]jr|[Ss]a?lu?t|[Yy]o|[Hh]i"
        grandpy_answer = json.loads(self.gp.answer_message("salut"))

        assert re.search(hello_pattern, grandpy_answer['message'])
        print("Réponse de GP:", grandpy_answer['message'])

    @pytest.mark.testgp4
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

    @pytest.mark.testgp5
    def test_what_answer_message_returns_if_the_user_asks_how_grandpy_is_doing(self):

        # expected_answer = {
        #     'message': 'Bien sûr mon poussin ! La voici : 7 Cité Paradis, 75010 Paris.\n',
        #     }
        
        # expected_answer_js = json.dumps(expected_answer, ensure_ascii=False, sort_keys=True)

        KNOWMORE = lambda source, url: f"[En savoir plus sur <a href='{url}' target='_blank'>{source}</a>]"
        
        EXP_STATE_OF_MIND = [
            "Le Lundi, ça ne va jamais très fort n'est-ce pas 🥱 ? Après le week-end, la reprise ! Mais faut se reprendre 💪",
            "Ça va ça va... 😐 Un Mardi comme les autres.",
            "Correct ! 😺 Mercredi... Il doit y avoir des sorties ciné aujourd'hui ! 🎦🍿",
            f"Oui ! Savais-tu que dans le temps 👴, dans les années 60 et au début 70, le jeudi était une journée libre pour les enfants ? Maintenant c'est le Mercredi, et encore ça dépend {KNOWMORE('Wikipédia', 'https://fr.wikipedia.org/wiki/Rythmes_scolaires_en_France')}. Que le temps passe vite !😔",
            "Oh déjà Vendredi 😱! Bientôt le week-end 😺! À part ça ça va bien !",
            "Oui ! C'est Samedi ! J'espère que tu t'en protites bien 😎! ",
            "Ça va ! C'est Dimanche, mais pour nous les 🤖, pas de repit ! 🦾"
        ]

        self.gp = GrandPy()

        grandpy_answer = lambda message: json.loads(self.gp.answer_message(message))["message"]

        assert grandpy_answer("Comment ça va ?") in EXP_STATE_OF_MIND
        assert grandpy_answer("Comment va ?") in EXP_STATE_OF_MIND
        assert grandpy_answer("comment vas-tu ?") in EXP_STATE_OF_MIND
        assert grandpy_answer("comment tu vas ???") in EXP_STATE_OF_MIND
        assert grandpy_answer("Comment allez vous ?") in EXP_STATE_OF_MIND

        assert grandpy_answer("comment vas-tu à la boulangerie d'à côté") not in EXP_STATE_OF_MIND
        assert grandpy_answer("Comment allez vous à la piscine municipale ?") not in EXP_STATE_OF_MIND

        #print(grandpy_answer("comment vas-tu ?"))

class TestGrandPyAutoResponses():

    @pytest.mark.testgpau1
    def test_if_give_footer_info_returns_the_expected_string(self):
        
        expected_answer = """
        <div id='footer-notes'>
            2019, 2020 — Créé par Jeffrey G.<br/>pour OpenClassrooms
        </div>
        <div>
            <a href="https://github.com/Ludophilia/P7v2" target="_blank">
                <img src="{{ url_for('static', filename='img/GitHub-Mark-Light-32px.png') }}" alt="Octocat" width="25" height="25"/>
            </a>
        </div>
        """
        gp = GrandPy()

        assert gp.give_footer_info() == expected_answer

    @pytest.mark.testgpau2
    def test_if_start_conversation_returns_the_expected_string(self):
        
        expected_answer = """<span>Salut 👋, qu'est-ce que je peux faire pour toi ?<br><br>
        Tu peux me demander:<br>
        - L'adresse d'OpenClassrooms (ex: "tu connais l'adresse d'OC ?")<br>
        - Quelle heure il est<br>
        - Quel temps il fait aujourd'hui<br>
        <br>
        ...Ou tout simplement me saluer ou me demander comment je vais, ça fait toujours plaisir !
        </span>
        """
       
        gp = GrandPy()

        # start_conversation = re.sub(r"\t+", " ", gp.start_conversation()).strip()
        # expected_answer = re.sub(r"\t+",  " ", expected_answer)

        # start_conversation = re.sub(r"\s+", " ", gp.start_conversation()).strip()
        # expected_answer = re.sub(r"\s+",  " ", expected_answer)

        assert expected_answer == gp.start_conversation()