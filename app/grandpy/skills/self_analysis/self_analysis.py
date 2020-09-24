from app.grandpy.skills.self_analysis import speech

def give_website_info(message):

    """Donne des informations sur le site. Retourne le paramètre str modifié"""

    message += f"{speech.SITE_INFO}<br>"

    return message
