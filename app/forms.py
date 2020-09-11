from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField  
from wtforms.validators import DataRequired

class Form(FlaskForm):
    textarea = TextAreaField("Discutez avec GrandPy", validators=[DataRequired()])