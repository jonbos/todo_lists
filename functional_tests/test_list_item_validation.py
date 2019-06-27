import time

from selenium.webdriver.common.keys import Keys
from unittest import skip

from .base import FunctionalTest


class InputValidationTest(FunctionalTest):

    def test_cant_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id(
            'id_new_item').send_keys(Keys.ENTER)

        # The home page refreshes, and there is an error message saying
        # that list items can't be blank
        self.wait_for(lambda: self.assertEqual(self.browser.find_element_by_css_selector(
            '.has-error').text(), "You can't have an empty list item"))

        #########
        # She tries again with some text for the item, which now works
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy cheese')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1. Buy cheese')

        # Perversely, she now decides to submit a second blank list item
        inputbox = self.browser.find_element_by_id(
            'id_new_item').send_keys(Keys.ENTER)

        # She receives a similar warning on the list page
        self.wait_for(lambda: self.assertEqual(self.browser.find_element_by_css_selector(
            '.has error').text(), "You can't have an empty list item"))

        # And she can correct it by filling some text in
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy a scooter')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1. Buy cheese')
        self.wait_for_row_in_list_table('2. Buy a scooter')
