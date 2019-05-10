import requests
import json
import random
import os.path as pth
import sys
import config as cf
import re

class GrandPy:

    def __init__(self):
        self.maps_info = {} #Supprimez pas. Réutilisez si vous voulez d'autres infos de l'API maps.

    def build_stopwords(self):
        
        if not pth.exists("stopwords.js") : 

            r = requests.get("https://raw.githubusercontent.com/6/stopwords-json/master/dist/fr.json")
            stopwords_txt = r.text
            with open("stopwords.js", "x") as f:
                f.write(stopwords_txt)
        
        with open("stopwords.js") as f:
            stopwords_list = f.read().replace('[','').replace(']','').replace("\"","").split(",")
        
        stopwords_list_lg = []

        for word in stopwords_list:
            stopwords_list_lg += [word, word.capitalize()] #Wow, reconstruire la liste, c'est lourd comme méthode

        return stopwords_list_lg
    
    def remove_pounctuation(self, string_to_parse):
        
        punctuations = ["\'", "\"", "?", ",", ".", "!?", "?!", "-", "!", ";", ":"]
        for punctuation in punctuations:
            while punctuation in string_to_parse: 
                if punctuation == "\'" or punctuation == "-":
                    string_to_parse = string_to_parse.replace(punctuation," ")
                else:
                    string_to_parse = string_to_parse.replace(punctuation,"")

        return string_to_parse

    def remove_stopwords(self, string_to_parse):
        
        stopwords_list = self.build_stopwords()
        
        list_from_string_to_parse = self.remove_pounctuation(string_to_parse).split()
        
        for stopword in stopwords_list:
            if stopword in list_from_string_to_parse: 
                stopword_occurences = list_from_string_to_parse.count(stopword)
                for stopword_occurence in range(stopword_occurences):
                    list_from_string_to_parse.remove(stopword)
        
        return list_from_string_to_parse

    def get_maps_info(self):
        
        if len(self.maps_info) == 0: #Design economique pour éviter d'apppeler l'API à chaque fois.
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=openclassrooms+paris&key={}".format(cf.API_KEY) 
            r = requests.get(url)
            self.maps_info = r.json() 
        
        return self.maps_info 

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

        maps_info = self.get_maps_info()
        keywords_list = self.remove_stopwords(string_to_parse)
        
        keywords_str = str()
        for keyword in keywords_list: keywords_str += "{} ".format(keyword) #Meh solution
        
        grandpy_answer = ""
        message_answer = {}
        reaction = 0

        for keyword in keywords_list:

            if re.fullmatch(r"(^[Bb]onjour$|^[Bb]jr$|^[Ss]a?lu?t$|^[Yy]o$|^[Hh]i$)", keyword):
                reaction += 1
                greetings = ["Bonjour!", "Salut!", "Yo!", "Hi!!"]
                ln = random.randint(0,len(greetings)-1)
                grandpy_answer += "{}\n".format(greetings[ln]) #Curieux, le \n n'est pas considéré comme un saut de ligne du point de vue front end...
            
            if re.fullmatch(r"(^[oO]pen[cC]las.{1,2}rooms?$|^[oO][cC]$)", keyword):
                if re.search(r"[Aa]d{1,2}res{1,2}e?", keywords_str) and re.search(r"[Cc]on{1,2}ai(tre|[ts]?)", keywords_str):
                    address = self.get_address(maps_info)
                    message_answer["pi_location"] = self.get_coordinates(maps_info)
                    reaction += 1
                    grandpy_answer += "Bien sûr mon poussin ! La voici : {}.\n".format(address)

        if reaction == 0: 
            grandpy_answer = "Désolé, je ne sais rien faire d'autre que saluer ou donner une certaine adresse... Et oui je suis borné moi :)"

        message_answer["gp_message"] = grandpy_answer
        
        message_answer = json.dumps(message_answer, ensure_ascii=False, sort_keys=True)

        return message_answer