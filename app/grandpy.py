import requests, json, random, re
import os.path as pth
import config as cf 

class GrandPy:

    def __init__(self):
        self.maps_info = {}
        self.wiki_info = {} 

    def build_stopwords(self):
        
        if not pth.exists("stopwords.js") : 
            r = requests.get("https://raw.githubusercontent.com/6/stopwords-json/master/dist/fr.json")
            stopwords_txt = r.text
            with open("stopwords.js", "x") as f:
                f.write(stopwords_txt)
        
        with open("stopwords.js") as f:
            stopwords_list = f.read().replace('[','').replace(']','').replace("\"","").split(",")
            stopwords_list = stopwords_list + [word.capitalize() for word in stopwords_list]

        return stopwords_list
    
    def remove_pounctuation(self, string_to_parse):
        
        punctuations = ["\'", "\"", "?", ",", ".", "!?", "?!", "-", "!", ";", ":"]
        for punctuation in punctuations:
            while punctuation in string_to_parse: 
                string_to_parse = string_to_parse.replace(punctuation," ")
           
        return string_to_parse

    def remove_stopwords(self, string_to_parse):
        
        stopwords_list = self.build_stopwords()
        
        word_list = self.remove_pounctuation(string_to_parse).split()
        
        for stopword in stopwords_list:
            if stopword in word_list: 
                [word_list.remove(stopword) for _ in range(word_list.count(stopword))]
        
        return word_list

    def get_maps_info(self):
        
        if len(self.maps_info) == 0: #Design economique pour éviter d'apppeler l'API à chaque fois.
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=openclassrooms+paris&key={}".format(cf.API_KEY) 
            r = requests.get(url)
            self.maps_info = r.json() 
        
        return self.maps_info 

    def get_wiki_info(self):
        
        if len(self.wiki_info) == 0:
            url = "https://fr.wikipedia.org/w/api.php?action=parse&format=json&prop=wikitext&page=Cité Paradis&section=1"
            r = requests.get(url)
            self.wiki_info = r.json()
        
        return self.wiki_info 

    def get_anecdocte(self, r_formatted):
        
        anecdocte_wikitext = r_formatted["parse"]["wikitext"]["*"].split('\n')
        wiki_url = "https://fr.wikipedia.org/wiki/" + r_formatted["parse"]["title"].replace(" ", "_")

        symb_to_remove = ["[[wikt:", "[[", "]]", "{{", "}}"]
        anecdocte = ""

        anecdocte_complete = {}
        anecdocte_complete["url"] = wiki_url

        for line in anecdocte_wikitext:
            if re.search(r"[La] cité [Pp]aradis est une voie publique", line): #Extrait la réponse à la question du wikitexte
                anecdocte = line 

        for symbol in symb_to_remove: 
            anecdocte = anecdocte.replace(symbol,"") #Retire les {{}}, [[]] du wikitexte qui figurent toujours la réponse

        anecdocte = re.sub(r"\|\w+\s?\w*\s?\w*", "", anecdocte) #Cherche à retirer "|10e", "|arrondissement de Paris"...

        anecdocte_complete["anecdocte"] = anecdocte
        
        return anecdocte_complete

    def get_address(self, r_formatted):
        
        for result in r_formatted["results"]:
            if result["name"] == "Openclassrooms": 
                address = result["formatted_address"].replace(", France", "")
                return address 

    def get_coordinates(self, r_formatted):
        
        for result in r_formatted["results"]:
            if result["name"] == "Openclassrooms": 
                coordinates = result["geometry"]["location"]
                return coordinates

    def answer_message(self, string_to_parse):

        keywords_list = self.remove_stopwords(string_to_parse)
        
        keywords_str = str()
        for keyword in keywords_list: keywords_str += "{} ".format(keyword) #Bof la solution
        
        grandpy_answer = ""
        json_answer = {}
        reaction = 0

        for keyword in keywords_list:

            if re.fullmatch(r"(^[Bb]onjour$|^[Bb]jr$|^[Ss]a?lu?t$|^[Yy]o$|^[Hh]i$)", keyword):
                reaction += 1
                greetings = ["Bonjour!", "Salut!", "Yo!", "Hi!!"]
                lucky_number = random.randint(0,len(greetings)-1)
                grandpy_answer += "{}\n".format(greetings[lucky_number]) #Curieux, le \n n'est pas considéré comme un saut de ligne du point de vue front end...
            
            if re.fullmatch(r"(^[oO]pen[cC]las.{1,2}rooms?$|^[oO][cC]$)", keyword):
                if re.search(r"[Aa]d{1,2}res{1,2}e?", keywords_str) and re.search(r"[Cc]on{1,2}ai(tre|[ts]?)", keywords_str):
                    
                    reaction += 1

                    maps_info = self.get_maps_info()
                    address = self.get_address(maps_info)
                    json_answer["pi_location"] = self.get_coordinates(maps_info)
                    grandpy_answer += "Bien sûr mon poussin ! La voici : {}.\n".format(address)

                    anecdocte_complete = self.get_anecdocte(self.get_wiki_info())
                    json_answer["pi_anecdocte"] = anecdocte_complete

        if reaction == 0: 
            grandpy_answer = "Désolé, je ne sais rien faire d'autre que saluer ou donner une certaine adresse... Et oui je suis borné moi :)"

        json_answer["gp_message"] = grandpy_answer

        json_answer = json.dumps(json_answer, ensure_ascii=False, sort_keys=True)

        return json_answer