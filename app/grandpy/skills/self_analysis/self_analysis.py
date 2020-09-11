from app.grandpy.skills.self_analysis import speech

def give_website_info(message):

    """Donne des informations sur le site. Retourne le paramètre str modifié"""

    message += speech.SITE_INFO

    return message
