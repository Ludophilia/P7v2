import requests, json, random, re, os
import os.path as pth
import config as cf 
from app.gp_ressources.answers import answers

class GrandPy:

    def build_stopwords(self):

        """Telecharge la liste des stopwords si elle n'existe pas, construit à partir de la version texte de cette liste, une list python de ces stopwords (+majuscules)"""

        stopwords_filepath = "app/gp_ressources/stopwords.js"
        
        if not pth.exists(stopwords_filepath): 
            r = requests.get("https://raw.githubusercontent.com/6/stopwords-json/master/dist/fr.json")
            stopwords_txt = r.text
            with open(stopwords_filepath, "x") as f:
                f.write(stopwords_txt)
        
        with open(stopwords_filepath) as f:
            stopwords_list = f.read().replace('[','').replace(']','').replace("\"","").split(",")
            stopwords_list += [word.capitalize() for word in stopwords_list]

        return stopwords_list
    
    def remove_pounctuation(self, string_to_parse):

        """Retire la ponctuation de l'input utilisateur et renvoie un str de cet input"""

        punctuations = ["\'", "\"", "?", ",", ".", "!?", "?!", "-", "!", ";", ":", 
        "[", "]", "(", ")", "{", "}"]

        for punctuation in punctuations:
            while punctuation in string_to_parse: 
                string_to_parse = string_to_parse.replace(punctuation," ")
           
        return string_to_parse

    def remove_stopwords(self, string_to_parse):
        
        """Retire les stopwords de l'input utilisateur et renvoie une list de mots clés"""

        stopwords_list = self.build_stopwords()
        
        keywords = self.remove_pounctuation(string_to_parse).split()
        
        for stopword in stopwords_list:
            while stopword in keywords: 
                keywords.remove(stopword)   

        return keywords

    def get_api_data(self, source):

        """Telecharge les données Maps sur OC ou de Wikipédia sur la Cité Paradis si elles n'existent pas, les stocke dans un fichier .js, et les rappelle sous forme de dict"""
        
        maps_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=openclassrooms+paris&key={}".format(cf.API_KEY) 
        wiki_url = "https://fr.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&titles=Cité Paradis&formatversion=2&exsentences=3&exlimit=1&explaintext=1&exsectionformat=plain"

        data_url = maps_url if source == "maps" else wiki_url
        data_pth = "app/gp_ressources/{0}_info.js".format(source)

        if not pth.exists(data_pth): 
            r = requests.get(data_url)
            api_data = r.text # donc <class 'str'>

            with open(data_pth, "w") as f:
                f.write(api_data)

        with open(data_pth, "r") as f:
            api_data_js = json.loads(f.read())

        return api_data_js

    def get_anecdocte_and_url(self, wiki_data_js):

        """Récupère l'anecdocte de GP sur la Cité Paradis et l'url de la fiche wikipédia associée à partir des données js de l'API Wikimedia. Renvoie un dict"""

        anecdocte_and_url = {} ; title = wiki_data_js["query"]["pages"][0]["title"]

        anecdocte_and_url["url"] = "https://fr.wikipedia.org/wiki/{}".format(title).replace(" ", "_")
        anecdocte_and_url["anecdocte"] = wiki_data_js["query"]["pages"][0]["extract"].split('\n')[-1]

        return anecdocte_and_url

    def answer_message(self, string_to_parse):

        """Filtre l'input de l'utilisateur et renvoie une réponse en fonction des mots clés qui y figure"""
    
        message = "" ; grandpy_response = {} ; reactions = 0
        keywords_str = " ".join(self.remove_stopwords(string_to_parse)) #En attendant de modifier ce que fait remove_stopwords par exemple (pour obtenir une str directement au lieu d'une list)

        hello_pattern = r"([Bb]onjour|[Bb]jr|[Ss]a?lu?t|[Yy]o|[Hh]i)"
        oc_pattern = r"([oO]pen[cC]las.{1,2}rooms?|[oO][cC])"
        address_pattern = r"[Aa]d{1,2}res{1,2}e?"
        know_pattern = r"[Cc]on{1,2}ai(tre|[ts]?)" #Dans un fichier à part ?

        if re.search(hello_pattern, keywords_str):
            
            reactions += 1 ; greetings = answers["greetings"]
            message += "{}\n".format(greetings[random.randint(0,len(greetings)-1)]) 

        if re.search(oc_pattern, keywords_str):

            if re.search(know_pattern, keywords_str):
            
                if re.search(address_pattern, keywords_str):
                        
                    reactions += 1 ; oc_maps_data_js = self.get_api_data("maps")
                    
                    oc_address = oc_maps_data_js["results"][0]["formatted_address"].replace(", France", "") 
                    message += "Bien sûr mon poussin ! La voici : {}.\n".format(oc_address)

                    grandpy_response["anecdocte_and_url"] = self.get_anecdocte_and_url(self.get_api_data("wiki"))
                    grandpy_response["location"] = oc_maps_data_js["results"][0]["geometry"]["location"]

        if not reactions: 
            message = "Désolé, je ne sais rien faire d'autre que saluer ou donner une certaine adresse... Et oui je suis borné moi :)"

        grandpy_response["message"] = message

        return json.dumps(grandpy_response, ensure_ascii=False, sort_keys=True)