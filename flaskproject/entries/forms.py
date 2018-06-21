from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField
from wtforms import validators

class CreateEntryForm(FlaskForm):
    body = TextAreaField('Body', [validators.Length(min=1, max=300)])
    category_id = SelectField('Category', coerce=int)
    title = StringField('Title', [validators.Length(min=1, max=70)])

class UpdateEntryForm(FlaskForm):
    body = TextAreaField('Body', [validators.Length(min=1, max=300)])
    category_id = SelectField('Category', coerce=int)
    title = StringField('Title', [validators.Length(min=1, max=70)])
