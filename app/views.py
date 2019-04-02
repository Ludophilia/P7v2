from flask import Flask, render_template, redirect # , url_for
from app.forms import Form

app = Flask("app") #ou __name__ vu que __name__ == "app"
app.config.from_object("config") 

@app.route('/', methods=['GET', 'POST'])
def index():
    form = Form()
    if form.validate_on_submit():
        if form.textarea.data == "bonjour":
            return redirect('/bonjour')
        else:
            return redirect('/erreur')
    return render_template("page.html", form=form)

@app.route('/bonjour')
def bonjour():
    return "bonjour"

@app.route('/erreur')
def erreur():
    return "je ne comprends pas"