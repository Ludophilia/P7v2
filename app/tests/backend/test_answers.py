import re, time, json

import pytest

from app.tests.backend.testtools import TestTools
from app.grandpy import GrandPy
from app.grandpy.skills import APIManager
from app.grandpy.skills.self_analysis.speech import GITHUB

@pytest.mark.gpans #31/07/20 - OK
class TestGrandPyAnswerToASingleQuestion(TestTools):
    
    @pytest.mark.gpans1
    def test_what_answer_message_returns_if_the_user_says_nothing_interesting(self):
                        
        actual_message = self.ask_grandpy("ONE MORE DOG REJECTED")

        expected_answer = "Désolé, je n'ai pas compris ton message... 😕 Dans une prochaine version peut-être ?"

        assert actual_message == expected_answer

    @pytest.mark.gpans2
    def test_what_answer_message_returns_if_the_user_says_hello(self):
        
        hello_pattern = r"Bonjour!|Salut!|Yo!|Hi!!|👋"

        messages = ["slt", "salut", "Bonjour", "Salutations", "👋", "Yo !!"]

        for m in messages: 
            message = self.ask_grandpy(m)
            assert re.search(hello_pattern, message)

    @pytest.mark.gpans3
    def test_what_answer_message_returns_if_the_user_asks_for_OC_address(self, monkeypatch):
        
        # FAUT FAIRE CE TEST :
        # FAUT ENSUITE VOIR CE QU'IL SE PASSE EN FRONT
        
        #GrandPy("127.0.0.1")
        monkeypatch.setattr(APIManager, "get_location_data", self.get_fake_api_data)
        
        actual_message = self.ask_grandpy("adresse oc connaitre")
        actual_coordinates = self.ask_grandpy("adresse oc connaitre", key="oc_coordinates")
        actual_anecdocte = self.ask_grandpy("adresse oc connaitre", key="oc_anecdote")

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
                assert self.ask_grandpy(message) in EXP_STATE_OF_MIND
            else:
                assert self.ask_grandpy(message) not in EXP_STATE_OF_MIND

    @pytest.mark.gpans5
    def test_if_grandpy_replies_as_expected_when_asked_for_the_time(self):
        
        expected_answer = f"🕗 Il est {time.strftime('%H:%M')} !!"
        messages = [
            "il est quelle heure ?", "quelle heure est-il ?", "tu as l'heure ?", "Quelle heure il est"
        ]

        for message in messages:
            assert self.ask_grandpy(message, options={'timezone': 2}) == expected_answer

    @pytest.mark.gpans6
    def test_if_grandpy_replies_as_expected_when_asked_for_the_weather(self, monkeypatch):

        monkeypatch.setattr(APIManager, "get_weather_data", self.get_fake_weather_data)

        expected_answer = f"<img src='https://openweathermap.org/img/wn/04d.png' alt='weather-icon' width='25' height='25'>Il fait actuellement 22°C à Paris. Les températures min et max pour le reste de la journée seront respectivement de 21°C et 24°C."
        expected_unexpected_answer = f"Désolé, impossible de te donner la météo. As-tu bien accepté que je te géolocalise quand je te l'ai demandé ? 🤔"

        options1 = {"location": {"latitude": 48.896, "longitude": 2.32}}
        options2 = {"location": None} 

        questions = ["Quel temps il fait ?", "Quel temps fait-il ?", "quel temps ?", "quel temps aujourd'hui ?"]

        for question in questions:
            assert self.ask_grandpy(f"{question}", options=options1) == expected_answer
            assert self.ask_grandpy(f"{question}", options=options2) == expected_unexpected_answer

    @pytest.mark.gpans7
    def test_if_grandpy_replies_as_expected_when_asked_for_infos_bout_the_app(self):

        SITE_INFO = lambda link : f"Bien sûr ! Cette app web est la concrétisation d'un des projets à réaliser dans le cadre d'un des parcours \"développeur d'application\" proposé par OpenClassrooms.En fait, il s'agit même de sa 2ème version, vu que la 1ère, des mots de Jeffrey G, son auteur, était \"un peu de la merde\".D'un point de vue technique, côté frontend , l'app est construite avec le combo HTML5 + CSS3 + JS, sans l'aide d'un framework. Côté backend, est utilisé exclusivement Python3 avec le framework Flask.Si ça t'intéresse davantage, je t'invite à te rendre sur {link}, tu en apprendras sans doute plus !"
        expected_message = SITE_INFO(GITHUB)

        actual_message = self.ask_grandpy("Puis-je avoir des infos sur ce site ?")
        
        assert actual_message == expected_message

@pytest.mark.gpansmu #31/07/20 - OK
class TestGrandPyAnswerToMultipleQuestions(TestTools):

    @pytest.mark.gpansmu1
    def test_what_answer_message_returns_if_the_user_says_hello_and_asks_for_OC_address(self, monkeypatch):

        monkeypatch.setattr(APIManager, "get_location_data", self.get_fake_api_data)
        hello_pattern = r"Bonjour!|Salut!|Yo!|Hi!!|👋"

        actual_message = self.ask_grandpy("salut grandpy ! Connais-tu l'adresse d'oc?")
        expected_message = "Bien sûr mon poussin ! La voici : \"7 Cité Paradis, 75010 Paris\".  Et voilà une carte pour t'aider en plus !!"

        assert re.search(hello_pattern, actual_message)
        assert expected_message in actual_message


@pytest.mark.gpau #31/07/20 - OK
class TestGrandPyAutoResponses(TestTools):

    @pytest.mark.gpau2
    def test_if_start_conversation_returns_the_expected_string(self):
        
        expected_answer = """Salut 👋, qu'est-ce que je peux faire pour toi ?<br><br>
        Tu peux me demander, dans le formulaire juste en bas avec 'Nouveau message' écrit dedans :<br><br>
        - "Tu connais l'adresse d'OpenClassrooms ?" pour obtenir l'adresse d'Openclassrooms 🏫 !<br>
        - "Quel temps fait-il ?" pour obtenir la météo ⛅️ de ton lieu (📍localisation nécessaire) !<br>
        - "Quelle heure il est ?" pour obtenir l'heure 🕓 qu'il est !<br>
        - "Jouons à pile ou face" si tu veux jouer au jeu du même nom 🎲 !<br>
        - "T'as des infos sur ce site ?" pour obtenir des infos sur ce site 📁 !<br>
        <br>
        Sinon, tu peux toujours m'envoyer un "salut" ou une "👋" pour me saluer 👊 ou me demander "comment tu vas" pour prendre des nouvelles 🍺, ça fait toujours plaisir !
        """
       
        assert expected_answer == GrandPy("127.0.0.1").start_conversation()