import unittest

from itertools import zip_longest
from collections import namedtuple

from wtforms import Form
from wtforms.validators import DataRequired
from wtforms import RadioField

from app import create_app
from app.main.forms import QuestionForm
from app.main.forms import GuessResultForm
from app.main.forms import NewLanguageForm


RadioFieldInfo = namedtuple('RadioFieldInfo',
                            ['label', 'choices', 'validator_classes'])
StringFieldInfo = namedtuple('StringFieldInfo', ['label', 'validator_classes'])


class FormTestCase(unittest.TestCase):

    def setUp(self):
        app = create_app('testing')
        self.ctx = app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def assertValidators(self, validators, validator_classes):
        for v, v_class in zip_longest(validators, validator_classes):
            self.assertIsInstance(v, v_class)


class QuestionFormTestCase(FormTestCase):

    def setUp(self):
        super().setUp()
        self.form = QuestionForm()

    def test_answer_field_exist(self):
        answer = getattr(self.form, 'answer')
        self.assertIsNotNone(answer)

    def test_answer_field_properties(self):
        answer = getattr(self.form, 'answer')
        radio = RadioFieldInfo('Answer', [('yes', 'Yes'), ('no', 'No')],
                               [DataRequired])
        self.assertEqual(answer.label.text, radio.label)
        self.assertEqual(answer.choices, radio.choices)
        self.assertValidators(answer.validators, radio.validator_classes)

    def test_submit_field_exist(self):
        self.assertIsNotNone(self.form.submit)


class GuessResultFormTestCase(FormTestCase):

    def setUp(self):
        super().setUp()
        self.form = GuessResultForm()

    def test_result_field_exist(self):
        result = getattr(self.form, 'result')
        self.assertIsNotNone(result)

    def test_result_field_properties(self):
        result = getattr(self.form, 'result')
        radio = RadioFieldInfo('Result', [('yes', 'Yes'), ('no', 'No')],
                               [DataRequired])
        self.assertEqual(result.label.text, radio.label)
        self.assertEqual(result.choices, radio.choices)
        self.assertValidators(result.validators, radio.validator_classes)

    def test_submit_field_exist(self):
        self.assertIsNotNone(self.form.submit)


class NewLanguageFormTestCase(FormTestCase):

    def setUp(self):
        super().setUp()
        self.form = NewLanguageForm()

    def test_language_field_exist(self):
        language = getattr(self.form, 'language')
        self.assertIsNotNone(language)

    def test_language_field_properties(self):
        language = getattr(self.form, 'language')
        langinfo = StringFieldInfo('New Language Name', [DataRequired])
        self.assertEqual(language.label.text, langinfo.label)
        self.assertValidators(language.validators, langinfo.validator_classes)

    def test_question_field_exist(self):
        question = getattr(self.form, 'question')
        self.assertIsNotNone(question)

    def test_question_field_properties(self):
        question = getattr(self.form, 'question')
        langinfo = StringFieldInfo(
            'What makes this language different than others?', [DataRequired])
        self.assertEqual(question.label.text, langinfo.label)
        self.assertValidators(question.validators, langinfo.validator_classes)

    def test_answer_field_exist(self):
        answer = getattr(self.form, 'answer')
        self.assertIsNotNone(answer)

    def test_answer_field_properties(self):
        answer = getattr(self.form, 'answer')
        radio = RadioFieldInfo(
            'The answer to your question is',
            [('yes', 'Yes'), ('no', 'No')], [DataRequired])
        self.assertEqual(answer.label.text, radio.label)
        self.assertEqual(answer.choices, radio.choices)
        self.assertValidators(answer.validators, radio.validator_classes)

    def test_submit_field_exist(self):
        self.assertIsNotNone(self.form.submit)
