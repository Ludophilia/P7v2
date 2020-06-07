import requests, json, random, re, os
import os.path as pth
import config as cf 
import app.ressources.gp_speech as speech
import app.ressources.gp_patterns as patterns

class GrandPy:

    def extract_keywords(self, user_input):
        
        def stopwords():

            """Renvoie une liste python de stopwords (minuscules). Télécharge et construit cette liste si elle n'existe pas"""

            stopwords_filepath = "app/ressources/stopwords.js"

            if not pth.exists(stopwords_filepath): 
                with open(stopwords_filepath, "w") as stopwords_file:
                    stopwords_list = requests.get("https://raw.githubusercontent.com/6/stopwords-json/master/dist/fr.json").json()

                    json.dump(stopwords_list, stopwords_file, ensure_ascii=False)
            else:
                with open(stopwords_filepath) as stopwords_file:
                    stopwords_list = json.load(stopwords_file)

            return stopwords_list
    
        def remove_punctuation(user_input):

            """Retire la ponctuation et les whitespaces en trop de l'input utilisateur (str) et renvoie un str de cet input"""

            sp_punctuations = ["\'", "\""] #"-", 
            punctuations = ["?", ",", ".", "!?", "?!", "!", ";", ":", "[", "]", "(", ")", "{", "}"] + sp_punctuations

            for punctuation in punctuations:
                user_input = user_input.replace(punctuation, " ") if punctuation in sp_punctuations else user_input.replace(punctuation, "")

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
        
        maps_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=openclassrooms+paris&key={}".format(cf.API_KEY) 
        wiki_url = "https://fr.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&titles=Cité Paradis&formatversion=2&exsentences=3&exlimit=1&explaintext=1&exsectionformat=plain"

        data_url = maps_url if api_name == "maps" else wiki_url
        data_pth = "app/ressources/{0}_data.js".format(api_name)

        if not pth.exists(data_pth): 
            with open(data_pth, "w") as f:
                f.write(requests.get(data_url).text)

        with open(data_pth, "r") as f:
            json_formatted_api_data = json.loads(f.read())

        return json_formatted_api_data

    def get_anecdocte_and_url(self, jsf_wiki_data):

        """Récupère l'anecdocte de GP sur la Cité Paradis et l'url de la fiche wikipédia associée à partir des données jsf (json-formatted) de l'API Wikimedia. Renvoie un dict"""

        title = jsf_wiki_data["query"]["pages"][0]["title"]
        wikipedia_part = jsf_wiki_data["query"]["pages"][0]["extract"].split('\n')[-1]
        wiki_url = "https://fr.wikipedia.org/wiki/{}".format(title).replace(" ", "_")

        anecdocte_and_url = dict(
            anecdocte = "{} {} ".format(speech.ANECDOCTE_STARTER, wikipedia_part),
            wiki_url = speech.KNOWMORE("Wikipédia", wiki_url)
        )

        return anecdocte_and_url

    def answer_message(self, user_input):

        """Renvoie une réponse à l'input utilisteur en fonction des mots clés qui y figurent"""

        message = "" ; grandpy_response = {}
        keywords = "\n".join(self.extract_keywords(user_input))

        hello_found = re.search(patterns.HELLO, keywords, re.M)
        oc_found = re.search(patterns.OC, keywords, re.M)
        know_found = re.search(patterns.KNOW, keywords, re.M)
        address_found = re.search(patterns.ADDRESS, keywords, re.M)

        if hello_found:
            
            greetings = speech.GREETINGS
            random_position = random.randint(0,len(greetings)-1)

            message += "{}\n".format(greetings[random_position]) 

        if oc_found and know_found and address_found:

            oc_maps_data_js = self.get_api_data("maps")
            oc_address = oc_maps_data_js["results"][0]["formatted_address"].replace(", France", "") 

            message += speech.ADDRESSFOUND(oc_address)

            grandpy_response.update(
                anecdocte_and_url = self.get_anecdocte_and_url(self.get_api_data("wiki")),
                location = oc_maps_data_js["results"][0]["geometry"]["location"]
            )

        if not message: 
            message = speech.SORRY

        grandpy_response["message"] = message

        return json.dumps(grandpy_response, ensure_ascii=False, sort_keys=True)

    def deal_with_clicks_on_logo(self, nth_time):

        """Renvoie une réponse à l'utilisateur en fonction du nombre de fois qu'il a appuyé sur le logo de grandpy"""

        return speech.INTERROGATE_CLICK_ON_LOGO if nth_time == "n0" else speech.ANNOYED.get(nth_time, "...")