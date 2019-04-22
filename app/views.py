from flask import Flask, render_template, redirect, request # , url_for
from app.forms import Form
import json

app = Flask("app") #ou __name__ vu que __name__ == "app"
app.config.from_object("config") 

@app.route('/', methods=['GET', 'POST'])
def index():
    form = Form()
    return render_template("page.html", form=form)

#Qu'est-ce que j'essaie de faire ? 

# Il faut écrire ici qqch qui peut gérer ce que le front-end lui aurait envoyé. 
#Comment gérer une requete POST avec flask

@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == "POST":
        request_data_str = request.data.decode("utf-8") #Du bytes converti en str
        if "bonjour" in request_data_str.split() or "Bonjour" in request_data_str.split():
            return "Bonjour"
        else:
            return "Désolé, je ne comprends rien d'autre que bonjour ou Bonjour... Et oui je suis borné moi :)"