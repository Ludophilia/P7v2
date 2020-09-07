import time 

from app.grandpy.skills.clock import speech

def give_time(user_data, message):

    """Génère un message où GrandPy donne l'heure qu'il est en fonction du fuseau horaire de l'utilisateur."""

    user_tzone = user_data.get("options").get("timezone")
    gp_tzone = int((time.altzone if time.daylight else time.timezone) / -3600)

    user_current_time = time.strftime("%H:%M", time.gmtime(time.time() + user_tzone * 3600))
    gp_current_time = time.strftime("%H:%M")

    message += speech.CURRENT_TIME(user_current_time)
    message += speech.DFTZ_EXTRA(gp_current_time) if user_tzone != gp_tzone else speech.NRML_EXTRA
    message += "<br>"

    return message