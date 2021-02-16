import json, re

class Parser:

    """Représente le Parser, c'est à dire le système qui analyse le message envoyé à l'utilisateur, en extrait les mots clés et les reconnait ceux qui font "reagir" GrandPy"""

    def __init__(self) -> None:
        self.HELLO = r"^b(on)?j(ou)?r$|^slt$|^salut(ations?)?$|^yo$|^hi$|^👋$"
        self.OC = r"^o(pen)?c(las{1,2}rooms?)?$"
        self.ADDRESS = r"^ad{1,2}res{1,2}e?$"
        self.KNOW = r"^con{1,2}ai(tre|[ts]?|sai[ts]?)(-tu)?$"
        self.HOW = r"^com{1,2}ent$"
        self.GO = r"^vas?(-tu)?$|^al{1,2}ez(-vous)?$"
        self.AT = r"^[àa]$" # [aA] = dangereux
        self.QUESTION = r"^\?{1,3}\!{0,2}$"
        self.WHAT = r"^quel(le)?$"
        self.TIME = r"^heure$"
        self.WEATHER = r"^temps$"
        self.PLAY = r"^jou(ons|e[zr])$"
        self.HEADS = r"^pile$"
        self.TAILS = r"^face$"
        self.INFO = r"^info(rmation)?s?$"
        self.WEBSITE = r"^(site|app)(\s(web|internet))?$"
        self.PLACEOFINTEREST = r"ad{1,2}res{1,2}e? ((\w+\s?){1,8})(\?|$)"

    @property
    def __stopwords(self) -> list:

        """Renvoie une liste python de stopwords (minuscules)."""

        stopwords_filepath = "app/ressources/stopwords.js"

        with open(stopwords_filepath) as stopwords_file:
            stopwords_list = json.load(stopwords_file)

        return stopwords_list
    
    def __remove_punctuation(self, user_input: str) -> str:

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
        
    def __extract_keywords_from_user_input(self, user_input: str, multiline = True) -> str:
        
        """Retire les stopwords et les mots répétés de l'input utilisateur sans ponctuation 
        et renvoie une chaine de charactère contenant les mots "clés" restants (minuscules uniquement)"""

        words_in_user_input = self.__remove_punctuation(user_input).split()
        sep = "\n" if multiline else " "
        keywords = []

        for word in words_in_user_input:
            word = word.lower()
            if word not in self.__stopwords and word not in keywords:
                keywords.append(word) 


        return f"{sep}".join(keywords) #Renvoyer Keywords in array à la place. Pourquoi ? Cela permet d'utiliser la liste des 
        # keywords de façon positionnelle, pour pouvoir repérer l'adresse du lieu recherché qui devrait se trouver
        # à une certaine position.

    def __find_matches_from_keywords(self, keywords: str) -> list:

        """ Analyse la chaine de keywords à la recherche de patterns qui font réagir grandpy
        et retourne la liste des keywords déclencheurs """

        matches = [] 
        patterns_combi = [
            (self.HELLO, "hello"), (self.PLAY, "play"), (self.HEADS, "heads"),
            (self.TAILS, "tails"), (self.OC, "oc"), (self.KNOW, "know"), 
            (self.ADDRESS, "address"), (self.HOW, "how"), (self.AT, "at"), 
            (self.GO, "go"), (self.QUESTION, "question"), (self.WHAT, "what"),
            (self.TIME, "time"), (self.WEATHER, "weather"),
            (self.INFO, "info"), (self.WEBSITE, "website")
        ]
        
        for pattern, equiv in patterns_combi:

            if re.search(pattern, keywords, re.I|re.M):
                matches += [equiv]

        return matches

    def extract_place_from_user_message(self, user_input: str) -> str:

        """ Analyse la chaine utilisateur et renvoie l'adresse qui y figure. L'implémentation actuelle 
        nécessite que l'utilisateur utilise un '?' pour terminer la sous chaine qui constitue l'adresse. """

        keywords = self.__extract_keywords_from_user_input(user_input, False)
        extract_poi = re.search(self.PLACEOFINTEREST, keywords)

        return extract_poi.group(1).strip()

    def find_matches(self, user_input: str) -> list: 

        """ Extraie les mots-clés de la chaine utilisateur et renvoie les codes des mots-clés 
        reconnus par le parser """

        keywords_str = self.__extract_keywords_from_user_input(user_input)
        matches = self.__find_matches_from_keywords(keywords_str)

        return matches
