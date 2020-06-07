""" Données utilisées pour construire les réponses de GrandPy """

GREETINGS = ["Bonjour!", "Salut!", "Yo!", "Hi!!"]
ADDRESSFOUND = lambda address: "Bien sûr mon poussin ! La voici : {}.\n".format(address)
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
KNOWMORE = lambda source, url: "[En savoir plus sur <a href='{1}' target='_blank'>{0}</a>]".format(source, url)


# Après les réponses supplémentaires :
    # Welcome speech, (ce que grandpy peut faire)
    # comment vas-tu, (aléatoire)
    # quelle heure est-il, 
    # quel temps il fait)