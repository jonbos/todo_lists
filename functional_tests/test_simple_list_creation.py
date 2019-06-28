from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_for_one_user(self):

        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        input_box = self.get_item_input_box()
        self.assertEqual(input_box.get_attribute(
            'placeholder'), 'Enter a To-Do Item')

        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        input_box.send_keys('Buy peacock feathers')

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1. Buy peacock feathers')
        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very
        # methodical)
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.wait_for_row_in_list_table('1. Buy peacock feathers')
        self.wait_for_row_in_list_table(
            '2. Use peacock feathers to make a fly')

        # She visits that URL - her to-do list is still there.
        # Satisfied, she goes back to sleep

    def test_multiple_users_can_start_lists_at_different_URLS(self):
        # Edith starts a new TO-DO list
        self.browser.get(self.live_server_url)
        input_box = self.get_item_input_box()
        input_box.send_keys('Buy peacock feathers')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1. Buy peacock feathers')
        edith_list_url = self.browser.current_url

        # She notices she has been given a unique URL for her TO-DO list
        self.assertRegex(edith_list_url, '/lists/.+')

        # Now a new user, Francis, comes along to the site.

        # We use a new browser session to make sure that no information
        # of Edith's is coming through from cookies etc
        self.browser.quit()

        # Francis visits the home page.  There is no sign of Edith's
        # list
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_elements_by_tag_name('body')
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('Make a fly', page_text)

        # Francis starts a new list by entering a new item. He
        # is less interesting than Edith...
        input_box = self.get_item_input_box()
        input_box.send_keys('Buy milk')
        input_box.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1. Buy milk')

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')

        # Still no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Both are satisfied
