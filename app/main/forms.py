from flask.ext.wtf import Form
from wtforms import RadioField
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import Required


class QuestionForm(Form):
    answer = RadioField('Answer', choices=[('yes', 'Yes'), ('no', 'No')],
                        validators=[Required()])
    submit = SubmitField()


class GuessResultForm(Form):
    result = RadioField('Result', choices=[('yes', 'Yes'), ('no', 'No')],
                        validators=[Required()])
    submit = SubmitField()


class NewLanguageForm(Form):
    language = StringField('New Language Name')
    question = StringField('What makes this language different than others?')
    answer = RadioField('The answer to your question is',
                        choices=[('yes', 'Yes'), ('no', 'No')])
    submit = SubmitField()
