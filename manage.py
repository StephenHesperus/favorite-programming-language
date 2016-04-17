#!/usr/bin/env python
import os

# Start coverage as early as possible.
COV = None
if os.environ.get('COVERAGE') is not None:
    import coverage as coveragepy
    COV = coveragepy.coverage(branch=True, include='app/*')
    COV.start()

from flask.ext.script import Manager
from flask.ext.script import Shell
from flask.ext.migrate import Migrate
from flask.ext.migrate import MigrateCommand

from app import create_app
from app import db
from app.models import LanguageTest


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, LanguageTest=LanguageTest)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test(coverage=False, no_functional=False):
    '''Run all the tests.'''

    import unittest
    unit_tests = unittest.TestLoader().discover('tests')
    ftests = unittest.TestLoader().discover(
        'tests', pattern='functional*.py')
    if no_functional:
        tests = unit_tests
    else:
        tests = unittest.TestSuite(tests=(unit_tests, ftests))

    unittest.TextTestRunner(verbosity=2).run(tests)

    if coverage and COV is not None:
        COV.stop()
        COV.save()
        print('-'*80, 'Coverage Summary:', sep='\n')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'covhtml')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()


@manager.command
def populate_db():
    '''Populate database with initial data.'''
    from app.models import LanguageTest
    # initialize database
    LanguageTest.init(db)


if __name__ == '__main__':
    manager.run()
