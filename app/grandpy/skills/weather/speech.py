""" Données utilisées pour construire les réponses de GrandPy """

CURRENT_WEATHER = lambda data: f"Il fait actuellement {data['tcur']}°C à {data['city']}. Les températures min et max pour le reste de la journée seront respectivement de {data['tmin']}°C et {data['tmax']}°C."
NO_COORDS_GIVEN = f"Désolé, impossible de te donner la météo. As-tu bien accepté que je te géolocalise quand je te l'ai demandé ? 🤔"
