from flask import session
from flask import render_template
from flask import redirect
from flask import url_for
from flask import abort
from flask import current_app
from flask import request

from . import main
from .forms import QuestionForm
from .forms import GuessResultForm
from .forms import NewLanguageForm
from .. import db
from ..models import get_question
from ..models import get_language
from ..models import check_answer
from ..models import LanguageTest


@main.route('/')
def index():
    session['question_id'] = 1
    return render_template('index.html')


@main.route('/question', methods=['GET', 'POST'])
def question():
    id_ = session.get('question_id')
    if id_ is None:
        return redirect(url_for('.index'))

    question = get_question(id_)
    if question is None:
        return redirect(url_for('.new_language'))

    form = QuestionForm()
    if form.validate_on_submit():
        answer = form.answer.data == 'yes'
        if check_answer(id_, answer):
            return redirect(url_for('.guess'))
        else:
            session['question_id'] = id_ + 1
            return redirect(url_for('.question'))
    return render_template('question.html', question=question, form=form)


@main.route('/guess', methods=['GET', 'POST'])
def guess():
    id_ = session.get('question_id')
    if id_ is None:
        return redirect(url_for('.index'))

    lang = get_language(id_)
    form = GuessResultForm()
    if form.validate_on_submit():
        if form.result.data == 'yes':
            return redirect(url_for('.index'))
        else:
            question = get_question(id_ + 1)
            if question:
                session['question_id'] = id_ + 1
                return redirect(url_for('.question'))
            else:
                return redirect(url_for('.new_language'))
    return render_template('guess.html', result=lang, form=form)


@main.route('/new_language', methods=['GET', 'POST'])
def new_language():
    id_ = session.get('question_id')
    if id_ is None:
        return redirect(url_for('.index'))

    form = NewLanguageForm()
    if form.validate_on_submit():
        question = form.question.data
        answer = form.answer.data == 'yes'
        lang = form.language.data
        langtest = LanguageTest(question, answer, lang)
        db.session.add(langtest)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template('new_language.html', form=form)


@main.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...', 200
