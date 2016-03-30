import unittest

from flask import render_template
from flask import url_for
from flask import current_app
from flask import request
from werkzeug.exceptions import InternalServerError

from app import create_app
from app import db


class ErrorTestCaseBase(unittest.TestCase):

    def setUp(self):
        app = create_app('testing')
        self.app = app
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_error_404(self):
        resp = self.client.get('/non_exist_page')
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(render_template('404.html').encode(), resp.data)

    def test_error_500(self):

        @self.app.route('/error_500')
        def error_500():
            raise InternalServerError()

        resp = self.client.get('/error_500')
        self.assertEqual(resp.status_code, 500)
        self.assertEqual(render_template('500.html').encode(), resp.data)

    def test_shut_down(self):
        client = self.client
        app = self.app

        # werkzeug.server.shutdown doesn't exist.
        resp = client.get(url_for('main.server_shutdown'))
        self.assertEqual(resp.status_code, 500)
        self.assertEqual(render_template('500.html').encode(), resp.data)

        # Mock werkzeug.server.shutdown
        environ_base = {'werkzeug.server.shutdown': lambda : None}
        resp = client.get(url_for('main.server_shutdown'),
                          environ_base=environ_base)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, b'Shutting down...', resp.data)

        current_app.testing = False
        resp = client.get(url_for('main.server_shutdown'))
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(render_template('404.html').encode(), resp.data)

