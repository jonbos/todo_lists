from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class InputValidationTest(FunctionalTest):

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # The browser intercepts the request, and does not load the
        # list page
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:invalid'
        ))

        # She starts typing some text for the new item and the error disappears
        self.get_item_input_box().send_keys("Buy cheese")
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'
        ))

        # And she can submit it successfully
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1. Buy cheese')

        # Perversely, she now decides to submit a second blank list item
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Again, the browser will not comply
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:invalid'
        ))

        # And she can correct it by filling some text in
        self.get_item_input_box().send_keys("Buy party poppers")
        self.wait_for(
            lambda: self.browser.find_elements_by_css_selector(
                '#id_text:valid'))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1. Buy cheese')
        self.wait_for_row_in_list_table('2. Buy party poppers')

    def test_cannot_add_duplicate_items(self):
        # Edith goes to the home page and starts a new list
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys("Buy cookies")
        self.get_item_input_box().send_keys(Keys.ENTER)

        # The page refreshes and shows her item
        self.wait_for_row_in_list_table("1. Buy cookies")

        # She accidentally tries to enter a duplicate item
        self.get_item_input_box().send_keys("Buy cookies")
        self.get_item_input_box().send_keys(Keys.ENTER)

      # She sees a helpful error message
        self.wait_for(lambda: self.assertEqual(
            self.get_error_element().text,
            "You've already got that on your list"
        ))

    def test_error_messages_are_cleared_on_input(self):
        # Edith starts a list and causes a validation error:
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys("Cause a duplication error")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1. Cause a duplication error")
        self.get_item_input_box().send_keys("Cause a duplication error")
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()))

        # She starts typing in the input box to clear the error
        self.get_item_input_box().send_keys("a")

        # The error message disappears
        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()))


    def test_error_messages_are_cleared_on_click(self):
        # Edith starts a list and causes a validation error:
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys("Cause a duplication error")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1. Cause a duplication error")
        self.get_item_input_box().send_keys("Cause a duplication error")
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()))

        # She starts typing in the input box to clear the error
        self.get_item_input_box().click()

        # The error message disappears
        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()))

