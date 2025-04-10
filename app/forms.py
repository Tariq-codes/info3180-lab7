from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired

class MovieForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    description = TextAreaField('Movie Description', validators=[DataRequired()])
    poster = FileField('Movie Poster', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Only image files are allowed!')])