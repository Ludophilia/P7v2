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
    
    return render_template("page.html", form=form, api_key=api_key)

@app.route('/grandpy', methods=['GET', 'POST'])
def test():
    if request.method == "POST":
        gp = GrandPy()
        user_message = request.data.decode("utf-8")
        answer = gp.answer_message(user_message)

        return answer