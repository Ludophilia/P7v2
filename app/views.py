from flask import Flask, render_template, request 
from app.forms import Form
from app.grandpy import GrandPy
import os, config, json

app = Flask("app") #ou __name__ vu que __name__ == "app"
app.config.from_object("config")

@app.route('/', methods=['GET', 'POST'])
def index():
    form = Form()
    gm_api_key=config.GM_API_KEY
    fa_key=config.FA_KEY
    
    return render_template("page.html", form=form, gm_api_key=gm_api_key, fa_key=fa_key)

@app.route('/grandpy/<path:mode>', methods=['GET', 'POST'])
def grandpy(mode):

    # Différentes instances de GrandPy.

    # Separation par ip ? Un grandPy par ip ?

        # Si client_ip in ["known_client_ip"]
        # Retourner le grandpy associé à cet ip ?    

    # Il faut aussi un truc pour supprimer les instances de grandpy au bout de 15mn 1h.

    def pick_the_right_grandpy_instance(user_ip):
        
        owners = {"127.0.0.1": GrandPy('127.0.0.1')}

        if user_ip not in owners: 
            owners[user_ip] = GrandPy(user_ip)

        return owners.get(user_ip)
    
    gp = GrandPy()

    print("[views.py] Client IP ?", request.origin)
    print("[views.py] Client IP ?", request.remote_addr)
    print("[views.py] Client IP ?", request.environ['REMOTE_ADDR'])
    print("[views.py] Client IP ?", request.environ.get('HTTP_X_FORWARDED_FOR'))

    if request.method == "POST":

        user_data = json.loads(request.data.decode("utf-8"))

        if mode == "chat/":
            return gp.answer_message(user_data) 
        
        elif mode == "wtf/":
            return gp.deal_with_clicks_on_logo(user_data)
    
    if request.method == "GET":

        if mode == "starter/":
            return gp.start_conversation()