import unittest

from app import db
from app import create_app


class ViewTestCaseBase(unittest.TestCase):

    def setUp(self):
        app = create_app('testing')
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        db.create_all()

    def tearDown(self):
        self.ctx.pop()
        db.drop_all()


class IndexViewTestCase(ViewTestCaseBase):

    def test_index_page_route(self):
        # Test index page can start the game.
        client = self.client
        resp = client.get('/')
        self.assertIn(b'/question', resp.data,
                      'Question page links should be in index page.')
