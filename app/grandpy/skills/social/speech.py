""" Données utilisées pour construire les réponses de GrandPy """

GREETINGS = ["Bonjour!", "Salut!", "Yo!", "Hi!!", "👋"]

KNOWMORE = lambda source, url: f"[En savoir plus sur <a href='{url}' target='_blank'>{source}</a>]"

STATE_OF_MIND = [
    "Le Lundi, ça ne va jamais très fort n'est-ce pas 🥱 ? Mais faut se reprendre !! 💪",
    "Ça va ça va... Un Mardi comme les autres. 😐",
    "Correct ! Mercredi... Il doit y avoir des sorties ciné aujourd'hui ! 🎦🍿",
    f"Ça va ! Ça va ! Savais-tu que dans le temps 👴, dans les années 60 et au début 70, le jeudi était une journée libre pour les enfants ? Maintenant c'est le Mercredi, et encore ça dépend {KNOWMORE('Wikipédia', 'https://fr.wikipedia.org/wiki/Rythmes_scolaires_en_France')}. Que le temps passe vite ! 😔",
    "Oh déjà Vendredi ! Bientôt le week-end ! 😺 À part ça ça va bien !",
    "Bien ! C'est Samedi ! J'espère que tu t'en protites bien ! 😎",
    "Ça va ! C'est Dimanche, mais pour nous les 🤖, pas de repit ! 🦾"
]