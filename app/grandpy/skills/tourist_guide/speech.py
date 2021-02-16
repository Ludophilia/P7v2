""" Données utilisées pour construire les réponses de GrandPy """

ANECDOTE_STARTER = "Mais t'ai-je déjà raconté l'histoire de ce quartier "\
    "qui m'a vu en culottes courtes ?"
NO_ANECDOTE = "Désolé, je n'ai pas d'anecdote sur ce lieu! Wikip... "\
    "JE ne sais pas tout non plus ! 😅"

ADDRESSFOUND = lambda address: f"Bien sûr mon poussin ! La voici : "\
     f"\"{address}\". <br> Et voilà une carte pour t'aider en plus !!"
KNOWMORE = lambda source, url: f"[En savoir plus sur <a href='{url}' "\
     f"target='_blank'>{source}</a>]"

NO_ADDRESS = "Désolé, je n'ai pas d'adresse pour ce lieu... 😞"