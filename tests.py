'''
This test file is an attempt from me writing tests for my code.
The tests will contain two parts: one is to test the application control flow,
and the other to unit test.
'''

import os
import unittest
import tempfile

import app


# functional tests
class FavProgLangTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()
        app.init_db()

    def tearDown(self):
        #  self.ctx.pop()
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])

    def test_index_page_can_go_to_question_page(self):
        resp = self.app.get('/')
        question = b'/question'
        self.assertIn(question, resp.data,
                      'Question page url is not in index page.')


if __name__ == '__main__':
    unittest.main()
