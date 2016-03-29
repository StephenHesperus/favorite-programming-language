#!/usr/bin/env python
import os

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
def test(coverage=False):
    '''Run all the tests.'''
    import unittest
    unit_tests = unittest.TestLoader().discover('tests')
    functional_tests = unittest.TestLoader().discover(
        'tests', pattern='functional*.py')
    tests = unittest.TestSuite(tests=(unit_tests, functional_tests))

    if coverage:
        import coverage as coveragepy
        cov = coveragepy.coverage(branch=True, include='app/*')
        cov.start()

    unittest.TextTestRunner(verbosity=2).run(tests)

    if coverage:
        cov.stop()
        cov.save()
        print('-'*80, 'Coverage Summary:', sep='\n')
        cov.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'covhtml')
        cov.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        cov.erase()


@manager.command
def deploy():
    """Run deployment tasks."""
    from flask.ext.migrate import upgrade

    # migrate database to latest revision
    upgrade()

    # initialize database


if __name__ == '__main__':
    manager.run()
