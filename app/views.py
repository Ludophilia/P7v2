import json, config
from flask import Flask, render_template, request
from app import app
from app.ressources.forms import Form
from app.ressources.grandpy import GrandPy
from app.models import Robot, db 
#from app.ressources.gp_manager import pick_the_right_grandpy_instance

@app.route('/', methods=['GET', 'POST'])
def index():
    form = Form()
    gm_api_key=config.GM_API_KEY
    fa_key=config.FA_KEY
    
    return render_template("page.html", form=form, gm_api_key=gm_api_key, fa_key=fa_key)

@app.route('/grandpy/<path:mode>', methods=['GET', 'POST'])
def grandpy(mode):

    # Différentes instances de GrandPy.# Separation par ip ? Un grandPy par ip ?
    # Il faut aussi un truc pour supprimer les instances de grandpy au bout de 15mn/1h.

    user_ip = request.environ.get('HTTP_X_FORWARDED_FOR') or request.remote_addr
    
    # Qu'est-ce qu'on doit faire ? Enregistrer le grandpy ?

    if not Robot.query.get(user_ip):
        db.session.add(Robot(id=f"{user_ip}"))
        db.session.commit()
    print("[views.py] DB", Robot.query.all())
    
    gp = GrandPy(user_ip) ; print("[views.py] gp.owner:", gp.owner)

    if request.method == "POST":

        user_data = json.loads(request.data.decode("utf-8"))

        if mode == "chat/":
            return gp.answer_message(user_data) 
        
        elif mode == "wtf/":
            return gp.deal_with_clicks_on_logo(user_data)
    
    if request.method == "GET":

        if mode == "starter/":
            return gp.start_conversation()