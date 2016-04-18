from functools import wraps

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


def id_in_session_required(f):
    '''
    View decorator for main blueprint: make sure ``id`` is set in ``session``,
    otherwise return to home page :http:get:`/`.
    '''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        id_ = session.get('question_id')
        if id_ is None:
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


@main.route('/')
def index():
    '''
    .. http:get:: /question

       Home Page.
    '''
    session['question_id'] = 1
    return render_template('index.html')


@main.route('/question', methods=['GET', 'POST'])
@id_in_session_required
def question():
    '''
    .. http:get:: /question

       Show a question form on the page.

    .. http:post:: /question

       Check user's answer against database record.

       :form answer: The user's answer(yes/no) to the question
       :status 302: When the game is not started from index page,
                      redirect to :http:get:`/`
                    when there's no more question,
                      redirect to :http:get:`/new_language`
                    when form parameters are missing,
                      return to the same page
                    when there's a guess,
                      redirect to :http:get:`/guess`
    '''
    id_ = session.get('question_id')
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
@id_in_session_required
def guess():
    '''
    .. http:get:: /guess

       Show a guess result form on the page.

    .. http:post:: /guess

       See if the user agree with our guess.

       :form result: The user agrees/disagrees(yes/no) with the guess
       :status 302: When the game is not started from index page,
                      redirect to :http:get:`/`
                    when form parameters are missing,
                      return to the same page
                    when the user agrees with the guess,
                      finish the game, redirect to :http:get:`/`
                    when the user disagrees with the guess,
                      redirect to the next question :http:get:`/question`
    '''
    id_ = session.get('question_id')
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
@id_in_session_required
def new_language():
    '''
    .. http:get:: /new_language

       Show a new language test submission form.

    .. http:post:: /new_language

       Add a new language test to the database.

       :form question: The question of the test
       :form answer: The answer to the question
       :form language: The language name for the question
       :status 302: When the game is not started from index page,
                      redirect to :http:get:`/`
                    when form parameters are missing,
                      return to the same page
                    when the language test is added,
                      finish the game, redirect to :http:get:`/`
    '''
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
    '''
    .. note:: For development only, to use it, make sure
       :attr:`current_app.testing` is ``True``.

    Shut down the developement server.
    '''
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...', 200
