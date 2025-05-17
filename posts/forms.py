from wtforms import Form, StringField, TextAreaField
from wtforms.validators import DataRequired

class PostForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])