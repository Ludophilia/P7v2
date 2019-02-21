from flask import Flask

app = Flask(__name__)
app.config.from_object("configu") #s'ecrit normalement config, mais mal écrit pour voir ce que ça va donner

@app.route('/')
def index():
    return "Hello weirdo !"

if __name__ == "__main__":
    app.run()