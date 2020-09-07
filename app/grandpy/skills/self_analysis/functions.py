from app.grandpy.skills.self_analysis import speech

def give_website_info(message):

    """Donne des informations sur le site. Retourne le paramètre str modifié"""

    project_glink = """
    <span id="footer_sns">
        <a href="https://github.com/Ludophilia/P7v2" target="_blank">
            <img src="static/img/GitHub-Mark-Light-32px.png" alt="Octocat" width="25" height="25"/>
        </a>
    </span>
    """

    message += speech.SITE_INFO(project_glink)

    return message
