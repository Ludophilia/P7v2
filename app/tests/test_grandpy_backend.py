from app import app
from app.grandpy import requests, GrandPy
import json, pytest, re, time, math

class TestTools():

    def setup_method(self):
        self.gp = GrandPy()

    def teardown_method(self):
        pass

    def wrap_message(self, message, options={}): 
        return {"user_message": message, "options": options}

    def send_and_unwrap(self, message, key="message"):

        message_formatted = json.loads(self.gp.answer_message(message)).get(key)

        return message_formatted if key == "location" else message_formatted.replace("<span>", "").replace("</span>", "").replace("<br>", "")
    
    def get_fake_weather_data(self, user_location):

        round = lambda x: math.ceil(x) if x - math.floor(x) > 0.5 else math.floor(x)

        if not user_location: return None

        current_f = {
            "weather": [{
                "description": "couvert",
                "icon": "04d"
            }],
            "main": {
                "temp": 21.94,
                "feels_like": 18.89,
                "temp_min": 21,
                "temp_max": 24.44,
                "humidity": 40
            },
            "name": "Paris"            
        }

        daily_f = {
            "daily": [
                {"temp": {
                    "min": 21,
                    "max": 24.44,
                }}
            ]
        }

        forecast = {**current_f, **daily_f}

        fake_weather_data = dict(
            tcur = round(forecast["main"]["temp"]),
            city = forecast["name"],
            description = forecast["weather"][0]["description"],
            icon = forecast["weather"][0]["icon"],
            tmin = round(forecast["daily"][0]["temp"]["min"]),
            tmax = round(forecast["daily"][0]["temp"]["max"])
        )

        return fake_weather_data

    def get_fake_api_data(self, api_name):
        
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

        wiki_api_response = {
            "query": {
                "pages": [
                    {
                        "title": "Cité Paradis",
                        "extract": "La cité Paradis est une voie publique située dans le 10e arrondissement de Paris.\n\n\nSituation et accès\nLa cité Paradis est une voie publique située dans le 10e arrondissement de Paris. Elle est en forme de té, une branche débouche au 43, rue de Paradis, la deuxième au 57, rue d'Hauteville et la troisième en impasse."
                    }
                ]
            }
        }
        return gm_api_response if api_name == "maps" else wiki_api_response

class TestParser:

    @pytest.mark.tprs1
    def test_if_build_stopwords_output_the_expected_stopwords_list(self):

        pass
        
        #Implémentation modifiée

        # self.gp = GrandPy()
        # stopwords_list = self.gp.stopwords()
        # samples = ["nous-mêmes", "différentes", "ouverts", "dire", "directe", "absolument", "dit", "dite", "dits",
        # "divers", "comme", "suivantes", "ès", "dix-huit", "strictement", "rare", "dixième", "doit", "doivent"]

        # assert len(stopwords_list) >= 600 and type(stopwords_list) == type([])
        # for sample in samples: assert sample in stopwords_list

    @pytest.mark.tprs2
    def test_if_remove_punctuation_remove_punctuation_from_user_input(self):
        pass
        
        #Implémentation modifiée
        
        # self.gp = GrandPy()

        # test_string = self.gp.extract_keywords("  Salut????!?!,' {comment} tu vas depuis le temps!!!, vieille; branche velue? ;)            ")
        # expected_result = "Salut comment tu vas depuis le temps vieille branche velue"

        # assert test_string == expected_result and type(test_string) == type("")

    @pytest.mark.tprs3
    def test_if_remove_stopwords_remove_stopwords_from_user_input(self):
        pass
        
        # self.gp = GrandPy()
        # test_string = self.gp.extract_keywords("Salut, salut mon gros gros pote! Comment tu vas depuis le temps, vieille branche velue? ;)")
        # # test_string = self.gp.remove_stopwords("Salut tu connais l'adresse d'oc")

        # # expected_result = "Salut comment tu vas depuis le temps vieille branche velue "
        # expected_result =['salut', 'gros', 'pote', 'temps', 'vieille', 'branche', 'velue']
        
        # assert test_string == expected_result and type(test_string) == type([])
        # # assert type(test_string) == type("")
        # # print("DE REMOVE_STOPWORDS", test_string)

    @pytest.mark.tprs4
    def test_what_extract_keywords_do(self):
        pass
        # self.gp = GrandPy()

        # print(self.gp.extract_keywords("tu connais l'adresse d'oc?"))

@pytest.mark.gppr
class TestPatternRecognition(TestTools):
    
    @pytest.mark.gppr1
    def test_what_patterns_is_recognized_when_user_ask_for_the_time(self):

        keywords = "\n".join(["quelle", "heure", "?"])
        matches = self.gp.search_patterns(keywords)
        print(matches)
        
        for item in matches:
            assert item in ["what", "time", "question"]

@pytest.mark.gpgmg #31/07/20 - OK
class TestGrandPyGaming(TestTools):

    @pytest.mark.gpgmg1
    def test_a_game_of_heads_or_tails(self):

        for props in ["Pile", "pile", "Face", "face"]:
        
            actual_answer1 = self.send_and_unwrap(self.wrap_message("Jouons à pile ou face"))
            expected_answer1 = "OK ! Je tire une pièce au hasard, devine le résultat !Pile ou face ?"

            assert actual_answer1 == expected_answer1
            assert "#HT" in self.gp.isWaitingForAnAnswer

            actual_answer2 = self.send_and_unwrap(self.wrap_message(props))
            ht_results = [f"BRAVO ! La réponse est bien {gr_readable}, tu as gagné 🎊!" for gr_readable in ["pile", "face"]] + [
                f"PERDU 🤡! La réponse est {gr_readable} ! Une prochaine fois peut-être !" for gr_readable in ["pile", "face"]]
            expected_answer2 = [
                "Je lance la pièce et..." + result for result in ht_results 
            ]

            assert actual_answer2 in expected_answer2
            assert "#HT" not in self.gp.isWaitingForAnAnswer

    @pytest.mark.gpgmg2
    def test_how_a_game_of_heads_or_tails_that_goes_wrong_is_handled_by_grandpy(self):
        
        #Déclenche le jeu
        self.send_and_unwrap(self.wrap_message("jouons à pile ou face"))

        for message, error_time in [("pile et face lol", 1), ("pile et face !!", 2), ("je persiste: pile ET face", 3)]:

            try_again = f"Désolé, je n'ai pas compris ta réponse. Peux-tu recommencer ? Il te reste {3-error_time} essai{'s' if error_time < 2 else ''} !!Pile ou face ?"
            too_bad = "Désolé, tu as épuisé tes essais ! Le jeu pile ou face est terminé ! À une prochaine fois peut-être 🎲!"
            expected_answer = try_again if error_time < 3 else too_bad

            actual_answer = self.send_and_unwrap(self.wrap_message(message))

            assert actual_answer == expected_answer
            assert self.gp.memory.get("HT_ERROR") == error_time if error_time < 3 else self.gp.memory.get("HT_ERROR") == None
            if error_time == 3: assert "#HT" not in self.gp.isWaitingForAnAnswer

@pytest.mark.gpansmu #31/07/20 - OK
class TestGrandPyAnswerToMultipleQuestions(TestTools):

    @pytest.mark.gpansmu1
    def test_what_answer_message_returns_if_the_user_says_hello_and_asks_for_OC_address(self, monkeypatch):

        monkeypatch.setattr(self.gp, "get_api_data", self.get_fake_api_data)
        hello_pattern = r"Bonjour!|Salut!|Yo!|Hi!!|👋"

        actual_message = self.send_and_unwrap(self.wrap_message("salut grandpy ! Connais-tu l'adresse d'oc?"))
        expected_message = "Bien sûr mon poussin ! La voici : \"7 Cité Paradis, 75010 Paris\".  Et voilà une carte pour t'aider en plus !!"

        assert re.search(hello_pattern, actual_message)
        assert expected_message in actual_message

@pytest.mark.gpans #31/07/20 - OK
class TestGrandPyAnswerToASingleQuestion(TestTools):
    
    @pytest.mark.gpans1
    def test_what_answer_message_returns_if_the_user_says_nothing_interesting(self):
                        
        actual_message = self.send_and_unwrap(self.wrap_message("ONE MORE DOG REJECTED"))

        expected_answer = "Désolé, je n'ai pas compris ton message... 😕 Dans une prochaine version peut-être ?"

        assert actual_message == expected_answer

    @pytest.mark.gpans2
    def test_what_answer_message_returns_if_the_user_says_hello(self):
        
        hello_pattern = r"Bonjour!|Salut!|Yo!|Hi!!|👋"

        messages = ["slt", "salut", "Bonjour", "Salutations", "👋", "Yo !!"]

        for m in messages: 
            message = self.send_and_unwrap(self.wrap_message(m))
            assert re.search(hello_pattern, message)

    @pytest.mark.gpans3
    def test_what_answer_message_returns_if_the_user_asks_for_OC_address(self, monkeypatch):
        
        monkeypatch.setattr(self.gp, "get_api_data", self.get_fake_api_data)

        message_data = self.wrap_message("adresse oc connaitre")

        actual_message = self.send_and_unwrap(message_data)
        actual_coordinates = self.send_and_unwrap(message_data, "location")
        actual_anecdocte = self.send_and_unwrap(message_data, "anecdocte")

        expected_message = "Bien sûr mon poussin ! La voici : \"7 Cité Paradis, 75010 Paris\".  Et voilà une carte pour t'aider en plus !!"
        expected_coordinates = {'lat': 48.8747265, 'lng': 2.3505517} # From MOCK API DATA.
        expected_anecdocte = "Mais t'ai-je déjà raconté l'histoire de ce quartier qui m'a vu en culottes courtes ? La cité Paradis est une voie publique située dans le 10e arrondissement de Paris. Elle est en forme de té, une branche débouche au 43, rue de Paradis, la deuxième au 57, rue d'Hauteville et la troisième en impasse. [En savoir plus sur <a href='https://fr.wikipedia.org/wiki/Cité_Paradis' target='_blank'>Wikipédia</a>]"

        assert expected_message == actual_message
        assert expected_coordinates == actual_coordinates
        assert expected_anecdocte == actual_anecdocte

    @pytest.mark.gpans4
    def test_what_answer_message_returns_if_the_user_asks_how_grandpy_is_doing(self):

        KNOWMORE = lambda source, url: f"[En savoir plus sur <a href='{url}' target='_blank'>{source}</a>]"
        
        EXP_STATE_OF_MIND = [
            "Le Lundi, ça ne va jamais très fort n'est-ce pas 🥱 ? Mais faut se reprendre !! 💪",
            "Ça va ça va... Un Mardi comme les autres. 😐",
            "Correct ! Mercredi... Il doit y avoir des sorties ciné aujourd'hui ! 🎦🍿",
            f"Ça va ! Ça va ! Savais-tu que dans le temps 👴, dans les années 60 et au début 70, le jeudi était une journée libre pour les enfants ? Maintenant c'est le Mercredi, et encore ça dépend {KNOWMORE('Wikipédia', 'https://fr.wikipedia.org/wiki/Rythmes_scolaires_en_France')}. Que le temps passe vite ! 😔",
            "Oh déjà Vendredi ! Bientôt le week-end ! 😺 À part ça ça va bien !",
            "Bien ! C'est Samedi ! J'espère que tu t'en protites bien ! 😎",
            "Ça va ! C'est Dimanche, mais pour nous les 🤖, pas de repit ! 🦾"
        ]

        messages = [
            "Comment ça va ?", "ça va ?", "ca va ?", "Comment va ?", "comment vas-tu ?", 
            "comment tu vas ???", "Comment allez vous ?"
        ]

        misleading_messages = [
            "comment vas-tu à la boulangerie d'à côté", "Comment allez vous à la piscine municipale ?"
        ]    

        for message in [*messages, *misleading_messages]:
            if message in messages:
                assert self.send_and_unwrap(self.wrap_message(message)) in EXP_STATE_OF_MIND
            else:
                assert self.send_and_unwrap(self.wrap_message(message)) not in EXP_STATE_OF_MIND

    @pytest.mark.gpans5
    def test_if_grandpy_replies_as_expected_when_asked_for_the_time(self):
        
        current_time = time.strftime("%H:%M")
        expected_answer = f"🕗 Il est {current_time} !!"

        messages = [
            "il est quelle heure ?", "quelle heure est-il ?", "tu as l'heure ?", "Quelle heure il est"
        ]

        for message in messages:
            assert self.send_and_unwrap(self.wrap_message(message, {'timezone': 2})) == expected_answer

    @pytest.mark.gpans6
    def test_if_grandpy_replies_as_expected_when_asked_for_the_weather(self, monkeypatch):

        monkeypatch.setattr(self.gp, "get_weather_data", self.get_fake_weather_data)

        expected_answer = f"<img src='https://openweathermap.org/img/wn/04d.png' alt='weather-icon' width='25' height='25'>Il fait actuellement 22°C à Paris. Les températures min et max pour le reste de la journée seront respectivement de 21°C et 24°C."
        expected_unexpected_answer = f"Désolé, impossible de te donner la météo. As-tu bien accepté que je te géolocalise quand je te l'ai demandé ? 🤔"

        options1 = {"location": {"latitude": 48.896, "longitude": 2.32}}
        options2 = {"location": None} 

        questions = ["Quel temps il fait ?", "Quel temps fait-il ?", "quel temps ?", "quel temps aujourd'hui ?"]

        for question in questions:
            assert self.send_and_unwrap(self.wrap_message(f"{question}", options1)) == expected_answer
            assert self.send_and_unwrap(self.wrap_message(f"{question}", options2)) == expected_unexpected_answer

    @pytest.mark.gpans7
    def test_if_grandpy_replies_as_expected_when_asked_for_infos_bout_the_app(self):

        project_glink = """
        <span id="footer_sns">
            <a href="https://github.com/Ludophilia/P7v2" target="_blank">
                <img src="static/img/GitHub-Mark-Light-32px.png" alt="Octocat" width="25" height="25"/>
            </a>
        </span>
        """

        SITE_INFO = lambda link : f"Bien sûr ! Cette app web est la concrétisation d'un des projets à réaliser dans le cadre d'un des parcours \"développeur d'application\" proposé par OpenClassrooms.<br><br>En fait, il s'agit même de sa 2ème version, vu que la 1ère, des mots de Jeffrey G, son auteur, était \"un peu de la merde\".<br><br>D'un point de vue technique, côté frontend , l'app est construite avec le combo HTML5 + CSS3 + JS, sans l'aide d'un framework. Côté backend, est utilisé exclusivement Python3 avec le framework Flask.<br><br>Si ça t'intéresse davantage, je t'invite à te rendre sur {link}, tu en apprendras sans doute plus !"

        message = "Puis-je avoir des infos sur ce site ?"

        actual_message = json.loads(self.gp.answer_message(self.wrap_message(message))).get("message")
        expected_message = SITE_INFO(project_glink)
        
        assert actual_message == expected_message
        
@pytest.mark.gpau #31/07/20 - OK
class TestGrandPyAutoResponses(TestTools):

    @pytest.mark.gpau2
    def test_if_start_conversation_returns_the_expected_string(self):
        
        expected_answer = """<span>Salut 👋, qu'est-ce que je peux faire pour toi ?<br><br>
        Tu peux me demander, dans le formulaire juste en bas avec 'Nouveau message' écrit dedans :<br><br>
        - "Tu connais l'adresse d'OpenClassrooms ?" pour obtenir l'adresse d'Openclassrooms 🏫 !<br>
        - "Quel temps fait-il ?" pour obtenir la météo ⛅️ de ton lieu (📍localisation nécessaire) !<br>
        - "Quelle heure il est ?" pour obtenir l'heure 🕓 qu'il est !<br>
        - "Jouons à pile ou face" si tu veux jouer au jeu du même nom 🎲 !<br>
        - "T'as des infos sur ce site ?" pour obtenir des infos sur ce site 📁 !<br>
        <br>
        Sinon, tu peux toujours m'envoyer un "salut" ou une "👋" pour me saluer 👋 ou me demander "comment tu vas" pour prendre des nouvelles 🍺, ça fait toujours plaisir !
        </span>"""
       
        assert expected_answer == self.gp.start_conversation()

@pytest.mark.gpapi #31/07/20 - OK
class TestApiDataReception(TestTools):

    @pytest.mark.gpapi1
    def test_if_get_maps_info_retrieves_the_expected_data(self):
        
        get_address = lambda maps_data: maps_data["results"][0]["formatted_address"].replace(", France", "") 
        maps_data = self.gp.get_location_data("maps")

        assert get_address(maps_data) == "7 Cité Paradis, 75010 Paris"
    
    @pytest.mark.gpapi2
    def test_if_get_wiki_info_retrieves_the_expected_data(self):

        extract_anecdocte = lambda wiki_data: wiki_data["query"]["pages"][0]["extract"].split('\n')[-1]
        extract_title = lambda wiki_data: wiki_data["query"]["pages"][0]["title"]

        expected_anecdocte = "La cité Paradis est une voie publique située dans le 10e arrondissement de Paris. Elle est en forme de té, une branche débouche au 43, rue de Paradis, la deuxième au 57, rue d'Hauteville et la troisième en impasse."
        expected_title = "Cité Paradis"

        wiki_data = self.gp.get_location_data("wiki")

        assert extract_anecdocte(wiki_data) == expected_anecdocte
        assert extract_title(wiki_data) == expected_title

    @pytest.mark.gpapi3
    def test_if_get_weather_data_retrieve_the_correct_data(self):

        user_location = {"latitude": "48.896735799681274", "longitude": "2.325297188151602"}

        result = self.gp.get_weather_data(user_location)

        assert type(result) == type(dict())
        assert type(result["tcur"]) == type(int())
        assert type(result["city"]) == type(str())
        assert type(result["description"]) == type(str())
        assert type(result["tmin"]) == type(int())
        assert type(result["tmax"]) == type(int())
        assert type(result["icon"]) == type(str())
