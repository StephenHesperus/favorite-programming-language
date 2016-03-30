import unittest

from app import create_app
from app import db
from app.models import LanguageTest
from app.models import get_question
from app.models import get_language
from app.models import check_answer


class ModelTestCaseBase(unittest.TestCase):

    def setUp(self):
        app = create_app('testing')
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()


class LanguageTestModelTestCase(ModelTestCaseBase):

    def test_properties(self):
        lt = LanguageTest('Is it interpreted?', True, 'Python')
        self.assertEqual(lt.question, 'Is it interpreted?')
        self.assertEqual(lt.answer, True)
        self.assertEqual(lt.language, 'Python')

    def test_init(self):
        questions = LanguageTest.query.all()
        self.assertEqual(questions, [], 'LanguageTest records should be empty.')

        lt = LanguageTest('Is it interpreted?', True, 'Python')
        db.session.add(lt)
        db.session.commit()
        questions = LanguageTest.query.all()
        self.assertEqual(questions, [lt],
                         '%r should be in database now.' % lt)

    def test___repr__(self):
        lt = LanguageTest('Is it interpreted?', True, 'Python')
        self.assertEqual(
            repr(lt),
            "<LanguageTest q='Is it interpreted?', a=True, lang='Python'>")

    def test___eq__(self):
        lt1 = LanguageTest('Is it interpreted?', True, 'Python')
        lt2 = LanguageTest('Is it interpreted?', True, 'Python')
        lt3 = LanguageTest('Does it enforce indentation?', False, 'Ruby')
        self.assertEqual(lt1, lt2)
        self.assertNotEqual(lt1, lt3)

    def test_get_question(self):
        lt = LanguageTest('Is it interpreted?', True, 'Python')
        db.session.add(lt)
        db.session.commit()

        question = get_question(100)
        self.assertIsNone(question, 'question should be None.')
        question = get_question(1)
        self.assertEqual(question, lt.question)

    def test_get_language(self):
        lt = LanguageTest('Is it interpreted?', True, 'Python')
        db.session.add(lt)
        db.session.commit()

        language = get_language(100)
        self.assertIsNone(language, 'language should be None.')
        language = get_language(1)
        self.assertEqual(language, lt.language)

    def test_check_answer(self):
        lt = LanguageTest('Is it interpreted?', True, 'Python')
        db.session.add(lt)
        db.session.commit()

        has_guess1 = check_answer(1, True)
        self.assertTrue(has_guess1, 'has_guess1 should be True.')
        has_guess2 = check_answer(1, False)
        self.assertFalse(has_guess2, 'has_guess2 should be False.')
