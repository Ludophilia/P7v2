""" Données utilisées pour construire les réponses de GrandPy """

STARTER = """Salut 👋, qu'est-ce que je peux faire pour toi ?<br><br>
        Tu peux me demander :<br>
        - Si je connais l'adresse d'OpenClassrooms 🏫 !<br>
        - Quel temps ⛅️ il fait actuellement (j'ai besoin de te 📍localiser pour ça) !<br>
        - L'heure 🕓 qu'il est !<br>
        - Des infos sur ce site 📁 !<br>
        <br>
        Sinon, tu peux toujours me saluer 👋 ou me demander comment je vais 🙁🙂, ça fait toujours plaisir !<br><br>
        On peut jouer à quelque chose aussi, mais juste pile ou face 🎲 pour le moment !<br>
        """

KNOWMORE = lambda source, url: f"[En savoir plus sur <a href='{url}' target='_blank'>{source}</a>]"

GREETINGS = ["Bonjour!", "Salut!", "Yo!", "Hi!!", "👋"]

SORRY = "Désolé, je n'ai pas compris ton message... 😕 Dans une prochaine version peut-être ?"

STATE_OF_MIND = [
    "Le Lundi, ça ne va jamais très fort n'est-ce pas 🥱 ? Mais faut se reprendre !! 💪",
    "Ça va ça va... Un Mardi comme les autres. 😐",
    "Correct ! Mercredi... Il doit y avoir des sorties ciné aujourd'hui ! 🎦🍿",
    f"Ça va ! Ça va ! Savais-tu que dans le temps 👴, dans les années 60 et au début 70, le jeudi était une journée libre pour les enfants ? Maintenant c'est le Mercredi, et encore ça dépend {KNOWMORE('Wikipédia', 'https://fr.wikipedia.org/wiki/Rythmes_scolaires_en_France')}. Que le temps passe vite ! 😔",
    "Oh déjà Vendredi ! Bientôt le week-end ! 😺 À part ça ça va bien !",
    "Bien ! C'est Samedi ! J'espère que tu t'en protites bien ! 😎",
    "Ça va ! C'est Dimanche, mais pour nous les 🤖, pas de repit ! 🦾"
]

INTERROGATE_CLICK_ON_LOGO = "Pourquoi tu appuies sur mon logo, t'es fou ou quoi ? Je suis plus très jeune, c'est fragile ici !!"

ANNOYED = dict(
    n1 = "Mais !?",
    n2 = "Ça va !?",
    n3 = "Tu peux arrêter ??",
    n4 = "C'EST FINI OUI ?",
    n5 = "FRANCHEMENT ?",
    n7 = "Aucune empathie hein :/",
    n9 = "10 fois de suite... OK. T'as gagné.")

ANECDOCTE_STARTER = "Mais t'ai-je déjà raconté l'histoire de ce quartier qui m'a vu en culottes courtes ?"

ADDRESSFOUND = lambda address: f"Bien sûr mon poussin ! La voici : \"{address}\". <br> Et voilà une carte pour t'aider en plus !!"

CURRENT_TIME = lambda user_current_time: f"🕗 Il est {user_current_time}"
NRML_EXTRA = " !!"
DFTZ_EXTRA = lambda gp_current_time: f"... du moins là où tu es car chez moi il est {gp_current_time} ! Que de distance nous sépare, c'est beau internet !🥺"

CURRENT_WEATHER = lambda data: f"Il fait actuellement {data['tcur']}°C à {data['city']}. Les températures min et max de la journée seront respectivement de {data['tmin']}°C et {data['tmax']}°C."
NO_COORDS_GIVEN = f"Désolé, impossible de te donner la météo. As-tu bien accepté que je te géolocalise quand je te l'ai demandé ? 🤔"

FOOTER_TEXT = "2019, 2020 — Créé par Jeffrey G. pour OpenClassrooms."
FOOTER_SNS = "pour en savoir plus"

HT_EXPLAIN_RULES = "OK ! Je tire une pièce au hasard, devine le résultat !<br>Pile ou face ?"
HT_TOSS_COIN = "Je lance la pièce et...<br>"
HT_PLAYER_VICTORY = lambda gr_readable: f"BRAVO ! La réponse est bien {gr_readable}, tu as gagné 🎊!"
HT_PLAYER_DEFEAT = lambda gr_readable: f"PERDU 🤡! La réponse est {gr_readable} ! Une prochaine fois peut-être !"

HT_ERROR = lambda remaining : f"Désolé, je n'ai pas compris ta réponse. Peux-tu recommencer ? Il te reste {remaining} essai{'s' if remaining > 1 else ''} !!<br>Pile ou face ?"
HT_OUT_OF_TRIES = "Désolé, tu as épuisé tes essais ! Le jeu pile ou face est terminé ! À une prochaine fois peut-être 🎲!"

# Dans la V3 ?:
    # Quel est le sens de la vie
    # Raconte moi une blague
    # Tic tac toe 