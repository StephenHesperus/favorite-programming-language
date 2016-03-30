import unittest

from flask import url_for
from flask import render_template

from app import db
from app import create_app
from app.models import LanguageTest
from app.models import get_question
from app.main.forms import QuestionForm
from app.main.forms import GuessResultForm
from app.main.forms import NewLanguageForm


class ViewTestCaseBase(unittest.TestCase):

    def setUp(self):
        app = create_app('testing')
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        db.create_all()
        # This will add one row to the database:
        # LanguageTest('Is it interpreted?', True, 'Python')
        LanguageTest.init(db)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()


class IndexViewTestCase(ViewTestCaseBase):

    def test_index_view_get(self):
        # Test index page can start the game.
        client = self.client
        resp = client.get(url_for('main.index'))
        self.assertIn(url_for('main.question').encode(), resp.data,
                      'Question page links should be in index page.')


class QuestionViewTestCase(ViewTestCaseBase):

    def test_question_view_get_redirect_to_index_view(self):
        # Test going directly to question page redirects to index page.
        client = self.client
        resp = client.get(url_for('main.question'), follow_redirects=True)
        self.assertEqual(render_template('index.html').encode(), resp.data,
            'Going directly to question should redirect to index page.')

    def test_question_view_get_show_question_form(self):
        client = self.client
        # With proper session data, the question page now shows.
        with client.session_transaction() as sess:
            sess['question_id'] = 1
        resp = client.get(url_for('main.question'), follow_redirects=True)
        q, yes, no, submit = b'Is it interpreted?', b'Yes', b'No', b'submit'
        for el in [q, yes, no, submit]:
            self.assertIn(el, resp.data,
                '"%s" should be in response data.' % el.decode())
        self.assertIn(url_for('main.index').encode(), resp.data,
            'Index page link should be in question page.')

    def test_question_view_get_redirect_to_new_language_view(self):
        client = self.client
        with client.session_transaction() as sess:
            sess['question_id'] = 2
        resp = client.get(url_for('main.question'), follow_redirects=True)
        self.assertEqual(
            render_template('new_language.html', form=NewLanguageForm()),
            resp.data.decode(),
            'No more question leads to new language view.')

    def test_question_view_post_redirect_to_guess_view(self):
        client = self.client
        with client.session_transaction() as sess:
            sess['question_id'] = 1
        resp = client.post(url_for('main.question'), data=dict(
                answer='yes'
            ), follow_redirects=True)
        self.assertEqual(resp.data.decode(), render_template(
                'guess.html', form=GuessResultForm(), result='Python'
            ), 'Have a guess to the question redirects to guess page.')

    def test_question_view_post_redirect_to_question_view(self):
        '''Test no guess to the current question leads to the next question.'''
        # Add another record to the database so that we have another question
        # to redirect to.
        lt = LanguageTest('Does it enforce indentation?', False, 'Ruby')
        db.session.add(lt)
        db.session.commit()

        client = self.client
        with client.session_transaction() as sess:
            sess['question_id'] = 1
        resp = client.post(url_for('main.question'), data=dict(
                answer='no'
            ), follow_redirects=True)
        q = get_question(sess['question_id'] + 1)
        self.assertEqual(resp.data.decode(), render_template(
                'question.html', form=QuestionForm(), question=q
            ), 'No guess to the question redirects to the next question.')
