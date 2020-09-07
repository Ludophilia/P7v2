import random
from datetime import date

from app.grandpy.skills.social import speech

def say_hello(message):

    """Génère un message de salutation de GrandPy."""

    greetings = speech.GREETINGS
    random_position = random.randint(0,len(greetings)-1)

    message += f"{greetings[random_position]}<br>"

    return message

def give_state_of_mind(message):
    
    """Génère un message où GrandPy explique comment il va."""

    day = date.today().weekday()
    message += f"{speech.STATE_OF_MIND[day]}<br>"

    return message

