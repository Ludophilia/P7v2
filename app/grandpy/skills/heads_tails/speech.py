""" Données utilisées pour construire les réponses de GrandPy """

HT_EXPLAIN_RULES = "OK ! Je tire une pièce au hasard, devine le résultat !<br>Pile ou face ?"
HT_TOSS_COIN = "Je lance la pièce et...<br>"
HT_PLAYER_VICTORY = lambda gr_readable: f"BRAVO ! La réponse est bien {gr_readable}, tu as gagné 🎊!"
HT_PLAYER_DEFEAT = lambda gr_readable: f"PERDU 🤡! La réponse est {gr_readable} ! Une prochaine fois peut-être !"

HT_ERROR = lambda remaining : f"Désolé, je n'ai pas compris ta réponse. Peux-tu recommencer ? Il te reste {remaining} essai{'s' if remaining > 1 else ''} !!<br>Pile ou face ?"
HT_OUT_OF_TRIES = "Désolé, tu as épuisé tes essais ! Le jeu pile ou face est terminé ! À une prochaine fois peut-être 🎲!"