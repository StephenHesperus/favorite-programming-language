'''
This test file is an attempt from me writing tests for my code.
The tests will contain two parts: one is to test the application control flow,
and the other to unit test.
'''

import os
import unittest
import tempfile

from selenium import webdriver

import app


# functional tests
class FavProgLangTestCase(unittest.TestCase):
    '''
    Things to test:
    1. index page -> question page
    2. question page -> guess correct -[yes]-> index page
    3. guess correct -[no]-> has more questions -[yes]-> question page
    4. guess correct -[no]-> has more questions -[no]-> add new language
       page
    5. add new language page -> index page
    '''

    def setUp(self):
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()
        app.init_db()
        self.index_page_url = 'http://127.0.0.1:5000/'
        self.driver = webdriver.Chrome()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])
        self.driver.close()

    def test_index_page_can_go_to_question_page(self):
        resp = self.app.get('/')
        question = b'/question'
        self.assertIn(question, resp.data,
                      'Question page url is not in index page.')

    def test_question_has_a_correct_guess_finish_game(self):
        """
        This test tests this story:
        Index Page -> Question Page -> Have A Guess? -[Yes]-> Guess Page
            -> Guess Correct? -[Yes]-> Index Page
        During test, we assume the first record in database language test
        table is:
        LanguageTest('Is it interpreted?', True, 'Python')
        """
        driver = self.driver
        # index page to question page
        driver.get(self.index_page_url)
        qlink = driver.find_element_by_tag_name('a')
        qlink.click()
        # question page, choose yes, we have a guess result for it
        qyes = driver.find_element_by_css_selector('input[value="yes"]')
        qsubmit = driver.find_element_by_css_selector('input[type="submit"]')
        self.assertIsNotNone(
            qyes, 'Question answer yes radio button should exist.')
        self.assertIsNotNone(qsubmit, 'Question submit button should exist.')
        qyes.click()
        qsubmit.click()
        # guess page, we guess correctly
        gyes = driver.find_element_by_css_selector('input[value="yes"]')
        gsubmit = driver.find_element_by_css_selector('input[type="submit"]')
        self.assertIsNotNone(
            gyes, 'Guess correctness yes radio button should exist.')
        self.assertIsNotNone(gsubmit, 'Guess submit button should exist.')
        gyes.click()
        gsubmit.click()
        # redirect to index page
        self.assertEqual(
            driver.current_url, self.index_page_url,
            'It should redirect to index page %s now.' % self.index_page_url)


if __name__ == '__main__':
    unittest.main()
