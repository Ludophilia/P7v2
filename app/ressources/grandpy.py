import requests, json, random, re, os, time, math
import os.path as pth
import config as cf 
import app.ressources.gp_speech as speech
import app.ressources.gp_patterns as patterns
from datetime import date as dt

class APIManager:
    
    """Représente l'APIManager, c'est à dire le système qui télécharge les données des différentes 
    API et les rend disponible à d'autres système"""

    def get_location_data(self, api_name):

        """Telecharge les données Maps sur OC ou de Wikipédia sur la Cité Paradis 
        si elles n'existent pas, les stocke dans un fichier .js, et les rappelle sous forme de dict"""
        
        maps_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=openclassrooms+paris&key={cf.GM_API_KEY}"
        wiki_url = "https://fr.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&titles=Cité Paradis&formatversion=2&exsentences=3&exlimit=1&explaintext=1&exsectionformat=plain"

        data_url = maps_url if api_name == "maps" else wiki_url
        data_pth = f"app/ressources/{api_name}_data.js"

        if not pth.exists(data_pth): 
            with open(data_pth, "w") as f:
                f.write(requests.get(data_url).text)

        with open(data_pth, "r") as f:
            json_formatted_api_data = json.loads(f.read())

        return json_formatted_api_data

    def get_weather_data(self, user_location):
        
        """Acquiert les données météo de et renvoie certaine d'entres elles sous forme de dict."""

        latitude, longitude = user_location["latitude"], user_location["longitude"]
        round = lambda x: math.ceil(x) if x - math.floor(x) > 0.5 else math.floor(x)

        owm_cur_url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={cf.OWM_API_KEY}&lang=fr&units=metric"
        owm_dal_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={latitude}&lon={longitude}&appid={cf.OWM_API_KEY}&lang=fr&units=metric&exclude=current,hourly"

        forecast = {
            **requests.get(owm_cur_url).json(),
            **requests.get(owm_dal_url).json()
        }

        weather_data = dict(
            tcur = round(forecast["main"]["temp"]),
            city = forecast["name"],
            description = forecast["weather"][0]["description"],
            icon = forecast["weather"][0]["icon"],
            tmin = round(forecast["daily"][0]["temp"]["min"]),
            tmax = round(forecast["daily"][0]["temp"]["max"])
        )
        return weather_data

class Parser:

    """Représente le Parser, c'est à dire le système qui analyse le message envoyé à l'utilisateur, 
    en extrait les mots clés et les reconnait ceux qui font "reagir" GrandPy"""

    def stopwords(self):

        """Renvoie une liste python de stopwords (minuscules)."""

        stopwords_filepath = "app/ressources/stopwords.js"

        with open(stopwords_filepath) as stopwords_file:
            stopwords_list = json.load(stopwords_file)

        return stopwords_list
    
    def remove_punctuation(self, user_input):

        """Retire la ponctuation et les whitespaces en trop de l'input utilisateur (str) 
        et renvoie un str de cet input"""

        gp1 = ["\'", "\""] #"-",
        gp2 = ["!?", "!", "?", "?!"] #"-", 
        gp3 = [",", ".", ";", ":", "[", "]", "(", ")", "{", "}", ">", "<"]

        for punctuation in gp1 + gp2 + gp3:

            if punctuation in gp1: 
                user_input = user_input.replace(punctuation, f" ")
            elif punctuation in gp2: 
                user_input = user_input.replace(punctuation, f" {punctuation}")
            elif punctuation in gp3:
                user_input = user_input.replace(punctuation, "")

        return re.sub(r"\s+", " ", user_input).strip()
        
    def extract_keywords(self, user_input):
        
        """Retire les stopwords et les mots répétés de l'input utilisateur sans ponctuation 
        (pf pour punctuation-free) et renvoie la list des mots "clés" restants (minuscules uniquement)"""

        words_in_user_input = self.remove_punctuation(user_input).split()
        keywords = []

        for word in words_in_user_input:
            word = word.lower()
            if word not in self.stopwords() and word not in keywords:
                keywords.append(word) 

        return keywords

    def search_patterns(self, keywords):

        """ Analyse les keywords à la recherche de patterns et retourne la liste des patterns trouvés """

        matches = [] 
        patterns_combi = [
            (patterns.HELLO, "hello"), (patterns.PLAY, "play"), (patterns.HEADS, "heads"),
            (patterns.TAILS, "tails"), (patterns.OC, "oc"), (patterns.KNOW, "know"), 
            (patterns.ADDRESS, "address"), (patterns.HOW, "how"), (patterns.AT, "at"), 
            (patterns.GO, "go"), (patterns.QUESTION, "question"), (patterns.WHAT, "what"),
            (patterns.TIME, "time"), (patterns.WEATHER, "weather"),
            (patterns.INFO, "info"), (patterns.WEBSITE, "website")
        ]
        
        for pattern, equiv in patterns_combi:

            if re.search(pattern, keywords, re.I|re.M):
                matches += [equiv]

        return matches

class GrandPy(Parser, APIManager):

    """Représente GrandPy, le robot qui répond aux messages et joue parfois avec l'utilisateur."""

    def __init__(self, owner_ip_adress):

        self.owner = owner_ip_adress
        self.memory = {}
        self.isWaitingForAnAnswer = set()
        self.awsers = 0

    def get_anecdocte(self, jsf_wiki_data):

        """Récupère l'anecdocte de GP sur la Cité Paradis et l'url de la fiche wikipédia 
        associée à partir des données jsf (json-formatted) de l'API Wikimedia. 
        Renvoie un str contenant l'anecdocte"""

        title = jsf_wiki_data["query"]["pages"][0]["title"]
        wiki_url = f"https://fr.wikipedia.org/wiki/{title}".replace(" ", "_")

        wikipedia_part = jsf_wiki_data["query"]["pages"][0]["extract"].split('\n')[-1]
        knowmore_part = speech.KNOWMORE("Wikipédia", wiki_url)

        return f"{speech.ANECDOCTE_STARTER} {wikipedia_part} {knowmore_part}"

    def say_hello(self, message):

        """Génère un message de salutation de GrandPy."""

        greetings = speech.GREETINGS
        random_position = random.randint(0,len(greetings)-1)

        message += f"{greetings[random_position]}<br>"

        return message

    def give_state_of_mind(self, message):
        
        """Génère un message où GrandPy explique comment il va."""

        day = dt.today().weekday()
        message += f"{speech.STATE_OF_MIND[day]}<br>"

        return message

    def give_time(self, user_data, message):

        """Génère un message où GrandPy donne l'heure qu'il est en fonction du fuseau horaire de l'utilisateur."""

        user_tzone = user_data.get("options").get("timezone")
        gp_tzone = int((time.altzone if time.daylight else time.timezone) / -3600)

        user_current_time = time.strftime("%H:%M", time.gmtime(time.time() + user_tzone * 3600))
        gp_current_time = time.strftime("%H:%M")

        message += speech.CURRENT_TIME(user_current_time)
        message += speech.DFTZ_EXTRA(gp_current_time) if user_tzone != gp_tzone else speech.NRML_EXTRA
        message += "<br>"

        return message

    def give_weather(self, user_data, message):

        """Génère un message où GrandPy donne la météo (temperature actuelle, minimale, maximale) 
        en fonction des coordonnées géo de l'utilisateur."""

        user_location = user_data.get("options").get("location")

        if not user_location:
            message += speech.NO_COORDS_GIVEN

        else:
            weather_data = self.get_weather_data(user_location)
            wc_icon = weather_data['icon']

            message += f"<img src='https://openweathermap.org/img/wn/{wc_icon}.png' alt='weather-icon' width='25' height='25'>"
            message += speech.CURRENT_WEATHER(weather_data)
        
        message += "<br>"

        return message

    def give_oc_address(self, message, grandpy_response):

        """Génère un message où GrandPy donne l'adresse d'openclassrooms.Génère aussi un autre message contenant une anecdocte 
        sur la rue d'OC et renvoie les coordonnés du lieu pour un affichage sur une carte."""

        oc_maps_data_js = self.get_location_data("maps")
        oc_address = oc_maps_data_js["results"][0]["formatted_address"].replace(", France", "") 

        message += f"{speech.ADDRESSFOUND(oc_address)}<br>"

        grandpy_response.update(
            anecdocte = self.get_anecdocte(self.get_location_data("wiki")),
            location = oc_maps_data_js["results"][0]["geometry"]["location"]
        )

        return {"message": message, "grandpy_response": grandpy_response}

    def play_heads_or_tails(self, matches, message):

        """Gère tout ce qui a à voir avec le jeu pile ou face proposé par grandpy. Retourne le paramètre message modifié."""

        if "play" in matches and not self.isWaitingForAnAnswer:

            self.isWaitingForAnAnswer.add("#HT")
            message += speech.HT_EXPLAIN_RULES
            print("[grandpy.py] gp.isWaitingForAnAnswer:", self.isWaitingForAnAnswer)
            print("[grandpy.py] gp.memory:", self.memory)

        elif self.isWaitingForAnAnswer:
        
            if ("heads" in matches) ^ ("tails" in matches):

                playerschoice = 0 if "heads" in matches else 1
                gamesresult = random.randint(0,1)
                gr_readable = ["pile", "face"][gamesresult]

                bravo, shame = speech.HT_PLAYER_VICTORY(gr_readable),speech.HT_PLAYER_DEFEAT(gr_readable)

                message += speech.HT_TOSS_COIN
                message += bravo if playerschoice == gamesresult else shame
                if self.memory.get("HT_ERROR"): self.memory.pop("HT_ERROR")
                self.isWaitingForAnAnswer.remove("#HT")

                print("[grandpy.py] gp.isWaitingForAnAnswer:", self.isWaitingForAnAnswer)
                print("[grandpy.py] gp.memory:", self.memory)

            else:
                #Les lignes fautives ?
                if self.memory.get("HT_ERROR") == None:
                    self.memory["HT_ERROR"] = 1  
                else:
                     self.memory["HT_ERROR"] + 1
                
                remaining = 3 - self.memory["HT_ERROR"]

                if remaining == 0:
                    message += speech.HT_OUT_OF_TRIES
                    self.memory.pop("HT_ERROR")
                    self.isWaitingForAnAnswer.remove("#HT")

                else:
                    message += speech.HT_ERROR(remaining)

                print("[grandpy.py] gp.isWaitingForAnAnswer:", self.isWaitingForAnAnswer)
                print("[grandpy.py] gp.memory:", self.memory)

        return message

    def give_website_info(self, message):

        """Donne des informations sur le site. Retourne le paramètre str modifié"""

        project_glink = """
        <span id="footer_sns">
            <a href="https://github.com/Ludophilia/P7v2" target="_blank">
                <img src="static/img/GitHub-Mark-Light-32px.png" alt="Octocat" width="25" height="25"/>
            </a>
        </span>
        """

        message += speech.SITE_INFO(project_glink)

        return message

    def answer_message(self, user_data):

        """Renvoie une réponse (sous forme de json) à l'input utilisteur en fonction des mots clés qui y figurent"""

        user_message = user_data.get("user_message", "")
        message = ""
        grandpy_response = {}
        keywords = "\n".join(self.extract_keywords(user_message))
        matches = self.search_patterns(keywords)

        self.awsers += 1
        print("[grandpy.py] Number of Answers:", self.awsers) #L'info reste-t-elle en mémoire ?

        if self.isWaitingForAnAnswer:

            if "#HT" in self.isWaitingForAnAnswer:
                message += self.play_heads_or_tails(matches, message)

        else:

            if "hello" in matches:

                message += self.say_hello(message)

            if "info" in matches and "website" in matches:
                
                message += self.give_website_info(message)

            if "play" in matches and "heads" in matches and "tails" in matches:

                message += self.play_heads_or_tails(matches, message)

            if ("how" in matches or "question" in matches) and ("go" in matches) and (
            not "at" in matches):

                message += self.give_state_of_mind(message)

            if ("question" in matches or "what" in matches) and "time" in matches:

                message += self.give_time(user_data, message)

            if ("question" in matches or "what" in matches) and "weather" in matches:
                
                message += self.give_weather(user_data, message)

            if "oc" in matches and "know" in matches and "address" in matches:

                # Une autre approche pour la v3, mettre chaque nouveau message dans un array. 
                # On itéra sur l'array pour afficher chaque message 

                oc_address = self.give_oc_address(message, grandpy_response)

                grandpy_response = oc_address.get("grandpy_response") 
                message += oc_address.get("message")

        message += f"{speech.SORRY}" if len(message) == 0 else "" 
        grandpy_response["message"] = message
        return json.dumps(grandpy_response, ensure_ascii=False, sort_keys=True)

    def deal_with_clicks_on_logo(self, user_data):

        """Renvoie une réponse (sous forme de str) à l'utilisateur en fonction du 
        nombre de fois qu'il a appuyé sur le logo de grandpy"""

        self.awsers += 1
        print("[grandpy.py] Number of Answers:", self.awsers)

        nth_time = user_data.get("reactions", "")

        return speech.INTERROGATE_CLICK_ON_LOGO if nth_time == "n0" else speech.ANNOYED.get(nth_time, "...")

    def start_conversation(self):

        """Renvoie un message sympa pour démarrer la conversation avec l'utilisateur """

        starter = f"{speech.STARTER}"

        return starter