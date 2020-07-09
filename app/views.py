from flask import Flask, render_template, request 
from app.forms import Form
from app.grandpy import GrandPy
import os, config

app = Flask("app") #ou __name__ vu que __name__ == "app"

app.config.from_object("config")

@app.route('/', methods=['GET', 'POST'])
def index():
    form = Form()
    api_key=config.API_KEY
    fa_key=config.FA_KEY
    
    return render_template("page.html", form=form, api_key=api_key, fa_key=fa_key)

@app.route('/grandpy/<path:mode>', methods=['GET', 'POST'])
def grandpy(mode):

    gp = GrandPy()

    if request.method == "POST":

        user_data = request.data.decode("utf-8")

        if mode == "chat/":
            return gp.answer_message(user_data) 
        
        elif mode == "wtf/":
            return gp.deal_with_clicks_on_logo(user_data)
    
    if request.method == "GET":

        if mode == "footer/":
            return gp.give_footer_info()
