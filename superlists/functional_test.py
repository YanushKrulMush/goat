from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(unittest.TestCase):

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
        self.browser.get('http://localhost:8000')

        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a To-Do item')

        inputbox.send_keys('task 1')
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_table('1: task 1')

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('task 2')
        inputbox.send_keys(Keys.ENTER)

        self.check_for_row_in_table('1: task 1')
        self.check_for_row_in_table('2: task 2')

        self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main()
