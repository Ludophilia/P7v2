#Obj : écrire un formulaire qui contient un champ texte et un formulaire de validation

#Comment faire pour créer le formulaire avec le TDD ? Je ne peux rien écrire tant que je n'ai pas écrit les tests... Oh, on va quand même mettre le code en commentaire et le décommenter une fois le code  

from flask_wtf import FlaskForm #Faut-il tester les imports ? Du genre : assert FlaskForm in flask_wtf ? #Pour le moment, je passe, on verra avec le code coverage
from wtforms.fields import TextAreaField, SubmitField  
from wtforms.validators import DataRequired

class Form(FlaskForm):
    textarea = TextAreaField("Discutez avec GrandPy", validators=[DataRequired()])
    submit_button = SubmitField("envoyer")