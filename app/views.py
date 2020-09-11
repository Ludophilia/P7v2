import json, config

from flask import render_template, request

from app import app
from app.forms import Form
from app.models import Robot, Memory, State, db 
from app.grandpy import GrandPy

@app.route('/', methods=['GET', 'POST'])
def index():
    form = Form()
    gm_api_key=config.GM_API_KEY
    fa_key=config.FA_KEY
    
    return render_template("page.html", form=form, gm_api_key=gm_api_key, fa_key=fa_key)

@app.route('/grandpy/<path:mode>', methods=['GET', 'POST'])
def grandpy(mode):

    user_ip = request.environ.get('HTTP_X_FORWARDED_FOR') or request.remote_addr
    
    if not Robot.query.get(user_ip):
        db.session.add(Robot(id=f"{user_ip}"))
        db.session.commit()
        
    print("[views.py] Robots", Robot.query.all())

    gp = GrandPy(user_ip)

    if request.method == "POST":

        user_data = json.loads(request.data.decode("utf-8"))

        if mode == "chat/":
            return gp.build_response(user_data) 
        
        elif mode == "wtf/":
            return gp.deal_with_clicks_on_logo(user_data)
    
    if request.method == "GET":

        if mode == "starter/":
            return gp.start_conversation()