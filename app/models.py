from . import db


class LanguageTest(db.Model):
    __tablename__ = 'languagetests'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.Boolean, nullable=False)
    language = db.Column(db.String(50), nullable=False)

    @staticmethod
    def init(db):
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

    def __eq__(self, other):
        return (self.question == other.question and
                self.answer == other.answer and
                self.language == other.language)


def get_question(id_):
    t = LanguageTest.query.filter_by(id=id_).first()
    if t is not None:
        return t.question

def check_answer(id_, answer):
    t = LanguageTest.query.filter_by(id=id_).first()
    if t is not None:
        return t.answer == answer

def get_language(id_):
    t = LanguageTest.query.filter_by(id=id_).first()
    if t is not None:
        return t.language
