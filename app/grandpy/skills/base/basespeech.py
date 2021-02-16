""" Données utilisées pour construire les réponses de GrandPy """

STARTER = """Salut 👋, qu'est-ce que je peux faire pour toi ?<br><br>
        Tu peux me demander, dans le formulaire juste en bas avec 'Nouveau message' écrit dedans :<br><br>
        - "Tu connais l'adresse de (un lieu de ton choix)" pour obtenir l'adresse d'un 🏫 , n'oublie pas le '?' si tu mets plusieurs questions !<br>
        - "Quel temps fait-il ?" pour obtenir la météo ⛅️ de ton lieu (📍localisation nécessaire) !<br>
        - "Quelle heure il est ?" pour obtenir l'heure 🕓 qu'il est !<br>
        - "Jouons à pile ou face" si tu veux jouer au jeu du même nom 🎲 !<br>
        - "T'as des infos sur ce site ?" pour obtenir des infos sur ce site 📁 !<br>
        <br>
        Sinon, tu peux toujours m'envoyer un "salut" ou une "👋" pour me saluer 👊 ou me demander "comment tu vas" pour prendre des nouvelles 🍺, ça fait toujours plaisir !
        """

SORRY = "Désolé, je n'ai pas compris ton message... 😕 Dans une prochaine version peut-être ?"

INTERROGATE_CLICK_ON_LOGO = "Pourquoi tu appuies sur mon logo, t'es fou ou quoi ? Je suis plus très jeune, c'est fragile ici !!"

ANNOYED = dict(
    n1 = "Mais !?",
    n2 = "Ça va !?",
    n3 = "Tu peux arrêter ??",
    n4 = "C'EST FINI OUI ?",
    n5 = "FRANCHEMENT ?",
    n7 = "Aucune empathie hein :/",
    n9 = "10 fois de suite... OK. T'as gagné."
)

HT_REMINDER = lambda waiting_for_htev, remaining: f"<br><br> ET... AH OUI! Un jeu pile ou face est toujours en cours : il te reste encore {remaining} essai{'s' if remaining > 1 else ''}!" if waiting_for_htev else ""

# Dans la V3 ?:
    # Quel est le sens de la vie
    # Raconte moi une blague
    # Tic tac toe 