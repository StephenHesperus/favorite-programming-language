from . import db


class LanguageTest(db.Model):
    '''
    The language test model.

    :param int id: The primary key, starting from 1
    :param str question: The question of the language test
    :param bool answer: The answer to the question
    :param str language: The language name of the language test
    '''
    __tablename__ = 'languagetests'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.Boolean, nullable=False)
    language = db.Column(db.String(50), nullable=False)

    @staticmethod
    def init(db):
        '''
        Initialize the table using database db. Put some tests record in the
        table.

        :param db: The database extension instance
        :type db: ``SqlAlchemy``
        :return: ``None``
        '''
        langtest = LanguageTest('Is it interpreted?', True, 'Python')
        db.session.add(langtest)
        db.session.commit()

    def __init__(self, question, answer, language):
        self.question = question
        self.answer = answer
        self.language = language

    def __repr__(self):
        '''Representation.'''
        return '<LanguageTest q=%r, a=%r, lang=%r>' % (
                self.question, self.answer, self.language)

    def __eq__(self, other):
        '''
        As long as the three fields: question, answer and language
        are the same, then those two records are considered equal.
        '''
        return (type(other) == type(self) and
                self.question == other.question and
                self.answer == other.answer and
                self.language == other.language)


def get_question(id_):
    '''
    Get the question field of a LanguageTest record with ``id==id_``. If the
    LanguageTest can't be found, then return ``None``.

    :param int id_: The id field of a LanguageTest record
    :return: The question field of the LanguageTest record
    :rtype: str, ``None``
    '''
    t = LanguageTest.query.filter_by(id=id_).first()
    if t is not None:
        return t.question

def check_answer(id_, answer):
    '''
    Check if the answer is the same as the answer field in the LanguageTest
    record with ``id==id_``.

    :param int id_: The id field of a LanguageTest record
    :param bool answer: The answer to check
    :return: The check result
    :rtype: bool, ``None``
    '''
    t = LanguageTest.query.filter_by(id=id_).first()
    if t is not None:
        return t.answer == answer

def get_language(id_):
    '''
    Get the language field of a LanguageTest record with ``id==id_``. If the
    LanguageTest can't be found, then return ``None``.

    :param int id_: The id field of a LanguageTest record
    :return: The language field of the LanguageTest record
    :rtype: str, ``None``
    '''
    t = LanguageTest.query.filter_by(id=id_).first()
    if t is not None:
        return t.language
