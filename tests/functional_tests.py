import unittest
import threading

from selenium import webdriver

from app import db
from app import create_app
from app.models import LanguageTest


class FavProgLangTestCase(unittest.TestCase):
    '''
    Things to test:
        x All the flows in wiki/app-flow-chart.svg
        x Can't go to any other pages without starting from index page
    Setup:
        - A running testing server hosting the application
    '''

    index_page_url = 'http://127.0.0.1:5000/'

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('testing')

        # Suppress logging to keep unittest output clean
        import logging
        logger = logging.getLogger('werkzeug')
        logger.setLevel('ERROR')

        # Start the Flask server.
        threading.Thread(target=cls.app.run).start()

        #  cls.driver = webdriver.Chrome()
        cls.driver = webdriver.Firefox()
        cls.ctx = cls.app.app_context()
        cls.ctx.push()

        db.create_all()
        # Populate database with data.
        LanguageTest.init(db)

    @classmethod
    def tearDownClass(cls):
        cls.driver.get(cls.index_page_url + 'shutdown')
        cls.driver.close()
        db.drop_all()
        db.session.remove()
        cls.ctx.pop()

    def setUp(self):
        db.create_all()
        self.driver.delete_all_cookies()

    def tearDown(self):
        pass

    def test_index_page_can_go_to_question_page(self):
        driver = self.driver
        driver.get(self.index_page_url)
        qlink = driver.find_element_by_tag_name('a')
        self.assertIn('/question', qlink.get_attribute('href'),
                      'Question page url is not in index page.')

    def test_question_has_a_correct_guess_finish_game(self):
        """
        This test tests this story:
        Index Page -> Question Page -> Have A Guess? -[Yes]-> Guess Page
            -> Guess Correct? -[Yes]-> Index Page
        During test, we assume the _first_ record in database language test
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
        During test, we assume the _first two_ records in database language test
        table are:
        LanguageTest('Is it interpreted?', True, 'Python')
        LanguageTest('Does it enforce indentation?', False, 'Ruby')
        """
        # Setup test database
        lt = LanguageTest('Does it enforce indentation?', False, 'Ruby')
        db.session.add(lt)
        db.session.commit()

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

    def test_cannot_guess_language_go_to_new_language_page_finish_game(self):
        """
        This test tests this story:
        Index Page -> Question Page -> Have A Guess? -[Yes]-> Guess Page
            -> Guess Correct? -[No]-> Has More Questions?
            -[No]-> Add New Language Page -> Index Page
        During test, we assume the _only_ record in database language test
        table is:
        LanguageTest('Is it interpreted?', True, 'Python')
        """
        driver = self.driver
        # Index page to question page
        driver.get(self.index_page_url)
        qlink = driver.find_element_by_tag_name('a')
        qlink.click()
        # Question page, choose yes, we have a guess result for it
        qyes = driver.find_element_by_css_selector('input[value="yes"]')
        qsubmit = driver.find_element_by_css_selector('input[type="submit"]')
        self.assertIsNotNone(
            qyes, 'Question answer yes radio button should exist.')
        self.assertIsNotNone(qsubmit, 'Question submit button should exist.')
        qyes.click()
        qsubmit.click()
        # Guess page, choose _no_, our guess is wrong
        gno = driver.find_element_by_css_selector('input[value="no"]')
        gsubmit = driver.find_element_by_css_selector('input[type="submit"]')
        self.assertIsNotNone(
            gno, 'Guess correctness no radio button should exist.')
        self.assertIsNotNone(gsubmit, 'Guess submit button should exist.')
        gno.click()
        gsubmit.click()
        # Since we don't know about the language, we go to add new language
        # page.
        self.assertEqual(driver.current_url,
            self.index_page_url + 'new_language',
            'We should be at new language page now.')
        # And since we're here, we'll add the new language.
        llang = driver.find_element_by_css_selector('input[name="language"')
        lq = driver.find_element_by_css_selector('input[name="question"]')
        lano = driver.find_element_by_css_selector(
                'input[name="answer"][value="no"]')
        lsubmit = driver.find_element_by_css_selector('input[type="submit"]')
        llang.send_keys('Ruby')
        lq.send_keys('Does it enforce indentation?')
        lano.click()
        lsubmit.click()
        # Now we should be at index page now
        self.assertEqual(driver.current_url, self.index_page_url,
            'We should be at index page by now.')
        # At last, we will verify the new language is entered into the database
        t = LanguageTest.query.order_by(-LanguageTest.id).first()
        nl = LanguageTest('Does it enforce indentation?', False, 'Ruby')
        self.assertEqual(t, nl, '%r should be in database now' % nl)

    def test_can_not_go_to_question_page_initially(self):
        driver = self.driver
        driver.get(self.index_page_url + 'question')
        self.assertEqual(driver.current_url, self.index_page_url,
            'We can\'t go to question page not from index page.')

    def test_can_not_go_to_guess_page_initially(self):
        driver = self.driver
        driver.get(self.index_page_url + 'guess')
        self.assertEqual(driver.current_url, self.index_page_url,
            'We can\'t go to guess page not from index page.')

    def test_can_not_go_to_add_new_language_page_initially(self):
        driver = self.driver
        driver.get(self.index_page_url + 'new_language')
        self.assertEqual(driver.current_url, self.index_page_url,
            'We can\'t go to add new language page not from index page.')
