""" Données utilisées pour construire les réponses de GrandPy """

GREETINGS = ["Bonjour!", "Salut!", "Yo!", "Hi!!"]

SORRY = "Désolé, je ne sais rien faire d'autre que saluer ou donner une certaine adresse... :/"

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

ADDRESSFOUND = lambda address: f"Bien sûr mon poussin ! La voici : {address}.\n"

KNOWMORE = lambda source, url: f"[En savoir plus sur <a href='{url}' target='_blank'>{source}</a>]"

FOOTER = """
        <div id="footer_text">
            2019, 2020 — Créé par Jeffrey G. pour OpenClassrooms.
        </div>
        <div id="footer_sns">
            <a href="https://github.com/Ludophilia/P7v2" target="_blank">
                <img src="static/img/GitHub-Mark-Light-32px.png" alt="Octocat" width="25" height="25"/>
            </a><span>pour en savoir plus</span>
        </div>
        """

# Après les réponses supplémentaires :
    # Welcome speech, (ce que grandpy peut faire)
    # comment vas-tu, (aléatoire)
    # quelle heure est-il, 
    # quel temps il fait)