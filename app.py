import os

from flask import Flask
from flask import render_template
from flask import url_for
from flask import redirect
from flask import session
from flask.ext.wtf import Form
from wtforms import RadioField
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy


basedir = os.path.abspath(os.path.dirname(__name__))
app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'EVtH`,}c?K=/cR!l4l?.iqe>n^A<<~Z8qUmt9K3|oZ/>GSK|$Eu7nQC\'o;EIIBB9Xep{<1HTjSY4W!kB*!nwd_c1ryc7LO?/XP60eko}n}]>!T*Zi_[B0H"X"Z@0s)HTu>J`6"wx+]B~"n4IuE@#2|j=:|n7\'dtVR-t?Vb0o2x|ftFq>LNp~\'kul19WS8.yqv@j/4(VeS+_UKs`V{SQ9G}-s6~/qrbFXF[Nwh{H<xXahk}S<EnQrYj3=..Q@/Y?2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
        os.path.join(basedir, 'data.sqlite')


class LanguageTest(db.Model):
    __tablename__ = 'languagetests'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.Boolean, nullable=False)
    language = db.Column(db.String(50), nullable=False)

    @staticmethod
    def init():
        langtest = LanguageTest('Is it interpreted?', True, 'Python')
        db.session.add(langtest)
        db.session.commit()

    def __init__(self, question, answer, language):
        self.question = question
        self.answer = answer
        self.language = language

    def __repr__(self):
        return '<LanguageTest q=%r, a=%r, lang=%r>' % (
                self.question, self.answer, self.language)


class GuessGame(object):

    def get_question(self, id_):
        t = LanguageTest.query.filter_by(id=id_).first()
        if t is not None:
            return t.question

    def check_answer(self, id_, answer):
        t = LanguageTest.query.filter_by(id=id_).first()
        if t is not None:
            return t.answer == answer

    def get_language(self, id_):
        t = LanguageTest.query.filter_by(id=id_).first()
        if t is not None:
            return t.language


game = GuessGame()


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


@app.route('/')
def index():
    session['question_id'] = 1
    return render_template('index.html')


@app.route('/question', methods=['GET', 'POST'])
def question():
    id_ = session.get('question_id')
    if id_ is None:
        return redirect(url_for('index'))

    question = game.get_question(id_)
    if question is None:
        return redirect(url_for('new_language'))

    form = QuestionForm()
    if form.validate_on_submit():
        answer = form.answer.data == 'yes'
        if game.check_answer(id_, answer):
            return redirect(url_for('guess'))
        else:
            session['question_id'] = id_ + 1
            return redirect(url_for('question'))
    return render_template('question.html', question=question, form=form)


@app.route('/guess', methods=['GET', 'POST'])
def guess():
    id_ = session.get('question_id')
    if id_ is None:
        return redirect(url_for('index'))

    lang = game.get_language(id_)
    form = GuessResultForm()
    print('form.result.data before validate', form.result.data,
          form.validate_on_submit())
    if form.validate_on_submit():
        print('form.result.data', form.result.data)
        if form.result.data == 'yes':
            return redirect(url_for('index'))
        else:
            return redirect(url_for('new_language'))
    return render_template('guess.html', result=lang, form=form)


@app.route('/new_language', methods=['GET', 'POST'])
def new_language():
    id_ = session.get('question_id')
    if id_ is None:
        return redirect(url_for('index'))

    form = NewLanguageForm()
    if form.validate_on_submit():
        question = form.question.data
        answer = form.answer.data == 'yes'
        lang = form.language.data
        langtest = LanguageTest(question, answer, lang)
        db.session.add(langtest)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('new_language.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)
