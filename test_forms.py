from app.forms import * 
from wtforms.fields import TextAreaField, SubmitField  
from wtforms.validators import DataRequired

#Essayons le code coverage pour avoir une idée si on doit tester les imports. Comment on teste des imports dans Python

# def test_imports():
#     assert FlaskForm in flask_wtf



# def test_form():
#     # print(Form.textarea)
#     # print(TextAreaField("Discutez avec GrandPy", validator=DataRequired))
#     assert Form.textarea == TextAreaField("Discutez avec GrandPy", validator=DataRequired) #marche pas,  Essayons de voir quelle valeur ça a avec pytest -s : et pourtant : <UnboundField(TextAreaField, ('Discutez avec GrandPy',), {'validator': <class 'wtforms.validators.DataRequired'>})> == <UnboundField(TextAreaField, ('Discutez avec GrandPy',), {'validator': <class 'wtforms.validators.DataRequired'>})>.