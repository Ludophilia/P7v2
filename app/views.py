from flask import Flask, render_template, redirect, request # , url_for
from app.forms import Form
from app.grandpy import GrandPy
import json

app = Flask("app") #ou __name__ vu que __name__ == "app"
app.config.from_object("config") 

@app.route('/', methods=['GET', 'POST'])
def index():
    form = Form()
    return render_template("page.html", form=form)

@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == "POST":
        
        gp = GrandPy()
        user_message = request.data.decode("utf-8") 
        answer = gp.answer_message(user_message)

        return answer