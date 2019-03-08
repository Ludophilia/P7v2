from flask import Flask

app = Flask("app") #__name__ ça marche aussi vu que __name__ == "app"
app.config.from_object("config") # L'objet config fait référence au module config.py.

from app import views #Il faut que app soit déjà initialisé pour views qui repose sur app soit importé, d'où l'import à la fin