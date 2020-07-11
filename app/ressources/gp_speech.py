""" Données utilisées pour construire les réponses de GrandPy """

GREETINGS = ["Bonjour!", "Salut!", "Yo!", "Hi!!", "👋"]

SORRY = "Désolé, je n'ai compris ta réponse :/ Dans une prochaine version (v3) peut-être ?"

INTERROGATE_CLICK_ON_LOGO = "Pourquoi tu appuies sur mon logo, t'es fou ou quoi ? Je suis plus très jeune, c'est fragile ici !!"
ANNOYED = dict(
    n1 = "Mais !?",
    n2 = "Ça va !?",
    n3 = "Tu peux arrêter ??",
    n4 = "C'EST FINI OUI ?",
    n5 = "FRANCHEMENT ?",
    n7 = "Aucune empathie hein :/",
    n9 = "10 fois de suite..."
)
ANECDOCTE_STARTER = "Mais t'ai-je déjà raconté l'histoire de ce quartier qui m'a vu en culottes courtes ?"

ADDRESSFOUND = lambda address: f"<span>Bien sûr mon poussin ! La voici : \"{address}\". <br> Et voilà une carte pour t'aider en plus !!</span>"

KNOWMORE = lambda source, url: f"[En savoir plus sur <a href='{url}' target='_blank'>{source}</a>]"

FOOTER = """
        <div id="footer_container">
            <div id="footer_text">
                2019, 2020 — Créé par Jeffrey G. pour OpenClassrooms.
            </div>
            <div id="footer_sns">
                <a href="https://github.com/Ludophilia/P7v2" target="_blank">
                    <img src="static/img/GitHub-Mark-Light-32px.png" alt="Octocat" width="25" height="25"/>
                </a><span>pour en savoir plus</span>
            </div>
        </div>
        """

STARTER = """<span>Salut 👋, qu'est-ce que je peux faire pour toi ?<br><br>
        Tu peux me demander:<br>
        - L'adresse d'OpenClassrooms (ex: "tu connais l'adresse d'OC ?")<br>
        - Quelle heure il est<br>
        - Quel temps il fait aujourd'hui<br>
        <br>
        ...Ou tout simplement me saluer ou me demander comment je vais, ça fait toujours plaisir !
        </span>
        """


# Après les réponses supplémentaires :
    # comment vas-tu, (aléatoire)
    # quelle heure est-il, 
    # quel temps il fait)
    # Pile ou face ???