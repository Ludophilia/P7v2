import requests
import json
import random
import os.path as pth
import sys

class GrandPy:

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

    def answer_message(self, string_to_parse):
        # On scanne la liste des mots clés et pour chaque mot clé significatif, on alimente une str qui devient de plus en plus massive.

        keywords_list = self.remove_stopwords(string_to_parse)
        print(keywords_list)
        
        grandpy_answer = ""
        reaction = 0

        for keyword in keywords_list:
            if keyword in ['Bonjour', 'bonjour', 'Salut', 'salut', 'Yo', 'yo']:
                reaction += 1
                greetings = ["Bonjour!", "Salut!", "Yo!", "Hi!!"]
                ln = random.randint(0,len(greetings)-1)
                grandpy_answer += "{}\n".format(greetings[ln])

            if keyword in ['openclassrooms', 'Openclassrooms', 'OpenClassrooms', 'OC']:
                if "adresse" in keywords_list and ("connais" in keywords_list or "Connais" in keywords_list):
                    reaction += 1
                    grandpy_answer += "Bien sûr mon poussin ! La voici : 7 cité Paradis, 75010 Paris.\n"

        if reaction == 0 : 
            grandpy_answer = "Désolé, je ne sais rien faire d'autre que saluer ou donner une certaine adresse... Et oui je suis borné moi :)"

        return grandpy_answer

# gp = GrandPy()
# gp.answer_message("salut, bitch, je;?LK t'ai, ,,,,manqué ? celui celui celui certes certes certes bat beau ta reum pd,,,!?")
# gp.answer_message("Salut GrandPy! Tu connais l'adresse d'Openclassrooms")
