from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from contextlib import contextmanager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of


class NewVisitorTest(LiveServerTestCase):

    @contextmanager
    def wait_for_page_load(self, timeout=30):
        old_page = self.browser.find_element_by_tag_name('html')
        yield WebDriverWait(self.browser, timeout).until(staleness_of(old_page))

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)

        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a To-Do item')

        inputbox.send_keys('task 1')
        inputbox.send_keys(Keys.ENTER)
        with self.wait_for_page_load(timeout=10):
            user1_list_url = self.browser.current_url
            self.assertRegex(user1_list_url, '/lists/.+')
            self.check_for_row_in_table('1: task 1')

        inputbox = self.browser.find_element_by_id('id_new_item')  # two list items
        inputbox.send_keys('task 2')
        inputbox.send_keys(Keys.ENTER)
        with self.wait_for_page_load(timeout=10):
            self.check_for_row_in_table('1: task 1')
            self.check_for_row_in_table('2: task 2')

        # Second user
        self.browser.quit()
        self.browser = webdriver.Firefox()

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('task 1', page_text)
        self.assertNotIn('task 2', page_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('user 2 task 1')
        inputbox.send_keys(Keys.ENTER)

        with self.wait_for_page_load(timeout=10):
            user2_list_url = self.browser.current_url
            self.assertRegex(user2_list_url, '/lists/.+')
            self.assertNotEquals(user1_list_url, user2_list_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('task 1', page_text)
        self.assertIn('user 2 task 1', page_text)

        self.fail('Finish the test!')
