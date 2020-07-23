import requests, json, random, re, os, time, math
import os.path as pth
import config as cf 
import app.ressources.gp_speech as speech
import app.ressources.gp_patterns as patterns
from datetime import date as dt

class GrandPy:

    def extract_keywords(self, user_input):
        
        def stopwords():

            """Renvoie une liste python de stopwords (minuscules). Télécharge et construit cette liste si elle n'existe pas"""

            stopwords_filepath = "app/ressources/stopwords.js"

            # if not pth.exists(stopwords_filepath): 
            #     with open(stopwords_filepath, "w") as stopwords_file:
            #         stopwords_list = requests.get("https://raw.githubusercontent.com/6/stopwords-json/master/dist/fr.json").json()

            #         json.dump(stopwords_list, stopwords_file, ensure_ascii=False)
            # else:
            with open(stopwords_filepath) as stopwords_file:
                stopwords_list = json.load(stopwords_file)

            return stopwords_list
    
        def remove_punctuation(user_input):

            """Retire la ponctuation et les whitespaces en trop de l'input utilisateur (str) et renvoie un str de cet input"""

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

        """Retire les stopwords et les mots répétés de l'input utilisateur sans ponctuation (pf pour punctuation-free) et renvoie la list des mots "clés" restants (minuscules uniquement)"""

        words_in_user_input = remove_punctuation(user_input).split()
        keywords = []

        for word in words_in_user_input:
            word = word.lower()
            if word not in stopwords() and word not in keywords:
                keywords.append(word) 

        return keywords

    def get_api_data(self, api_name):

        """Telecharge les données Maps sur OC ou de Wikipédia sur la Cité Paradis si elles n'existent pas, les stocke dans un fichier .js, et les rappelle sous forme de dict"""
        
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
        
        """Acquière les données météo de et renvoie certaine d'entres elles sous forme de dict."""

        latitude, longitude = user_location["latitude"], user_location["longitude"]
        round = lambda x: math.ceil(x) if x - math.floor(x) > 0.5 else math.floor(x)

        owm_url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={cf.OWM_API_KEY}&lang=fr&units=metric"
        response = requests.get(owm_url).json()

        weather_data = dict(
            tcur = round(response["main"]["temp"]),
            city = response["name"],
            description = response["weather"][0]["description"],
            tmin = round(response["main"]["temp_min"]),
            tmax = round(response["main"]["temp_max"]),
            icon = response["weather"][0]["icon"]
        )

        return weather_data

    def get_anecdocte(self, jsf_wiki_data):

        """Récupère l'anecdocte de GP sur la Cité Paradis et l'url de la fiche wikipédia associée à partir des données jsf (json-formatted) de l'API Wikimedia. Renvoie un str contenant l'anecdocte"""

        title = jsf_wiki_data["query"]["pages"][0]["title"]
        wiki_url = f"https://fr.wikipedia.org/wiki/{title}".replace(" ", "_")

        wikipedia_part = jsf_wiki_data["query"]["pages"][0]["extract"].split('\n')[-1]
        knowmore_part = speech.KNOWMORE("Wikipédia", wiki_url)

        return f"<span>{speech.ANECDOCTE_STARTER} {wikipedia_part} {knowmore_part}</span>"

    def search_patterns(self, keywords):

        """ Analyse les keywords à la recherche de patterns """
        
        matches = [] 
        
        # Aie aie aie, ça s'allonge...
        
        if re.search(patterns.HELLO, keywords, re.M):
            matches += ["hello"]

        if re.search(patterns.OC, keywords, re.M):
            matches += ["oc"]

        if re.search(patterns.KNOW, keywords, re.M):
            matches += ["know"]

        if re.search(patterns.ADDRESS, keywords, re.M):
            matches += ["address"]
                
        if re.search(patterns.HOW, keywords, re.M):
            matches += ["how"]

        if re.search(patterns.AT, keywords, re.M):
            matches += ["at"]

        if re.search(patterns.GO, keywords, re.M):
            matches += ["go"]

        if re.search(patterns.QUESTION, keywords, re.M):
            matches += ["question"]

        if re.search(patterns.WHAT, keywords, re.M):
            matches += ["what"]

        if re.search(patterns.TIME, keywords, re.M):
            matches += ["time"]

        if re.search(patterns.WEATHER, keywords, re.M):
            matches += ["weather"]

        return matches

    def answer_message(self, user_data):

        """Renvoie une réponse (sous forme de json) à l'input utilisteur en fonction des mots clés qui y figurent"""

        user_message = user_data.get("user_message", "") ; message = "<span>" ; grandpy_response = {}
        keywords = "\n".join(self.extract_keywords(user_message))
        matches = self.search_patterns(keywords)

        if "hello" in matches:
            
            greetings = speech.GREETINGS
            random_position = random.randint(0,len(greetings)-1)

            message += f"{greetings[random_position]}<br>"

        if ("how" in matches or "question" in matches) and ("go" in matches) and (
        not "at" in matches):

            day = dt.today().weekday()
            message += f"{speech.STATE_OF_MIND[day]}<br>"

        if ("question" in matches or "what" in matches) and "time" in matches:

            user_tzone = user_data.get("options").get("timezone")
            gp_tzone = int((time.altzone if time.daylight else time.timezone) / -3600)

            user_current_time = time.strftime("%H:%M", time.gmtime(time.time() + user_tzone * 3600))
            gp_current_time = time.strftime("%H:%M")

            message += speech.CURRENT_TIME(user_current_time)
            message += speech.DFTZ_EXTRA(gp_current_time) if user_tzone != gp_tzone else speech.NRML_EXTRA
            message += "<br>"

        if ("question" in matches or "what" in matches) and "weather" in matches:
            
            user_location = user_data.get("options").get("location")

            if not user_location:
                message += speech.NO_CURRENT_WEATHER

            else:
                data = self.get_weather_data(user_location)
                wc_icon = data['icon']

                message += f"<img src='http://openweathermap.org/img/wn/{wc_icon}.png' alt='weather-icon' width='25' height='25'> "
                message += speech.CURRENT_WEATHER(data)
            
            message += "<br>"

        if "oc" in matches and "know" in matches and "address" in matches:

            oc_maps_data_js = self.get_api_data("maps")
            oc_address = oc_maps_data_js["results"][0]["formatted_address"].replace(", France", "") 

            message += f"{speech.ADDRESSFOUND(oc_address)}<br>"

            grandpy_response.update(
                anecdocte = self.get_anecdocte(self.get_api_data("wiki")),
                location = oc_maps_data_js["results"][0]["geometry"]["location"]
            )

        message += f"{speech.SORRY}</span>" if len(message) == 6 else "</span>" 
      
        grandpy_response["message"] = message

        return json.dumps(grandpy_response, ensure_ascii=False, sort_keys=True)

    def deal_with_clicks_on_logo(self, user_data):

        """Renvoie une réponse (sous forme de str) à l'utilisateur en fonction du nombre de fois qu'il a appuyé sur le logo de grandpy"""

        nth_time = user_data.get("reactions", "")

        return speech.INTERROGATE_CLICK_ON_LOGO if nth_time == "n0" else speech.ANNOYED.get(nth_time, "...")
    
    def give_footer_info(self):

        """Renvoie le footer (sous forme d'une html str)"""

        footer = f"""
        <div id="footer_container">
            <div id="footer_text">
                {speech.FOOTER_TEXT}
            </div>
            <div id="footer_sns">
                <a href="https://github.com/Ludophilia/P7v2" target="_blank">
                    <img src="static/img/GitHub-Mark-Light-32px.png" alt="Octocat" width="25" height="25"/>
                </a><span>{speech.FOOTER_SNS}</span>
            </div>
        </div>
        """

        return footer

    def start_conversation(self):

        """Renvoie un message sympa pour démarrer la conversation avec l'utilisateur """

        starter = f"<span>{speech.STARTER}</span>"

        return starter