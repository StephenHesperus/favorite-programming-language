'''
This test file is an attempt from me writing tests for my code.
The tests will contain two parts: one is to test the application control flow,
and the other to unit test.
'''

import os
import unittest
import tempfile

import app

from selenium import webdriver
from app import LanguageTest


# functional tests
class FavProgLangTestCase(unittest.TestCase):
    '''
    Things to test:
        - All the flows in app-flow-chart.svg
        - Can't go to any other pages without starting from index page
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

    def test_no_guess_for_question_has_more_questions_go_to_next_question(self):
        """
        This test tests this story:
        Index Page -> Question Page -> Have A Guess?
            -[No]-> Has More Questions? -[Yes]-> Question Page
        During test, we assume the first two records in database language test
        table are:
        LanguageTest('Is it interpreted?', True, 'Python')
        LanguageTest('Does it enforce indentation?', False, 'Ruby')
        """
        # Setup test database
        lt = LanguageTest('Does it enforce indentation?', False, 'Ruby')
        app.db.session.add(lt)
        app.db.session.commit()

        driver = self.driver
        # Index page to question page
        driver.get(self.index_page_url)
        qlink = driver.find_element_by_tag_name('a')
        qlink.click()
        # Question page, choose no, we don't have a guess result for it
        qno = driver.find_element_by_css_selector('input[value="no"]')
        qsubmit = driver.find_element_by_css_selector('input[type="submit"]')
        self.assertIsNotNone(
            qno, 'Question answer no radio button should exist.')
        self.assertIsNotNone(qsubmit, 'Question submit button should exist.')
        qno.click()
        qsubmit.click()
        # We should go back to question page now, which shows the second
        # question.
        self.assertEqual(driver.current_url, self.index_page_url + 'question',
                         'We should be at question page now.')

    @unittest.skip('WIP')
    def test_guess_wrongly_no_more_questions_go_to_new_language_page(self):
        pass


if __name__ == '__main__':
    unittest.main()
